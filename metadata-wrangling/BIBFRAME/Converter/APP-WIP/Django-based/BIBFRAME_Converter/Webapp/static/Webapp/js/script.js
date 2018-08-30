$(document).ready(function(){

	$(function() {
		$(".file-format").hide();
	});

    $(function() {
		$('button[name=users]').on('click', function() {
			$(".file-format").toggle();
		});
	});
});