$(document).ready(function(){

	$(function() {
		$(".file-format").hide();
		$(".bib_form").hide();
		$(".marc_form").hide();
	});

    $(function() {
		$('button[name=start]').on('click', function() {
			$(".file-format").slideDown();
			$('.welcome').slideUp()
		});
	});

	 $(function() {
		$('.marc').click(function() {
			if($('.marc').is(':checked')) {
				$("#marc_select").addClass("active");
				$(".marc_form").slideDown();
				$(".bib_form").slideUp();
				$("#bib_select").removeClass("active");
			}
		});
	});

	 $(function() {
		$('.bib').click(function() {
			if($('.bib').is(':checked')) {
				$(".bib_form").slideDown();
				$("#bib_select").addClass("active");
				$(".marc_form").slideUp();
				$("#marc_select").removeClass("active");
			}
		});
	});

	 $('#isAgeSelected').click(function() {
    $("#txtAge").toggle(this.checked);
});
});