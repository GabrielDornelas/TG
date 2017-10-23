var five = require('johnny-five');
var arduino = new five.Board();

arduino.on('ready', function(){
	var potenciometro = new five.Sensor({
		pin: "A0",
		freq: 500
	});
	potenciometro.on("data", function(){
		console.log(this.value);
	});
});