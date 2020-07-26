$(function() {
    var master_password = null; // Хранит мастер пароль для расшифровки данных таблицы
    var press_timer; // Хранит значение таймера для события долгого нажатия кнопки "Пароль"
    var is_allow_copy = true; // Разрешает копирование при долгом нажатии кнопки "Пароль"
    var is_allow_show_page = false; // Разрешает отображение страницы

    master_password = $('body').attr('master_password');
    $('body').attr('master_password', null);

    if (master_password != 'DoesNotExist') {
        $('#EnterKeyModal').modal('show'); // Открываем модальное окно ввода ключа
    } else {
        // При первом посещении страницы, а также исходя из результата "DoesNotExist", мастер пароля в базе не существует, поэтому...
        $('#in-oldpassword').attr('disabled', 'disabled'); // Отключаем поле ввода старого пароля в модальном окне изменения пароля
        $('#MasterPasswordModal').modal('show'); // Открываем модальное окно изменения пароля
    }

    function create_account() { // Функция создания нового аккаунта в таблице
        var site = $("#in-site").val();
        var description = $("#in-description").val();
        var login = $("#in-login").val();
        var password = encrypt($("#in-password").val(), master_password);

        $.ajax({
            url: "create_account/",
            type: "POST",
            data: {
                site: encrypt(site, master_password),
                description: encrypt(description, master_password),
                login: encrypt(login, master_password),
                password: password,
            },
            success: function(res) {
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

    function delete_account(account_id) { // Функция удаления аккаунта
        $.ajax({
            url: "delete_account/",
            type: "POST",
            data: {
                account_id: account_id,
            },
            success: function(res) {
                if (res['status'] == "success") {
                    $('#Accounts_table').find('tbody').find('tr[data-id="' + account_id + '"]').remove(); // Удаляем запись из таблицы
                    $('#AccountModal').modal('hide'); // Закрываем модальное окно удаления аккаунта
                } else {
                    swal("Ошибка!", res['result']);
                }
            },
        });
    }

    function change_info_account() { // Функция изменения информации аккаунта
        var site = $("#modal-site").val();
        var description = $("#modal-description").val();
        var login = $("#modal-login").val();
        var new_password = $('#modal-newpassword').val();
        var account_id = $('#AccountModal').find('#modal-btn-delete').attr('data-diss-id');

        if (new_password !== "") { // Если был введен новый пароль...
            new_password = encrypt(new_password, master_password); // Шифруем его
        }

        if ($("#modal-site").val() !== "") {
            if ($("#modal-description").val() !== "") {
                if ($("#modal-login").val() !== "") {
                    $.ajax({
                        url: "change_info_account/",
                        type: "POST",
                        data: {
                            site: encrypt(site, master_password),
                            description: encrypt(description, master_password),
                            login: encrypt(login, master_password),
                            new_password: new_password,
                            account_id: account_id
                        },
                        success: function(res) {
                            if (res['status'] == "success") {
                                var tr = $('#Accounts_table').find('tbody').find('tr[data-id="' + account_id + '"]'); // Ищем в таблице аккаунт который изменяли
                                // Обновляем значения в таблице
                                tr.find('.td-site').text(site);
                                tr.find('.td-description').text(description);
                                tr.find('.td-login').text(login);
                                if (new_password !== "") { // Если был введен пароль...
                                    tr.find('.td-password').text(new_password);
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
                }
            } else {
                swal('Заполните поле "Описание"');
            }
        } else {
            swal('Заполните поле "Сайт"');
        }
    }

    function change_or_create_master_password(new_master_password) { // Функция изменения мастер пароля
        var sites = {},
            descriptions = {},
            logins = {},
            passwords = {}; // Переменные для хранения массивов данных

        if ($('#Accounts_table > tbody  > tr > td').length > 0) { // Если таблица не пустая...
            $('#Accounts_table > tbody  > tr > td').each(function(index, td) {
                if (td.className == 'td-site') {
                    // Шифруем строку из ячейки и присваиваем ее массиву под индексом ее id в базе данных
                    sites[td.getAttribute('data-id')] = encrypt(td.innerHTML, new_master_password);
                } else if (td.className == 'td-description') {
                    descriptions[td.getAttribute('data-id')] = encrypt(td.innerHTML, new_master_password);
                } else if (td.className == 'td-login tdencrypt') {
                    logins[td.getAttribute('data-id')] = encrypt(td.innerHTML, new_master_password);
                } else if (td.className == 'td-password tdencrypt') {
                    // Тоже самое, только предварительно расшировать, потому что пароль хранится в ячейке в зашифрованном виде
                    passwords[td.getAttribute('data-id')] = encrypt(decrypt(td.innerHTML, master_password), new_master_password);
                }
            });
        }

        $.ajax({
            url: "change_or_create_master_password/",
            type: "POST",
            data: {
                sites: JSON.stringify(sites),
                descriptions: JSON.stringify(descriptions),
                logins: JSON.stringify(logins),
                passwords: JSON.stringify(passwords),
                new_master_password: encrypt(new_master_password, new_master_password),
            },
            success: function(res) {
                if (res['status'] == "success") {
                    location.href = location.href;
                } else {
                    swal("Ошибка!", res['result']); // Это кастомный alert
                }
            },
        });
    }

    function check_key() { // Функция авторизации/проверки ключа
        var key = $('#in-enterpassword').val();

        if (key === '') { // Если ключ не был введен...
            $('#in-enterpassword').focus(); // Переводим фокус на input
            $('#EnterKeyModal').modal('show'); // Повторяем запрос ключа
        } else {
            key = decrypt(master_password, key); // Расшифровываем полученый пароль введенным ключем

            if (key === '') { // Если расшифровка не дала результата...
                $('#in-enterpassword').val(''); // Чистим input ввода ключа
                $('#in-enterpassword').focus(); // Переводим фокус на input
                $('#EnterKeyModal').modal('show'); // Повторяем запрос ключа
            } else {
                master_password = key; // Присваиваем ключ глобальной переменной "Мастер пароль"
                is_allow_show_page = true;
                $('#EnterKeyModal').modal('hide'); // Скрываем модальное окно ввода пароля
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

    function show_or_copy_password() { // Функция копирования/отображения пароля аккаунта
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

    function encrypt(str, key) { // Функция шифрования строки
        return CryptoJS.AES.encrypt(str, key).toString();
    }

    function decrypt(str, key) { // Функция дешифрования строки
        try {
            return CryptoJS.AES.decrypt(str, key).toString(CryptoJS.enc.Utf8);
        } catch (e) {
            if (e.message == 'Malformed UTF-8 data') { // Если были искажены данные
                return "";
            } else {
                swal("Ошибка!", 'Error: function Decrypt()');
                throw e;
            }
        }
    }

    $("#btnenterpassword").on('click', function() { // Собитие нажатия кнопки "ОК" в модальном окне ввода ключа
        check_key(); // Проходим авторизацию
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
                                change_or_create_master_password($("#in-renewpassword").val());
                            } else {
                                swal('Не правильный старый пароль');
                            }
                        } else {
                            change_or_create_master_password($("#in-renewpassword").val());
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
        show_or_copy_password();
    });

    $("#modal-btn-login").on('click', function() { // Событие нажатия кнопки "Логин" в модальном окне просмотра аккаунта
        copy_clipboard($('#Accounts_table').find('.td-login[data-id="' + $('#modal-btn-delete').attr('data-diss-id') + '"]').text());
    });

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

    $('#EnterKeyModal').on('shown.bs.modal', function() { // Событие открытия модального окна ввода ключа
        // Данное событие необходимо для реализации автофокуса для input
        $('#in-enterpassword').focus();
    });

    $("#EnterKeyModal").on('hidden.bs.modal', function() { // Событие закрытия модального окна ввода ключа
        if (is_allow_show_page) { // Если не нажата кнопка "Отмена"...
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

    $('#in-search').on('keyup', function() {
        if ($(this).val() === "") {
            $('tbody tr').css('display', '');
        } else {
            var td = $('tbody tr .td-site:contains(' + $(this).val() + ')');
            $('tbody tr').fadeOut(100);
            td.parent().fadeIn(100);
        }
    });

    $('#in-enterpassword').on('keydown', function(e) {
        if (e.keyCode === 13) { // Если нажата клавиша "Enter"...
            check_key(); // Проходим авторизацию
        }
    });

    // Событие долгого нажатия кнопки "Пароль" клавишой мыши или сенсором телефона в модальном окне просмотра аккаунта
    $("#modal-btn-password").on('touchend mouseup', (function() { // Событие отжатия клавиши или сенсора
        clearTimeout(press_timer); // Очищаем таймер
    })).on('touchstart mousedown', (function() { // Событие нажатия клавиши или сенсора
        press_timer = window.setTimeout(function() { // Устанавливаем таймер
            is_allow_copy = false; // Запрещаем копирование пароля в буфер обмена так как...
            show_or_copy_password(); // В этой функции мы покажем пароль на экране
        }, 500); // 500 миллисекунд
    }));
});