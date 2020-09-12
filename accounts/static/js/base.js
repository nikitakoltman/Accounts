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

    $(document).ready(function() {
        main_hide_preload();
    });
});