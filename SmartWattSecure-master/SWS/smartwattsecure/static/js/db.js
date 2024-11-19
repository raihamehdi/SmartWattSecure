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

// Function to fetch data from the backend
async function fetchData() {
    try {
      const response = await fetch('/api/energy_data'); // Replace with your actual API endpoint
      const data = await response.json();

      // Update text data in the boxes
      document.getElementById('unitsData').innerText = `${data.units} Units`;
      document.getElementById('currentData').innerText = `${data.current} A`;
      document.getElementById('voltageData').innerText = `${data.voltage} V`;

      // Update graph data
      updateGraph(data.voltageHistory);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  // Initialize Chart.js for the voltage graph
  const ctx = document.getElementById('voltageGraph').getContext('2d');
  const voltageChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array(10).fill(''), // Empty labels for now
      datasets: [{
        label: 'Voltage',
        data: [], // Empty data initially
        borderColor: '#FF5733',
        backgroundColor: 'rgba(255, 87, 51, 0.2)',
        fill: true,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { display: false },
        y: { beginAtZero: true }
      }
    }
  });

  // Function to update the voltage graph with new data
  function updateGraph(voltageHistory) {
    voltageChart.data.labels = voltageHistory.map(() => '');
    voltageChart.data.datasets[0].data = voltageHistory;
    voltageChart.update();
  }

  // Fetch data initially and then every 5 seconds
  fetchData();
  setInterval(fetchData, 5000);