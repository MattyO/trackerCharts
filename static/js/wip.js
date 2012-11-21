$(document).ready(function(){
    $.ajax({
        url:"/wip.json", 
        dataType:"json",
        success: function(data){
            var max = 0;
            $.each(data, function(i, d){
                if(d.wip > max){
                    max = d.wip;
                }
            });

            var wipWidth = $("#wip").width();
            var chart = d3.select("#wip").append("svg")
                .attr("class", "chart")
                .attr("width", wipWidth )
                .attr("height", max*20);
            chart.selectAll('rect')
                    .data(data)
                .enter().append('rect')
                    .attr('x', function(d,i){return 20 * i})
                    .attr('y', function(d,i){return (max - d.wip) * 20 })
                    .attr("width", 20)
                    .attr("height", function(d){ return 20 * d.wip;});
            chart.append("line")
                .attr("y1",max*20)
                .attr("y2",max*20)
                .attr("x1", 0)
                .attr("x2", wipWidth)
                .style("stroke", "#000");

            //names on charts
            /*
            chart.selectAll(".name")
                    .data(data)
                .enter().append("text")
                    .attr("class", "name")
                    .attr("x", 2)
                    .attr("y", function(d,i){return 20 * i})
                    .attr("dy",".35em")
                    .attr("text-anchor", "start")
                    .text(function(d){ return d.name;});
            */
            /*var chart = d3.select("#wip").append("div")
                .attr("class", "chart");
            chart.selectAll("div")
                    .data(data)
                .enter()
                    .append("div")
                        .style("width", function(d){return d.wip * 100 + "px";})
                        .text(function(d){return d.name + " - " + d.wip; });
                        */
        }
    });
});
