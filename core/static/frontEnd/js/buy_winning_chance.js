const number_of_winning_chance = document.querySelector('#number_of_winning_chance');
const point_to_be_charged = document.querySelector('#point_to_be_charged');


number_of_winning_chance.oninput = (e) =>{


//ajax starts

$.ajax({
         url:'/fe/buy/winning/chance/',
         type:'get',
         data: {
            winning_chance_number: e.target.value,
         },
         success: function(response){
            let number_of_winnging_chance = response.number_of_winnging_chance;
            point_to_be_charged.value = (number_of_winnging_chance * 0.333).toFixed(2);
//            point_to_be_charged.value = number_of_winnging_chance * 2;
         },
       });
//ajax ends

}