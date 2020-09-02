$("#click-here").click(function(e) {
  e.preventDefault();
  var aid = $(this).attr("href");
  $('html,body').animate({scrollTop: $(aid).offset().top},'slow');
});


function run_dashboard(){
  console.log("hi")
  google.charts.load('current', {'packages':['corechart']});
      $("body").css("background-image","none")
      $.ajax({
        type : 'POST',
        url : "/users/admin_landing_page",
        success: function(response) {
          $("#studnets").append(response['num_of_students'])
          $("#classes").append(response['num_of_classes'])
          $("#questions").append(response['num_of_questions'])
              google.charts.setOnLoadCallback(drawChart_q2n);
              google.charts.setOnLoadCallback(drawChart_score2exams);
              google.charts.setOnLoadCallback(drawChart_students_per_cls);
              function drawChart_q2n() {

                    // Create the data table.
                    var data = new google.visualization.DataTable();
                    data.addColumn('string', 'Notion');
                    data.addColumn('number', 'Number_of_Questions');
                    let rows = []
                    for (notion in response['q_by_notion']){
                      rows.push([notion,response['q_by_notion'][notion]])
                    }
                    data.addRows(rows);

                    // Set chart options
                    var options = {title:'Number of Questions by Notion',
                                   width:600,
                                   height:500,
                                   backgroundColor:"ghostwhite",
                                   is3D:true
                                  };

                    // Instantiate and draw our chart, passing in some options.
                    var chart = new google.visualization.PieChart(document.getElementById('q2n_chart_div'));
                    chart.draw(data, options);
                  }
              function drawChart_score2exams(){

                data_array = [['class',"avg_score"]]
                for (exam in response['avg_score_by_exam']){
                  data_array.push([exam,response['avg_score_by_exam'][exam]])
                }
                var data = google.visualization.arrayToDataTable(data_array)
                var options = {
                    title:"Average score by exam",
                    width: 500,
                    height: 300,
                    backgroundColor:"ghostwhite",
                    bar: {groupWidth: "95%"},
                    legend: { position: "none" },
                    is3D:true
                }
                var chart = new google.visualization.ColumnChart(document.getElementById("score2exam_chart"));
                chart.draw(data, options);
              }
              function drawChart_students_per_cls(){
                data_array=[['class','students',{ role: 'annotation' }]]

                for (cls in response['students_by_class']){

                  data_array.push([cls,response['students_by_class'][cls]["stdnt_amnt"],"max: "+response['students_by_class'][cls]["max_capacity"]])
                }
                var data = google.visualization.arrayToDataTable(data_array)
                var options = {
                  title:"Number of Students per Class",
                  width: 500,
                  height: 300,
                  vAxis:{title:"Studnets"},
                  hAxis:{title:"Class"},
                  backgroundColor:"ghostwhite",
                  is3D:true
                }
                var chart = new google.visualization.ColumnChart(document.getElementById('stdnt2class_chart'));
                chart.draw(data, options);
              }

            }
      });
    }
