$(function() {
    $.ajaxSetup({ // Функция присвоение CSRF токена для всех ajax функций
        beforeSend: function(xhr, settings) {
            if (
                settings.type == "POST" ||
                settings.type == "PUT" ||
                settings.type == "DELETE"
            ) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== "") {
                        var cookies = document.cookie.split(";");
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == name + "=") {
                                cookieValue = decodeURIComponent(
                                    cookie.substring(name.length + 1)
                                );
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                }
            }
        },
    });

    var master_password = null; // Хранит мастер пароль для расшифровки данных таблицы
    var press_timer; // Хранит значение таймера для события долгого нажатия кнопки "Пароль"
    var is_allow_copy = true; // Разрешает копирование при долгом нажатии кнопки "Пароль"
    get_master_password();

    function get_master_password() {
        $.ajax({
            url: "getmasterpassword/",
            type: "POST",
            success: function(result) {
                var res = JSON.parse(result);

                if (res['status'] == "success") {
                    enter_password(res['result']);
                } else {
                    if (res['result'] == 'DoesNotExist') {
                        // При первом посещении страницы, а также исходя из результата "DoesNotExist", мастер пароля в базе не существует, поэтому...
                        $('#in-oldpassword').attr('disabled', 'disabled'); // Отключаем поле ввода старого пароля в модальном окне изменения пароля
                        $('#MasterPasswordModal').modal('show'); // Открываем модальное окно изменения пароля
                    } else {
                        swal("Ошибка!", res['result']); // Это кастомный alert
                    }
                }
            },
        });
    }

    function enter_password(result) {
        $('#EnterKeyModal').modal('show'); // Открываем модальное окно ввода ключа
        $('#EnterKeyModal').attr('result', result); // Задаем атрибут с зашифрованной строкой
    }

    $("#btnenterpassword").on('click', function() { // Собитие нажатия кнопки "ОК" в модальном окне ввода ключа
        check_key(); // Проходим авторизацию
    });

    $("#EnterKeyModal").on('hidden.bs.modal', function() { // Событие закрытия модального окна ввода ключа
        if (master_password !== null) { // Если не нажата кнопка "Отмена"...
            if ($('#Accounts_table > tbody  > tr > td').length > 0) { // Если таблицы не пустая...
                $('#Accounts_table > tbody  > tr > td').each(function(index, td) { // Проходим циклом по всем ячейкам
                    // Кроме ячейки пароля и ячейки в которой находится кнопка "Open"
                    if (td.className !== 'td-password tdencrypt' && td.className !== 'td-btn') {
                        td.innerHTML = decrypt(td.innerHTML, master_password); // Расшифровываем ячейку
                    }
                });
                sort_table(); // Сортируем таблицу
            }
            $('.account_container').css('display', 'block'); // Показываем таблицу
        }
    });

    $('#EnterKeyModal').on('shown.bs.modal', function() { // Событие открытия модального окна ввода ключа
        // Данное событие необходимо для реализации автофокуса для input
        $('#in-enterpassword').focus();
    });

    $('#in-enterpassword').keydown(function(e) {
        if (e.keyCode === 13) { // Если нажата клавиша "Enter"...
            check_key(); // Проходим авторизацию
        }
    });

    function check_key() { // Функция авторизации/проверки ключа
        var key = $('#in-enterpassword').val();
        var result = $('#EnterKeyModal').attr('result');

        if (key === '') { // Если ключ не был введен...
            $('#in-enterpassword').focus(); // Переводим фокус на input
            enter_password(result); // Повторяем запрос ключа
        } else {
            key = decrypt(result, key); // Расшифровываем полученый пароль введенным ключем

            if (key === '') { // Если расшифровка не дала результата...
                $('#in-enterpassword').val(''); // Чистим input ввода ключа
                $('#in-enterpassword').focus(); // Переводим фокус на input
                enter_password(result); // Повторяем запрос ключа
            } else {
                master_password = key; // Присваиваем ключ глобальной переменной "Мастер пароль"
                $('#EnterKeyModal').modal('hide'); // Скрываем модальное окно ввода пароля
                $('#EnterKeyModal').attr('result', ''); // Чистим атрибут
            }
        }
    }

    function sort_table() { // Функция сортировки таблицы
        if ($('#Accounts_table tr').length > 1) { // Если таблица не пустая...
            $("#Accounts_table").tablesorter({
                sortList: [
                    [0, 0] // Сортируем по первому столбцу, по алфавиту
                ]
            });
        }
    }

    function change_master_password(newmp) { // Функция изменения мастер пароля
        var sites = {},
            descriptions = {},
            logins = {},
            passwords = {}; // Переменные для хранения массивов данных

        if ($('#Accounts_table > tbody  > tr > td').length > 0) { // Если таблица не пустая...
            $('#Accounts_table > tbody  > tr > td').each(function(index, td) {
                if (td.className == 'td-site') {
                    // Шифруем строку из ячейки и присваиваем ее массиву под индексом ее id в базе данных
                    sites[td.getAttribute('data-id')] = encrypt(td.innerHTML, newmp);
                } else if (td.className == 'td-description') {
                    descriptions[td.getAttribute('data-id')] = encrypt(td.innerHTML, newmp);
                } else if (td.className == 'td-login tdencrypt') {
                    logins[td.getAttribute('data-id')] = encrypt(td.innerHTML, newmp);
                } else if (td.className == 'td-password tdencrypt') {
                    // Тоже самое, только предварительно расшировать, потому что пароль хранится в ячейке в зашифрованном виде
                    passwords[td.getAttribute('data-id')] = encrypt(decrypt(td.innerHTML, master_password), newmp);
                }
            });
        }

        $.ajax({
            url: "changemasterpassword/",
            type: "POST",
            data: {
                newmp: encrypt(newmp, newmp),
                sites: JSON.stringify(sites),
                descriptions: JSON.stringify(descriptions),
                logins: JSON.stringify(logins),
                passwords: JSON.stringify(passwords),
            },
            success: function(result) {
                var res = JSON.parse(result);

                if (res['status'] == "success") {
                    location.href = location.href;
                } else {
                    swal("Ошибка!", res['result']);
                }
            },
        });
    }

    function create_account() { // Функция создания нового аккаунта в таблице
        var site = $("#in-site").val();
        var description = $("#in-description").val();
        var login = $("#in-login").val();
        var password = encrypt($("#in-password").val(), master_password);

        $.ajax({
            url: "createaccount/",
            type: "POST",
            data: {
                site: encrypt(site, master_password),
                description: encrypt(description, master_password),
                login: encrypt(login, master_password),
                password: password,
            },
            success: function(result) {
                var res = JSON.parse(result);

                if (res['status'] == "success") {
                    var id = res['accountid'];

                    var tr = '<tr data-id="' + id + '">' +
                        '<td class="td-site" data-id="' + id + '">' + site + '</td>' +
                        '<td class="td-description" data-id="' + id + '">' + description + '</td>' +
                        '<td class="td-login tdencrypt" data-id="' + id + '">' + login + '</td>' +
                        '<td class="td-password tdencrypt" data-id="' + id + '">' + password + '</td>' +
                        '<td class="td-btn">' +
                        '<button class="btn btn-primary" data-toggle="modal" data-target="#AccountModal" data-id="' + id + '">Open</button>' +
                        '</td>' +
                        '</tr>'; // Формируем запись для таблицы

                    $('#Accounts_table').find('tbody').append(tr); // Добавляем в конец таблицы только что созданную запись аккаунта
                    // Вызов сортировки два раза, так как вызов один раз приведет к обратной сортировке алфавита (от Я до А)
                    sort_table();
                    sort_table();
                    $('#CreateAccountModal').modal('hide'); // Закрываем модальное окно создания аккаунта
                    // Чистим поля
                    $('#in-site').val('');
                    $('#in-description').val('');
                    $('#in-login').val('');
                    $('#in-password').val('');
                } else {
                    swal("Ошибка!", res['result']);
                }
            },
        });
    }

    function delete_account(datadissid) { // Функция удаления аккаунта
        $.ajax({
            url: "deleteaccount/",
            type: "POST",
            data: {
                datadissid: datadissid,
            },
            success: function(result) {
                var res = JSON.parse(result);

                if (res['status'] == "success") {
                    $('#Accounts_table').find('tbody').find('tr[data-id="' + datadissid + '"]').remove(); // Удаляем запись из таблицы
                    $('#AccountModal').modal('hide'); // Закрываем модальное окно удаления аккаунта
                } else {
                    swal("Ошибка!", res['result']);
                }
            },
        });
    }

    function change_info_account() { // Функция изменения информации аккаунта
        var id = $('#AccountModal').find('#modal-btn-delete').attr('data-diss-id');
        var site = $("#modal-site").val();
        var description = $("#modal-description").val();
        var login = $("#modal-login").val();
        var newpassword = $('#modal-newpassword').val();

        if (newpassword !== "") { // Если был введен новый пароль...
            newpassword = encrypt(newpassword, master_password); // Шифруем его
        }

        if ($("#modal-site").val() !== "") {
            if ($("#modal-description").val() !== "") {
                if ($("#modal-login").val() !== "") {
                    $.ajax({
                        url: "changeinfoaccount/",
                        type: "POST",
                        data: {
                            id: id,
                            site: encrypt(site, master_password),
                            description: encrypt(description, master_password),
                            login: encrypt(login, master_password),
                            newpassword: newpassword,
                        },
                        success: function(result) {
                            var res = JSON.parse(result);

                            if (res['status'] == "success") {
                                var tr = $('#Accounts_table').find('tbody').find('tr[data-id="' + id + '"]'); // Ищем в таблице аккаунт который изменяли
                                // Обновляем значения в таблице
                                tr.find('.td-site').text(site);
                                tr.find('.td-description').text(description);
                                tr.find('.td-login').text(login);
                                if (newpassword !== "") { // Если был введен пароль...
                                    tr.find('.td-password').text(newpassword);
                                    $('#modal-newpassword').val(''); // Чистим input ввода пароля
                                }
                                $('#AccountModal').modal('hide'); // Скрываем модальное окно просмотра аккаунта
                            } else {
                                swal("Ошибка!", res['result']);
                            }
                        },
                    });
                } else {
                    swal('Заполните поле "Логин"');
                    return false;
                }
            } else {
                swal('Заполните поле "Описание"');
                return false;
            }
        } else {
            swal('Заполните поле "Сайт"');
            return false;
        }
    }

    function encrypt(str, key) { // Функция шифрования строки
        return CryptoJS.AES.encrypt(str, key).toString();
    }

    function decrypt(str, key) { // Функция дешифрования строки
        try {
            return CryptoJS.AES.decrypt(str, key).toString(CryptoJS.enc.Utf8);
        } catch (e) {
            if (e.message == 'Malformed UTF-8 data') {
                // Рандомно возникающая ошибка, не известно почему, но она не мешает нормальному функционированию
                console.error(e);
            } else {
                // Прочие гипотетически возможные ошибки
                swal("Ошибка!", 'Error: function Decrypt()');
                throw e;
            }
        }
    }

    $('#AccountModal').on('show.bs.modal', function(event) { // Событие открытия модального окна просмотра аккаунта
        var id = $(event.relatedTarget).attr('data-id');
        var site = $('.td-site[data-id="' + id + '"]').text();
        var description = $('.td-description[data-id="' + id + '"]').text();
        var login = $('.td-login[data-id="' + id + '"]').text();
        var password = $('.td-password[data-id="' + id + '"]').text();

        // Заполняем модальное окно
        $(this).find('#modal-site').val(site);
        $(this).find('#modal-description').val(description);
        $(this).find('#modal-login').val(login);
        $(this).find('#modal-password').val(password);
        $(this).find('#modal-newpassword').val('');
        $(this).find('#modal-btn-delete').attr('data-diss-id', id);
        $(this).find('#modal-btn-delete').attr('data-site', site);
    });

    $("#btnsendaccount").on('click', function() { // Событие нажатия на кнопку "Отправить" в модальном окне создания нового аккаунта
        if ($("#in-site").val() !== "") {
            if ($("#in-description").val() !== "") {
                if ($("#in-login").val() !== "") {
                    if ($("#in-password").val() !== "") {
                        create_account();
                    } else {
                        swal('Заполните поле "Пароль"');
                    }
                } else {
                    swal('Заполните поле "Логин"');
                }
            } else {
                swal('Заполните поле "Описание"');
            }
        } else {
            swal('Заполните поле "Сайт"');
        }
    });

    $("#btnsendmasterpassword").on('click', function() { // Событие нажатия на кнопку "Отправить" в модальном окне изменения мастер пароля
        if (($("#in-oldpassword").val() === "" && $("#in-oldpassword").attr('disabled')) ||
            ($("#in-oldpassword").val() !== "" && !$("#in-oldpassword").attr('disabled'))) {
            if ($("#in-newpassword").val() !== "") {
                if ($("#in-renewpassword").val() !== "") {
                    if ($("#in-newpassword").val() === $("#in-renewpassword").val()) {
                        if (!$("#in-oldpassword").attr('disabled')) {
                            if (master_password === $('#in-oldpassword').val()) {
                                change_master_password($("#in-renewpassword").val());
                            } else {
                                swal('Не правильный старый пароль');
                            }
                        } else {
                            change_master_password($("#in-renewpassword").val());
                        }
                    } else {
                        swal('Пароли не совпадают');
                    }
                } else {
                    swal('Заполните поле "Подтвердите новый пароль"');
                }
            } else {
                swal('Заполните поле "Новый пароль"');
            }
        } else {
            swal('Заполните поле "Старый пароль"');
        }
    });

    $("#modal-btn-delete").on('click', function() { // Событие нажатия на кнопку "Удалить" в модальном окне просмотра аккаунта
        swal({
                title: "Ты уверен?",
                text: "Эту запись потом не восстановить!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: '#DD6B55',
                confirmButtonText: 'Да, удалить это!'
            },
            function() { // Если была нажата кнопка "Да, удалить это!"...
                delete_account($("#modal-btn-delete").attr("data-diss-id")); // Удаляем аккаунт
            });
    });

    $("#modal-btn-save").on('click', function() { // Событие нажатия кнопки "Сохранить" в модальном окне просмотра аккаунта
        var key = decrypt($('#modal-password').val(), master_password);

        if (key !== '') { // Если расшифрока дала результат...
            change_info_account(); // Изменяем аккаунт
        } else {
            swal('Не правильный пароль');
        }
    });

    $("#modal-btn-password").on('click', function() { // Событие нажатия кнопки "Пароль" в модальном окне просмотра аккаунта
        get_password();
    });

    $("#modal-btn-login").on('click', function() { // Событие нажатия кнопки "Логин" в модальном окне просмотра аккаунта
        copy_clipboard($('#Accounts_table').find('.td-login[data-id="' + $('#modal-btn-delete').attr('data-diss-id') + '"]').text());
    });

    // Событие долгого нажатия кнопки "Пароль" клавишой мыши или сенсором телефона в модальном окне просмотра аккаунта
    $("#modal-btn-password").on('touchend mouseup', (function() { // Событие отжатия клавиши или сенсора
        clearTimeout(press_timer); // Очищаем таймер
    })).on('touchstart mousedown', (function() { // Событие нажатия клавиши или сенсора
        press_timer = window.setTimeout(function() { // Устанавливаем таймер
            is_allow_copy = false; // Запрещаем копирование пароля в буфер обмена так как...
            get_password(); // В этой функции мы покажем пароль на экране
        }, 500); // 500 миллисекунд
    }));

    function get_password() { // Функция копирования/отображения пароля аккаунта
        var key = decrypt($('#modal-password').val(), master_password);

        if (key !== '') { // Если расшифрока дала результат...
            if (is_allow_copy) { // Если копирование разрешено...
                copy_clipboard(key); // Копируем пароль в буфер обмена
            } else {
                swal(key); // Выводим пароль на экран
                is_allow_copy = true; // Разрешаем в дальнейшем копирование
            }
        } else {
            swal('Не правильный пароль');
        }
    }

    function copy_clipboard(text) { // Функция копирования текста в буфер обмена
        var $tmp = $("<input>");
        $("#AccountModal").append($tmp);
        $tmp.val(text).select();
        document.execCommand("copy");
        $tmp.remove();
    }
});