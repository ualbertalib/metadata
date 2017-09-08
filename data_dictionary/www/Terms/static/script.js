$(document).ready(function () {
	$(function() {
		$('button#profile').bind('click', function() {
		  	$.getJSON($SCRIPT_ROOT + '/getProperties', {
		    	profile: $(this).val() ,
			}, function(data) {
				$.each(data.result, function( index, value ) {
		     		$('#result').append(value + ' ')
		     	});
		    });
		  	return false;
		});
	});
});