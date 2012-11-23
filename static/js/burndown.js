$(document).ready(function(){
    /*$.ajax({
        url:"/11111/burndown.json", 
        dataType:"json",
        success: function(data){
*/

        var stateLabels = Array("","","" );
        var margin = {top: 20, right: 20, bottom: 30, left: 50};
        var width = 960 - margin.left - margin.right;
        var height = 500 - margin.top - margin.bottom;

        var parseDate = d3.time.format("%Y.%m.%d %H:%M:%S").parse

        var x = d3.time.scale()
            .range([0,width]);
        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")

        var area = d3.svg.area()
            .x(function(d){return x(d.datetime);})
            .y0(function(d){return height;})
            .y1(function(d){return y(d.all.total);})

        var svg = d3.select("body")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top +")");
            
        d3.json("/687393/burndown.json", function(data, error){
            data = data.states

            $.each(data, function(i,state){
                data[i].all.total = +state.all.total ;
                data[i].datetime = parseDate(state.datetime);
                console.log("total:" + data[i].all.total+","+data[i].datetime);
            });

            /*data.forEach(function(d){
                d.all.total = +d.all.total;
                d.datetime = parseDate(d.datetime);
            });*/

            x.domain(d3.extent(data, function(d){ return d.datetime; }));
            y.domain([0, d3.max(data, function(d){ return d.all.total; })]);

            svg.append("path")
                .datum(data)
                .attr("class", "area")
                .attr("d", area);

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0,"+height+")")
                .call(xAxis);
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

        });

});
/*
        }
    });

});
/*
var burndown = d3.select("#burndown").append("svg");
    .attr("width": 400)
    .attr("height":400);

burndown.selectAll("path")
    .data(

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


*/
