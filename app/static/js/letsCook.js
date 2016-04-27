$(function(){
	var loading = function(){
		var over = '<div id="overlay">'+
        '<div id="fountainG">'+
            '<div id="fountainG_1" class="fountainG"></div>'+
            '<div id="fountainG_2" class="fountainG"></div>'+
            '<div id="fountainG_3" class="fountainG"></div>'+
            '<div id="fountainG_4" class="fountainG"></div>'+
            '<div id="fountainG_5" class="fountainG"></div>'+
            '<div id="fountainG_6" class="fountainG"></div>'+
            '<div id="fountainG_7" class="fountainG"></div>'+
            '<div id="fountainG_8" class="fountainG"></div>'+
			'<br><div id="loadingMessage">' +
				'<div id="lmOne">Going to the store...</div>' +
				'<div id="lmTwo">Calling Mom...</div>' +
				'<div id="lmThree">Looking in the fridge...</div>' +
				'<div id="lmFour">Browsing through cookbooks...</div>' +
				'<div id="lmFive">Your recipes are on their way!</div>' +
			'</div>' +
        '</div>' +
	   '</div>';
	   
	   
		var delayCount = 1500;
		$(over).appendTo('body');
		$('#lmTwo').hide();
		$('#lmThree').hide();
		$('#lmFour').hide();
		$('#lmFive').hide();
		$('#lmOne').delay(delayCount).fadeOut(800);
		$('#lmTwo').delay(delayCount*2).fadeIn(800).delay(delayCount).fadeOut(800);
		$('#lmThree').delay(delayCount*4).fadeIn(800).delay(delayCount).fadeOut(800);
		$('#lmFour').delay(delayCount*6).fadeIn(800).delay(delayCount).fadeOut(800);
		$('#lmFive').delay(delayCount*8).fadeIn(800);
	}
	
    $('#letsCook').click(function(){
        var ingredients = [$('#ingredient1').val(),$('#ingredient2').val(),$('#ingredient3').val(),$('#ingredient4').val()];
        var has_ingredients = false;
        for (var i = 0; i < ingredients.length; i++) {
            if(ingredients[i]){
                has_ingredients = true;
                break;
            }
        };

        if(has_ingredients){
            $('#letsCookDiv').remove("#error-message")
            $('#ingredient-form').removeClass('has-error');
            $.ajax({
                url: '/recipe-list',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response){
                    console.log(response);
                    window.location = '/recipe-list/view';
                },
                error: function(error){
                    console.log(error);
                }
            });
            loading();
        }
        else {
            $('#letsCookDiv').append('<div style="margin-top: 5px;" id="error-message">Sorry, you need to add at least one ingredient, silly!</div>')
            $('#ingredient-form').addClass('has-error');
        }
    });

    $('#testRecipe').click(function(){
        window.location = '/recipe-list/view';
        // $.ajax({
        //     url: '/recipe-list/view',
        //     data: 'testing',
        //     type: 'GET',
        //     success: function(data, response){
        //         console.log(response);
        //         window.location = '/recipe-list/view';
        //     },
        //     error: function(error){
        //         console.log(error);
        //     }
        // });
    });
});