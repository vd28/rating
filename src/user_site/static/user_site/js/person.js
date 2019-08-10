onPageLoad('person', () => {

  function buildHistoryChart(selector, data, options) {

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

        series[idx].data.push({
          name: Highcharts.time.dateFormat('%e of %b', new Date(item.revision.created_at)),
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

  const personId = $('meta[name="person_id"]').attr('content');

  $.ajax({
    method: 'GET',
    url: `/api/persons/${personId}/snapshots?period=quarter`,
    contentType: 'application/json',
    dataType: 'json',
    cache: false,
    success: response => {

      const payload = response.payload;

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
        ]
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
        ]
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
        ]
      );

    }
  });

});
