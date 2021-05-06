// Set up a new Speech Recognizer
const recognition = new webkitSpeechRecognition();
// Set the new language setting.
// More info here: https://stackoverflow.com/questions/14257598/what-are-language-codes-in-chromes-implementation-of-the-html5-speech-recogniti
recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

// Start recognizing after the button is clicked.
document.getElementById("record").onclick = function() {
    document.getElementById("record").style.backgroundColor = "#FF5733";
    recognition.start();
}
recognition.onspeechend = () => {
    document.getElementById("record").style.backgroundColor = "#5a17ee";
}

// Once a result is parsed, send the parsed text to a Rasa server and update HTML
recognition.onresult = function(event) {
    var transcript = event.results[0][0].transcript;
    // console.log(transcript)
    // console.log('Confidence: ' + event.results[0][0].confidence);
    var textnode = document.createElement("h2");
    textnode.innerHTML = `<code>You: ${transcript}</code>`;
    document.getElementById("output").appendChild(textnode);
    
    // Translating languages here
    console.log(transcript);
    console.log(document.getElementById("language").value);
    if(document.getElementById("language").value=="French"){
        // Convert transcript from French to English
    }
    else if(document.getElementById("language").value=="Spanish"){
        // Convert transcript from Spanish to English
    }
    else if(document.getElementById("language").value=="German"){
        // Convert transcript from German to English
    }
    
    let payload = {
        method: "POST",
        body: JSON.stringify({text: transcript})        
    }
    fetch("/api/", payload)
    .then(result => {
        result.json()
        .then(response => {
            console.log(response[0].text);

            // Convert back to english here
            if(document.getElementById("language").value=="French"){
                // Convert transcript from English to French
            }
            else if(document.getElementById("language").value=="Spanish"){
                // Convert transcript from English to Spanish
            }
            else if(document.getElementById("language").value=="German"){
                // Convert transcript from English to German
            }

            let textnode = document.createElement("h2");
            textnode.innerHTML = `<code>Bot: ${response[0].text}</code>`;
            document.getElementById("output").appendChild(textnode);
            // console.log(speechSynthesis.volume);
            speechSynthesis.speak(new SpeechSynthesisUtterance(response[0].text));
        })
    })
    .catch(error => console.log(error));
}
// voiceOn="https://www.freeiconspng.com/thumbs/sound-png/sound-png-3.png";
// voiceOff="https://www.freeiconspng.com/thumbs/sound-off-icon/mute-off-sound-off-icon-1.png"
voiceOn = "./static/images/voiceOn.png";
voiceOff = "./static/images/voiceOff.png";
document.getElementById("mute-unmute").onclick = () => {
    var button = document.getElementById('mute-unmute');
    if(button.src.match(voiceOn)){
        SpeechSynthesisUtterance.volume = 0;
        button.setAttribute("src", voiceOff);
    } else {
        SpeechSynthesisUtterance.volume = 1;
        button.setAttribute("src", voiceOn);
    }
}