/* Личный кабинет */

$(function() {
    let storage = window.localStorage;

    $('.simple-tabs').on('click', function() {
        /* Переключение вкладок меню */
        $('.swiper-container').find('div').removeClass('active');
        $('[data-tabs="' + $(this).attr('data-tabs-id') + '"]').addClass('active');
    });

    $(".js-auth-location").hover(
        /* Показать ip адрес при наведении на локацию */
        function() {
            $('.auth-ip[data-number="' + $(this).attr('data-number') + '"]').show();
        },
        function() {
            $('.auth-ip[data-number="' + $(this).attr('data-number') + '"]').hide();
        }
    );

    $(".auth-ip").hover(
        /* Чтобы блок с ip адресом не пропал если hover переходит с локации на блок ip адреса */
        function() {
            $(this).show();
        },
        function() {
            $(this).hide();
        }
    );

    $('.simple-tabs').on('click', function() {
        /* Задаем активный раздел */
        storage.setItem('lk_active_swiper_tab', $(this).attr('data-tabs-id'));
    });

    let tab = storage.getItem('lk_active_swiper_tab');

    if (tab == null) {
        // Если значение не найдено то ставим первый раздел
        tab = '1';
        storage.setItem('lk_active_swiper_tab', tab);
    }

    // Активируем раздел
    $('.js-swiper-tabs[data-tabs="' + tab + '"]').addClass('active');

    function formatDate(format_date, format_string)
    {
        let yyyy = format_date.getFullYear();
        let yy = yyyy.toString().substring(2);
        let m = format_date.getMonth() + 1;
        let mm = m < 10 ? '0' + m : m;
        let d = format_date.getDate();
        let dd = d < 10 ? '0' + d : d;

        let H = format_date.getHours();
        let HH = H < 10 ? '0' + H : H;
        let M = format_date.getMinutes();
        let MM = M < 10 ? '0' + M : M;
        let S = format_date.getSeconds();
        let SS = S < 10 ? '0' + S : S;

        format_string = format_string.replace(/yyyy/i, yyyy);
        format_string = format_string.replace(/yy/i, yy);
        format_string = format_string.replace(/mm/i, mm);
        format_string = format_string.replace(/m/i, m);
        format_string = format_string.replace(/dd/i, dd);
        format_string = format_string.replace(/d/i, d);
        format_string = format_string.replace(/HH/i, HH);
        format_string = format_string.replace(/H/i, H);
        format_string = format_string.replace(/ii/i, MM);
        format_string = format_string.replace(/i/i, M);
        format_string = format_string.replace(/SS/i, SS);
        format_string = format_string.replace(/S/i, S);

        return format_string;
    }

    Date.prototype.format = function(format)
    {
        return formatDate(this, format);
    }

    $('.js-auth-date').each(function() {
        let date = new Date(Date.parse($(this).text().replace(/\s/g, '').replace('_', 'T')));
        let current_date = new Date();
        let string = '';

        if (current_date.format('dd') == date.format('dd')) {
            string = 'Сегодня в ' + date.format('HH:ii');
        } else if (current_date.format('dd') == (parseInt(date.format('dd')) - 1).toString()) {
            string = 'Вчера в ' + date.format('HH:ii');
        } else if (current_date.format('yyyy') == date.format('yyyy')) {
            string = date.format('dd.mm') + ' в ' + date.format('HH:ii');
        } else {
            string = date.format('dd.mm.yyyy') + ' в ' + date.format('HH:ii');
        }

        $(this).text(string);
    });
});