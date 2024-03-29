onPageLoad('department_person_rating', () => {

  $('#peron-types-select').selectmenu({
    change: (event, ui) => {
      $('meta[data-name="person_type_id"]').attr('data-content', ui.item.value);
      $('#scopus').DataTable().rows().invalidate('data').draw(false);
      $('#google-scholar').DataTable().rows().invalidate('data').draw(false);
      $('#semantic-scholar').DataTable().rows().invalidate('data').draw(false);
      $('#wos').DataTable().rows().invalidate('data').draw(false);
    }
  });

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
      const url = params ? '/api/rating/persons/?' + params : '/api/rating/persons/';
      const revisionId = $('meta[data-name="revision_id"]').attr('data-content');
      const universityId = $('meta[data-name="university_id"]').attr('data-content');
      const personTypeId = $('meta[data-name="person_type_id"]').attr('data-content');
      const departmentId = $('meta[data-name="department_id"]').attr('data-content');

      $.ajax({
        method: 'POST',
        url,
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({
          snapshot: settings.sTableId,
          revision_id: revisionId,
          //university_id: universityId,
          person_type_ids: personTypeId === '-1' ? [] : [personTypeId],
          department_id: departmentId
        }),
        success: response => {
          const payload = response.payload;
          payload.objects.forEach(person => {
            person.linkEl = `<a href="/persons/${person.id}/">${person.full_name}</a>`
          });
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
      {name: 'full_name', data: 'linkEl', targets: 0},
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
      {name: 'full_name', data: 'linkEl', targets: 0},
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
      {name: 'full_name', data: 'linkEl', targets: 0},
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
      {name: 'full_name', data: 'linkEl', targets: 0},
      {name: 'publications', data: 'publications', targets: 1}
    ]
  }));

});
