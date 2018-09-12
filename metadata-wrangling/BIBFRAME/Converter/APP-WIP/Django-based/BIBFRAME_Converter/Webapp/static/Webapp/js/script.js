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
                        var marc = data['latest_progress_marc'];
                        var st;
                        var tr;
                        var id;
                        var bib = data['latest_progress_bib'];
                        var bst;
                        var btr;
                        var bid;
                        for (var i = 0; i < marc.length; i++) {
                        	if (marc[i] != null) {
                        		console.log(marc[i]);
	                        	st = marc[i].stage 
	                        	id = marc[i].process_ID
	                        	overall = '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: ' + marc[i].M_to_B_percent/3 + '%" aria-valuenow="' + marc[i].M_to_B_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: ' + marc[i].name_percent/3 + '%" aria-valuenow="' + marc[i].name_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: ' + marc[i].title_percent/3 + '%" aria-valuenow="' + marc[i].title_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> </div>' 
	                            tr = "<td>" + id + "</td>" +
	                            "<td>" + marc[i].all_names + "</td>" +
	                            "<td>" + marc[i].all_titles + "</td>" + 
	                            "<td>" + marc[i].p_names + "</td>" +
	                            "<td>" + marc[i].c_names + "</td>" +
	                            "<td>" + marc[i].M_to_B_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: '+ marc[i].M_to_B_percent +'%;" aria-valuenow="'+ marc[i].M_to_B_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ marc[i].M_to_B_percent +' </div> </div>' + "</td>" +
	                            "<td>" + marc[i].name_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: '+ marc[i].name_percent +'%;" aria-valuenow="'+ marc[i].name_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ marc[i].name_percent +' </div> </div>' + "</td>" +
	                            "<td>" + marc[i].title_index + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: '+ marc[i].title_percent +'%;" aria-valuenow="'+ marc[i].title_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ marc[i].title_percent +' </div> </div>' + "</td>" 
	                             $('.progress_row'+ id).html(tr);
	                             $('.overall_progress' + id).html(overall);
	                             $('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .' + st).addClass("current");
	                             $('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .' + st).prevAll().addClass("done").removeClass("current");
	                             if (st.indexOf("The process was completed in") >= 0) {
	                             	$('.progress_stage' + id + ' .progress-container .results').html(st).addClass("completed");
	                             	$('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .Writing_to_BIBFRAME').prevAll().addClass("done").removeClass("current");
	                             	$('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .Writing_to_BIBFRAME').addClass("done").removeClass("current");
	                            };
	                        };
                         };
                        for (var i = 0; i < bib.length; i++) {
                        	if (bib[i] != null) {
	                        	bst = bib[i].stage 
	                        	bid = bib[i].process_ID
	                        	boverall = '<div class="progress"> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: ' + bib[i].name_percent/2 + '%" aria-valuenow="' + bib[i].name_percent/2 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: ' + bib[i].title_percent/2 + '%" aria-valuenow="' + bib[i].title_percent/2 + '" aria-valuemin="0" aria-valuemax="100"></div> </div>' 
	                            btr = "<td>" + bid + "</td>" +
	                            "<td>" + bib[i].all_names + "</td>" +
	                            "<td>" + bib[i].all_titles + "</td>" + 
	                            "<td>" + bib[i].p_names + "</td>" +
	                            "<td>" + bib[i].c_names + "</td>" +
	                            "<td>" + bib[i].name_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: '+ bib[i].name_percent +'%;" aria-valuenow="'+ bib[i].name_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ bib[i].name_percent +' </div> </div>' + "</td>" +
	                            "<td>" + bib[i].title_index + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: '+ bib[i].title_percent +'%;" aria-valuenow="'+ bib[i].title_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ bib[i].title_percent +' </div> </div>' + "</td>" 
	                             $('.progress_row'+ bid).html(btr);
	                             $('.overall_progress' + bid).html(boverall);
	                             $('.progress_stage' + bid + ' .progress-container .wrapper .progress-nav .' + bst).addClass("current");
	                             $('.progress_stage' + bid + ' .progress-container .wrapper .progress-nav .' + bst).prevAll().addClass("done").removeClass("current");
	                             if (bst.indexOf("The process was completed in") >= 0) {
	                             	$('.progress_stage' + bid + ' .progress-container .results').html(st).addClass("completed");
	                             	$('.progress_stage' + bid + ' .progress-container .wrapper .progress-nav .Writing_to_BIBFRAME').prevAll().addClass("done").removeClass("current");
	                             	$('.progress_stage' + bid + ' .progress-container .wrapper .progress-nav .Writing_to_BIBFRAME').addClass("done").removeClass("current");
	                            };
                        	};
	                    };
                	}
               	);
       },1000);

	$(function() {
		$('button[objid]').on('click', function() {
			var id = $(this).attr("objid");
			console.log(id);
			$('.progress_table'+id).toggle();

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
		$(':regex(class, .*progress_table.*)').hide();

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

	$('#myModal').on('shown.bs.modal', function () {
  		$('#myInput').trigger('focus')
})

	$(window).on('load',function(){
        $('#exampleModal').modal('hide');
    });

});