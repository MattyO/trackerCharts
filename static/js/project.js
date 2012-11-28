/*$.each($(".burndowns"), function(){
    var this_id = $(this).attr('id');
    var project_id = this_id.substr(2);
    $.ajax({
        url: '/' + project_id + '/labels.json',
        dataType: 'json', 
        success: function(labels){
            $.each(labels, function(counter, label){
                create_burndown(project_id, label, "#"+this_id);
            });
        }
    });
}); */


//var project_id = parseInt($("#project-id").html());
var project_id = $("h1").first().attr('id')
$.each($(".burndown"), function(){
    var label = $(this).attr('id');
    create_burndown(project_id, label , "#"+label);
});
