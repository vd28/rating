onPageLoad('cooperating', () => {
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
    labels_data.push(data['data'][i]['organization_name'])
    datasets_data.push(data['data'][i]['number'])
  }


var densityData = {
  label: 'Срівробітництво',
  data: datasets_data,
  backgroundColor: [
    'rgba(0, 99, 132, 0.6)',
    'rgba(30, 99, 132, 0.6)',
    'rgba(60, 99, 132, 0.6)',
    'rgba(90, 99, 132, 0.6)',
    'rgba(120, 99, 132, 0.6)',
    'rgba(150, 99, 132, 0.6)',
    'rgba(180, 99, 132, 0.6)',
    'rgba(210, 99, 132, 0.6)',
    'rgba(240, 99, 132, 0.6)'
  ],
  borderColor: [
    'rgba(0, 99, 132, 1)',
    'rgba(30, 99, 132, 1)',
    'rgba(60, 99, 132, 1)',
    'rgba(90, 99, 132, 1)',
    'rgba(120, 99, 132, 1)',
    'rgba(150, 99, 132, 1)',
    'rgba(180, 99, 132, 1)',
    'rgba(210, 99, 132, 1)',
    'rgba(240, 99, 132, 1)'
  ],
  borderWidth: 2,
  hoverBorderWidth: 0
};

var chartOptions = {

  scales: {
    yAxes: [{
      barPercentage: 1
    }]
  },
  elements: {
    rectangle: {
      borderSkipped: 'left',
    }
  }
};
//diagram.canvas.width = 2000;
diagram.canvas.height = (labels_data.length*100);

var barChart = new Chart(diagram, {

  type: 'horizontalBar',
  data: {
    labels: labels_data,
    datasets: [densityData],
  },
  options:{ chartOptions,  responsive: true,maintainAspectRatio: false}
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

        url :'/api/doc-knowledge/cooperating/',
        contentType: 'application/json',
        dataType: 'json',
        data:{},


         success:data => {
             callback(data);
             drawGraph(data);
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

      {name: 'organization_name', data: 'organization_name', targets: 0},
      {name: 'number', data: 'number', targets: 1}
    ]


  }));

  });
