var graph = new Rickshaw.Graph({
                element: document.querySelector("#wip"),
                
                renderer: 'bar', 
                series:[{ data: [{x:0,y:1},{x:1, y:4}],
                            color:'steelblue'
                        }]
            });
            graph.render();
            alert(data);

