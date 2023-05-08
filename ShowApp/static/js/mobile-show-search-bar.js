var searchBarInput =  document.querySelector(".search-bar-mobile");
var navLeft = document.querySelector(".nav-left");
var goodid = document.getElementById("search-bar-mobile");
var userIcon =  document.querySelector(".nav-user-icon");
var button = document.getElementById("zeub");

function searchMobile(){
    if (goodid.style.display === "block")
    {
        goodid.style.display = "none";
    }
    else
    {
        goodid.style.display = "block";
    }
    navLeft.classList.toggle("on-cherche-mobile");
    searchBarInput.classList.toggle("on-active-on-mobile"); 
    userIcon.classList.toggle("on-cherche-mobile");

}

function zeubWasClicked(){
    button.type = "submit";
}

