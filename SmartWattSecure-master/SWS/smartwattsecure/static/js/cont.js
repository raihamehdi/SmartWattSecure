document.addEventListener("DOMContentLoaded", function () {
    const currentPath = window.location.pathname;

    const dashboardLink = document.getElementById("dashboard-link");
    const analyticsLink = document.getElementById("analytics-link");
    const contactLink = document.getElementById("contact-link");

        // Set active class based on current path
        if (currentPath.includes("dashboard")) {
        dashboardLink.classList.add("active");
        } else if (currentPath.includes("analytics")) {
        analyticsLink.classList.add("active");
        } else if (currentPath.includes("contact")) {
        contactLink.classList.add("active");
        }

        // Event delegation for link clicks
        document
        .querySelector(".sidebar-nav ul")
        .addEventListener("click", function (event) {
            if (event.target.tagName === "A") {
            // Remove active class from all links
            dashboardLink.classList.remove("active");
            analyticsLink.classList.remove("active");
            contactLink.classList.remove("active");
            // Add active class to the clicked link
            event.target.classList.add("active");
            }
        });
    });


window.onload = function () {
    // Remove active class from all buttons (just in case)
    document.querySelectorAll('.sidebar-nav a').forEach(function (link) {
        link.classList.remove('active');
    });

    // Add active class to the Contact button
    document.getElementById('contact-link').classList.add('active');
};
