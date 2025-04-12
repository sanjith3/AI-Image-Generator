document.addEventListener("DOMContentLoaded", function () {
    // Select all buttons
    const buttons = document.querySelectorAll("button");

    // Add hover effect to buttons
    buttons.forEach(button => {
        button.addEventListener("mouseenter", () => {
            button.style.transform = "scale(1.05)";
        });

        button.addEventListener("mouseleave", () => {
            button.style.transform = "scale(1)";
        });
    });

    // Show an alert when the download button is clicked
    const downloadButtons = document.querySelectorAll(".download-btn");
    downloadButtons.forEach(button => {
        button.addEventListener("click", () => {
            alert("Your download is starting...");
        });
    });

    // Scroll functionality for images
    function scrollImages(direction) {
        const container = document.querySelector(".image-grid");
        if (container) {
            const scrollAmount = 300; // Adjust as needed
            container.scrollBy({ left: direction * scrollAmount, behavior: "smooth" });
        }
    }

    // Add event listeners to scroll buttons
    const leftScroll = document.querySelector(".scroll-btn.left");
    const rightScroll = document.querySelector(".scroll-btn.right");

    if (leftScroll && rightScroll) {
        leftScroll.addEventListener("click", () => scrollImages(-1));
        rightScroll.addEventListener("click", () => scrollImages(1));
    }
});

// Create floating particles for the background
document.addEventListener('DOMContentLoaded', () => {
    const background = document.createElement('div');
    background.className = 'background';
    document.body.appendChild(background);

    // Generate particles
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.top = `${Math.random() * 100}vh`;
        particle.style.left = `${Math.random() * 100}vw`;
        particle.style.animationDuration = `${Math.random() * 5 + 3}s`;
        background.appendChild(particle);
    }
});