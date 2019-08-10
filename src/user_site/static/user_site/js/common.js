function buildPaginationParams(data) {
  const params = {
    page: data.start / data.length + 1,
    limit: data.length
  };

  if (data.search.value) {
    params.t = data.search.value;
  }

  if (data.order.length > 0) {
    let ordering = '';

    data.order.forEach(item => {
      const column = data.columns[item.column];
      if (column.name) {
        ordering += item.dir === 'asc' ? column.name : '-' + column.name;
      }
    });

    if (ordering) {
      params.o = ordering;
    }
  }

  return params;
}

function onPageLoad(endpoint, callback) {
  const metaEndpoint = $('meta[name="endpoint"]').attr('content');
  if (metaEndpoint === endpoint) {
    console.debug('Execute callback for ' + endpoint);
    callback();
  }
}

$(() => {
  $('.top-nav__link.top-nav__link_state').click(function (e) {
    e.stopPropagation();
    $(this).parent('.top-nav').toggleClass('top-nav_responsive');
  });

  $('.top-nav__dropdown-toggle').click(function (e) {
    e.stopPropagation();
    $(this).next('.top-nav__dropdown-menu').toggle();
  });

  $('.top-nav__dropdown-menu').click(function (e) {
    e.stopPropagation();
  });

  $(window).click(() => {
    $('.top-nav').each(function () {
      if ($('.top-nav__link.top-nav__link_state', this).is(':hidden')) {
        $('.top-nav__dropdown-menu', this).hide();
      }
    })
  });
});

$(() => {
  $('#footer-current-year').text(new Date().getFullYear());
});
