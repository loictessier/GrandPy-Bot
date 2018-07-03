function grandpyAnswer(){
    // display a loading gif
    $.post('/grandpy', {
        user_raw_text: $("#user_input").val()
    }).done(function(response){
        var user_input = document.getElementById("user_input");
        $("#chat ul").append('<li class="question">' + user_input.value + ' </li>');
        user_input.value = "";

        if(response['answer']['address'] !== ""){
            // Send address
            $("#chat ul").append('<li class="answer">' + response['answer']['address'] + ' </li>');
            // Initialize and display the map
            var mapId = Math.random().toString(36).substring(2, 15);
            $("#chat ul").append('<div id="' + mapId + '" class="map answer"></div>');
            initMap(
                response['answer']['location']['lat'], 
                response['answer']['location']['lng'],
                mapId
            );
        
        }
        // Send extract
        if(response['answer']['extract'] != "" && response['answer']['extract'] != null){
            $("#chat ul").append('<li class="answer">' + response['answer']['extract'] 
                + ' [<a href='+ response['answer']['lien'] +'>En savoir plus sur Wikipedia</a>]</li>');
        }
        $("#chat").scrollTop($('#chat').prop("scrollHeight"));

    }).fail(function() {
        $("#chat ul").append('<li class="answer">Grandpybot est fatigué, il répondra à tes questions une autre fois.</li>');
    });
}

// TODO displaymap(lat, long)
function initMap(lat, lng, mapId){
    // The location of Uluru
    var location = {lat: lat, lng: lng};
    // The map, centered at Uluru
    var map = new google.maps.Map(
        document.getElementById(mapId), {zoom: 10, center: location});
    // The marker, positioned at Uluru
    var marker = new google.maps.Marker({position: location, map: map});
}