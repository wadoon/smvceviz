#!/usr/bin/python3

# viztracer -- Visualize the Traces of NuSMV and NuXMV
# Copyright (C) 2014 - Alexander Weigl
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

__author__ = "Alexander Weigl <Alexander.Weigl@student.kit.edu>"
__version__ = "0.1-rc"
__license__ = "GPLv3"

import sys
import os, os.path

from functools import partial

from jinja2 import Environment
from collections import defaultdict
from argparse import ArgumentParser


TEMPLATE = """
<html>
  <head>
  <link href="nusmv-style.css" rel="stylesheet" type="text/css" />
  <script src="https://code.jquery.com/jquery-2.1.1.min.js" language="javascript"></script>
  <script src="/home/weigla/Projects/viztracer/filter.js" language="javascript"></script>
  </head>
  <body>
  <div class="helper">
    <h2>Modules</h2>
    {% for mod in trace.modules_names() %}
    <div>
        <h3>{{mod}}</h3>
        <ul>
            <li><label><input type="checkbox" checked value="div.{{mod}} tr"/>Hide all</label></li>
            {% for var in trace.variables_in_module(mod) %}
                <li><label><input type="checkbox" checked value="div.{{mod}} tr.{{var}}"/> {{var}}</label></li>
            {% endfor %}
        </ul>
    </div>
    {% endfor %}
  </div>

  {% for l in range(length) %}
  <h2>Step {{ l + 1 }}</h2>
    {% for mod in sorted(modules.keys()) %}
    <div class="state {{mod}}">
      <h3>{{mod}}</h3>
      <table>
        {% for var in sorted(modules[mod][l].keys()) %}
          <tr class="{{ classes(modules, mod, l, var) }}">
             <th>{{var}}</th>
             <td>{{modules[mod][l][var]}}</td>
          </tr>
        {% endfor %}
      </table>
    </div>
    {% endfor %}
  {% endfor %}
  </body>
</html>
"""


class Trace(object):
    """Represent a counterexample trace.

    Two special modules: `input`, `global`.
    """

    def __init__(self):
        self.modules = defaultdict(lambda: [{}])
        self.modules['input']
        self.modules['global']
        self.input_module = False


    def modules_names(self):
        return sorted(self.modules.keys())

    def variables_in_module(self, module):
        vars = set()

        for step in self.modules[module]:
            v = set(step.keys())
            vars = vars | v

        return sorted(vars)

    def parse_line(self, line):
        line = line.strip()
        if line.startswith("-> Input"):
            self.input_module = True
            self.new_step()

        elif line.startswith("-> State"):
            self.input_module = False

        else:
            key, value = parse_assign(line)
            if key:
                if self.input_module:
                    module = 'input'
                else:
                    try:
                        module, key = key.split('.', 1)
                    except ValueError:
                        module = 'global'

                self.modules[module][-1][key] = value

    def new_step(self):
        for value in self.modules.values():
            value.append({})

    def complete_states(self):
        for key, mod in self.modules.items():
            new_trace = []
            prev = None
            for step in mod:
                if new_trace:
                    d = dict(new_trace[-1])
                    d.update(step)
                    new_trace.append(d)
                else:
                    new_trace.append(step)

            self.modules[key] = new_trace

    @staticmethod
    def from_file(filename):
        """Read in filename and creates a trace object.

        :param filename: path to nu(x|s)mv output file
        :type filename: str
        :return:
        """
        trace = Trace()
        reached = False
        with open(filename) as fp:
            for line in fp.readlines():
                if not reached and line.strip() == "Trace Type: Counterexample":
                    reached = True
                    continue
                elif reached:
                    trace.parse_line(line)
            return trace


def parse_assign(string):
    """Parse an assignment line:

    >>> parse_assign("    scenario8.Actuator_MagazinVacuumOn = TRUE")
    ("scenario8.Actuator_MagazinVacuumOn", "TRUE")
    """
    try:
        a, b = string.split(" = ")
        return a.strip(), b.strip()
    except:
        print("Error with assignment: %s" % string, file=sys.stderr)
        return None, None


def classes(modules, mod, step, var, m1="m1", m2="m2", sub_seperator="$"):
    def changed():
        """determines if the value has changed since last step.
        """
        if step == 0:
            return "changed"

        try:
            c = modules[mod][step - 1][var] != modules[mod][step][var]
            return "changed" if c else "not-changed"
        except:
            return "changed"

    def compare():
        """compares to modules with each other
        """
        if mod == m1:
            omod = m2

        elif mod == m2:
            omod = m1

        else:
            return "no-compare"

        try:
            c = modules[mod][step][var] != modules[omod][step][var]
            return "not-equals" if c else "equals"
        except:
            return "not-equals one-sided"


    def submodule_name():
        if sub_seperator in var:
            return ' '.join(var.split(sub_seperator))
        return "no-sub-module " + var

    return ' '.join((changed(), compare(), submodule_name()))


def main():
    ap = ArgumentParser()
    ap.add_argument("-1", '--module1', action="store", dest="module1",
                    default="m1",
                    help="module of the current revision")
    ap.add_argument("-2", '--module2', action="store", dest="module2",
                    default="m2",
                    help="module of the next revision")

    ap.add_argument("file")

    args = ap.parse_args()

    trace = Trace.from_file(args.file)
    trace.complete_states()
    jinja = Environment()

    cmp = partial(classes, sub_seperator="$", m1=args.module1, m2=args.module2)

    jinja.globals.update(sorted=sorted, classes=cmp)
    T = jinja.from_string(TEMPLATE)

    print(T.render(
        css=open(os.path.join(os.path.dirname(__file__), "nusmv-style.css")),
        modules=trace.modules,
        trace=trace,
        length=len(trace.modules['input'])))


__name__ == "__main__" and main()