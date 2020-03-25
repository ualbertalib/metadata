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
        url: "/submission/thesisSubmission/",
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
