$(document).ready(function(){

	setInterval(function(){
            $.getJSON('/progress/',
                    function (data) {
                        var json = data['latest_progress_list'];
                        var st;
                        var tr;
                        for (var i = 0; i < json.length; i++) {
                        	st = json[i].stage 
                        	overall = '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: ' + json[i].M_to_B_percent/3 + '%" aria-valuenow="' + json[i].M_to_B_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: ' + json[i].name_percent/3 + '%" aria-valuenow="' + json[i].name_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: ' + json[i].title_percent/3 + '%" aria-valuenow="' + json[i].title_percent/3 + '" aria-valuemin="0" aria-valuemax="100"></div> </div>' 
                            tr = "<td>" + json[i].process_ID + "</td>" +
                            "<td>" + json[i].all_names + "</td>" +
                            "<td>" + json[i].all_titles + "</td>" + 
                            "<td>" + json[i].p_names + "</td>" +
                            "<td>" + json[i].c_names + "</td>" +
                            "<td>" + json[i].M_to_B_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: '+ json[i].M_to_B_percent +'%;" aria-valuenow="'+ json[i].M_to_B_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ json[i].M_to_B_percent +' </div> </div>' + "</td>" +
                            "<td>" + json[i].name_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: '+ json[i].name_percent +'%;" aria-valuenow="'+ json[i].name_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ json[i].name_percent +' </div> </div>' + "</td>" +
                            "<td>" + json[i].title_index + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width: '+ json[i].title_percent +'%;" aria-valuenow="'+ json[i].title_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ json[i].title_percent +' </div> </div>' + "</td>" 
                             $('.progress_row').html(tr);
                             $('.progress_stage').html(st);
                             $('.overall_progress').html(overall);

                        }
                    });
       },1000);

	function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Full name:</td>'+
            '<td>'+d.name+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extension number:</td>'+
            '<td>'+d.extn+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extra info:</td>'+
            '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
    '</table>';
	};


	$(document).ready(function() {
    var table = $('.table table-her').DataTable( {
        "ajax": "../ajax/data/objects.txt",
        "columns": [
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { "data": "name" },
            { "data": "position" },
            { "data": "office" },
            { "data": "salary" }
        ],
        "order": [[1, 'asc']]
    } );
     
    // Add event listener for opening and closing details
    $('.le-hover').on('click', ']', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
	} );

	$(function() {
		$('button[name=view_progress]').on('click', function() {
			$('.progress_head').toggle();
			$('.progress_row').toggle();
			$('.progress_stage').toggle();
			$('.progress_stage_head').toggle();
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
		$('.progress_row').hide();
		$('.progress_stage').hide();
		$('.progress_stage_head').hide();
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