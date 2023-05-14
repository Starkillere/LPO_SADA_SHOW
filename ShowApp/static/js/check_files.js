var Poster = document.getElementById("je-post")

function IsOkToSend(){
    var TypeOfPost = document.getElementById("pet-select").value;
    if (TypeOfPost === "article"){
        var img_font = document.getElementById("image");
        if (img_font.value === ""){
            alert("Vous devez renseigner une image pour l'article !");
        }
        else{
            Poster.type = "submit";
        }
    }
    else if (TypeOfPost === "podcast"){
        var img_font = document.getElementById("image");
        var podcast = document.getElementById("podcast");
        if (img_font.value === "" || podcast === ""){
            alert("Vous devez renseigner une image et un fichier audio pour le podcast !");
        }
        else{
            Poster.type = "submit";
        }
    }
    else if (TypeOfPost === "interview"){
        var interview = document.getElementById("interview");
        if (interview.value === ""){
            alert("Vous devez renseigner une vidéo pour l'interview !");
        }
        else{
            Poster.type = "submit";
        }
    }
}