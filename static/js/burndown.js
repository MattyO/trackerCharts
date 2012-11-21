$(document).ready(function(){
    $.ajax({
        url:"/11111/burndown.json", 
        dataType:"json",
        success: function(data){
            var lines = new Array(); 
            $.each(data.states, function(i, state){

                //alert(labels.datetime);

                $.each(state.all, function(key,d){
                    if(lines[key] == undefined){
                        lines[key] = new Array();
                    }
                    var testobj = {count:d, datetime:state.datetime}
                    console.log("test object");
                    console.log(testobj);
                    lines[key].push({count:d, datetime:state.datetime});
                });
            });

            console.log("done with main loop.  just checking values");

            console.log(lines);

            console.log(lines.started);
            for (key in lines){
                for (data_key in lines[key]){
                    console.log(lines[key][data_key].count + " " + lines[key][data_key].datetime);
                }
            }

            $.each(lines, function(i,d){
                alert(i);
            });

                /*
                $.each(d.all.keys()), function(i,d,key){
                    lines[key].append(d);
                });*/
        }
    });

});
/*
var burndown = d3.select("#burndown").append("svg");
    .attr("width": 400)
    .attr("height":400);

burndown.selectAll("path")
    .data(
*/
    

