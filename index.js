var locationButton = document.getElementById('locations-button')
var settingsButton = document.querySelectorAll('settings-button')

// var xhttp = new XMLHttpRequest();
// xhttp.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//         scoreData = JSON.parse(this.responseText);
//         for (var i = 0; i < Object.keys(scoreData).length; i++) {
//             var tr = high_scores_table.insertRow()
//             tr.classList.add('score-entry')
//             var place = tr.insertCell()
//             place.appendChild(document.createTextNode(i+1))
//             var name = tr.insertCell()
//             name.appendChild(document.createTextNode(Object.keys(scoreData)[i]))
//             var score = tr.insertCell()
//             score.appendChild(document.createTextNode(scoreData[Object.keys(scoreData)[i]]))
//         }
//     }
// };
// xhttp.open("GET", "/scores", true);
// xhttp.send();

locationsButton.addEventListener('click', function(){
    window.location.href='/locations'
})

settingsButton.addEventListener('click', function(){
    window.location.href='/settings'
})
