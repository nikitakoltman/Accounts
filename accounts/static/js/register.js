$(document).ready(function() {
    let error = $('#in-hide-form_error').val(),
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
            case 'broken rule [pass == pass2]':
                swal('Ошибка валидации', 'Пароли не совподают');
                break;
            case 'broken rule [len > 8]':
                swal('Ошибка валидации', 'Длинна пароля должна быть больше 8 символов');
                break;
            case 'broken rule [a-z]':
                swal('Ошибка валидации', 'Пароль должен содержать как минимум одну маленькую букву');
                break;
            case 'broken rule [A-Z]':
                swal('Ошибка валидации', 'Пароль должен содержать как минимум одну заглавную букву');
                break;
            case 'broken rule [0-9]':
                swal('Ошибка валидации', 'Пароль должен содержать как минимум одну цифру');
                break;
            default:
                swal('Критическая ошибка', error);
        }
    }

    let pattern_email = /^[a-z0-9_-]+@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$/i,

        is_username = false,
        is_email = false,
        is_password = false,
        is_password2 = false;

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
        let username = $("#id_username").val(),
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
                    let is_exist_username = result['is_exist_username'],
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
                    else if (!is_password) {
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

    $('.js-generate_password').on('touchstart mousedown', function() {
        let password = generate_random_string(10);
        $('#id_password').val(password);
        swal('Генератор', 'Ваш пароль: ' + password + '\nСтарайтесь избегать хранения паролей на электронных устройствах в открытом виде.');
        check_password();
    });

    $('#id_password').on('keyup', function() {
        check_password();
    }).focus(function() {
        $('#password_info').show();
    }).blur(function() {
        $('#password_info').hide();
    });

    $('#id_password2').on('keyup change', function() {
        check_password2();
    });

    function check_password() {
        let password = $('#id_password').val(),

            is_length = false,
            is_letter = false,
            is_capital = false,
            is_number = false;

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

    }

    function check_password2() {
        let password = $('#id_password').val(),
            password2 = $('#id_password2').val();

        if (password == password2) {
            $('#id_password2').removeClass('input-invalid');
            is_password2 = true;
        } else {
            $('#id_password2').addClass('input-invalid');
            is_password2 = false;
        }
    }
});