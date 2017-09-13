
$(document).ready(function () {
	$(function() {
		$('button[name=profile]').on('click', function() {
		  	$.getJSON($SCRIPT_ROOT + '/_getProperties', {
		    	g: $(this).val(),
			}, function(data) {
				$.each(data.result.properties, function( index, value ) {
		     		$('ul[name=properties]').append("<li><button class='dropdown-item' id='prop' type='button' name='property' value='" + value + "' data-toggle='button'>" + value + "</button></li>")
		     	});

		    });
		  	return false;
		});
	});

	$(function() {
		$('#properties').on('click', 'button', function() {
		  	$.getJSON($SCRIPT_ROOT + '/_getAnnotations', {
		    	p: $(this).val(),
		    	g: $('button[name=profiles]').val(),
			}, function(data) {
				$.each(data.result.triples, function( index, value ) {
		     		$('ul[name=annotations]').append("<li><input name='annotation' size='50' maxlength='100' value='" + value.annotation + "'></input><input size='50' maxlength='100' name='value' value='" + value.value + "'></input></li>")
		     	});

		    });
		  	return false;
		});
	});
});