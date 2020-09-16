$(function() {
    let error = $('#in-hide-form_error').val();

    show_form_error(error);

    function show_form_error(error) {
        switch (error) {
            case 'None':
                break;
            case 'Token is not valid':
                swal('Ошибка', 'Введенный код не верный.');
                break;
            default:
                swal('Критическая ошибка', error);
        }
    }
});