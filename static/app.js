
BASE_URL = "http://127.0.0.1:5000"
let score = 0

$("#myForm").on("submit", sendData)

setTimeout(function () {
    $('#submitGuess').prop('disabled', true)
    $('#guess').prop('disabled', true)
    $('#timer').text('Time is up!')
    //save the highest score in session and how many times they played
    moreStatistics()
}, 10000)

async function sendData(e) {
    e.preventDefault()
    word = $("#guess").val()
    console.log(word)
    try {
        const response = await axios({
            url: `${BASE_URL}/check_word`,
            method: "GET",
            params: {
                guess: word
            }
        });
        console.log(response)

        if (response.data.result == "ok") {
            $("#result").text('Good guess!')
            // add score
            score += word.length

        } else if (response.data.result == "not-on-board") {
            $("#result").text('Doesn not exist on board!')
        } else {
            $("#result").text('Not a word!')
        }
        $("#score").text(`Your score is ${score}!`)
    } catch (e) {
        console.log(e)
        console.log('something went wrong')
    }
}

async function moreStatistics() {
    try {
        const response = await axios({
            url: `${BASE_URL}/more_statistics`,
            method: "POST",
            data: {
                score: score
            }
        });
        console.log(response)


    } catch (e) {
        console.log(e)
        console.log('something went wrong')
    }
}