// Set the navbar item to "active" upon a match to the current page's URL
document.querySelectorAll(".nav-link").forEach((link) => {
    if (link.getAttribute('href') === window.location.pathname) {
        // Remove any existing 'active' class from other links
        document.querySelectorAll(".nav-link.active").forEach((activeLink) => {
            activeLink.classList.remove("active");
        });
        // Add the 'active' class to the current link
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
    }
});