$(function() {
	$('.random-string').text(generate_random_string(16));

    setInterval(
    	function() { $('.random-string').text(generate_random_string(16)); },
        2000
    );
});