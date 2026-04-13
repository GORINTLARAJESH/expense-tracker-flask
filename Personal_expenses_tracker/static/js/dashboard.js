/* ================= INIT ================= */

document.addEventListener("DOMContentLoaded", () => {

    setActiveSidebar();
    initSearch();
    initSmoothScroll();
    initButtonLoading();
    initRefreshButton();
    loadTheme();

});


/* ================= ACTIVE SIDEBAR ================= */

function setActiveSidebar() {
    const currentPath = window.location.pathname;

    document.querySelectorAll(".menu-item").forEach(item => {
        const link = item.querySelector("a");

        if (link && link.getAttribute("href") === currentPath) {
            item.classList.add("active");
        }
    });
}


/* ================= SEARCH FILTER ================= */

function initSearch() {
    const searchInput = document.querySelector(".search-box input");

    if (!searchInput) return;

    searchInput.addEventListener("keyup", function () {
        let filter = this.value.toLowerCase();
        let rows = document.querySelectorAll("tbody tr");

        rows.forEach(row => {
            let text = row.innerText.toLowerCase();
            row.style.display = text.includes(filter) ? "" : "none";
        });
    });
}


/* ================= SAFE SMOOTH SCROLL ================= */

function initSmoothScroll() {
    document.querySelectorAll("a[href^='#']").forEach(anchor => {
        anchor.addEventListener("click", function (e) {

            const href = this.getAttribute("href");

            // ❌ Prevent crash
            if (!href || href === "#" || href.length === 1) return;

            const target = document.querySelector(href);

            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        });
    });
}


/* ================= THEME ================= */

function toggleTheme() {
    document.body.classList.toggle("light-mode");

    const theme = document.body.classList.contains("light-mode") ? "light" : "dark";

    localStorage.setItem("theme", theme);

    showToast(`🌓 ${theme.charAt(0).toUpperCase() + theme.slice(1)} mode activated`);
}

function loadTheme() {
    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light-mode");
    }
}


/* ================= TOAST ================= */

function showToast(message, type = "success") {

    const existing = document.querySelector(".custom-toast");
    if (existing) existing.remove();

    let toast = document.createElement("div");
    toast.className = `custom-toast toast-${type}`;

    const icon = type === "success" ? "✅" :
                 type === "error" ? "❌" : "ℹ️";

    toast.innerHTML = `${icon} ${message}`;

    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 100);

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}


/* ================= BUTTON LOADING ================= */

function initButtonLoading() {
    document.querySelectorAll("form").forEach(form => {

        form.addEventListener("submit", function () {

            if (!form.checkValidity()) return;

            const btn = form.querySelector("button");

            if (btn && !btn.disabled) {
                const original = btn.innerHTML;

                btn.innerHTML = "⏳ Processing...";
                btn.disabled = true;

                setTimeout(() => {
                    btn.innerHTML = original;
                    btn.disabled = false;
                }, 5000);
            }
        });
    });
}


/* ================= REFRESH CHART ================= */

function initRefreshButton() {
    const btn = document.getElementById("refreshCharts");

    if (!btn) return;

    btn.addEventListener("click", async () => {

        btn.innerHTML = "🔄 Refreshing...";
        btn.disabled = true;

        try {
            const res = await fetch("/api/chart-data");
            const data = await res.json();

            if (typeof renderMonthlyChart !== "undefined") {
                renderMonthlyChart(data.months || [], data.monthly_data || []);
            }

            if (typeof renderCategoryChart !== "undefined") {
                renderCategoryChart(data.categories || [], data.category_data || []);
            }

            showToast("Charts updated!");
        } catch (e) {
            console.error(e);
            showToast("Error updating charts", "error");
        }

        btn.innerHTML = "🔄 Refresh Charts";
        btn.disabled = false;
    });
}