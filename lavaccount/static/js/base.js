$(function() {
    window.main_show_preload = function() {
        $('.windows8').removeClass('preload-done');
        $('.windows8').css({ display: '' });
        $('#page-preload').removeClass('preload-done');
    }

    window.main_hide_preload = function() {
        $('#page-preload').addClass('preload-done');
        $('.windows8').addClass('preload-done');
        setTimeout(function() {
            $('.windows8').css({ display: 'none' });
        }, 1000);
    }

    window.preload_show = function() {
        $('#page-preload').css('background', 'rgb(0 0 0 / 0.5)');
        main_show_preload();
    }

    window.preload_hide = function() {
        main_hide_preload();
        $('#page-preload').css('background', '#000000');
    }

    window.onbeforeunload = function() { // Сделать затухание при преходах по ссылками на сайте
        main_show_preload();
    }

    window.generate_random_string = function(length_string) {
        let chars = 'qwertyuiopasdfghjklzxcvbnm1234567890!@#$%QWERTYUIOPASDFGHJKLZXCVBNM',
            word = '';
        // TODO: Сделать что-то по приличней, сейчас костыль.
        do {
            for (let i = 0; i < length_string; i++) {
                word += chars[Math.round(Math.random() * (chars.length - 1))];
            }
            if (word.match(/[a-z][A-Z][0-9]/)) {
                return word;
            } else {
                word = '';
            }
        }
        while (!word.match(/[a-z][A-Z][0-9]/));
    }

    function checkCookies() {
        let cookieDate = localStorage.getItem('cookieDate');
        let cookieNotification = document.getElementById('cookie_notification');
        let cookieBtn = cookieNotification.querySelector('.cookie_accept');

        // Если записи про кукисы нет или она просрочена на 1 год, то показываем информацию про кукисы
        if (!cookieDate || (+cookieDate + 31536000000) < Date.now()) {
            cookieNotification.classList.add('show');
        }

        // При клике на кнопку, в локальное хранилище записывается текущая дата в системе UNIX
        cookieBtn.addEventListener('click', function() {
            localStorage.setItem('cookieDate', Date.now());
            cookieNotification.classList.remove('show');
        })
    }

    checkCookies();

    $(document).ready(function() {
        main_hide_preload();
    });
});