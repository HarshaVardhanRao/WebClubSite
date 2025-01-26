'use strict';



/**
 * add event on element
 */

const addEventOnElem = function (elem, type, callback) {
  if (elem.length > 1) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else {
    elem.addEventListener(type, callback);
  }
}



/**
 * navbar toggle
 */

const navbar = document.querySelector("[data-navbar]");
const navTogglers = document.querySelectorAll("[data-nav-toggler]");
const navLinks = document.querySelectorAll("[data-nav-link]");
const overlay = document.querySelector("[data-overlay]");

const toggleNavbar = function () {
  navbar.classList.toggle("active");
  overlay.classList.toggle("active");
}

addEventOnElem(navTogglers, "click", toggleNavbar);

const closeNavbar = function () {
  navbar.classList.remove("active");
  overlay.classList.remove("active");
}

addEventOnElem(navLinks, "click", closeNavbar);



/**
 * header active
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 100) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
});



/**
 * scroll reveal effect
 */

const sections = document.querySelectorAll("[data-section]");

const reveal = function () {
  for (let i = 0; i < sections.length; i++) {

    if (sections[i].getBoundingClientRect().top < window.innerHeight / 16) {
      sections[i].classList.add("active");
    }

  }
}

reveal();
addEventOnElem(window, "scroll", reveal);




/*slider*/
let slideIndex = 0; // Start from the first slide
let slideTimeout;

showSlides();

// Next/previous controls
function plusSlides(n) {
  clearTimeout(slideTimeout);
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  clearTimeout(slideTimeout);
  showSlides(slideIndex = n - 1); // Subtract 1 to match array index
}

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");

  if (slideIndex >= slides.length) { slideIndex = 0 } // Reset to the first slide if it reaches the end
  if (slideIndex < 0) { slideIndex = slides.length - 1 } // Set to the last slide if it goes before the first
  
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  
  slides[slideIndex].style.display = "block";
  dots[slideIndex].className += " active";
  
  // Call showSlides again after 5 seconds
  slideTimeout = setTimeout(function() {
    showSlides(slideIndex += 1);
  }, 3000);
}

