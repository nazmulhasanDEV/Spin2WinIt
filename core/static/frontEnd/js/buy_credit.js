const credit__amount = document.querySelector('.credit__amount');
const amount_to__be_charged = document.querySelector('.amount_to__be_charged');


credit__amount.oninput = (e) =>{


//ajax starts

$.ajax({
         url:'',
         type:'get',
         data: {
            credit_amount: e.target.value,
         },
         success: function(response){
            let credit_amnt = response.credit_amount;
            amount_to__be_charged.value = (credit_amnt * (0.10)).toFixed(2);
         },
       });
//ajax ends

}