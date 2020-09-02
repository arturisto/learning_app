


function user_view_manage(clicked_id){
  if(clicked_id=="create_user_form"){
      if ($("#"+clicked_id).hasClass("show")){ //if it has class show then it was open before the click
           clear_new_user_form()
      }
      else{ //the form is now being opened
        if (check_toggle("update_user_form")){
          clear_updt_form()
          change_view("u_user_find","u_update_form")
          }
        if(check_toggle("delete_user_form")){
            clear_input("delete_user_form")
        }
      }
    }
    if (clicked_id == "update_user_form"){
      if($("#"+clicked_id).hasClass("show")){ // if it has class show it was open before the click
        clear_input("u_user_find")
        clear_updt_form()
        change_view("u_user_find","u_update_form")
      }
      else{
        if ($("#create_user_form").hasClass("show")){
            $("#create_user_form").collapse('toggle')

          }
        if (check_toggle("delete_user_form")){
              clear_input("delete_user_form")
          }
        }
    }
    if (clicked_id == "delete_user_form"){
      if($("#"+clicked_id).hasClass("show")){ // if it has class show it was open before the click
        clear_input("delete_user_form")
      }

        check_toggle("create_user_form")
        if (check_toggle("update_user_form")){
            clear_updt_form()
            change_view("u_user_find","u_update_form")
            }
        }

        if (document.getElementById("alert")){
            $("#alert").remove()
        }
}
function clear_input(id){
  $("#"+id+" input").val("")
}
function clear_new_user_form(){
  $("#id").val("")
  $("#name").val("")
  $("#email").val("")
  $("#username").val("")
  $("#password").val("")
  $("#confirm_pas").val("")
}
function clear_updt_form(){
  $('#name_update').val("");
  $('#email_update').val("");
  $('#user_update').val("");
  $('#role_update').val("");
  $('#u_user_id').val("");
}
function upd_user_search(){
  event.preventDefault();
  user_email = $("#u_update_email").val();
  $.ajax({
    type : 'POST',
    url : "/users/find_user",
    data : JSON.stringify(user_email),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) {
      change_view("u_update_form","u_user_find")
      clear_input("u_update_email")
      $('#name_update').val(response['name']);
      $('#email_update').val(response['email']);
      $('#user_update').val(response['username']);
      $('#role_update').val(response['role']);
      $('#u_user_id').val(response['user_id']);
    },
    error:function(){
      insert_error("Requested email wasn't found", "u_update_email")
    }
  });
}


function search_class(){
  check_toggle("create_class_form")
  event.preventDefault();
  class_name = $("#class_search_input").val();
  $.ajax({
    type : 'POST',
    url : "/users/find_class",
    data : JSON.stringify(class_name),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) {
      var newRow=""
      for (var user of response[class_name]){
        newRow +="<tr><td><input type='checkbox'class='form-check-input' value='"+user[0]+"' name='student_"+user[0]+"'</td>"+
           "<td>"+user[1]+"</td>"+
           "<td>"+user[2]+"</td>"
      }
       $("#studnets_in_class").append(newRow)
       $("#cls_name_hidden").val(class_name)
       change_view("class_show","class_find_form")
    }
  });
}
function show_class_view_manage(){
  if($("#update_class_form").hasClass("show")==false){
    check_toggle("create_class_form")
    $("#class_search_input").val("")
  }
  else{
    change_view("class_find_form","delete_student_form")
    $("#class_search_input").val("")
    $("#studnets_in_class").empty()
  }

}
function change_view(id_to_show,id_to_hide){
  $("#"+id_to_hide).addClass("d-none")
  $("#"+id_to_hide).removeClass("d-inline")
  $("#"+id_to_show).addClass("d-inline")
  $("#"+id_to_show).removeClass("d-none")
}

function check_toggle(id){
  if($("#"+id).hasClass("show"))
  {
    $("#"+id).collapse('toggle')
    return true
  }
  else{return false}
}

function insert_error(msg,elem_before_error){

  let html_to_add = '<div class="alert alert-danger small-alert" id ="alert" role="alert">'+msg+'</div>'
  $(html_to_add).insertAfter("#"+elem_before_error)

}
