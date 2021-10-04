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

  for(var i = 0;i<data.length;i++){
    labels_data.push(data[i]['organization_name'])
    datasets_data.push(data[i]['number'])
  }


var densityData = {
  label: 'Наукова співпраця',
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

function table(table_data){
   $(document).ready(function() {
    var datatable = $('#coop').DataTable( {
        data: table_data,
         order: [[1, 'desc']],
        columns: [
             { title: "#" },
            { title: "Заклади-партнери" },
            { title: "К-ть документів" },
        ],
        fnRowCallback: function (nRow, aData, iDisplayIndex) {
         var info = $(this).DataTable().page.info();
         $("td:nth-child(1)", nRow).html(info.start + iDisplayIndex + 1);
         return nRow;
        },
        columnDefs: [
      {
        targets: [0],
        searchable: false,
        bSearchable: false,
        className: 'dt-center'
      },
      {name: '#', data: 'number', targets: 0},
      {name: 'organization_name', data: 'organization_name', targets: 1},
      {name: 'number', data: 'number', targets: 2}
    ]
    } );

} );}
 $.getJSON('/api/cooperating/', function(data) {
        table(data);
        drawGraph(data);
        });






  });
