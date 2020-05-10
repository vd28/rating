  onPageLoad('post', () => {

function BuildNewsReport(data){
  if(data['data'].length>0){
   for (var i = 0; i < data['data'].length; i++){
      var div = document.createElement('div');
      div.setAttribute('class', 'card');
      document.getElementById("card").append(div);


      var title = document.createElement('p');
      title.setAttribute('class', 'title')
      title.innerHTML = data['data'][i]['title'];
      div.append(title);

      var content = document.createElement('p');
      content.innerHTML=data['data'][i]['content'];
      div.append(content);

      var p = document.createElement('p');
      p.setAttribute('class','img');
      var image = data['data'][i]['img'];
      if(image.length>1){
        var img = document.createElement('img');
        img.src =' http://127.0.0.1:8000/'+'img/' + data['data'][i]['img'];
        div.append(p);
        p.append(img);
      }

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
   else{
       var div = document.createElement('div');
      div.setAttribute('class', 'card');
      document.getElementById("card").append(div);
      var newsIsEmpty = document.createElement('p');
       newsIsEmpty.setAttribute('class', 'date');
       newsIsEmpty.innerHTML = 'Вибачте, на данний момент новин немає. Спробуйте перевірити цю сториінку, пізніше';
       div.append(newsIsEmpty)

   }
}
  const universityId = $('meta[data-name="university_id"]').attr('data-content');
  $.ajax({

        url :'/api/post/post/',
        contentType: 'application/json',
        dataType: 'json',
        data:{},


         success:data => {
            BuildNewsReport(data)

             }
      });
      })
