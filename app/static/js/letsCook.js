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
				'<span id="lmOne">Going to the store...</span>' +
				'<span id="lmTwo">Calling Mom...</span>' +
				'<span id="lmThree">Looking in the fridge...</span>' +
				'<span id="lmFour">Browsing through cookbooks...</span>' +
                '<span id="lmFive">Putting out fire...</span>' +
                '<span id="lmSix">Trying to find your Facebook account...</span>' +
                '<span id="lmSeven">Doing a taste test...</span>' +
                '<span id="lmEight">Buying new stove...</span>' +
				'<span id="lmNine">Your recipes are on their way!</span>' +
			'</div>' +
        '</div>' +
	   '</div>';
	   
	   
		var delayCount = 1500;
		$(over).appendTo('body');
		$('#lmTwo').hide();
		$('#lmThree').hide();
		$('#lmFour').hide();
		$('#lmFive').hide();
        $('#lmSix').hide();
        $('#lmSeven').hide();
        $('#lmEight').hide();
        $('#lmNine').hide();
		$('#lmOne').delay(delayCount).fadeOut(800);
		$('#lmTwo').delay(delayCount*2).fadeIn(800).delay(delayCount).fadeOut(800);
		$('#lmThree').delay(delayCount*4).fadeIn(800).delay(delayCount).fadeOut(800);
		$('#lmFour').delay(delayCount*6).fadeIn(800).delay(delayCount).fadeOut(800);
        $('#lmFive').delay(delayCount*8).fadeIn(800).delay(delayCount).fadeOut(800);
        $('#lmSix').delay(delayCount*10).fadeIn(800).delay(delayCount).fadeOut(800);
        $('#lmSeven').delay(delayCount*12).fadeIn(800).delay(delayCount).fadeOut(800);
        $('#lmEight').delay(delayCount*14).fadeIn(800).delay(delayCount).fadeOut(800);
		$('#lmNine').delay(delayCount*16).fadeIn(800);
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
            $('#ingredient-form-incing').removeClass('has-error');
            $.ajax({
                url: '/recipe-list/0',
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
            if ( $('#error-message').length ){
                ;
            }
            else{
                $('#letsCookDiv').append('<div style="margin-top: 5px;" id="error-message">Sorry, you need to add at least one ingredient, silly!</div>')
            }
            $('#ingredient-form-incing').addClass('has-error');
        }
    });

    $('#inRush').click(function(){
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
            $('#ingredient-form-incing').removeClass('has-error');
            $.ajax({
                url: '/recipe-list/1',
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
            if ( $('#error-message').length ){
                ;
            }
            else{
                $('#letsCookDiv').append('<div style="margin-top: 5px;" id="error-message">Sorry, you need to add at least one ingredient, silly!</div>')
            }
            $('#ingredient-form-incing').addClass('has-error');
        }
    });
});