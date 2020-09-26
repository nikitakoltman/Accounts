/* Личный кабинет */

$(function() {
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
});