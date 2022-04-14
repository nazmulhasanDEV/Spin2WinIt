const span_inner_close_btn = document.querySelector('#span_inner_close_btn');
const game__prize__flash__message = document.querySelector('.game__prize__flash__message');
const flash_msg_main_content = document.querySelector('.flash_msg_main_content');
let winning__moment__audio = document.querySelector('#winning__moment__audio');

span_inner_close_btn.onclick = () =>{
    game__prize__flash__message.style.display = 'none';
    flash_msg_main_content.style.display = 'none';
    winning__moment__audio.pause();
    winning__moment__audio.currentTime = 0;
}