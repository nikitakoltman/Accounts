$(function(){let i=/^[a-z0-9_-]+@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$/i,n=!1;$("#id_email").on("input",function(){0==$(this).val().search(i)?($(this).removeClass("input-invalid"),n=!0):($(this).addClass("input-invalid"),n=!1)}),$("form").on("submit",function(){if(!n)return!1})});