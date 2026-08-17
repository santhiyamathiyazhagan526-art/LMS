// ===============================
// STAFF PANEL JAVASCRIPT
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Active Sidebar Menu
    // ===============================

    const currentPage = window.location.pathname;

    const menuLinks = document.querySelectorAll(".sidebar a");

    menuLinks.forEach(link => {

        if (link.getAttribute("href") === currentPage) {

            link.parentElement.classList.add("active");

        }

    });

    // ===============================
    // Sidebar Toggle (Mobile)
    // ===============================

    const toggleButton = document.getElementById("sidebarToggle");

    const sidebar = document.querySelector(".sidebar");

    if (toggleButton && sidebar) {

        toggleButton.addEventListener("click", function () {

            sidebar.classList.toggle("show");

        });

    }

    // ===============================
    // Close Sidebar on Mobile
    // ===============================

    document.addEventListener("click", function (e) {

        if (
            window.innerWidth <= 992 &&
            sidebar &&
            !sidebar.contains(e.target) &&
            toggleButton &&
            !toggleButton.contains(e.target)
        ) {
            sidebar.classList.remove("show");
        }

    });

    // ===============================
    // Dashboard Card Animation
    // ===============================

    const cards = document.querySelectorAll(".dashboard-card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";

        card.style.transform = "translateY(25px)";

        setTimeout(() => {

            card.style.transition = "0.5s";

            card.style.opacity = "1";

            card.style.transform = "translateY(0)";

        }, index * 100);

    });

    // ===============================
    // Button Ripple Effect
    // ===============================

    document.querySelectorAll(".btn").forEach(button => {

        button.addEventListener("click", function () {

            this.classList.add("shadow");

            setTimeout(() => {

                this.classList.remove("shadow");

            }, 200);

        });

    });

});


// ===============================
// Live Clock
// ===============================

function updateClock() {

    const clock = document.getElementById("liveClock");

    if (!clock) return;

    const now = new Date();

    clock.innerHTML = now.toLocaleTimeString();

}

setInterval(updateClock, 1000);

updateClock();


// ===============================
// Greeting Message
// ===============================

function updateGreeting() {

    const greeting = document.getElementById("greeting");

    if (!greeting) return;

    const hour = new Date().getHours();

    let message = "";

    if (hour < 12) {

        message = "Good Morning";

    }

    else if (hour < 17) {

        message = "Good Afternoon";

    }

    else {

        message = "Good Evening";

    }

    greeting.innerHTML = message;

}

updateGreeting();


// ===============================
// Table Hover Effect
// ===============================

document.querySelectorAll("tbody tr").forEach(row => {

    row.addEventListener("mouseenter", function () {

        this.style.background = "#f8f9fa";

    });

    row.addEventListener("mouseleave", function () {

        this.style.background = "";

    });

});


// ===============================
// Smooth Scroll
// ===============================

document.documentElement.style.scrollBehavior = "smooth";