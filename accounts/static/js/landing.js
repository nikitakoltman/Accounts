$(function() {
	generate_random_string();

    setInterval(
    	function() { generate_random_string(16) },
        2000
    );

    function generate_random_string(length_string) {
        let chars = 'qwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()*QWERTYUIOPASDFGHJKLZXCVBNM',
            word = '';
        for (let i = 0; i < length_string; i++) {
            word += chars[Math.round(Math.random() * (chars.length - 1))];
        }
        $('.random-string').text(word);
    }
});