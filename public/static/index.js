var locationsButton = document.getElementById('nav-locations-button')
var settingsButton = document.getElementById('nav-settings-button')
var infoButton = document.getElementById('nav-info-button')


locationsButton.addEventListener('click', function(){
    window.location.href='/locations'
    console.log("location button clicked")
})

settingsButton.addEventListener('click', function(){
    window.location.href='/settings'
    console.log("settings button clicked")
})

infoButton.addEventListener('click', function(){
    window.location.href='/information'
    console.log("Information button clicked")
})
