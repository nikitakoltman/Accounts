$(function() {
    let error = $('#error_1_id_old_password strong').text();

    show_form_error(error);

    function show_form_error(error) {
        if (error) {
            switch (error) {
                case 'Ваш старый пароль введен неправильно. Пожалуйста, введите его снова.':
                    swal('Ошибка', error);
                    break;
                default:
                    swal('Критическая ошибка', error);
                    break;
            }
        }
    }
});