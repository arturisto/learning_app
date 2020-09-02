var exams_to_class

function change_view(id_to_show,id_to_hide){
  $("#"+id_to_hide).addClass("d-none")
  $("#"+id_to_hide).removeClass("d-inline")
  $("#"+id_to_show).addClass("d-inline")
  $("#"+id_to_show).removeClass("d-none")
}
function q_crt_btn_show(){
  if($("#create-question").hasClass("show")){ //the form was open before the click
    reset_create_q_view()
  }
  else{
    if($("#delete-question").hasClass("show")){
      $("#q_delete").val("")
      $("#form_delete_body").empty=""
      change_view("delete-q1","form_delete_body")
      $("#delete-question").collapse('hide')
    }
  }
}


function q_delete_srch(){
  event.preventDefault();
  var search_key_string =  $("#q_delete").val();
  $.ajax({
    type : 'POST',
    url : "/hub/delete_quest",
    contentType: 'application/json;charset=UTF-8',
    data : JSON.stringify(search_key_string),
    success: function(response) {
          $('#form_delete_body').empty()
          change_view("delete-selection","delete-q1")
          var newRow=""
          $.each(response,function(i,item){
            newRow +="<tr><td><input type='checkbox'class='form-check-input' value='"+item[0]+"' name='"+item[0]+"'</td>"+
               "<td>"+item[0]+"</td>"+
               "<td>"+item[1]+"</td>"+
               "<td>"+item[2]+"</td>"+
               "<td>"+item[3]+"</td>"+
               "<td>"+item[4]+"</td>"+
               "<td>"+item[5]+"</td></tr>"
          });
          $("#form_delete_body").append(newRow)
          }
  });

}

function q_delete_show(){
  if ($('#delete-question').hasClass("show")==false)
  {
      change_view('delete-q1','delete-selection')
  }
  if($("#create-question").hasClass("show")){
    $("#create-question").collapse("hide")
      }

}

function e_create_show(){
  if ($("#create-exam").hasClass("show") == false){ //the create exam form is being opened
        if(document.getElementById("q_chosing_table")){
          $("#q_chosing_table").remove()
          if ($("#delete-exam").hasClass("show")==true){
              $("#delete-exam").removeClass("show")
              $("#e_delete_show").addClass("collapsed")
          }//end of if delete-exam
          };

          if($("#delete-exam").hasClass("show")){
            change_view("delete-exam-search","delete_exam_selection")
            $("#delete-exam").collapse("hide")
            clear_e_delete()
            $("#e_delete").val("")
          }
          if($("#assign-exam").hasClass("show")){
            $("#assign-exam").collapse("hide")
            reset_cls_assign_selection()
          }
        $.ajax({
          type : 'POST',
          url : "/hub/get_questions_for_exam",
          contentType: 'application/json;charset=UTF-8',
          success: function(response) {
            //create the header of the table
            var insertedHtml = '<tr id="q_chosing_table"><td ><label for="q_chooser"> Choose questions to be added</label></td><td>\
                                <table class="table" id="q_chooser">\
                                  <thead>\
                                    <tr>\
                                      <th scope="col"></th>\
                                      <th scope="col">Title</th>\
                                      <th scope="col">Question Body</th>\
                                      <th scope="col">Type</th>\
                                      <th scope="col">Notion</th>\
                                      <th scope="col">Complexity</th>\
                                    </tr>\
                                  </thead>\
                                  <tbody>'

            //create the rows from the data recieved in the response
            $.each(response,function(i,item){
              insertedHtml +="<tr><td><input type='checkbox'class='form-check-input' value='"+item[0]+"' name='q_ID_"+item[0]+"'</td>"+
                        "<td>"+item[1]+"</td>"+
                        "<td>"+item[2]+"</td>"+
                        "<td>"+item[3]+"</td>"+
                        "<td>"+item[4]+"</td>"+
                        "<td>"+item[5]+"</td></tr>"
                                    });
            //close the table the row of the outer table
            insertedHtml+='</tbody></table></td></tr>'
            insert_after = $("#form_create_exam_body").find("tr").eq(3)
            $(insertedHtml).insertAfter($(insert_after))
          }

      });
  }

}
function e_delete_show(){

  $("#e_delete").val()
  if($("#delete-exam").hasClass("show")){
    $("#form_delete_exam_body").empty()
    change_view("delete-exam-search","delete_exam_selection")

  }
  else{

    if($("#create-exam").hasClass("show")){
      $("#create-exam").collapse("hide")
      reset_create_q_view()
    }
    if($("#assign-exam").hasClass("show")){

      $("#assign-exam").collapse("hide")
      reset_cls_assign_selection()
    }
  }
}

