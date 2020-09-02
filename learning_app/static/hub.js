let questions=[]  // global variable for questions from the DB - restarted upon page refresh
let current_question
let correct = "<span 'correct' style='color:green; font-weight: bold;'> Correct!</span>" //global correct
let incorrect = "<span id = 'incorrect' style='color:red; font-weight: bold;'> Incorrect!</span>" // global incorrect
let interval
const multi = "Multiple Choice Question"
const single = "Single Answer Question"

function shuffle(arr) {
        let ctr = arr.length;
        let temp;
        let index;
        // While there are elements in the array
        while (ctr > 0) {
    // Pick a random index
            index = Math.floor(Math.random() * ctr);
    // Decrease ctr by 1
            ctr--;
    // And swap the last element with it
            temp = arr[ctr];
            arr[ctr] = arr[index];
            arr[index] = temp;
        }
        return arr;
  }//end of shuffle

  function startTimer(duration, display) {

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
                    giveup(current_question["type"])
                    display.text("time's up")
                }
            }, 1000);
  }
function create_questions_list(response){
  if (timed == true){
    for (var key in response){
        if (response[key][1]>0){
          questions.push(response[key])
        }}}//end if timed true
  else{
    for (var key in response){
          questions.push(response[key])
    }}  //end ese
    questions = shuffle(questions)
    var first_q = questions.shift()
    get_question(first_q[0])
    }


$(document).ready(function(){
          var path = window.location.pathname;
          var page = path.split("/").pop();

          if (page == "free-for-all"){ // run this code onload only for free for all
              $.ajax({
                type : 'POST',
                url : "/hub/get_q_ids_free_for_all",
                data: JSON.stringify(timed),
                contentType: 'application/json;charset=UTF-8',
                success: function(response) {
                  create_questions_list(response)
                  }
              });
            }//end if free for all
            else{

            }

  }); //end of document block

  function get_next_question(){
    change_view("submit_giveup","btn_next_question")
    var next_question =questions.shift()
    get_question(next_question[0])
  }//end of get next question



  function submit_answer(qtype){
      if (qtype==multi){
              let user_answer = $("#multiple-answers input[type='radio']:checked").val()
              let checked_id = $("#multiple-answers input[type='radio']:checked").attr('id')
              if (checked_id === void(0)) {
                alert("Please choose an answer or Give Up")
                return
              }//end of if checked
              else{
                        if (user_answer == current_question['answer'] ){
                              $("label[for='"+checked_id+"']").append(correct)
                          }//end if answer correct
                        else{
                          $("label[for='"+checked_id+"']").append(incorrect)
                          giveup(qtype)
                            }  //end else incorrect
                      }
                  }// end if multi
        else{
            var user_answer = $("#answer-input").val();
            if (!user_answer){
              alert("Please enter an answer or Give Up")
              return
            } // end of if nothing was entered
            else{

                  if (user_answer == current_question['answer'] ){
                        $("#singe-answer-text").after(correct)
                      }
                  else{
                    $("#singe-answer-text").after(incorrect)
                    $("#answer-input").val(current_question['answer'])
                     }//end of else
              }//end of else
            }//end of single questions answer

    change_view("btn_next_question","submit_giveup")
    clearInterval(interval)
  }//end of submit

  function giveup(qtype){
    if (qtype==multi){
      let id = current_question['id']
      correct_id = $(":radio[value='"+current_question['answer']+"']").attr("id")
      $("label[for='"+correct_id+"']").append(correct)
    }
    else{
         $("#answer-input").val(current_question['answer']);
    }
    change_view("btn_next_question","submit_giveup")
    clearInterval(interval)
  }//end of giveup

  function change_view(id_to_show,id_to_hide){
    $("#"+id_to_hide).addClass("d-none")
    $("#"+id_to_hide).removeClass("d-inline")
    $("#"+id_to_show).addClass("d-inline")
    $("#"+id_to_show).removeClass("d-none")
  }
  function print_question(response){
        $("#notion").text(response["notion"])
        $("#subnotion").text(response["subnotion"])
        $("#qnumber").text(" Q#"+response["id"])
        $("#title").text(response["title"])
        $("#body").text(response["body"])
          current_question = response
          $("#multiple-answers input[type='radio']:checked").prop( "checked", false );
          if (response["type"] == "Multiple Choice Question"){
            change_view("multiple-answers","single-answer")
              a_list = shuffle([current_question["answer"],current_question["wrong1"],current_question["wrong2"],current_question["wrong3"]])
              for(i =0; i<=3;i++){
                $("#answer"+i).val(a_list[i])
                $("#label_answer"+i).text(a_list[i])
                $("#btn_submit").attr('onClick', 'submit_answer("'+multi+'");')
                $("#btn_giveup").attr('onClick', 'giveup("'+multi+'");')
              }//end for
            } //end if multiple choice Questions
            else{
              change_view("singe-answer","multiple-answers")
              $("#btn_submit").attr('onClick', 'submit_answer("'+single+'");')
              $("#btn_giveup").attr('onClick', 'giveup("'+single+'");')
              $("#single-answer").addClass("d-inline")
              $("#answer-input").val('')
            } //end else
            $("#correct").remove()
            $("#incorrect").remove()
            if(timed==true){
              display = $('#timer');
              display.removeClass("d-none")
              startTimer(current_question["time"]*60, display);

            }//end if tined
  } //end of print_questions

  function get_question(id){
    $.ajax({
      type : 'POST',
      url : "/hub/get_q_by_id",
      contentType: 'application/json;charset=UTF-8',
      data: JSON.stringify(id),
      success: function(response) {
          print_question(response)
      }

    });
  }
  function get_q_by_notions()
  {
    selected_notion = $("#notions option:selected").text()
    selected_subnotion = $("#subnotions option:selected").text()
    console.log(timed)
    $.ajax({
      type : 'POST',
      url : "/hub/get_q_by_notion",
      contentType: 'application/json;charset=UTF-8',
      data: JSON.stringify([selected_notion,selected_subnotion,timed]),
      success: function(response) {

              if (response=='false'){
                $("#notions-form-message").text("There is no questions for your selection")
              }
              else{
                change_view("questions-main-card","notions-form")
                create_questions_list(response)
              }
      }


    });

  }//end of function get_q_by_notions
