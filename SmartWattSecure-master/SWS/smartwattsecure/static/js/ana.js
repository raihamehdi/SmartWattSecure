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

    // Set 'active' class for the analytics link
    clearActive();
    analyticsLink.classList.add("active");

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

    // Add active class to the Analytics button
    document.getElementById('analytics-link').classList.add('active');
};

document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/units-consumed/")
        .then((response) => response.json())
        .then((data) => {
            const labels = data.map((item) => item.date);
            const units = data.map((item) => item.units);

            const ctx = document.getElementById("unitsConsumedChart").getContext("2d");
            
            // Set the width and height directly in JavaScript to force proper sizing
            ctx.canvas.width = document.getElementById("chartContainer").offsetWidth;
            ctx.canvas.height = 300; // Force a specific height for visibility

            new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Units Consumed",
                        data: units,
                        borderColor: "#c62828",
                        backgroundColor: "rgba(198, 40, 40, 0.1)",
                        fill: true,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: { display: true, text: "Date" },
                        },
                        y: {
                            title: { display: true, text: "Units" },
                            beginAtZero: true
                        },
                    },
                },
            });
        })
        .catch((error) => console.error("Error fetching data:", error));
});


// Adjust chart container styles to fit within the panel
const chartContainer = document.getElementById('chartContainer');
chartContainer.style.height = '300px';  // Adjust height as needed
chartContainer.style.width = '100%';    // Make it take the full panel width