function e_delete_btn(){
  event.preventDefault();
  var search_key_string =  $("#e_delete").val();
  $.ajax({
    type : 'POST',
    url : "/hub/find_exams_to_delete",
    contentType: 'application/json;charset=UTF-8',
    data : JSON.stringify(search_key_string),
    success: function(response) {
          $('#form_delete_exam_body').empty()
          change_view("delete_exam_selection","delete-exam-search")
          var newRow=""
          $.each(response,function(i,item){
            newRow +="<tr><td><input type='checkbox'class='form-check-input' value='"+item[0]+"' name='"+item[0]+"'</td>"+
               "<td>"+item[0]+"</td>"+
               "<td>"+item[1]+"</td>"+
               "<td>"+item[2]+"</td>"+
               "<td>"+item[3]+"</td>"+
               "<td>"+item[4]+"</td>"+
               "<td>"+item[5]+"</td></tr>"
          });
          $("#form_delete_exam_body").append(newRow)
          }
  });

}
function clear_e_delete(){
  $("#form_delete_exam_body").empty()
}


function reset_create_q_view(){
  $("#q_crt_form").trigger("reset")
  if ($("#questions-tab").hasClass("active")){
    // hide the multiple choice wrong answers when choosing a single entry exercise
      if ($("#qtype").children("option:selected").val() =="SINGLE"){
          for (i =1;i<=3; i++)
          {
            $('#wrong_answer'+i).addClass("d-none")
            $('#wrong_answer'+i).removeClass("d-inline")
            $("label[for='wrong_answer"+i+"']").addClass("d-none")
            $("label[for='wrong_answer"+i+"']").removeClass("d-inline")
          }
      };
      // #unhide the multiple choice wrong answers when choosing the multiple choice exercises
      if ($("#qtype").children("option:selected").val() =="MULTI"){

          for (i =1;i<=3; i++)
          {
            $('#wrong_answer'+i).addClass("d-inline")
            $('#wrong_answer'+i).removeClass("d-none")
            $("label[for='wrong_answer"+i+"']").addClass("d-inline")
          }
      };

  }

}
$(document).ready(function(){
    $('#qtype').on('change',function(){
      reset_create_q_view()
    });

      $("#e_delete_show").click(function(){
        if ($("#e_delete_show").hasClass("collapsed") == true){
              $("#create-exam").removeClass("show")
        }//end of if has collapsed
      }); //end of e_delete_exam click

  }); //end of document


function reset_cls_assign_selection(){
  $("#classes > option").each(function(){
    if($(this).attr("id") != "assing_choose_select"){
      $(this).remove()
    }
  })
}
function get_exm_and_cls_to_assign(){
  event.preventDefault();
  reset_cls_assign_selection()
  if($("#create-exam").hasClass("show")){
    $("#create-exam").collapse("hide")
    reset_create_q_view()
  }
  if($("#delete-exam").hasClass("show")){
    change_view("delete-exam-search","delete_exam_selection")
    $("#delete-exam").collapse("hide")
    clear_e_delete()
    $("#e_delete").val("")
  }

  $.ajax({
    type : 'POST',
    url : "/hub/get_cls_and_exams",
    contentType: 'application/json;charset=UTF-8',
    success: function(response) {
        exams_to_class = response
        let cls_as_options=""
        for(exam in exams_to_class){
          cls_as_options+="<option value='"+exam+"' id='"+exam+"'>"+exams_to_class[exam][0]+"</option>"
        $("#classes").append(cls_as_options)
        }
      }
  });
}

function prnt_assign_exms_to_cls(){
  event.preventDefault();
  let selected_cls = $("#classes option:selected").val()
  let newRow=""
  $("#tbl_exm_to_cls").empty()
  for (exam of exams_to_class[selected_cls][1]){
    newRow +="<tr><td><input type='checkbox'class='form-check-input' value='"+exam[0]+"' name='e_"+exam[0]+"'</td>"+
       "<td>"+exam[1]+"</td>"+
       "<td>"+exam[2]+"</td>"+
       "<td>"+exam[3]+"</td></tr>"
  }
  $("#tbl_exm_to_cls").append(newRow)

}


function notion_tab(){
  event.preventDefault();
  $.ajax({
    type : 'POST',
    url : "/hub/find_notions",
    contentType: 'application/json;charset=UTF-8',
    success: function(response) {
          let reponse_data = response[0]
          let turn_index = response[1]
          $('#notions_body').empty()
          let newRow=""
          $.each(response,function(i,item){
            if(item[1]=='notion'){
              newRow +="<tr><td><input type='checkbox'class='form-check-input' value='"+item[0]+"' name='n_"+item[0]+"'</td>"+
                 "<td>"+item[1]+"</td>"+
                 "<td>"+item[2]+"</td></tr>"}
            else{
              newRow +="<tr><td><input type='checkbox'class='form-check-input' value='"+item[0]+"' name='sn_"+item[0]+"'</td>"+
                 "<td>"+item[1]+"</td>"+
                 "<td>"+item[2]+"</td></tr>"}
          });
          $("#notions_body").append(newRow)
          }
  });

}
