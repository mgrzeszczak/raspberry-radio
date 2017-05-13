app = (function(){

  function init(){
    app.API_URL = 'http://127.0.0.1:5000/api';


    document.getElementById("add-form").addEventListener("submit", function(event){
        event.preventDefault()
    });


    axios.get(app.API_URL+"/status")
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }



  function play(which){
    axios.get(app.API_URL+'/play?nr='+which)
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }
  function pause(){
    axios.get(app.API_URL+'/pause')
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function prev(){
    axios.get(app.API_URL+'/prev')
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function next(){
    axios.get(app.API_URL+'/next')
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }


  function vol_up(){
    axios.get(app.API_URL+'/vol/up')
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function vol_down(){
    axios.get(app.API_URL+'/vol/down')
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function add(){
    var name = document.getElementById('name').value;
    var url = document.getElementById('url').value;
    
    if (name == '' || url == ''){
      console.log('not enough');
      return;
    }

    axios.post(app.API_URL+'/add',{
      name : name,
      url : url
    })
      .then(function (response) {
        update(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  function update(data){
      console.log(data);
      var volume_div = document.getElementById('volume-p');
      volume_div.innerHTML= 'Volume: '+data.volume+'%';
      var current_station = data.current_station;
      var is_playing = data.is_playing;
      var stations = [];
      var i= 0;
      for (i=0;i<data.stations.length;i++){
        stations.push({
          name : data.stations[i].name,
          playing : i==current_station? true : false
        });
      }
      var station_list = document.getElementById('station_list');
      var list_html = "";
      for (i=0;i<data.stations.length;i++){
        var station = stations[i];
        list_html = list_html + ("<a onclick=\"app.play(" +i+ ");\" href=\"#\" class=\"list-group-item "+ (station.playing&&is_playing? "active\">" : "\">"));
        list_html = list_html + (station.name+"</a>");
      }
      station_list.innerHTML = list_html;
  }

  return {
      init : init,
      play : play,
      pause : pause,
      vol_up : vol_up,
      vol_down : vol_down,
      prev : prev,
      next : next,
      update : update,
      add : add
  }
})()
