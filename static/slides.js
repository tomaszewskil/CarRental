let rental_slide = 1;
let car_slide = 1;

function next_rental(n) {
    show_rental(rental_slide += n);
}

function next_car(n) {
    show_car(car_slide += n)
}

function show_rental(n) {
    let i;
    let slides = document.getElementsByClassName("rental_slides");
    if (n > slides.length) {
        rental_slide = 1
    }
    if (n < 1) {
        rental_slide = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[rental_slide - 1].style.display = "block";
}

function show_car(n) {
    let j;
    let slides = document.getElementsByClassName("car_slides");
    if (n > slides.length) {
        car_slide = 1
    }
    if (n < 1) {
        car_slide = slides.length
    }
    for (j = 0; j < slides.length; j++) {
        slides[j].style.display = "none";
    }
    slides[car_slide - 1].style.display = "block";
}
