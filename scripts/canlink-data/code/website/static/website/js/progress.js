setInterval(function(){
            $.getJSON('/progress/',
                    function (data) {
                        var marc = data['latest_progress_marc'];
                        var st;
                        var tr;
                        var id;
                        var rdf = data['latest_progress_rdf'];
                        var rst;
                        var rtr;
                        var rid;
                        for (var i = 0; i < marc.length; i++) {
                            if (marc[i] != null) {
                                st = marc[i].stage 
                                id = marc[i].process_ID
                                overall = '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: ' + marc[i].M_to_B_percent/2 + '%" aria-valuenow="' + marc[i].M_to_B_percent/2 + '" aria-valuemin="0" aria-valuemax="100"></div> <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width: ' + marc[i].rdf_percent/2 + '%" aria-valuenow="' + marc[i].rdf_percent/2 + '" aria-valuemin="0" aria-valuemax="100"></div>  </div>' 
                                tr = "<td>" + id + "</td>" +
                                "<td>" + marc[i].M_to_B_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: '+ marc[i].M_to_B_percent +'%;" aria-valuenow="'+ marc[i].M_to_B_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ marc[i].M_to_B_percent +' </div> </div>' + "</td>" +
                                "<td>" + marc[i].rdf_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: '+ marc[i].rdf_percent +'%;" aria-valuenow="'+ marc[i].rdf_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ marc[i].rdf_percent +' </div> </div>' + "</td>"
                                 $('.progress_row'+ id).html(tr);
                                 $('.overall_progress' + id).html(overall);
                                 $('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .' + st).addClass("current");
                                 $('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .' + st).prevAll().addClass("done").removeClass("current");
                                 if (st.indexOf("The process was completed in") >= 0) {
                                    $('.progress_stage' + id + ' .progress-container .results').html(st).addClass("completed");
                                    $('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .Loading_RDF_statements').prevAll().addClass("done").removeClass("current");
                                    $('.progress_stage' + id + ' .progress-container .wrapper .progress-nav .Loading_RDF_statements').addClass("done").removeClass("current");
                                };
                            };
                        };
                        for (var i = 0; i < rdf.length; i++) {
                            if (rdf[i] != null) {
                                rst = rdf[i].stage 
                                rid = rdf[i].process_ID
                                roverall = '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: '+ rdf[i].rdf_percent +'%;" aria-valuenow="'+ rdf[i].rdf_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ rdf[i].rdf_percent +' </div> </div>' 
                                rtr = "<td>" + rid + "</td>" +
                                "<td>" + rdf[i].rdf_index  + '<div class="progress"> <div class="progress-bar progress-bar-striped bg-warning progress-bar-animated" role="progressbar" style="width: '+ rdf[i].rdf_percent +'%;" aria-valuenow="'+ rdf[i].rdf_percent +'" aria-valuemin="0" aria-valuemax="100"> '+ rdf[i].rdf_percent +' </div> </div>' + "</td>"
                                 $('.progress_row'+ rid).html(rtr);
                                 $('.overall_progress' + rid).html(roverall);
                                 $('.progress_stage' + rid + ' .progress-container .wrapper .progress-nav .' + rst).addClass("current");
                                 $('.progress_stage' + rid + ' .progress-container .wrapper .progress-nav .' + rst).prevAll().addClass("done").removeClass("current");
                                 if (rst.indexOf("The process was completed in") >= 0) {
                                    $('.progress_stage' + rid + ' .progress-container .results').html(rst).addClass("completed");
                                    $('.progress_stage' + rid + ' .progress-container .wrapper .progress-nav .Writing_to_File').prevAll().addClass("done").removeClass("current");
                                    $('.progress_stage' + rid + ' .progress-container .wrapper .progress-nav .Writing_to_File').addClass("done").removeClass("current");
                                };
                            };
                        };
                    }
                );
       },1000);