const weight_criteria = document.querySelector('#weight_criteria');
const select_product = document.querySelector('#select_product');
const add_group_up_products_btn = document.querySelector('.add_group_up_products_btn');
const selected_products_byCriteria = document.querySelector('#selected_products_byCriteria');

weight_criteria.onchange = (e) =>{
//ajax starts
$.ajax({
         url:'/ap/group/up/products/by/shipping/class/',
         type:'get',
         data: {
            weight_criteria_id: e.target.value,
         },
         success: function(response){
            let products = response.products;
            products.map((product)=>{
                const option = document.createElement('option');
                option.value = product.id;
                option.innerHTML = product.title;
                select_product.append(option);
            })
         },
       });
//ajax ends
}


add_group_up_products_btn.onclick = (e) =>{

var selectedOptions = [...select_product.options].filter(option=>option.selected).map(option=>option.value);

//ajax starts
$.ajax({
         url:'/ap/group/up/products/by/shipping/class/',
         type:'get',
         data: {
            selectedProductsByCriteria: JSON.stringify(selectedOptions),
         },
         //JSON.stringify(users)
         success: function(response){
            let products = response.crnt_selected_all_products_by_criteria;
            products.map((product)=>{
                const option = document.createElement('option');
                option.value = product.id;
                option.selected = true;
                option.innerHTML = product.title;
                selected_products_byCriteria.append(option);
            })
         },
       });
//ajax ends
}