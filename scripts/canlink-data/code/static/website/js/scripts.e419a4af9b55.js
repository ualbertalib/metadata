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
function submitForm(){

    //Prevent default submit
    // e.preventDefault();

    // show the loading bar - change color just in case it was resubmitted after error
    document.getElementById("pasteAreaSubmitButtonText").style.display = "none";
    document.getElementById("pasteAreaSubmitButtonLoading").style.display = "block";
    document.getElementById("pasteAreaSubmitButton").style.background = "#000021";
    // prepare csrf token
    var csrftoken = getCookie('csrftoken');
    // get the data
    var records = $('#records').val();

    // clear old messages if this is a resubmit
    $("#errors_body").empty();
    $("#warnings_body").empty();
    $("#theses_body").empty();
    document.getElementById("errors").style.display = "none";
    document.getElementById("warnings").style.display = "none";
    document.getElementById("theses").style.display = "none";


    //Send data  
    $.ajax({
        url: "thesisSubmission/", 
        type: "POST", // http method
        data: {
            csrfmiddlewaretoken: csrftoken,
            // recaptcha:grecaptcha.getResponse(),
            records: records
        }, 
        // handle a successful response
        success: function(response) {
            // stop the loading circle
            document.getElementById("pasteAreaSubmitButtonText").style.display = "block";
            document.getElementById("pasteAreaSubmitButtonLoading").style.display = "none";

            // parse the json 
            my_response = JSON.parse(response);
            // // TODO check the response here and do something with it
            console.log(my_response);

            localStorage.setItem('my_response', JSON.stringify(my_response));

            if (my_response.status == 1){
                window.location.replace("/thesisSubmission")
                // if (my_response.errors.length >= 1){
                //     document.getElementById("errors").style.display = "block";
                //     document.getElementById("pasteAreaSubmitButton").style.background = "#FF3838";
                //     $("#pasteAreaSubmitButtonText").html('Errors Occured');
                    
                //     for(error in my_response.errors){
                //         console.log(my_response.errors[error]);
                //         $("#errors_body").append("<div class='file_error'><div class='file_error_message'>" + my_response.errors[error] + "</div>");
                //     }

                // }
                // if (my_response.warnings.length >= 1){
                //     document.getElementById("warnings").style.display = "block";
                //     for(warning in my_response.warnings){
                //         console.log(my_response.warnings[warning]);
                //         $("#warnings_body").append("<div class='file_warning'><div class='file_warning_message'>" + my_response.warnings[warning] + "</div>");
                //     }
                // }
                // if (my_response.theses.length >= 1){
                //     document.getElementById("theses").style.display = "block";
                //     for(thesis in my_response.theses){
                //         console.log(my_response.theses[thesis]);
                //         $("#theses_body").append("<div class='file_thesis'><div class='file_thesis_message'>" + my_response.theses[thesis] + "</div>");
                //     }
                // }
            }
            else{
                // recaptcha error - someone tampered with the recaptcha code
                console.log("recaptcha error")
            }
            
            
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            alert("SERVER ERROR");    // not related to recaptcha - just some other error
            // stop the loading circle
            document.getElementById("pasteAreaSubmitButtonText").style.display = "block";
            document.getElementById("pasteAreaSubmitButtonLoading").style.display = "none";
        }
    });
};
