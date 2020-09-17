$(document).ready(function() {
    let error = $('#in-hide-form_error').val();

    show_form_error(error);

    function show_form_error(error) {
        switch (error) {
            case 'None':
                break;
            case 'Password is not valid':
                swal('Ошибка', 'Введенный пароль не верный.');
                break;
            default:
                swal('Критическая ошибка', error);
                break;
        }
    }
});