/* ================= INIT ================= */

document.addEventListener("DOMContentLoaded", () => {

    pageFade();
    initCounters();
    initCardHover();
    initScrollAnimation();
    initRippleEffect();

});


/* ================= PAGE LOAD FADE ================= */

function pageFade() {
    document.body.style.opacity = 0;

    setTimeout(() => {
        document.body.style.transition = "opacity 0.6s ease";
        document.body.style.opacity = 1;
    }, 100);
}


/* ================= COUNT-UP ANIMATION ================= */

function animateCounter(element, start, end, duration) {

    let startTime = null;

    function update(currentTime) {
        if (!startTime) startTime = currentTime;

        let progress = Math.min((currentTime - startTime) / duration, 1);
        let value = Math.floor(progress * (end - start) + start);

        element.innerText = "₹ " + value.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function initCounters() {
    const counters = document.querySelectorAll(".counter");

    if (!counters.length) return;

    counters.forEach(el => {
        let value = parseFloat(el.getAttribute("data-value")) || 0;
        animateCounter(el, 0, value, 1000);
    });
}


/* ================= CARD HOVER EFFECT ================= */

function initCardHover() {
    const cards = document.querySelectorAll(".card-custom");

    if (!cards.length) return;

    cards.forEach(card => {

        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.background = `
                radial-gradient(circle at ${x}px ${y}px, rgba(99,102,241,0.15), rgba(255,255,255,0.05))
            `;
        });

        card.addEventListener("mouseleave", () => {
            card.style.background = "rgba(255,255,255,0.05)";
        });

    });
}


/* ================= SCROLL ANIMATION ================= */

function initScrollAnimation() {
    const elements = document.querySelectorAll(".card-custom");

    if (!elements.length) return;

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("fade-in");
            }
        });
    }, {
        threshold: 0.2
    });

    elements.forEach(el => observer.observe(el));
}


/* ================= BUTTON RIPPLE EFFECT ================= */

function initRippleEffect() {
    const buttons = document.querySelectorAll(".btn-custom");

    if (!buttons.length) return;

    buttons.forEach(btn => {

        btn.addEventListener("click", function (e) {

            const ripple = document.createElement("span");
            ripple.classList.add("ripple");

            const rect = btn.getBoundingClientRect();

            ripple.style.left = (e.clientX - rect.left) + "px";
            ripple.style.top = (e.clientY - rect.top) + "px";

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);

        });

    });
}