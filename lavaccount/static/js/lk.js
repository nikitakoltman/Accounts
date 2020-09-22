$(function() {
    $('.simple-tabs').on('click', function() {
        $('.swiper-container').find('div').removeClass('active');
        $('[data-tabs="' + $(this).attr('data-tabs-id') + '"]').addClass('active');
    });

    $(".js-auth-location").hover(
        function() {
            $('.auth-ip[number="' + $(this).attr('number') + '"]').show();
        },
        function() {
            $('.auth-ip[number="' + $(this).attr('number') + '"]').hide();
        }
    );

    $(".auth-ip").hover(
        function() {
            $(this).css('display', 'block');
        },
        function() {
            $(this).css('display', 'none');
        }
    );
});