
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
			$('div[name=subtitle]').empty().append("<div class='col'><h5 class='text-center'>Annotation Type</h5></div><div class='col'><h5 class='text-center'>Current Value</h5></div><div class='col'></div>")
			$('button[name=properties]').html($(this).val());
		  	$('form[name=newAnnotation]').empty().append("<div class='input-group'><input type='text' name='annotation' class='col' placeholder='new annotation type'></input><input type='text' name='value' class='col' placeholder='new annotation value'></input><div class='col'></div><button type='button' name='save' class='btn btn-primary'>Save</button></div>")
			$('ul[name=annotations]').empty();
		  	$.getJSON($SCRIPT_ROOT + '/_getAnnotations', {
		    	p: $(this).val(),
		    	g: $('button[name=profiles]').html(),
			}, function(data) {
				$.each(data.result.triples, function( index, value ) {
		     		$('ul[name=annotations]').append("<form name='"+ value.annotation.split('/')[value.annotation.split('/').length-1] +"'><div class='input-group'><div name='annotation' class='col'>" + value.annotation + "</div><div name='value' class='col'>" + value.value + "</div><input type='text' name='value' class='col' placeholder='replace with (new value)'></input><button type='button' name='save' class='btn btn-primary'>Save</button><button type='button' name='delete' class='btn btn-primary'>Delete</button></div></div></form>")
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
		    	var form = $(this).closest("form").attr('name')
			$.getJSON($SCRIPT_ROOT + '/_setAnnotations', {
		    	p: p,
		    	g: g,
		    	a: a,
		    	ov: ov,
		    	nv: nv,
			}, function(data) {
					$.each(data.result, function( index, value ) {
						$("form[name="+form+"]").find("div[name=value]").html('')
						$("form[name="+form+"]").find("div[name=value]").html(value)
						$("form[name="+form+"]").find("input[name=value]").val('')

			     	});
			    });
		  		return false;
		  	
		});
	});

	$(function() {
		$('ul').on('click', 'button[name=delete]', function() {
		    	var p = $('button[name=properties]').html();
		    	var g = $('button[name=profiles]').html();
		    	var a = $(this).closest("form").find("div[name='annotation']").html();
		    	var ov = $(this).closest("form").find("div[name='value']").html();
		    	var form = $(this).closest("form").attr('name')
			$.getJSON($SCRIPT_ROOT + '/_delAnnotations', {
		    	p: p,
		    	g: g,
		    	a: a,
		    	ov: ov,
			}, function(data) {
					$("form[name="+form+"]").remove()		     	
			    });
		  		return false;
		});
	});


	$(function() {
		$('form[name=newAnnotation').on('click', 'button[name=save]', function() {
		    	var p = $('button[name=properties]').html();
		    	var g = $('button[name=profiles]').html();
		    	var a = $(this).closest("form").find("input[name='annotation']").val();
		    	var v = $(this).closest("form").find("input[name='value']").val();
		    	$(this).closest("form").find("input[name='annotation']").val('');
		    	$(this).closest("form").find("input[name='value']").val('');
			$.getJSON($SCRIPT_ROOT + '/_newAnnotation', {
		    	p: p,
		    	g: g,
		    	a: a,
		    	nv: v,
			}, function(data) {
					$.each(data.result, function( index, value ) {
						$('ul[name=annotations]').append("<form name='"+ a.split('/')[a.split('/').length-1] +"'><div class='input-group'><div name='annotation' class='col'>" + a + "</div><div name='value' class='col'>" + value + "</div><input type='text' name='value' class='col' placeholder='replace with (new value)'></input><button type='button' name='save' class='btn btn-primary'>Save</button><button type='button' name='delete' class='btn btn-primary'>Delete</button></div></div></form>")
			     	});
			    });
		  		return false;
		  	
		});
	});

});