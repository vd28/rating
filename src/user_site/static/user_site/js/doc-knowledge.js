onPageLoad('doc_knowledge', () => {

function drawGraph(data){
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

  var diagram= document.getElementById("diagram").getContext("2d");
  var labels_data = []
  var datasets_data = []

  for(var i = 0;i<data['data'].length;i++){
    labels_data.push(data['data'][i]['field_of_knowledge'])
    datasets_data.push(data['data'][i]['number'])
  }

  var chart = new Chart(diagram,{
       type: 'pie',
       data:
       {
         labels: labels_data,
         datasets:
             [{
             backgroundColor:colors,
             data: datasets_data,
             borderWidth:1,
             }]
       },
       options:
       {
           responsive: true,
           maintainAspectRatio:false,
           legend: {
             display: false,
             position: 'top'
           }
       }
  });
}

  $('#tabs').tabs();

  const dataTableOptions = {
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

 ajax: (data, callback, settings) => {

      const params = $.param(buildPaginationParams(data));
      const universityId = $('meta[data-name="university_id"]').attr('data-content');

      $.ajax({

        url :'/api/doc-knowledge/knowledge/',
        contentType: 'application/json',
        dataType: 'json',
        data:{},


         success:data => {
            console.log(data);
            drawGraph(data);
             callback(data);
             }



      });
    }
  };


  $('#doc').DataTable(Object.assign({}, dataTableOptions, {
    order: [[1, 'desc']],
    columnDefs: [
      {
        targets: [1],
        searchable: false,
        className: 'dt-center'
      },
      {name: 'field_of_knowledge', data: 'field_of_knowledge', targets: 0},
      {name: 'number', data: 'number', targets: 1}
    ]
  }));

  });
