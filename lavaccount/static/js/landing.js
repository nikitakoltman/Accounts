/* Лендинг */

$(function() {
	// Демонстрация работы генератора паролей
	$('.random-string').text(generate_random_string(10));

    setInterval(
    	function() { $('.random-string').text(generate_random_string(10)); },
        2000
    );
});