
// Get CSRF token 
getLocation()
getLocationFromInput()
function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getLocationFromInput() {
    var btn = document.getElementById('submit_btn')
    if (btn) {
        btn.addEventListener('click', function() {
            var loc_query = document.getElementById('location').value
            let url='/shownearbypetro/'
            fetch(url, {
            method:'POST',
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken':getToken('csrftoken'),
            },
            body:JSON.stringify({'loc_query':loc_query}) 
            })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                showResult(data)
            })
        }, false )
    }
}


function getLocation() {
  if (navigator.geolocation) {
    position = navigator.geolocation.getCurrentPosition(showPosition,showError);
   
} else {
    console.log("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
    var lat = position.coords.latitude; 
    var lng = position.coords.longitude;

    let url='/shownearbypetro/'
    fetch(url, {
      method:'POST',
      headers:{
          'Content-Type': 'application/json',
          'X-CSRFToken':getToken('csrftoken'),
      },
      body:JSON.stringify({'lat':lat, 'lng':lng,'loc_query':''}) 
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        showResult(data)
    })

}



function showResult(data) {

        
        var result = "";
        for (var i=0; i < data.petro.results.length; i++) {
            var name = data.petro.results[i].name
            var address = data.petro.results[i].vicinity
            li = "<li class='list-group-item list-group-flush' >" + name + " : " + address + "</li>"
            result += li
        }
        if (data.petro.status == 'OK') {
            document.getElementById('result').innerHTML = result
        } else {
            document.getElementById('result').innerHTML = data.petro.status
        }
        if (data.place.status == 'OK') {
            var current_pos = "Vị trí hiện tại của bạn : " + data.place.result.formatted_address;
            document.getElementById('current_pos').innerHTML = current_pos
        } else {
            document.getElementById('current_pos').innerHTML = data.place.status
        }   
}





function showError(error) {
    var x = document.getElementById('error_list')
    switch(error.code) {
      case error.PERMISSION_DENIED:
        x.innerHTML = "Người dùng không cho phép truy cập vào vị trí"
        break;
      case error.POSITION_UNAVAILABLE:
        x.innerHTML = "Thông tin về vị trí không sẵn có"
        break;
      case error.TIMEOUT:
        x.innerHTML = "The request to get user location timed out."
        break;
      case error.UNKNOWN_ERROR:
        x.innerHTML = "An unknown error occurred."
        break;
    }
}

