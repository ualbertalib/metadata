$(document).ready(function(){

	setInterval(function(){
            $.getJSON('/progress/',
                    function (data) {
                        var json = data['latest_progress_list'];
                        var tr;
                         $('.table table-hover').html("");
                        for (var i = 0; i < json.length; i++) {
                            tr = $('<tr/>');
                            tr.append("<td>" + json[i].date + "</td>");
                            tr.append("<td>" + json[i].time + "</td>");
                            tr.append("<td>" + json[i].temperature + "</td>");
                            tr.append("<td>" + json[i].humidity + "</td>");
                             $('.table table-hover').append(tr);

                        }
                    });
       },2000);

	$(function() {
		$('.close').on('click', function() {
			$('.alert').hide();	
		});
	});

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