$(function(){let t;$(".ip_system_select").on("change",function(){var t;t=$(".ip_system_select").val(),preload_show(),$.ajax({url:"get_ip_info_system_switch/",type:"POST",data:{system_name:t},success:function(e){"success"==e.status?swal({title:"Успех!",text:"Система "+t+" установлена.",type:"success"}):"doesnotexist"==e.result?swal("Ошибка","Настройка get_ip_info_system не найдена"):swal("Ошибка",e.result),preload_hide()}})}),$("#site_in_service_button").on("change",function(){let t="false",e="Да, открыть!",s="Сайт будет открыт!",o="#64dd55",c=this;$(this).attr("checked")||(t="true",e="Да, закрыть.",s="Сайт будет закрыт на техническое обслуживание!",o="#DD6B55"),swal({title:"Вы уверены?",text:s,type:"warning",showCancelButton:!0,confirmButtonColor:o,confirmButtonText:e},function(){!function(t,e){preload_show(),$.ajax({url:"site_in_service_switch/",type:"POST",data:{checked:e},success:function(e){"success"==e.status?"true"==e.checked?(t.setAttribute("checked","checked"),$("#site_in_service_button").addClass("toggle-button_active"),$(".navbar-brand").removeClass("logo").addClass("logo_site-close").text("Сайт закрыт")):(t.removeAttribute("checked"),$("#site_in_service_button").removeClass("toggle-button_active"),$(".navbar-brand").removeClass("logo_site-close").addClass("logo").text("LavAccount")):"doesnotexist"==e.result?swal("Ошибка","Настройка site_in_service не найдена"):swal("Ошибка",e.result),preload_hide()}})}(c,t)})}),$(".toggle-button").on("click",function(){t=$(this)}),$(".sweet-alert .cancel").on("click",function(){t.hasClass("toggle-button_active")?t.addClass("toggle-button_active"):t.removeClass("toggle-button_active")})});