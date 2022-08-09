var closeButton = document.querySelectorAll('.close')
var modalBackdrop = document.getElementById('bg-modal')
closeButton.addEventListener('click', function(){
modalBackdrop.classList.add('hidden')
console.log("Modal closed")
})
