$(function(){$(".input_clear").on("click",function(){$("#sum").val("").focus()}),$("#sum").on("keypress",function(n){if((n=n||window.event).charCode&&0!=n.charCode&&46!=n.charCode&&(n.charCode<48||n.charCode>57))return!1}),$("form").on("submit",function(){let n=$("#sum");if(""==n.val())return n.focus(),!1})});