$(document).ready(function() {
    var error = $('#in-hide-form_error').val(),
        username = $('#in-hide-username').val(),
        email = $('#in-hide-email').val();

    show_form_error(error);
    $('#id_username').val(username);
    $('#id_email').val(email);

    function show_form_error(error) {
        switch (error) {
            case 'None':
                break;
            case 'UNIQUE constraint failed: auth_user.username':
                swal('Ошибка', 'Данное имя уже занято, используйте другое.');
                break;
            case 'UNIQUE constraint failed: auth_user.email':
                swal('Ошибка', 'Данная почта уже занята, используйте другую.');
                break;
            default:
                swal('Не известная ошибка', error)
        }
    }
    var pattern = /^[a-z0-9_-]+@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$/i,
        mail = $('#id_email'),

        email = false,
        password = false,
        password2 = false,

        // password
        length = false,
        letter = false,
        capital = false,
        number = false;

    mail.on('keyup', function() {
        if (mail.val().search(pattern) == 0) {
            mail.removeClass('input-invalid');
            email = true;
        } else {
            mail.addClass('input-invalid');
            email = false;
        }
    });

    $("form").on('submit', function() {
        if (!(length && letter && capital && number && email && password && password2)) {
            return false;
        }
    });

    $('#id_password2').on('keyup', function() {
        var value2 = $(this).val(),
            value = $('#id_password').val();

        if (value === value2) {
            $('#id_password2').removeClass('input-invalid');
            password2 = true;
        } else {
            $('#id_password2').addClass('input-invalid');
            password2 = false;
        }
    });

    $('#id_password').on('keyup', function() {
        var value = $(this).val();

        if (value.length < 8) {
            $('#length').removeClass('valid').addClass('invalid');
            length = false;
        } else {
            $('#length').removeClass('invalid').addClass('valid');
            length = true;
        }

        if (value.match(/[a-z]/)) {
            $('#letter').removeClass('invalid').addClass('valid');
            letter = true;
        } else {
            $('#letter').removeClass('valid').addClass('invalid');
            letter = false;
        }

        if (value.match(/[A-Z]/)) {
            $('#capital').removeClass('invalid').addClass('valid');
            capital = true;
        } else {
            $('#capital').removeClass('valid').addClass('invalid');
            capital = false;
        }

        if (value.match(/[0-9]/)) {
            $('#number').removeClass('invalid').addClass('valid');
            number = true;
        } else {
            $('#number').removeClass('valid').addClass('invalid');
            number = false;
        }

        if (length && letter && capital && number) {
            $('#id_password').removeClass('input-invalid');
            password = true;
        } else {
            $('#id_password').addClass('input-invalid');
            password = false;
        }

    }).focus(function() {
        $('#password_info').show();
    }).blur(function() {
        $('#password_info').hide();
    });
});