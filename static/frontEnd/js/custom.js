const close__video = document.querySelector('.close_video');
const ads__video = document.querySelector('.ads__video');



close__video.onclick = ()=>{
    ads__video.pause();
}

