function clearImages(){
    $.ajax({
        url:"/restart",
        type:"POST",
        contentType: "application/json"});

}



function refreshPage(){
    window.location.reload();
}


function makeRequest(){

    var artistValue = document.getElementById('artist').value;
    var songValue = document.getElementById('song').value;

    document.getElementById("artist").remove();
    document.getElementById("song").remove();
    document.getElementById("submit-button").remove();
    document.getElementById("artist-label").remove();
    document.getElementById("song-label").remove();
    document.getElementById("clear-button").remove();

  
    if ((artistValue != "" && songValue == "") || (artistValue == "" && songValue != "")){
        console.log("Please enter both an artist and a song title.");
    }
    else{
        //Send artistValue and songValue into ai_musicvids.py

        document.getElementById("generating-text").innerHTML = "Generating... this may take a few minutes.\nContinue refreshing to see generations.";
        document.getElementById("maybe-generating").innerHTML = "";


        const dict_values = {artistValue, songValue};
        const s = JSON.stringify(dict_values);
        console.log(s);
  
        $.ajax({
            url:"/backend",
            type:"POST",
            contentType: "application/json",
            data: JSON.stringify(s)});
    }
  }
  
document.addEventListener("keydown", function(event){
    if (event.key === 'Enter'){
        makeRequest();
        event.stopImmediatePropagation();
    }
  });





