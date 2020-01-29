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
        $(".csv_form").hide();
        $(".marc_form").hide();
        $(':regex(class, .*progress_table.*)').hide();
        $('.process_button').prop('disabled', true).addClass('disabled')

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
                //$("#marc_select").addClass("active");
                $(".marc_form").slideDown();
                $(".csv_form").slideUp();
                //$("#bib_select").removeClass("active");
            }
        });
    });

     $(function() {
        $('.csv').click(function() {
            if($('.csv').is(':checked')) {
                $(".csv_form").slideDown();
                //$("#bib_select").addClass("active");
                $(".marc_form").slideUp();
                //$("#marc_select").removeClass("active");
            }
        });

    $(function() {
        $('.singin').click(function() {
            if($('.user_login').css("display") == "none") {
                $(".user_login").css("display", "inline");
            } else {
                $(".user_login").css("display", "none"); 
                };
            });
        });
    });

    $(function() {
        $(document).click(function() {
            if($('.user_login').css("display") == "inline") {
                $(".user_login").css("display", "none"); 
            };
        }); 
    });

    //user registration password match handler
    function PassMatch() {
    var password = $("#Password").val();
    var confirmPassword = $("#Password_conf").val();
    if (password != '') {
        if (password != confirmPassword) {
            $("#passCheck").html("&#10007;").css("color", "red");
            $('#register').prop('disabled', true).addClass('disabled');
        } else {
            $("#passCheck").html('&#10004;').css("color", "green");
            $('#register').prop('disabled', false).removeClass('disabled');
        }
    }
    }

    //user registration password match listener
    $(document).ready(function() {
       $("#Password_conf").keyup(PassMatch);
    });

    //user registration username check handler
    function userCheck() {
        $('#register').prop('disabled', false).removeClass('disabled');
        $.ajax({
        url : "/checkUser/", 
        type : "POST", 
        data : { username : $('#email').val() }, 

        // handle a successful response
        success : function(json) {
            if (json == 'This email address is taken') {
                $('#user').html("&#10007; ").css("color", "red")
                $('#data_response').html(json).css("color", "black")
                $('#register').prop('disabled', true).addClass('disabled');
            } else {
                $('#user').html('&#10004;').css("color", "green");
                $('#data_response').html('')
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#user').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
       };

    //user registration username check listener
    $(document).ready(function () {
        $('#email').keyup(userCheck)
    })

    //user registration institution key check handler
    function skeyCheck() {
        $('#register').prop('disabled', false).removeClass('disabled');
        var inst = $("#inst_selector").val(); 
        if (inst != '') {
        $.ajax({
        url : "/checkskey/", 
        type : "POST", 
        data : { institution : inst, skey: $('#inst_code').val() }, 

        // handle a successful response
        success : function(json) {
            if (json != '') {
                 $('#inst_codeCheck').html(json).css("color", "green")
            } else {
                $('#register').prop('disabled', true).addClass('disabled');
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#user').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });}
       };

    //user registration institution key check listener
    $(document).ready(function () {
        $('#inst_code').keyup(skeyCheck)
    })
    

    //user registration institution key check listener
    $(document).ready(function () {
        $('#csh-search').keyup(csh_suggest)
    })

    // password change form on user profile page toggle
    $(function() {
        $('.passChange').click(function() {
            if($('.pass_change').css("display") == "none") {
                $('.passChange_col').html('&#10134');   
            } else {
                $('.passChange_col').html('&#10133');   
            }
            $(".pass_change").slideToggle();
            });
        });

    // works view toggle
    $(function() {
        $('.itemViewToggle').click(function() {
            if($('.item_view_toggle').css("display") == "none") {
                $('.passChange_col').html('&#10134');   
            } else {
                $('.passChange_col').html('&#10133');   
            }
            $(".item_view_toggle").slideToggle();
            });
        });

    // user's file on user profile page toggle
    $(function() {
        $('.user_files_t').click(function() {
            if($('.user_files').css("display") == "none") {
                $('.user_files_col').html('&#10134');   
            } else {
                $('.user_files_col').html('&#10133');   
            }
            $(".user_files").slideToggle();
            });
        });

    //file upload form toggle
    $(function() {
        $('.fileuploadform').click(function() {
            if($('.file_uplaod_form').css("display") == "none") {
                $('.fileuploadform_col').html('&#10134');   
            } else {
                $('.fileuploadform_col').html('&#10133');   
            }
            $(".file_uplaod_form").slideToggle();
            });
        });

    //file paste form toggle
    $(function() {
        $('.filepasteform').click(function() {
            if($('.file_paste_form').css("display") == "none") {
                $('.filepasteform_col').html('&#10134');   
            } else {
                $('.filepasteform_col').html('&#10133');   
            }
            $(".file_paste_form").slideToggle();
            });
        });

    //user profie edit activation
    $(function() {
        $('.profie_edit').click(function() {
            $('.last_name_edit').show()
            $('.current_profile').hide()
            $('.profie_edit').hide()
            $('.profie_edit_cancel').show()
            $('.profie_edit_save').show()
            $('.inst_edit').show()
        });
    });

    //user profie edit cancel
    $(function() {
        $('.profie_edit_cancel').click(function() {
            $('.last_name_edit').hide()
            $('.current_profile').show()
            $('.profie_edit').show()
            $('.profie_edit_cancel').hide()
            $('.profie_edit_save').hide()
            $('.inst_edit').hide()
        });
    });

    //hover on marc data count
    $(function() {
        $('.marc_data').hover(function() {
            $('.marc_rows').addClass('marc_data')},
            function() {
            $('.marc_rows').removeClass('marc_data')
        });
    });

    //hover on tabular data count
    $(function() {
        $('.csv_data').hover(function() {
            $('.csv_rows').addClass('csv_data')},
            function() {
            $('.csv_rows').removeClass('csv_data')
        });
    });

    //hover on rdf data count
    $(function() {
        $('.rdf_data').hover(function() {
            $('.rdf_rows').addClass('rdf_data')},
            function() {
            $('.rdf_rows').removeClass('rdf_data')
        });
    });

    // show more subject facets
    $(function() {
        $('.sub_facets').click(function() {
            if($('.More_sub_facet').css("display") == "none") {
                $('.sub_facets').html('Show Less');   
            } else {
                $('.sub_facets').html('Show More');   
            }
            $(".More_sub_facet").slideToggle();
            });
        });

    // show more degree facets
    $(function() {
        $('.deg_facets').click(function() {
            if($('.More_deg_facet').css("display") == "none") {
                $('.deg_facets').html('Show Less');   
            } else {
                $('.deg_facets').html('Show More');   
            }
            $(".More_deg_facet").slideToggle();
            });
        });

    // show more creator facets
    $(function() {
        $('.cre_facets').click(function() {
            if($('.More_cre_facet').css("display") == "none") {
                $('.cre_facets').html('Show Less');   
            } else {
                $('.cre_facets').html('Show More');   
            }
            $(".More_cre_facet").slideToggle();
            });
        });

    // show more language facets
    $(function() {
        $('.lang_facets').click(function() {
            if($('.More_lang_facet').css("display") == "none") {
                $('.lang_facets').html('Show Less');   
            } else {
                $('.lang_facets').html('Show More');   
            }
            $(".More_lang_facet").slideToggle();
            });
        });

    // show more institution facets
    $(function() {
        $('.lang_facets').click(function() {
            if($('.More_inst_facet').css("display") == "none") {
                $('.lang_facets').html('Show Less');   
            } else {
                $('.lang_facets').html('Show More');   
            }
            $(".More_inst_facet").slideToggle();
            });
        });


     //make sure at least one file is selected for processing
     //disable the process button if number of selected files are less than 1 or more than 4
    $(function() {
        $('.file_selector').click(function() {
            var mrc = $(".file_selector:checked").length;
            if (mrc > 0 && 2 > mrc) {
            $('.process_button').html("PROCESS (" + mrc + " Item)").prop('disabled', false).removeClass('disabled')
            } else if (mrc > 0 && 5 > mrc) {
            $('.process_button').html("PROCESS (" + mrc + " Items)").prop('disabled', false).removeClass('disabled')
            } else if (mrc > 4) {
                alert("Maximum number of processes in limited to 4.")
                $('.process_button').html("PROCESS").prop('disabled', true).addClass('disabled')
            } else if (mrc < 1 || 4 < mrc) {
                $('.process_button').html("PROCESS").prop('disabled', true).addClass('disabled')
                
            };
        });
    });

    //abstract blob handlers
   $(function() {
        $('.read_more').click(function() {
            var id = $(this).attr("objid");
            $('.abstract-'+id).css("display", "none");
            $('.abstract-full-'+id).css("display", "block");
        });
   });

   $(function() {
        $('.read_less').click(function() {
            var id = $(this).attr("objid");
            $('.abstract-'+id).css("display", "block");
            $('.abstract-full-'+id).css("display", "none");
        });
   });

});

//csh search box auto suggest
function csh_suggest() {
    $('#register').prop('disabled', false).removeClass('disabled');
    var q = $("#csh-search").val(); 
    if (q.length > 2) {
    $.ajax({
    url : "/csh_autosuggest/", 
    type : "POST", 
    data : { query : q }, 

    // handle a successful response
    success : function(json) {
        if (json != '') {
             $('#suggestions').html(json)
        }
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
        $('#user').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
});}
   };

// show the loading gif
function loading() {
    $(".overlay").css("display", "block");
}

function select_autoseggest() {
    var term = $(this).attr('val');
    console.log(term);
    $('#csh-search').html(term)
}

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

//For getting CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//When submit is clicked
// $("#pasteAreaSubmitButton").click(function(e) {
function submitForm() {

    var lac = document.getElementById("lacCheckbox").checked;

    var csrftoken = getCookie('csrftoken');
    var records = $('#records').val();

    var formData = new FormData();
    var fileInput = document.getElementById('records_upload');
    var file = fileInput.files[0];

    var file_path = document.getElementById("records_upload").value;
    if (file_path != "") {
        formData.append('records_file', file);
    } else {
        formData.append("records", records);
    }

    formData.append("csrfmiddlewaretoken", csrftoken);
    formData.append("lac", lac);
    // show the loading circle
    document.getElementById("pasteAreaSubmitButtonText").style.display = "none";
    document.getElementById("pasteAreaSubmitButtonLoading").style.display = "block";

    //Send data  
    $.ajax({
        url: "/submit/thesisSubmission/",
        type: "POST",
        processData: false,
        contentType: false,
        data: formData,
        // handle a successful response
        success: function(response) {
            // stop the loading circle
            document.getElementById("pasteAreaSubmitButtonText").style.display = "block";
            document.getElementById("pasteAreaSubmitButtonLoading").style.display = "none";

            // parse the json 
            my_response = JSON.parse(response);

            if (my_response.status == 1) {
                // recaptcha successful
                localStorage.setItem('canlink_submission', JSON.stringify(my_response));
                window.location.replace("/submit/thesisSubmission")
            } else {
                // recaptcha error - someone tampered with the recaptcha code
                console.log("recaptcha error")
            }
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            alert("SERVER ERROR"); // not related to recaptcha - just some other error
            // stop the loading circle
            document.getElementById("pasteAreaSubmitButtonText").style.display = "block";
            document.getElementById("pasteAreaSubmitButtonLoading").style.display = "none";
        }
    });
};
