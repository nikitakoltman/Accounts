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
                swal('Ошибка', 'Введенное имя уже используейтся, введите другое.');
                break;
            case 'UNIQUE constraint failed: auth_user.email':
                swal('Ошибка', 'Введенная почта уже используется, введите другую.');
                break;
            default:
                swal('Критическая ошибка', error);
        }
    }

    var pattern_email = /^[a-z0-9_-]+@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$/i,

        is_username = false,
        is_email = false,
        is_password = false,
        is_password2 = false,

        // password
        is_length = false,
        is_letter = false,
        is_capital = false,
        is_number = false;

    $('#id_email').on('keyup', function() {
        if ($(this).val().search(pattern_email) == 0) {
            $(this).removeClass('input-invalid');
            is_email = true;
        } else {
            $(this).addClass('input-invalid');
            is_email = false;
        }
    });

    $("#js-btn_submit").on('click', function() {
        preload_show();
        var username = $("#id_username").val(),
            email = $("#id_email").val();

        $.ajax({
            url: "check_username_and_email/",
            type: "POST",
            data: {
                username: username,
                email: email,
            },
            success: function(result) {
                if (result['status'] == "success") {
                    var is_exist_username = result['is_exist_username'],
                        is_exist_email = result['is_exist_email'];

                    if ($('#id_username').val() == '') {
                        swal("Ошибка!", 'Заполните поле "Имя".');
                    }
                    else if (is_exist_username) {
                        swal("Ошибка", 'Введенное имя уже используейтся, введите другое.');
                    }
                    else if (is_exist_email) {
                        swal("Ошибка", 'Введенная почта уже используется, введите другую.');
                    }
                    else if (!is_email) {
                        $('#id_email').addClass('input-invalid');
                    }
                    else if (!(is_length && is_letter && is_capital && is_number && is_password)) {
                        $('#id_password').addClass('input-invalid');
                    }
                    else if (is_password2) {
                        $('form').submit();
                    }

                    preload_hide();
                } else {
                    preload_hide();
                    swal("Ошибка!", res['result']);
                }
            }
        });
    });

    $('#id_password2').on('keyup', function() {
        check_password2();
    });

    function check_password2() {
        var password = $('#id_password').val(),
            password2 = $('#id_password2').val();

        if (password === password2) {
            $('#id_password2').removeClass('input-invalid');
            is_password2 = true;
        } else {
            $('#id_password2').addClass('input-invalid');
            is_password2 = false;
        }
    }

    $('#id_password').on('keyup', function() {
        var password = $(this).val();

        if (password.length < 8) {
            $('#length').removeClass('valid').addClass('invalid');
            is_length = false;
        } else {
            $('#length').removeClass('invalid').addClass('valid');
            is_length = true;
        }

        if (password.match(/[a-z]/)) {
            $('#letter').removeClass('invalid').addClass('valid');
            is_letter = true;
        } else {
            $('#letter').removeClass('valid').addClass('invalid');
            is_letter = false;
        }

        if (password.match(/[A-Z]/)) {
            $('#capital').removeClass('invalid').addClass('valid');
            is_capital = true;
        } else {
            $('#capital').removeClass('valid').addClass('invalid');
            is_capital = false;
        }

        if (password.match(/[0-9]/)) {
            $('#number').removeClass('invalid').addClass('valid');
            is_number = true;
        } else {
            $('#number').removeClass('valid').addClass('invalid');
            is_number = false;
        }

        if (is_length && is_letter && is_capital && is_number) {
            $('#id_password').removeClass('input-invalid');
            is_password = true;
        } else {
            $('#id_password').addClass('input-invalid');
            is_password = false;
        }

        check_password2();

    }).focus(function() {
        $('#password_info').show();
    }).blur(function() {
        $('#password_info').hide();
    });
});