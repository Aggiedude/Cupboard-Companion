//http://bootsnipp.com/snippets/featured/dynamic-form-fields-add-amp-remove

$(document).ready(function(){	
	var addIncIngNext = 4;
	$('#addIncIngButton').click(function(){
		var addto = "#ingredient-form-incing";
		addIncIngNext = addIncIngNext + 1;
		var newIn = '<div class="form-group">' +
		'<label for="ingredient' + addIncIngNext +'" class="col-sm-4 control-label">Ingredient ' + addIncIngNext + '</label>' +
			'<div class="col-sm-8">' +
				'<input type="text" class="form-control" name="ingredient' + addIncIngNext +'" id="ingredient' + addIncIngNext + '" placeholder="ingredient ' + addIncIngNext + '">' +
			'</div>' +
		'</div>';
		var newInput = $(newIn);
		$('#buttondivincing').before(newInput);
		$("#ingredient" + addIncIngNext).attr('data-source',$(addto).attr('data-source'));
	});
	
	var addExIngNext = 4;
	$('#addExIngButton').click(function(){
		var addto = "#ingredient-form-exing";
		addExIngNext = addExIngNext + 1;
		var newIn = '<div class="form-group">' +
		'<label for="xingredient' + addExIngNext +'" class="col-sm-4 control-label">Ingredient ' + addExIngNext + '</label>' +
			'<div class="col-sm-8">' +
				'<input type="text" class="form-control" name="xingredient' + addExIngNext +'" id="xingredient' + addExIngNext + '" placeholder="ingredient ' + addExIngNext + '">' +
			'</div>' +
		'</div>';
		var newInput = $(newIn);
		$('#buttondivexing').before(newInput);
		$("#xingredient" + addExIngNext).attr('data-source',$(addto).attr('data-source'));
	});
});