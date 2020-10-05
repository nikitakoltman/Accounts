/* Личный кабинет */

$(function() {
    let storage = window.localStorage;

    $('.simple-tabs').on('click', function() {
        /* Переключение вкладок меню */
        $('.swiper-container').find('div').removeClass('active');
        $('[data-tabs="' + $(this).attr('data-tabs-id') + '"]').addClass('active');
    });

    $(".js-auth-location").hover(
        /* Показать ip адрес при наведении на локацию */
        function() {
            $('.auth-ip[number="' + $(this).attr('number') + '"]').show();
        },
        function() {
            $('.auth-ip[number="' + $(this).attr('number') + '"]').hide();
        }
    );

    $(".auth-ip").hover(
        /* Чтобы блок с ip адресом не пропал если hover переходит с локации на блок ip адреса */
        function() {
            $(this).show();
        },
        function() {
            $(this).hide();
        }
    );

    $('.simple-tabs').on('click', function() {
        /* Задаем активный раздел */
        storage.setItem('lk_active_swiper_tab', $(this).attr('data-tabs-id'));
    });

    let tab = storage.getItem('lk_active_swiper_tab');

    if (tab == null) {
        // Если значение не найдено то ставим первый раздел
        tab = '1';
        storage.setItem('lk_active_swiper_tab', tab);
    }

    // Активируем раздел
    $('.js-swiper-tabs[data-tabs="' + tab + '"]').addClass('active');
});