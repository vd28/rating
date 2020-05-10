onPageLoad('claster_analysis', () => {

function BuildAnalysisReport(data){
  for (var i = 0; i < data['data'].length; i++){
      var div = document.createElement('div');
      div.setAttribute('class', 'card');
      document.getElementById("card").append(div);

      var img = document.createElement('img');
      img.src =' http://127.0.0.1:8000/'+'img/' + data['data'][i]['img'];
      div.append(img);



      var humanCount = document.createElement('p');
      humanCount.innerHTML = "Загальна кількість людей, зареєстрованих в наукометричній базі Scopus : " + data['data'][i]['registered_in_scopus'];
      div.append(humanCount);

      var h_index_max = document.createElement('p');
      h_index_max.innerHTML="Максимальне значення індексу Хірша : " + data['data'][i]['h_index_max'];
      div.append(h_index_max);

      var h_index_min = document.createElement('p');
      h_index_min.innerHTML="Мінімальне значення індексу Хірша : " + data['data'][i]['h_index_min'];
      div.append(h_index_min);

      var h_index_average = document.createElement('p');
      h_index_average.innerHTML="Середнє значення індексу Хірша : " + data['data'][i]['h_index_average'];
      div.append(h_index_average);

      var dispersion = document.createElement('p');
      dispersion.innerHTML="Дисперсія : " + data['data'][i]['dispersion'];
      div.append(dispersion);

       var deviation = document.createElement('p');
       deviation.innerHTML="Стандартне відхилення  : " + data['data'][i]['deviation'];
       div.append(deviation);

       var dendrogram = document.createElement('p');
       dendrogram.innerHTML=data['data'][i]['dendrogram'];
       div.append(dendrogram);

       var histogram = document.createElement('p');
       histogram.innerHTML=data['data'][i]['histogram'];
       div.append(histogram);


       var timezone = 'UTC';
       var date = document.createElement('div');
       date.setAttribute('class', 'date');
       date.innerHTML = 'Дата : '+luxon.DateTime
          .fromISO(data['data'][i]['date'])
          .setLocale('uk')
          .setZone(timezone)
          .toFormat('d MMMM, yyyy HH:mm');
       div.append(date);


  }
}

  $.ajax({
    method: 'GET',
    url: '/api/rating/claster_analysis/',
    contentType: 'application/json',
    dataType: 'json',
    cache: false,
    success: response => {
      BuildAnalysisReport(response)


    }
  });

});
