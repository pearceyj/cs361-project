var startButton = document.getElementById('start-button')
var closeModalButton = document.querySelectorAll('.close-modal-button')
var modalBackdrop = document.getElementById('modal-backdrop')
var guideButton = document.getElementById('guide-button')
var guideModal = document.getElementById('guide-modal')
var highScoreButton = document.getElementById('scores-button')
var highScoreModal = document.getElementById('high-score-modal')
var tableHeader = document.getElementById('table-header')
var high_scores_table = document.getElementById('highscores-table')

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        scoreData = JSON.parse(this.responseText);
        for (var i = 0; i < Object.keys(scoreData).length; i++) {
            var tr = high_scores_table.insertRow()
            tr.classList.add('score-entry')
            var place = tr.insertCell()
            place.appendChild(document.createTextNode(i+1))
            var name = tr.insertCell()
            name.appendChild(document.createTextNode(Object.keys(scoreData)[i]))
            var score = tr.insertCell()
            score.appendChild(document.createTextNode(scoreData[Object.keys(scoreData)[i]]))
        }
    }
};
xhttp.open("GET", "/scores", true);
xhttp.send();

startButton.addEventListener('click', function(){
    window.location.href='/gameplay'
})

guideButton.addEventListener('click', function(){
    modalBackdrop.classList.remove('hidden')
    guideModal.classList.remove('hidden')
})

highScoreButton.addEventListener('click', function(){
    modalBackdrop.classList.remove('hidden')
    highScoreModal.classList.remove('hidden')
    console.log(highScoreModal)
})

//closes both the guide and high-score modal
for(var i = 0; i < closeModalButton.length; i++){
    closeModalButton[i].addEventListener('click', function(event){
        event.target.parentNode.parentNode.classList.add('hidden')
        modalBackdrop.classList.add('hidden')
    })
}
