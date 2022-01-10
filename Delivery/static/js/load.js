var navCustom = document.querySelector('.navCustom');

var cross = document.querySelector('.form-main img');
cross.addEventListener('click',dismiss);

function dismiss(){
    navCustom.classList.add('active');
    //navCustom.remove();
} 