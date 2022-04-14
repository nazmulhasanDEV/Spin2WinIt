const product__main__thumbnail__img = document.querySelector('.product__main__thumbnail__img')
const product__extra__images = document.querySelector('.product__extra__images');
const warning__msg = document.querySelector('.warning__msg');
const admin__prdctAdd_btn = document.querySelector('.admin__prdctAdd_btn');

const product__main__thumbnail__img_btn = document.querySelector('.product__main__thumbnail__img_btn');
const product__extra__images_btn = document.querySelector('.product__extra__images_btn');

const prev_thumb_img = document.querySelector('.prev_thumb_img');
const img_prev_list_for_extra_imgs = document.querySelector('.img_prev_list_for_extra_imgs');

const policy__section = document.querySelector('.policy__section');
const policy__option = document.querySelector('.policy__option');

product__main__thumbnail__img.style.display = 'none';
product__extra__images.style.display = 'none';
policy__section.style.display = 'none';

product__main__thumbnail__img_btn.onclick =()=>{
    product__main__thumbnail__img.click();
}


product__extra__images_btn.onclick =()=>{
    product__extra__images.click();
}


product__main__thumbnail__img.onchange = (e) =>{
    const [thumb_img] = product__main__thumbnail__img.files;

    if (thumb_img) {
        prev_thumb_img.src = URL.createObjectURL(thumb_img);
    }
}

product__extra__images.onchange = (e) =>{
    const extran_imgs = product__extra__images.files;
    if (extran_imgs['length'] > 5) {
        admin__prdctAdd_btn.disabled = 'true';
    }
    if (extran_imgs) {
        for (let i of extran_imgs) {
            const new_img = document.createElement('img');
            new_img.src = URL.createObjectURL(i);
            new_img.classList.add('extra__prev_imgs_size');
            img_prev_list_for_extra_imgs.appendChild(new_img);
        }
    }
}

if (policy__option.value == 'own') {
    policy__section.style.display = 'inherit';
}

policy__option.onchange = (e) => {
    if (e.target.value === 'own') {
          policy__section.style.display = 'inherit';
    }else {
        policy__section.style.display = 'none';
    }
}