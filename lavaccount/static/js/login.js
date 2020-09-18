$(function() {
    let error = $('#in-hide-form_error').val();

    show_form_error(error);

    function show_form_error(error) {
        switch (error) {
            case 'None':
                break;
            case 'Login error':
                swal('Ошибка', 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.');
                break;
            default:
                swal('Критическая ошибка', error);
                break;
        }
    }

    $('.js-show_password').on('touchstart mousedown', function() {
        $('#id_password').attr('type', 'text');
    }).on('touchend mouseup', function() {
    	$('#id_password').attr('type', 'password');
    });
});