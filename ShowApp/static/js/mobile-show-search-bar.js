/* ----| Hide this | => on-cherche-mobile ---- */
var notsend_button = document.querySelector(".send-research-button-active");
var navLeft = document.querySelector(".nav-left");
var userIcon = document.querySelector(".nav-user-icon");

/* ----| Show this | => on-active-on-mobile ---- */
var send_button = document.querySelector(".send-research-button");
var searchBarInput = document.querySelector(".search-bar-mobile");

function searchMobile(){
    /* ----|Hide| => on-cherche-mobile ---- */
    navLeft.classList.toggle("on-cherche-mobile");
    notsend_button.classList.toggle("on-cherche-mobile");

    if (userIcon != null) {
        userIcon.classList.toggle("on-cherche-mobile");
        }
    
    /* ----|Show| => on-active-on-mobile ---- */
    searchBarInput.classList.toggle("on-active-on-mobile-input");
    send_button.classList.toggle("on-active-on-mobile-button");
}