function initMap() {
    var besancon = {lat: 47.247315, lng: 5.999222};
    var map = new google.maps.Map(document.getElementById('map'), {zoom: 5.5, center: besancon});
    var marker = new google.maps.Marker({position: besancon, map: map})
}