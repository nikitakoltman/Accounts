$(function() {
    var animateButton = function(e) {

        e.preventDefault;
        //reset animation
        e.target.classList.remove('animate');

        e.target.classList.add('animate');
        setTimeout(function() {
            e.target.classList.remove('animate');
        }, 700);
    };

    var bubblyButtons = document.getElementsByClassName("bubbly-button");

    for (var i = 0; i < bubblyButtons.length; i++) {
        bubblyButtons[i].addEventListener('click', animateButton, false);
    }
});

$.ajaxSetup({ // Функция присвоение CSRF токена для всех ajax функций
    beforeSend: function(xhr, settings) {
        if (
            settings.type == "POST" ||
            settings.type == "PUT" ||
            settings.type == "DELETE"
        ) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== "") {
                    var cookies = document.cookie.split(";");
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == name + "=") {
                            cookieValue = decodeURIComponent(
                                cookie.substring(name.length + 1)
                            );
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            }
        }
    },
});