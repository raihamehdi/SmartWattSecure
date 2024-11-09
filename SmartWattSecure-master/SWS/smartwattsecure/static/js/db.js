document.addEventListener("DOMContentLoaded", function () {
    const dashboardLink = document.getElementById("dashboard-link");
    const analyticsLink = document.getElementById("analytics-link");
    const contactLink = document.getElementById("contact-link");

    // Remove 'active' class from all links
    function clearActive() {
        dashboardLink.classList.remove("active");
        analyticsLink.classList.remove("active");
        contactLink.classList.remove("active");
    }

    // Set 'active' class for the dashboard link
    clearActive();
    dashboardLink.classList.add("active");

    // Add event listeners to ensure correct active class when clicked
    dashboardLink.addEventListener("click", function () {
        clearActive();
        dashboardLink.classList.add("active");
    });

    analyticsLink.addEventListener("click", function () {
        clearActive();
        analyticsLink.classList.add("active");
    });

    contactLink.addEventListener("click", function () {
        clearActive();
        contactLink.classList.add("active");
    });
});

window.onload = function () {
    // Remove active class from all buttons (just in case)
    document.querySelectorAll('.sidebar-nav a').forEach(function (link) {
        link.classList.remove('active');
    });

    // Add active class to the Dashboard button
    document.getElementById('dashboard-link').classList.add('active');
};
