let answer_sheet = []
let exam_time
let exam_id
function exam_load(){

  exam_id = $("input[name='exam_radio']:checked").val();

  $.ajax({
    type : 'POST',
    url : "/hub/get_exam",
    contentType: 'application/json;charset=UTF-8',
    data : JSON.stringify(exam_id),
    success: function(response) {
      change_view("exam_setup","choose_exam")
      $("#exam_text_header").text("Exam "+response['name']+" is "+response['time']+"  minutes long")
      $("#exam_begin_btn").attr("onclick","begin_exam("+response['id']+")")
      exam_time = response['time']
      console.log("exam_time:"+ exam_time)

    }
  });

}

function begin_exam(exam_id){
  $.ajax({
    type : 'POST',
    url : "/hub/get_questions_by_exam",
    data: JSON.stringify(exam_id),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) {
      change_view("main-questions","exam_setup")
      create_questions_list(response)
      display = $('#timer');
      display.removeClass("d-none")
      startExamTimer(exam_time*60 ,display)
      }
  });

}

function get_next_exam_question(){
  if ($("#single-answer").hasClass("d-inline")){
    qtype= single
  }
  else{
    qtype = multi
  }
  if (qtype==multi){
          let user_answer = $("#multiple-answers input[type='radio']:checked").val()
          let checked_id = $("#multiple-answers input[type='radio']:checked").attr('id')
          if (checked_id === void(0)) {
            alert("Please choose an answer")
            return
          }//end of if checked
          else{
            answer_sheet.push({"q_id":current_question.id,
                                "answer":user_answer})
        }// end if multi
      }
    else{
        var user_answer = $("#answer-input").val();
        if (!user_answer){
          alert("Please enter an answer")
          return
        } // end of if nothing was entered
        else{
          answer_sheet.push({"q_id":current_question.id,
                              "answer":user_answer})
          }//end of else
        }//end of single questions answer


  var next_question =questions.shift()
  if( typeof next_question === "undefined"){ //there is no next question, the exam is over

      end_of_exam_sequence()
  }
  else{
    get_question(next_question[0])
  }
}

function startExamTimer(duration, display) {

          let timer = duration, minutes, seconds;
              interval = setInterval(function () {
              minutes = parseInt(timer / 60, 10);
              seconds = parseInt(timer % 60, 10);

              minutes = minutes < 10 ? "0" + minutes : minutes;
              seconds = seconds < 10 ? "0" + seconds : seconds;

              display.text( minutes + ":" + seconds)
              if(minutes==0 && seconds<20){
                $("#timer").css("color","red")
              }
              else{
                $("#timer").css("color","")
              }
              if (--timer < 0) {
                  clearInterval(interval)
                  display.text("time's up")
                  end_of_exam_sequence()
              }
          }, 1000);
}

function end_of_exam_sequence(){
  $("#btn_next_question").html("Submit Exam")
  $("#btn_next_question").attr("onclick", "submit_exam()")

}

function submit_exam(){
  clearInterval(interval)
  $("#examsubmitted").css("top","200px")

  let data = {"exam_id":exam_id,
              "answers":answer_sheet}
  $.ajax({
    type : 'POST',
    url : "/hub/submit_exam",
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    success: function(response) {
          }
  });

}
