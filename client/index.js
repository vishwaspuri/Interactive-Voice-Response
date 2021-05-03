// Set up a new Speech Recognizer
const recognition = new webkitSpeechRecognition();
// Set the new language setting.
// More info here: https://stackoverflow.com/questions/14257598/what-are-language-codes-in-chromes-implementation-of-the-html5-speech-recogniti
recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

// Start recognizing after the button is clicked.
document.getElementById("record").onclick = function() {
  recognition.start();
  console.log('Listening...');
}

// Once a result is parsed, send the parsed text to a Rasa server and update HTML
recognition.onresult = function(event) {
    // Log the transcript to the console.
    var transcript = event.results[0][0].transcript;
    console.log(transcript)
    console.log('Confidence: ' + event.results[0][0].confidence);
    var textnode = document.createElement("h2");
	textnode.innerHTML = `<code>You: ${transcript}</code>`;
	document.getElementById("output").appendChild(textnode);
    let payload = {
        method: "POST",
        body: JSON.stringify({text: transcript})        
    }
    fetch("/api/", payload)
    .then(result => {
        result.json()
        .then(response => {
            console.log(response);
            let textnode = document.createElement("h2");
            textnode.innerHTML = `<code>Bot: ${b.body}</code>`;
            document.getElementById("output").appendChild(textnode)
        })
    })
    .catch(error => console.log(error));
}