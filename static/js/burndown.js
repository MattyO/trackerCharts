$(document).ready(function(){
    $.ajax({
        url:"/projects.json", 
        dataType:"json",
        success: function(data){
            $.each(data.ids, function(counter, project_id){
                create_burndown(project_id, "all","#project_list .id-" + project_id);
            });
        }
    });



});

function create_burndown(project_id, label, placement){

    var burndown_url = "/"+ project_id + "/burndown.json";
    var margin = {top: 20, right: 20, bottom: 30, left: 50};
    var width = $(placement).width() - margin.left - margin.right;
    var height = $(placement).width() / 2 - margin.top - margin.bottom;

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
        .y1(function(d){return y(d[label].total);})

    var svg = d3.select(placement)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top +")");
        
    d3.json(burndown_url, function(data, error){
        data = data.states

        $.each(data, function(i,state){
            data[i].all.total = +state.all.total ;
            data[i].datetime = parseDate(state.datetime);
        });

        x.domain(d3.extent(data, function(d){ return d.datetime; }));
        y.domain([0, d3.max(data, function(d){ return d[label].total; })]);

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
}
