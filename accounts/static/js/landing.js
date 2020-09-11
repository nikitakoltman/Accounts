$(function() {
	generate_random_string();

    setInterval(
    	function() { generate_random_string() },
        2000
    );

    function generate_random_string() {
        let alphabet = 'qwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()*QWERTYUIOPASDFGHJKLZXCVBNM',
            word = '';
        for (let i = 0; i < 20; i++) {
            word += alphabet[Math.round(Math.random() * (alphabet.length - 1))];
        }
        $('.random-string').text(word);
    }
});