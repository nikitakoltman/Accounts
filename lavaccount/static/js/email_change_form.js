$(function() {
    let pattern_email = /^[a-z0-9_-]+@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$/i,
        is_email = false,
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

        if (!is_email) {
            preload_hide();
            return false;
        }

        preload_hide();
    });

    $('form').on('submit', function() {
        preload_show();
        let email = $("#id_email").val();

        if (!is_form_submit) {
            $.ajax({
                url: "/register/check_username_and_email/",
                type: "POST",
                data: {
                    username: '',
                    email: email,
                },
                success: function(result) {
                    if (result['status'] == "success") {
                        let is_exist_email = result['is_exist_email'];

                        if (is_exist_email) {
                            swal("Ошибка", 'Введенная почта уже используется, введите другую.');
                        } else if (!is_email) {
                            $('#id_email').addClass('input-invalid');
                        } else {
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
});