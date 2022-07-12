var backButton = document.getElementById('back-button')
var weatherCheckbox = document.getElementById('weather-checkbox')

backButton.addEventListener('click', function(){
    window.history.back()
    console.log("back button clicked")
})

weatherCheckbox.addEventListener('change', function(){
    if(this.checked){
        console.log("Weather checkbox CHECKED")
    }
    else {
        console.log("Weather checkbox UNCHECKED");
    }

})
