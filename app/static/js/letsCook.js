$(function(){
	var loading = function(){
		var over = '<div id="overlay">' +
			'<img id="loading" src="../static/css/loading.css">' +
			'</div>';
		$(over).appendTo('body');
	}
    $('#letsCook').click(function(){
        $.ajax({
            url: '/recipe-list',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});