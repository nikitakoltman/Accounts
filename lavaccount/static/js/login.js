$(function() {
    $('.js-show_password').on('click', function() {
    	password = $('#id_password');
        password.attr('type', password.attr('type') === 'password' ? 'text' : 'password');
    });
});