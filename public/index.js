var locationButton = document.getElementById('locations-button')
var settingsButton = document.querySelectorAll('settings-button')


locationsButton.addEventListener('click', function(){
    window.location.href='/locations'
})

settingsButton.addEventListener('click', function(){
    window.location.href='/settings'
})
