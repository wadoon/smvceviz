/**
 * Created by weigl on 18/09/14.
 */


$(function(){
   $("div.helper input[type=checkbox]").change(
        function() {
            var selector = $(this).attr('value');
            console.log("hide", selector)
            $(selector).toggle("hide");
        }
   );
});