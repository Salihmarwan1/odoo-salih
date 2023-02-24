odoo.define('api_regcheck.reg_check', function (require) {
    'use strict';

    console.log("loaddeddd")


    var publicWidget = require('web.public.widget');

    publicWidget.registry.RegCheckFlow = publicWidget.Widget.extend({
        selector: '.vehicle-search-container',
        events: {
            'click #get_car_model':'_get_car_model2',
        },

       
        _get_car_model2: async function () {
            var self = this;
            console.log("_get_car_model")
            console.log(this)
            console.log(document.getElementById("plate_number").value)
            var reg_val = document.getElementById("plate_number").value
            await self._rpc({
                model: 'vehicle.information',
                model_description : 'vehicle.information',
                make : 'vehicle.information',
                method: 'get_vehicle_information',
                args: [[reg_val]],
                kwargs: {
                    
                },
            }).then(res => {
                console.log(res['registration_number'])
                console.log(res['model_description'])
                console.log(res['car_make'])
                console.log(res['model']) 
                console.log(res['car_model'])
                //document.getElementById("model_field").value = res['model_description'] +" "+ res['year']
                document.getElementById("model_field").value = res['car_make'] +" "+ res['car_model'] +" "+ res['year'] 
                
                //Hitta fortsätt länken och updatera href med rätt bil model.
                var url = $('#confirm').attr('href')
                var model = $('#model_field').val() 
                
            })   
            //console.log(response)
        },

        
   

    });
});
