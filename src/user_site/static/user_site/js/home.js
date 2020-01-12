onPageLoad('home', () => {

  function buildChart(selector, data) {

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
          type: 'bar',
          height: data.length <= 3 ? null : data.length * 100,
        },

        credits: {
          enabled: false
        },

        title: {
          text: 'Кількість зареєстрованих співробітників'
        },

        legend: {
          verticalAlign: 'top'
        },

        xAxis: {
          type: 'category',
          title: {
            text: 'Факультети',
            align: 'high'
          },
          uniqueNames: false,
          labels: {
            style: {
              fontSize: '12px'
            }
          }
        },

        yAxis: {
          visible: false
        },

        plotOptions: {
          bar: {
            groupPadding: 0.12,
            minPointLength: 3,
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

  const universityId = $('meta[data-name="university_id"]').attr('data-content');

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