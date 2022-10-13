BASE_URL = "http://127.0.0.1:5000"
class WordList {
    constructor() {
        this.usedWords = new Set()
        this.score = 0

        setTimeout(this.timesUp.bind(this), 10000)

        //we put the submit button here and bind it here so that it will pass THIS particular form 
        $("#myForm").on("submit", this.checkCorrectness.bind(this))
    }

    checkDup(word) {
        return this.usedWords.has(word)
    }

    listWords(word) {
        $("#listOfWords").append(`<li>${word}</li>`)

    }
    async timesUp() {
        $('#submitGuess').prop('disabled', true)
        $('#guess').prop('disabled', true)
        $('#timer').text('Time is up!')
        //save the highest score in session and how many times they played
        await this.moreStatistics()
    }

    addToList(word) {
        this.usedWords.add(word)
    }

    async checkCorrectness(e) {
        console.log(e)
        e.preventDefault()
        let word = $("#guess").val()

        if (this.checkDup(word)) {
            $('#result').text('already used!')
        }

        try {
            const response = await axios({
                url: `${BASE_URL}/check_word`,
                method: "GET",
                params: {
                    guess: word
                }
            });

            if (response.data.result == "ok") {
                $("#result").text('Good guess!')
                // add score
                this.score += word.length
                $('#guess').val('')
                this.addToList(word)
                this.listWords(word)
            } else if (response.data.result == "not-on-board") {
                $("#result").text('Doesn not exist on board!')
            } else if (response.data.result = "not-a-word") {
                $("#result").text('Not a word!')
            }
            $("#score").text(`Your score is ${this.score}!`)
        } catch (e) {
            console.log(e)
            console.log('something went wrong')
        }
    }

    async moreStatistics() {
        try {
            const response = await axios({
                url: `${BASE_URL}/more_statistics`,
                method: "POST",
                data: {
                    score: this.score
                }
            });
            console.log(response)
            $('#highestScore').text(`Your highest score is ${response.data}`)

        } catch (e) {
            console.log(e)
            console.log('something went wrong in more statistics')
        }
    }
}



