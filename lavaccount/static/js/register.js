$(document).ready(function() {
    let username = $('#in-hide-username').val(),
        email = $('#in-hide-email').val();

    $('#id_username').val(username);
    $('#id_email').val(email);

    let pattern_email = /^[a-z0-9_-]+@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$/i,

        is_username = false,
        is_email = false,
        is_password = false,
        is_password2 = false,

        is_form_submit = false;

    $('#id_email').on('keyup', function() {
        if ($(this).val().search(pattern_email) == 0) {
            $(this).removeClass('input-invalid');
            is_email = true;
        } else {
            $(this).addClass('input-invalid');
            is_email = false;
        }
    });

    $('form').on('submit', function() {
        preload_show();
        let username = $("#id_username").val(),
            email = $("#id_email").val();

        if (!is_form_submit) {
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
                        } else if (is_exist_username) {
                            swal("Ошибка", 'Введенное имя уже используейтся, введите другое.');
                        } else if (is_exist_email) {
                            swal("Ошибка", 'Введенная почта уже используется, введите другую.');
                        } else if (!is_email) {
                            $('#id_email').addClass('input-invalid');
                        } else if (!is_password) {
                            $('#id_password').addClass('input-invalid');
                        } else if (is_password2) {
                            is_form_submit = true;
                            $('form').submit();
                        }

                        preload_hide();
                    } else {
                        preload_hide();
                        swal("Ошибка!", res['result']);
                    }
                }
            });

            return false;
        }
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