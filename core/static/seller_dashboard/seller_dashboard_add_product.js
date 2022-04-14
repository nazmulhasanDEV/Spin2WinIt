const ap_addProduct_category = document.getElementById('ap_addProduct_category');
const ap_addProduct_subcategory = document.querySelector('.ap_addProduct_subcategory');


ap_addProduct_category.onchange = (e) =>{


//ajax starts

ap_addProduct_subcategory.innerHTML = '';

$.ajax({
         url:'/seller/add/product/',
         type:'get',
         data: {
            current_prodct_cat: e.target.value,
         },
         success: function(response){
            let data_length = response.crrnt_product_subcat;
            data_length.map((data)=>{
                console.log(data);
                const option = document.createElement('option');
                option.value = data.id;
                option.innerHTML = data.name;
                ap_addProduct_subcategory.append(option);
            })
         },

       });
//ajax ends

}