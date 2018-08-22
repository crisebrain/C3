'use strict'

var accessToken;
// Session can be a random numbers or some type of user and session identifiers (preferably hashed). The length of the Session ID must not exceed 36 characters.
// TODO: Deben generar una sesión nueva para cada usuario que consuma la página, y mantener ese ID de session
// hasta que el usuario cierre la página.
var session = "miSesionDePruebaGabriel";
const agent = "facturasvoz-estable";
const baseUrl = "https://dialogflow.googleapis.com/v2/projects/" + agent + "/agent/sessions/" + session + ":detectIntent";
const lang = "es-MX";
const client = "paginaWeb";
const urlTokens = "https://200.66.102.202:6020/getToken";

var sampleRateHertz = 16000; // Framerate ideal
var downloadLink;
var recorder;
var stream;
var audioBase64;
var blob;

const configRecorder = {
	bufferLen: 4096,
	numChannels: 1,
	mimeType: 'audio/wav'
}


$.getScript("./dist/recorder.js", function() {
	console.log("cargado recorder.js");
});


// function dynamicallyLoadScript(url) {
//     var script = document.createElement("script"); // Make a script DOM node
//     script.src = url; // Set it's src to the provided URL

//     document.head.appendChild(script); // Add it to the end of the head section of the page (could change 'head' to 'body' to add it to the end of the body section instead)
// }


$(document).ready(function() {
	$("#input").keypress(function(event) {
		if (event.which == 13) {
			event.preventDefault();
			send("text");
		}
	});
	$("#rec").click(function(event) {
		switchRecorder();
	});

	downloadLink = document.getElementById('download');
});

function startRecord() {
	recorder && recorder.record();
    console.log('Recording...');
    updateRec();
}

function stopRecord() {
    recorder && recorder.stop();

    console.log('Stopped recording.');

    recorder.exportWAV(blob => {
    	window.blob = blob;
    	blobToDF();
    	createDownloadLink(); // TODO: si no necesitan el audio original comenten esta linea.
    });
    updateRec();
    clearVariables();
}

function clearVariables() {
	stream.getTracks().forEach(track => track.stop());
    stream.getTracks().forEach(track => stream.removeTrack(track));
    recorder.clear();
    
    recorder = null;
    stream = null;
}

function createDownloadLink() {
	var url = URL.createObjectURL(blob);
	downloadLink.href = url;
	downloadLink.download = new Date().toISOString() + '.wav';
}

function blobToDF() {
	var reader = new window.FileReader();

	reader.readAsDataURL(blob);
	reader.onloadend = function() {
		var base64;
		base64 = reader.result;
		base64 = base64.split(',')[1];
		window.audioBase64 = base64;
		send("audio");
	}
}

// Esta es la función principal que deben llamar para poder integrarla a sus desarrollos
function switchRecorder() {
	if (!recorder || recorder.recording == false) {
		try {
			navigator.mediaDevices.getUserMedia({ audio: true, video: false })
				.then(handleSuccess)
				.catch( (err)=> {
					msgUserErrorStream();
				});
			}
		catch(err)
		{
			console.log(err);
			msgUserErrorStream();
		}
	} else {
		stopRecord();
	}
}

// TODO: Completen esta función como mejor les apetezca.
function msgUserErrorStream() {
	alert("Ocurrió un error al intentar acceder al micrófono. Por favor:\n" + 
		"\n-Actualice el navegador" +
		"\n-Permita a su navegador acceder al micrófono." +
		"\n-Verifique la configuración del micrófono");
}

// TODO: Completen esta función como mejor les apetezca.
function incompatibleBrowser() {
	alert("Su navegador no es compatible con la grabación de voz. Por favor actualícelo.");
}

function setInput(text) {
	$("#input").val(text);
}

function updateRec() {
	console.log("updateRec")
	if(recorder)
		$("#rec").text(recorder.recording ? "Detener" : "Hablar");
}

function send(typePetition) {
	console.log("Asking for token")
	// Get Token for AUTH V2
	$.ajax({
		type: "POST",
		url: urlTokens,
		contentType: "application/json; charset=UTF-8",
		dataType: "json",
		data: JSON.stringify(
			{
				"client": client,
				"session": session,
				"agent": agent
			}),
		success: function(data) {
			console.log("Token received")
			accessToken = data.token;
			console.log(typePetition);
			sendToDF(typePetition);
		},
		error: function() {
			setResponse("Error al obtener el token.\n\n" + arguments[0].responseText);
			console.log(arguments);
		}
	});
	

	setResponse("Cargando...");
}


function sendToDF(typePetition) {
	var phraseHints = ["acuse", "acuse pendiente", "nit", "nit adquiriente", "rfc", "rfc es", "facturar"]

	console.log("Envio audio")

	function typeJson(typePetition) {
		if (typePetition == "text") {
			var text = $("#input").val();
			return JSON.stringify(
				{
					"queryInput": {
						"text": {
							"text": text,
	            			"languageCode": lang
	            		}
	            	}
				})
		}
		else if (typePetition == "audio") {
			return JSON.stringify(
			{
	            "queryInput":{
	                "audioConfig": {
	                    "audioEncoding": "AUDIO_ENCODING_LINEAR_16",
	                    "sampleRateHertz": sampleRateHertz,
	                    "languageCode": lang,
	                    "phraseHints": phraseHints
	                }
	            },
	            "inputAudio": audioBase64
	        })
		}
	}

	$.ajax({
		type: "POST",
		url: baseUrl,
		contentType: "application/json; charset=UTF-8",
		dataType: "json",
		headers: {
			"Authorization": "Bearer " + accessToken
		},
		data: typeJson(typePetition),

		success: function(data) {
			console.log("Recibo respuesta.")
			setResponse(JSON.stringify(data, undefined, 2));
			// TODO: Aquí manden a llamar su función que haga las peticiones.
		},
		error: function() {
			setResponse("Internal Server Error\n\n" + arguments[0].responseText);
			console.log(arguments[0].responseText);
		}
	});
}

// TODO: esta función establece la respuesta, edítenla según sus necesidades.
function setResponse(val) {
	$("#response").text(val);
}


var handleSuccess = (stream) => {
	var context;
	var input;

	this.stream = stream;

	try {
		context = new AudioContext({sampleRate: sampleRateHertz});
		input = context.createMediaStreamSource(stream);
	}
	catch(err) {
		if (err.name == "NotSupportedError"){
			console.log("Not supported sampleRate at " + sampleRateHertz + " Hz");
			context = new AudioContext();
			input = context.createMediaStreamSource(stream);
		}
	}

	// Se actualiza al sampleRate real
	if(input)
    	window.sampleRateHertz = input.context.sampleRate;
    	console.log("Media stream created at " + window.sampleRateHertz + " Hz");

    recorder = new Recorder(input, configRecorder);
    console.log('Recorder initialised.');

    startRecord();
};


// dynamicallyLoadScript("./dist/recorder.js");
