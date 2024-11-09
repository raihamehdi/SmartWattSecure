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
    const dailyBtn = document.getElementById("daily-btn");
    const weeklyBtn = document.getElementById("weekly-btn");
    const monthlyBtn = document.getElementById("monthly-btn");

    function fetchData(filter) {
        fetch(`/api/units-consumed/?filter=${filter}`)
            .then(response => response.json())
            .then(data => updateChart(data))
            .catch(error => console.error("Error fetching data:", error));
    }

    function updateChart(data) {
        const labels = data.map(item => item.date);
        const units = data.map(item => item.units);
        
        // Update chart data
        chart.data.labels = labels;
        chart.data.datasets[0].data = units;
        chart.update();
    }

    // Event listeners for buttons
    dailyBtn.addEventListener("click", () => fetchData('daily'));
    weeklyBtn.addEventListener("click", () => fetchData('weekly'));
    monthlyBtn.addEventListener("click", () => fetchData('monthly'));

    // Fetch daily data initially
    fetchData('daily');
});

fetch(`/api/units-consumed/?filter=${filter}`)
    .then(response => response.json())
    .then(data => {
        console.log("Fetched Data:", data);  // Log data to verify content
        updateChart(data);
    })
    .catch(error => console.error("Error fetching data:", error));
    
// Adjust chart container styles to fit within the panel
const chartContainer = document.getElementById('chartContainer');
chartContainer.style.height = '300px';  // Adjust height as needed
chartContainer.style.width = '100%';    // Make it take the full panel width
