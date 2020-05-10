onPageLoad('person', () => {

  function  drawGraph(target,data){

    function arrayRandElement(arr) {
      var rand = Math.floor(Math.random() * arr.length);
      return arr[rand];
    }

    var graph = Viva.Graph.graph();
    var NodesData =[{"name":data.self.full_name,"id":data.self.id}];

    data.joint_authors.forEach(person => {
     NodesData.push({"name":`${person.full_name} (${person.articles_count})`,"id":person.id})
    });

    for(var i=0;i<NodesData.length;i++){
      graph.addNode(NodesData[i].id,NodesData[i].name)
    }
    var countOfNodes = 0;





    data.joint_authors.forEach(person => {
      countOfNodes++;
      graph.addLink(person.id, data.self.id ,{connectionStrength:person.articles_count>4?  (3/1.5) :(countOfNodes<5 ? (person.articles_count==1 ? person.articles_count*1.2 : person.articles_count) : person.articles_count/1.5) });
    });

    var middle =graph.getNode(data.self.id);
    middle.isPinned = true;
    if(countOfNodes > 6){
      var idealLength = 120;
    }
    else{
      var idealLength = 90;
    }



   	var layout = Viva.Graph.Layout.forceDirected(graph, {
		springLength : 100,
		springCoeff : 0.0008,
		dragCoeff : 0.02,
		gravity : -1.2,
		springTransform: function (link, spring) {
                    spring.length = idealLength * (link.data.connectionStrength);
                  }
	  });

	  var middle = graph.getNode(data.self.id);
    layout.pinNode(middle, true);
    var colors = [
                        "#1f77b4", "#aec7e8",
                        "#ff7f0e", "#ffbb78",
                        "#2ca02c", "#98df8a",
                        "#d62728", "#ff9896",
                        "#9467bd", "#c5b0d5",
                        "#8c564b", "#c49c94",
                        "#e377c2", "#f7b6d2",
                        "#7f7f7f", "#c7c7c7",
                        "#bcbd22", "#dbdb8d",
                        "#17becf", "#9edae5"
                        ];


     var highlightRelatedNodes = function(nodeId, isOn) {
                   // just enumerate all realted nodes and update link color:
                   graph.forEachLinkedNode(nodeId, function(node, link){
                       var linkUI = graphics.getLinkUI(link.id);
                       if (linkUI) {
                           // linkUI is a UI object created by graphics below
                           linkUI.attr('stroke', isOn ? 'red' : 'gray');
                       }
                   });
                };

	  document.getElementById("graph").style.width =  $(target).width();
    document.getElementById("graph").style.height = "800px";
	  var graphics = Viva.Graph.View.svgGraphics(), nodeSize = 24;

	  graphics.node(function(node){

                          var ui = Viva.Graph.svg('g'),
                          circle = Viva.Graph.svg('circle')
                          .attr('r', 7)
                          .attr('width', nodeSize)
                          .attr('height', nodeSize)
                          .attr("fill", arrayRandElement(colors)),
                          svgText = Viva.Graph.svg('text').attr('y', '-' + (nodeSize)/2 + 'px').attr('x','-' + (nodeSize*4) + 'px').text(node.data);

                         ui.append(svgText);
                         ui.append(circle);


                         $(ui).hover(function() { // mouse over
                          highlightRelatedNodes(node.id, true);
                         }, function() { // mouse out
                          highlightRelatedNodes(node.id, false);
                         });

                         $(ui).click(function() { // mouse click
                          document.location.href = "/persons/{id}/".replace('{id}',node.id)
                         });

                         return ui;
    }).placeNode(function(nodeUI, pos) { nodeUI.attr('transform','translate(' +(pos.x ) + ',' + (pos.y) +')');});







    var renderer = Viva.Graph.View.renderer(graph,{
    layout:layout,
    graphics:graphics,
    container:document.getElementById('graph')});
    renderer.run();
  }

  function buildHistoryChart(selector, data, options, timezone) {

    timezone = timezone || 'UTC';
    const series = [];

    options.forEach((value, idx, collection) => {
      series.push({
        name: value.name,
        type: value.type,
        data: [],
        yAxis: value.yAxis,
        zIndex: collection.length - idx
      });
    });

    data.forEach(item => {
      options.forEach((value, idx) => {
        const name = luxon.DateTime
          .fromISO(item.revision.created_at)
          .setLocale('uk')
          .setZone(timezone)
          .toFormat('d MMMM, yyyy HH:mm');

        series[idx].data.push({
          name,
          y: item[value.src]
        });

      });
    });

    return Highcharts.chart(
      selector,
      {
        credits: {
          enabled: false
        },

        title: {
          text: null
        },

        plotOptions: {
          series: {
            minPointLength: 3
          },
          column: {
            maxPointWidth: 40
          }
        },

        lang: {
          noData: "No data to display"
        },

        noData: {
          style: {
            fontWeight: 'bold',
            fontSize: '15px',
            color: '#303030'
          }
        },

        xAxis: {
          type: 'category',
          title: {
            text: null
          },
          tickWidth: 0,
          uniqueNames: false,
          labels: {
            rotation: -45,
            style: {
              fontSize: '12px'
            }
          }
        },

        yAxis: [
          {
            title: {
              text: null
            },
            gridLineWidth: 1,
            gridLineDashStyle: 'dash',
            allowDecimals: false,
            min: 0,
            softMax: 20
          },
          {
            title: {
              text: null
            },
            opposite: true,
            gridLineWidth: 1,
            gridLineDashStyle: 'dash',
            allowDecimals: false,
            min: 0,
            softMax: 5
          }
        ],

        series
      }
    )
  }

  function findMaxId(payload,repos){
        var id =[]

        for(var i = 0; i<payload[repos].length;i++){
            id.push(payload[repos][i]['revision']['id'])
        }
        var min = id[0];
        var max = min;
        for (i = 1; i < id.length; ++i) {
            if (id[i] > max) max = id[i];
            if (id[i] < min) min = id[i];
        }
        return max


        };
   function SetTimeAverageCitSum(payload){
       var timezone = 'UTC';
       var max = findMaxId(payload,'scopus');
       var scopus_citations = 0;
       for(var i = 0; i<payload['scopus'].length;i++){
            if(payload['scopus'][i]['revision']['id'] == max){
                document.getElementById('data_time').innerHTML=luxon.DateTime
          .fromISO(payload['scopus'][i]['revision']['created_at'])
          .setLocale('uk')
          .setZone(timezone)
          .toFormat('d MMMM, yyyy HH:mm');
                document.getElementById('average_citations').innerHTML=payload['scopus'][i]['citations']/payload['scopus'][i]['documents'];
                scopus_citations = payload['scopus'][i]['citations'];
            }

        }
          max = findMaxId(payload,'google-scholar');
         for(var i = 0; i<payload['google-scholar'].length;i++){

             if(payload['google-scholar'][i]['revision']['id'] == max){
                document.getElementById('sum_citations').innerHTML=(payload['google-scholar'][i]['citations'] + scopus_citations);

            }
            }

   };

   function SetAllIndicators(payload){
          var max = findMaxId(payload,'scopus');
          for(var i = 0; i<payload['scopus'].length;i++){
            if(payload['scopus'][i]['revision']['id'] == max){
                document.getElementById('scopus_h_index').innerHTML=payload['scopus'][i]['h_index'];
                document.getElementById('scopus_citations').innerHTML=payload['scopus'][i]['citations'];
                document.getElementById('scopus_documents').innerHTML=payload['scopus'][i]['documents'];

            }
        }
            var max = findMaxId(payload,'google-scholar');
          for(var i = 0; i<payload['google-scholar'].length;i++){
            if(payload['google-scholar'][i]['revision']['id'] == max){
                document.getElementById('google_h_index').innerHTML=payload['google-scholar'][i]['h_index'];
                document.getElementById('google_citations').innerHTML=payload['google-scholar'][i]['citations'];
            }
        }

        var max = findMaxId(payload,'wos');
          for(var i = 0; i<payload['wos'].length;i++){
            if(payload['wos'][i]['revision']['id'] == max){
                document.getElementById('wos_publications').innerHTML=payload['wos'][i]['publications'];

            }
        }
         var max = findMaxId(payload,'semantic-scholar');
          for(var i = 0; i<payload['semantic-scholar'].length;i++){
            if(payload['semantic-scholar'][i]['revision']['id'] == max){
                document.getElementById('semantic_citation_velocity').innerHTML=payload['semantic-scholar'][i]['citation_velocity'];
                document.getElementById('semantic_influential_citation_count').innerHTML=payload['semantic-scholar'][i]['influential_citation_count'];
            }

        }


   }



  const personId = $('meta[data-name="person_id"]').attr('data-content');
  const tz = $('meta[data-name="timezone"]').attr('data-content');

  $.ajax({
    method: 'GET',
    url: `/api/persons/${personId}/joint-authors/`,
    contentType: 'application/json',
    dataType: 'json',
    cache: false,
    success: response => {
          drawGraph('#graph', response.payload);
    }
  });

  $.ajax({
    method: 'GET',
    url: `/api/persons/${personId}/snapshots/`,
    contentType: 'application/json',
    dataType: 'json',
    cache: false,
    success: response => {

      const payload = response.payload;


      SetTimeAverageCitSum(payload);
      SetAllIndicators(payload)



      buildHistoryChart(
        'scopus', payload['scopus'],
        [
          {
            src: 'h_index',
            name: 'h-index',
            type: payload['scopus'].length > 1 ? 'line' : 'column',
            yAxis: 1
          },
          {src: 'citations', name: 'Citations', type: 'column', yAxis: 0},
          {src: 'documents', name: 'Documents', type: 'column', yAxis: 0},
        ],
        tz
      );

      buildHistoryChart(
        'google-scholar', payload['google-scholar'],
        [
          {
            src: 'h_index',
            name: 'h-index',
            type: payload['google-scholar'].length > 1 ? 'line' : 'column',
            yAxis: 1
          },
          {src: 'citations', name: 'Citations', type: 'column', yAxis: 0}
        ],
        tz
      );

      buildHistoryChart(
        'wos', payload['wos'],
        [
          {src: 'publications', name: 'Publications', type: 'column', yAxis: 0}
        ]
      );

      buildHistoryChart(
        'semantic-scholar', payload['semantic-scholar'],
        [
          {src: 'citation_velocity', name: 'Citation Velocity', type: 'column', yAxis: 0},
          {src: 'influential_citation_count', name: 'Influential Citation Count', type: 'column', yAxis: 0}
        ],
        tz
      );

    }
  });

  $('#articles').DataTable({
    order: [[0, 'asc']],
    columnDefs: [
      {
        targets: [1, 2, 3, 4],
        searchable: false,
        orderable: false,
        className: 'dt-center',
        width: '13%'
      },
      {
        targets: [0],
        width: '48%'
      },
      {name: 'title', data: 'title', targets: 0},
      {name: 'scopus', data: 'scopus', targets: 1},
      {name: 'google_scholar', data: 'google_scholar', targets: 2},
      {name: 'wos', data: 'wos', targets: 3},
      {name: 'semantic_scholar', data: 'semantic_scholar', targets: 4}
    ],
    dom: 'lfr<"data-table-wrap"t>ip',
    pageMenu: [10, 25, 50, 100],
    pageLength: 25,
    language: {
      paginate: {
        next: '&#8594;',
        previous: '&#8592;'
      }
    },
    processing: true,
    serverSide: true,
    createdRow: (row, data, index) => {
      const plusHtml = `<span style="color: green">+</span>`;
      const minusHtml = `<span style="color: red">-</span>`;

      $('td', row).eq(1).html(data.scopus ? plusHtml : minusHtml);
      $('td', row).eq(2).html(data.google_scholar ? plusHtml : minusHtml);
      $('td', row).eq(3).html(data.wos ? plusHtml : minusHtml);
      $('td', row).eq(4).html(data.semantic_scholar ? plusHtml : minusHtml);
    },
    ajax: (data, callback, settings) => {

      const personId = $('meta[data-name="person_id"]').attr('data-content');

      $.ajax({
        method: 'GET',
        url: `/api/persons/${personId}/articles/`,
        contentType: 'application/json',
        dataType: 'json',
        cache: false,
        data: buildPaginationParams(data),
        success: response => {
          const payload = response.payload;
          callback({
            draw: data.draw,
            recordsTotal: payload.total,
            recordsFiltered: payload.total,
            data: payload.objects
          });
        },
        error: () => {
          callback({
            draw: data.draw,
            recordsTotal: 0,
            recordsFiltered: 0,
            data: []
          })
        }
      });
    }
  });
});
