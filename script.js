let slides = document.querySelectorAll(".slide");
let currentIndex = 0;

function changeSlide() {
    slides[currentIndex].classList.remove("active");
    currentIndex = (currentIndex + 1) % slides.length;
    slides[currentIndex].classList.add("active");
}

setInterval(changeSlide, 3000); // Change image every 3 seconds
