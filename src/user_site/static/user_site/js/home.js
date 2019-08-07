onPageLoad('/', () => {

  function buildChart(selector, data, src) {

    const scopusData = [];
    const googleScholarData = [];
    const orcidData = [];
    const semanticScholarData = [];
    const wosData = [];

    data.forEach(faculty => {

      orcidData.push({
        name: faculty.name,
        y: faculty.orcid
      });

      scopusData.push({
        name: faculty.name,
        y: faculty.scopus
      });

      googleScholarData.push({
        name: faculty.name,
        y: faculty.google_scholar
      });

      semanticScholarData.push({
        name: faculty.name,
        y: faculty.semantic_scholar
      });

      wosData.push({
        name: faculty.name,
        y: faculty.wos
      });

    });

    return Highcharts.chart(
      selector,
      {
        chart: {
          type: 'bar'
        },

        credits: {
          enabled: false
        },

        title: {
          text: null
        },

        xAxis: {
          type: 'category',
          title: {
            text: null
          },
          uniqueNames: false,
          tickWidth: 0,
          labels: {
            style: {
              fontSize: '12px'
            }
          }
        },

        yAxis: {
          title: {
            text: 'Кількість зареєстрованих співробітників'
          },
          gridLineWidth: 0,
          allowDecimals: false,
          min: 0,
          softMax: 2
        },

        plotOptions: {
          column: {
            maxPointWidth: 60,
            minPointLength: 5
          }
        },

        series: [
          {
            name: 'ORCID',
            data: orcidData
          },
          {
            name: 'Scopus',
            data: scopusData
          },
          {
            name: 'Google Scholar',
            data: googleScholarData
          },
          {
            name: 'Semantic Scholar',
            data: semanticScholarData
          },
          {
            name: 'Web of Science',
            data: wosData
          }
        ]
      }
    );

  }

  const universityId = $('meta[name="university_id"]').attr('content');

  $.ajax({
    method: 'GET',
    url: `/api/universities/${universityId}/faculties/stats/`,
    contentType: 'application/json',
    dataType: 'json',
    cache: false,
    success: response => {

      buildChart('chart', response.payload);

    }
  });

});
