onPageLoad('department_rating', () => {

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
      const url = params ? '/api/rating/departments/?' + params : '/api/rating/departments/';
      const revisionId = $('meta[data-name="revision_id"]').attr('data-content');
      const universityId = $('meta[data-name="university_id"]').attr('data-content');

      $.ajax({
        method: 'POST',
        url,
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({
          snapshot: settings.sTableId,
          revision_id: revisionId,
          university_id: universityId,
        }),
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
  };

  $('#scopus').DataTable(Object.assign({}, dataTableOptions, {
    order: [[1, 'desc']],
    columnDefs: [
      {
        targets: [1, 2, 3],
        searchable: false,
        className: 'dt-center'
      },
      {name: 'name', data: 'name', targets: 0},
      {name: 'h_index', data: 'h_index', targets: 1},
      {name: 'documents', data: 'documents', targets: 2},
      {name: 'citations', data: 'citations', targets: 3}
    ]
  }));

  $('#google-scholar').DataTable(Object.assign({}, dataTableOptions, {
    order: [[1, 'desc']],
    columnDefs: [
      {
        targets: [1, 2],
        searchable: false,
        className: "dt-center"
      },
      {name: 'name', data: 'name', targets: 0},
      {name: 'h_index', data: 'h_index', targets: 1},
      {name: 'citations', data: 'citations', targets: 2}
    ]
  }));

  $('#semantic-scholar').DataTable(Object.assign({}, dataTableOptions, {
    order: [[1, 'desc']],
    columnDefs: [
      {
        targets: [1, 2],
        searchable: false,
        className: "dt-center"
      },
      {name: 'name', data: 'name', targets: 0},
      {name: 'citation_velocity', data: 'citation_velocity', targets: 1},
      {name: 'influential_citation_count', data: 'influential_citation_count', targets: 2}
    ]
  }));

  $('#wos').DataTable(Object.assign({}, dataTableOptions, {
    order: [[1, 'desc']],
    columnDefs: [
      {
        targets: [1],
        searchable: false,
        className: "dt-center"
      },
      {name: 'name', data: 'name', targets: 0},
      {name: 'publications', data: 'publications', targets: 1}
    ]
  }));

});
