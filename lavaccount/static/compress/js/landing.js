$(function(){let t={letters:4,lettersUpper:3,numbers:3};$(".random-string").text(PassGenJS.getPassword(t)),setInterval(function(){$(".random-string").text(PassGenJS.getPassword(t))},2e3)});