//const axios = require('axios');
BASE_URL = "http://127.0.0.1:5000"

$("#submitGuess").on("click", () => sendData, $(this).val())

async function sendData(word) {
    alert('in heree')
    const response = await axios({
        url: `${BASE_URL}/check_word`,
        method: "POST",
        data: {
            word: word
        }
    });
    console.debug(response)
    return response
}
