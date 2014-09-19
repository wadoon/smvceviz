<html>
  <head>
  <link href="{{ css_path }}" rel="stylesheet" type="text/css" />
  <script src="https://code.jquery.com/jquery-2.1.1.min.js" language="javascript"></script>
  <script src="{{ js_path }}" language="javascript"></script>
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