const already_have_an_account = document.querySelector('.already_have_an_account');
const login_box = document.querySelector('.login-box');

const register_box = document.querySelector('.register-box');
const does_not_have_acccnt = document.querySelector('.does_not_have_acccnt');

const ap_login_reg_nxt_btn = document.querySelector('#ap_login_reg_nxt_btn');
const ap_main_reg_form = document.querySelector('.ap_main_reg_form');
const verification_code_main_box = document.querySelector('.verification_code_main_box');
const ap_login_reg_sbmit_btn = document.querySelector('#ap_login_reg_sbmit_btn');

ap_login_reg_nxt_btn.onclick = () => {
    ap_login_reg_nxt_btn.style.display = 'none';
    ap_main_reg_form.style.display = 'none';
    ap_main_reg_form.classList.add('hide');
    ap_main_reg_form.classList.remove('show');

    verification_code_main_box.classList.add('show');
    verification_code_main_box.classList.remove('hide');

    ap_login_reg_sbmit_btn.classList.add('show');
    ap_login_reg_sbmit_btn.classList.remove('hide');
}



function showLoginBox() {
    login_box.style.display = 'block';
    register_box.style.display = 'none';
}

function hideLoginBox() {
    login_box.style.display = 'none';
    register_box.style.display = 'block';
}

