function grandpyAnswer(){
    // display a loading gif
    $.post('/grandpy', {
        user_raw_text: $("#user_input").val()
    }).done(function(response){
        $("#answer ul").append('<li>Grandpy : ' + response['answer']['address'] + ' </li>');
        if(response['answer']['extract'] != ""){
            $("#answer ul").append('<li>Grandpy : ' + response['answer']['extract'] + ' </li>');
        }
    }).fail(function() {
        $("#answer ul").append('<li>Grandpybot est fatigué, il répondra à tes questions une autre fois.</li>');
    });
}