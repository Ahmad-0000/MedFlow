// Handles navigation bar

const navIcon = document.querySelector(".icon");
const nav = document.querySelector("#nav");
const links = document.querySelectorAll("#nav a")


// Show or hide navigation list
navIcon.addEventListener('click', () => {
    if (nav.style.width === "") {
        nav.style.width = "50%";
        for (let i = 0; i < links.length; i++) {
            links[i].style.display = "block";
        }
    } else {
        nav.style.width = "";
        for (let i = 0; i < links.length; i++) {
            links[i].style.display = "none";
        }
    }
});