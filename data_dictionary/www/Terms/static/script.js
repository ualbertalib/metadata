var g = ""
var p = ""
var a = ""

$(document).ready(function () {
	$(function() {
		$('button#profile').bind('click', function() {
		  	g = $(this).val();
		  	$.getJSON($SCRIPT_ROOT + '/_getP', {
		    	graph: $(this).val(),
			}, function(data) {
				$('button#property').remove()
				$.each(data.result, function( index, value ) {
		     		$('ul#properties').append("<li><button class='dropdown-item' type='button' id='property' value='" + value + "' data-toggle='button'>" + value + "</a></li>")
		     	});
		    });
		  	return false;
		});
	});

	$(function() {
		$('button#property').bind('click', function() {
			p = $(this).val()
		  	$.getJSON($SCRIPT_ROOT + '/_getA', {
		    	g: g,
		    	p: $(this).val(),
			}, function(data) {
				$('button#annotation').remove()
				$.each(data.result, function( index, value ) {
		     		$('ul#annotations').append("<li><button class='dropdown-item' type='button' id='annotation' value='" + value + "' data-toggle='button'>" + value + "</a></li>")
		     	});
		    });
		  	return false;
		});
	});
});