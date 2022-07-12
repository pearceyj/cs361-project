var locationsButton = document.getElementById('nav-locations-button')
var settingsButton = document.getElementById('nav-settings-button')


locationsButton.addEventListener('click', function(){
    window.location.href='/locations'
})

settingsButton.addEventListener('click', function(){
    window.location.href='/settings'
})
