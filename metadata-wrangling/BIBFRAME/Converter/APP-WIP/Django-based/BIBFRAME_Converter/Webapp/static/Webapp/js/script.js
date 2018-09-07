$(document).ready(function(){

	jQuery.expr[':'].regex = function(elem, index, match) {
    var matchParams = match[3].split(','),
        validLabels = /^(data|css):/,
        attr = {
            method: matchParams[0].match(validLabels) ? 
                        matchParams[0].split(':')[0] : 'attr',
            property: matchParams.shift().replace(validLabels,'')
        },
        regexFlags = 'ig',
        regex = new RegExp(matchParams.join('').replace(/^\s+|\s+$/g,''), regexFlags);
    return regex.test(jQuery(elem)[attr.method](attr.property));
	}

	setInterval(function(){
            $.getJSON('/progress/',
                    function (data) {
                        var json = data['latest_progress_list'];
                        var st;
                        var tr;
                        var id;
                        for (var i = 0; i < json.length; i++) {
                        	st = json[i].stage 
                        	id = json[i].process_ID
                        	overall = '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: ' + json[i].M_to_B_percent/3 + '%" aria-valuenow="' + json[i].M_to_B_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: ' + json[i].name_percent/3 + '%" aria-valuenow="' + json[i].name_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: ' + json[i].title_percent/3 + '%" aria-valuenow="' + json[i].title_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> </div>' 
                            tr = "<td>" + id + "</td>" +
                            "<td>" + json[i].all_names + "</td>" +
                            "<td>" + json[i].all_titles + "</td>" + 
                            "<td>" + json[i].p_names + "</td>" +
                            "<td>" + json[i].c_names + "</td>" +
                            "<td>" + json[i].M_to_B_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: '+ json[i].M_to_B_percent +'%;" aria-valuenow="'+ json[i].M_to_B_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ json[i].M_to_B_percent +' </div> </div>' + "</td>" +
                            "<td>" + json[i].name_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: '+ json[i].name_percent +'%;" aria-valuenow="'+ json[i].name_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ json[i].name_percent +' </div> </div>' + "</td>" +
                            "<td>" + json[i].title_index + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: '+ json[i].title_percent +'%;" aria-valuenow="'+ json[i].title_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ json[i].title_percent +' </div> </div>' + "</td>" 
                             $('.progress_row'+ id).html(tr);
                             $('.progress_stage' + id).html(st);
                             $('.overall_progress' + id).html(overall);

                        }
                    });
       },1000);

	$(function() {
		$('button[objid]').on('click', function() {
			var id = $(this).attr("objid");
			$('.progress_head').toggle();
			$('.progress_stage_head').toggle();
			$('.progress_row'+id).toggle();
			$('.progress_stage'+id).toggle();
		});
	});

	$(function() {
		$('.close').on('click', function() {
			$('.alert').hide();	
		});
	});

	$(function() {
		$(".file-format").hide();
		$(".bib_form").hide();
		$(".marc_form").hide();
		$('.progress_head').hide();
		$('.progress_stage_head').hide();
		$(':regex(class, .*progress_row.*)').hide();
		$(':regex(class, .*progress_stage.*)').hide();
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