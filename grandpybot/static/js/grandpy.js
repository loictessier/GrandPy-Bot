
// Called to display the answer of grandpy in the page application
function grandpyAnswer(){
    var user_input = document.getElementById("user_input");
    var user_input_value = user_input.value;
    $("#chat ul").append('<li class="question"><div class="speech-bubble">' + user_input_value + '</div></li>');
    user_input.value = "";
    $("#loading").show();
    $("#chat").scrollTop($('#chat').prop("scrollHeight"));
    
    $.post('/grandpy', {
        user_raw_text: user_input_value,

    }).done(function(response){       
        $("#loading").hide();
        if(response['answer']['address'] !== ""){
            // Send address
            $("#chat ul").append('<li class="answer"><div class="speech-bubble">' + response['answer']['address'] + '</div></li>');
            if(response['answer']['location'] !== ""){
                // Initialize and display the map
                var mapId = Math.random().toString(36).substring(2, 15);
                $("#chat ul").append('<div class="answer"><div class="speech-bubble"><div id="' + mapId + '" class="map"></div></div></div>');
                initMap(
                    response['answer']['location']['lat'], 
                    response['answer']['location']['lng'],
                    mapId
                );
            }
        }
        // Send extract
        if(response['answer']['extract'] !== "" && response['answer']['extract'] !== null){
            $("#chat ul").append('<li class="answer"><div class="speech-bubble">' + response['answer']['extract'] 
                + ' [<a href='+ response['answer']['lien'] +'>En savoir plus sur Wikipedia</a>]</div></li>');
        }
        $("#chat").scrollTop($('#chat').prop("scrollHeight"));

    }).fail(function() {
        $("#chat ul").append('<li class="answer"><div class="speech-bubble">Grandpybot est fatigué, il répondra à tes questions une autre fois.</div></li>');
    });
}

// init function for the google map api
function initMap(lat, lng, mapId){
    var location = {lat: lat, lng: lng};
    var map = new google.maps.Map(
        document.getElementById(mapId), {zoom: 10, center: location});
    var marker = new google.maps.Marker({position: location, map: map});
}