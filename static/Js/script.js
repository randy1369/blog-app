

const themeToggle = document.getElementById("theme-toggle");
const whiteThemeStylesheet = document.getElementById("white-theme-stylesheet");
const blackThemeStylesheet = document.getElementById("black-theme-stylesheet");
const offcanvasRight = document.getElementById("offcanvasRight");
const offcanvasLeft = document.getElementById("offcanvasLeft");


// Check if there is a saved theme preference in localStorage
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
    if (savedTheme === "style-black.css") {
        // If the black theme is saved, enable it
        enableBlackTheme();
    }
}

// Function to enable the black theme
function enableBlackTheme() {
    whiteThemeStylesheet.setAttribute("disabled", "true");
    blackThemeStylesheet.removeAttribute("disabled");
    document.getElementById("offcanvasRight").classList.add("black-theme");
    if (offcanvasLeft) {
        offcanvasLeft.classList.add("black-theme");
    }
    localStorage.setItem("theme", "style-black.css");
}

// Function to enable the white theme
function enableWhiteTheme() {
    blackThemeStylesheet.setAttribute("disabled", "true");
    whiteThemeStylesheet.removeAttribute("disabled");
    document.getElementById("offcanvasRight").classList.remove("black-theme");
    if (offcanvasLeft) {
        offcanvasLeft.classList.remove("black-theme");
    }
    localStorage.setItem("theme", "style-white.css");
}

// Toggle theme when the button is clicked
themeToggle.addEventListener("click", () => {
    if (whiteThemeStylesheet.getAttribute("disabled") === null) {
        // If the white theme is enabled, switch to the black theme
        console.log("Switching to black theme");
        enableBlackTheme();
    } else {
        // If the black theme is enabled, switch to the white theme
        console.log("Switching to white theme");
        enableWhiteTheme();
    }
});



