$(function() {
    $('.simple-tabs').on('click', function() {
        $('.swiper-container').find('div').removeClass('active');
        $('[data-tabs="' + $(this).attr('data-tabs-id') + '"]').addClass('active');
    });
});