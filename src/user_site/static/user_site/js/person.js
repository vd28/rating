onPageLoad('person', () => {

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

  const personId = $('meta[data-name="person_id"]').attr('data-content');
  const tz = $('meta[data-name="timezone"]').attr('data-content');

  $.ajax({
    method: 'GET',
    url: `/api/persons/${personId}/snapshots/`,
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
