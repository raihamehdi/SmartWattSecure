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


// Fetch the latest data using AJAX
function fetchData() {
    fetch("/api/energy_data/")
            .then((response) => {
                if (!response.ok) {
                throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                if (data.length > 0) {
                const latestData = data[0]; // Get the latest entry

                document.getElementById(
                    "voltage"
                ).innerText = `${latestData.voltage}`;
                document.getElementById(
                    "current"
                ).innerText = `${latestData.current}`;
                document.getElementById(
                    "power"
                ).innerText = `${latestData.power}`;
                document.getElementById(
                    "total-units"
                ).innerText = `${latestData.total_units_consumed}`;
                document.getElementById(
                    "prediction"
                ).innerText = `${latestData.prediction}`;
                } else {
                console.log("No data available.");
                }
            })
            .catch((error) => {
                console.error(
                "There was a problem with the fetch operation:",
                error
                );
            });
        }

        setInterval(fetchData, 10000);

// Global chart variable
let unitsConsumedChart;

// Fetch and render initial data for weekly view
fetchFilteredData("weekly");

// Handle filter changes
document.getElementById("time-filter").addEventListener("change", function () {
    const filter = this.value;
    fetchFilteredData(filter); // Fetch and display data based on the selected filter
});

// Function to fetch and render data based on filter
function fetchFilteredData(filter) {
    fetch(`/api/energy_data/?filter=${filter}`)
        .then(response => response.json())
        .then(data => {
            const formattedData = formatChartData(data);
            if (unitsConsumedChart) {
                updateChart(formattedData);
            } else {
                initializeChart(formattedData);
            }
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Format data for Chart.js
function formatChartData(data) {
    const labels = data.map(entry => entry.time_period);
    const units = data.map(entry => entry.units_consumed);
    return { labels, units };
}

// Initialize chart with given data
function initializeChart(data) {
    const ctx = document.getElementById("unitsConsumedChart").getContext("2d");
    unitsConsumedChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Units Consumed (kWh)",
                data: data.units,
                backgroundColor: "rgba(221, 7, 51, 0.2)",
                borderColor: "#DD0733",
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Units Consumed (kWh)"
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Time Period"
                    }
                }
            }
        }
    });
}

// Update chart with new data
function updateChart(data) {
    unitsConsumedChart.data.labels = data.labels;
    unitsConsumedChart.data.datasets[0].data = data.units;
    unitsConsumedChart.update();
}

// Download chart as PDF
document.getElementById("download-pdf").addEventListener("click", () => {
    const canvas = document.getElementById("unitsConsumedChart");
    const pdf = new jsPDF();
    pdf.text("Units Consumed Chart", 10, 10);
    pdf.addImage(canvas.toDataURL("image/png"), "PNG", 10, 20, 180, 100);
    pdf.save("units_consumed_chart.pdf");
});
