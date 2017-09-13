
$(document).ready(function () {
	$(function() {
		$('button[name=profile]').on('click', function() {
			$('button[name=profiles]').html($(this).val());
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
			$('button[name=properties]').html($(this).val());
		  	$.getJSON($SCRIPT_ROOT + '/_getAnnotations', {
		    	p: $(this).val(),
		    	g: $('button[name=profiles]').html(),
			}, function(data) {
				$('ul[name=annotations]').html('');
				$.each(data.result.triples, function( index, value ) {
		     		$('ul[name=annotations]').append("<form><div class='input-group'><div name='annotation' class='col-lg-3'>" + value.annotation + "</div><div name='value' class='col-lg-4'>" + value.value + "</div><input type='text' id='value' name='value' class='col-lg-4' placeholder='new value' name='value'></input><button type='button' id='save' class='btn btn-primary'>Save</button></div></div></form>")
		     	});

		    });
		  	return false;
		});
	});

	$(function() {
		$('ul').on('click', 'button#save', function() {
			var g = $('button[name=profiles]').html();
			var p = $('button[name=properties]').html();
			var a = $(this).closest("form").find("div[name='annotation']").html();
			var nv = $(this).closest("form").find("input[name='value']").val();
			var ov = $(this).closest("form").find("div[name='value']").html();
			var r = confirm("Set '" + a + "' from '" + ov + "' to the value '" + nv + "' for the property '" + p + "' in the profile '" + g + "'?");
			if (r == true) {
			  	$.getJSON($SCRIPT_ROOT + '/_setAnnotations', {
		    		p: p,
		    		g: g,
		    		a: a,
		    		ov: ov,
		    		nv: nv,
				}, function() {
					$.each(data.result, function( index, value ) {
			     		$(this).closest("form").find("div[name='value']").html(value)
			     	});
			    });
		  		return false;
		  	}
		});
	});
});