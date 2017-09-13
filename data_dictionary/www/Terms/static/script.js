
$(document).ready(function () {
	$(function() {
		$('button[name=profile]').on('click', function() {
			$('button[name=profiles]').html($(this).val());
		  	$.getJSON($SCRIPT_ROOT + '/_getProperties', {
		    	g: $(this).val(),
			}, function(data) {
				$('ul[name=properties]').empty();
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
				$('ul[name=annotations]').empty();
				$.each(data.result.triples, function( index, value ) {
		     		$('ul[name=annotations]').append("<form><div class='input-group'><div name='annotation' class='col-lg-3'>" + value.annotation + "</div><div name='value' class='col-lg-4'>" + value.value + "</div><input type='text' name='value' class='col-lg-4' placeholder='new value'></input><button type='button' name='save' class='btn btn-primary'>Save</button></div></div></form>")
		     	});

		    });
		  	return false;
		});
	});

	$(function() {
		$('ul').on('click', 'button[name=save]', function() {
		    	var p = $('button[name=properties]').html();
		    	var g = $('button[name=profiles]').html();
		    	var a = $(this).closest("form").find("div[name='annotation']").html();
		    	var ov = $(this).closest("form").find("div[name='value']").html();
		    	var nv = $(this).closest("form").find("input[name='value']").val();
		    	var form = $(this).closest("form").attr('lpformnum')
			$.getJSON($SCRIPT_ROOT + '/_setAnnotations', {
		    	p: p,
		    	g: g,
		    	a: a,
		    	ov: ov,
		    	nv: nv,
			}, function(data) {
					$.each(data.result, function( index, value ) {
						$("form[lpformnum="+form+"]").find("div[name=value]").html('')
						$("form[lpformnum="+form+"]").find("div[name=value]").html(value)
						$("form[lpformnum="+form+"]").find("input[name=value]").val('')

			     	});
			    });
		  		return false;
		  	
		});
	});

});