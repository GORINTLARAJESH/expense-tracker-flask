/* ================= GLOBAL CHART INSTANCES ================= */

let monthlyChartInstance = null;
let categoryChartInstance = null;


/* ================= MONTHLY CHART ================= */

function renderMonthlyChart(labels = [], data = []) {

    const canvas = document.getElementById("monthlyChart");

    // ❌ Prevent crash
    if (!canvas || typeof Chart === "undefined") {
        console.warn("Chart.js not loaded or canvas missing");
        return;
    }

    // Destroy old chart
    if (monthlyChartInstance) {
        monthlyChartInstance.destroy();
    }

    // Validate data
    if (!Array.isArray(labels) || labels.length === 0) {
        console.warn("No monthly data available");
        return;
    }

    const cleanData = (data || []).map(v => Number(v) || 0);

    monthlyChartInstance = new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Monthly Expense (₹)",
                data: cleanData,
                backgroundColor: "#6366f1",
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 800
            },
            plugins: {
                legend: {
                    labels: { color: "#fff" }
                }
            },
            scales: {
                x: {
                    ticks: { color: "#fff" }
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: "#fff" }
                }
            }
        }
    });
}


/* ================= CATEGORY CHART ================= */

function renderCategoryChart(labels = [], data = []) {

    const canvas = document.getElementById("categoryChart");

    if (!canvas || typeof Chart === "undefined") {
        console.warn("Chart.js not loaded or canvas missing");
        return;
    }

    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }

    if (!Array.isArray(labels) || labels.length === 0) {
        console.warn("No category data available");
        return;
    }

    const filteredLabels = [];
    const filteredData = [];

    data.forEach((val, i) => {
        const num = Number(val);
        if (num > 0) {
            filteredLabels.push(labels[i]);
            filteredData.push(num);
        }
    });

    if (filteredLabels.length === 0) {
        console.warn("No valid category data");
        return;
    }

    categoryChartInstance = new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: filteredLabels,
            datasets: [{
                data: filteredData,
                backgroundColor: [
                    "#6366f1",
                    "#8b5cf6",
                    "#22c55e",
                    "#f59e0b",
                    "#ef4444",
                    "#06b6d4"
                ]
            }]
        },
        options: {
            responsive: true,
            cutout: "65%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#fff" }
                }
            }
        }
    });
}


/* ================= INIT ================= */

document.addEventListener("DOMContentLoaded", () => {

    // ✅ Ensure Chart.js is loaded
    if (typeof Chart === "undefined") {
        console.error("Chart.js is NOT loaded ❌");
        return;
    }

    // Small delay for template data
    setTimeout(() => {

        // MONTHLY
        if (typeof months !== "undefined" && months.length > 0) {
            renderMonthlyChart(months, monthly_data || []);
        } else {
            console.warn("No monthly data available for chart");
        }

        // CATEGORY
        if (typeof categories !== "undefined" && categories.length > 0) {
            renderCategoryChart(categories, category_data || []);
        } else {
            console.warn("No category data available for chart");
        }

    }, 100);
});