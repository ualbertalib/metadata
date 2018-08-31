$(document).ready(function(){

	$(function() {
		$(".file-format").hide();
		$(".bib_form").hide();
		$(".marc_form").hide();
	});

    $(function() {
		$('button[name=users]').on('click', function() {
			$(".file-format").toggle();
		});
	});

	 $(function() {
		$('.marc').click(function() {
			if($('.marc').is(':checked')) {
				$(".marc_form").slideDown();
				$(".bib_form").slideUp();
			}
		});
	});

	 $(function() {
		$('.bib').click(function() {
			if($('.bib').is(':checked')) {
				$(".bib_form").slideDown();
				$(".marc_form").slideUp();
			}
		});
	});

	 $('#isAgeSelected').click(function() {
    $("#txtAge").toggle(this.checked);
});
});