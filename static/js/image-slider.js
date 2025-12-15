// //current position
// let pos = 0;
// //number of slides
// let totalSlides = document.querySelectorAll('#slider-wrap ul li').length;
// //get the slide width
// let sliderWidth = document.querySelector('#production-content').offsetWidth;
//
//
// document.addEventListener('DOMContentLoaded', function () {
//
//     /*****************
//      BUILD THE SLIDER
//      *****************/
//         // set width to be 'x' times the number of slides
//     var sliderEl = document.querySelector('#slider-wrap ul#slider');
//     if (sliderEl) {
//         sliderEl.style.width = (sliderWidth * totalSlides) + 'px';
//     }
//
//     // next slide
//     var nextBtn = document.getElementById('next');
//     if (nextBtn) nextBtn.addEventListener('click', slideRight);
//
//     // previous slide
//     var prevBtn = document.getElementById('previous');
//     if (prevBtn) prevBtn.addEventListener('click', slideLeft);
//
//
//     /*************************
//      //*> OPTIONAL SETTINGS
//      ************************/
//         // automatic slider (اگر خواستی فعال کن)
//         // var autoSlider = setInterval(slideRight, 3000);
//
//         // for each slide
//     var slides = document.querySelectorAll('#slider-wrap ul li');
//     var paginationList = document.querySelector('#pagination-wrap ul');
//     slides.forEach(function (liEl) {
//         // set its color (data-color)
//         var c = liEl.getAttribute('data-color');
//         if (c !== null) liEl.style.background = c;
//
//         // create a pagination <li> and append
//         var newLi = document.createElement('li');
//         if (paginationList) paginationList.appendChild(newLi);
//     });
//
//     // counter
//     if (typeof countSlides === 'function') countSlides();
//
//     // pagination
//     if (typeof pagination === 'function') pagination();
//
//     // hide/show controls/btns when hover
//     // pause automatic slide when hover
//     var sliderWrap = document.getElementById('slider-wrap');
//     if (sliderWrap) {
//         sliderWrap.addEventListener('mouseenter', function () {
//             sliderWrap.classList.add('active');
//             if (typeof autoSlider !== 'undefined') clearInterval(autoSlider);
//         });
//         sliderWrap.addEventListener('mouseleave', function () {
//             sliderWrap.classList.remove('active');
//             if (typeof autoSlider !== 'undefined') autoSlider = setInterval(slideRight, 3000);
//         });
//     }
//
// }); // DOMContentLoaded
//
//
// /***********
//  SLIDE LEFT
//  ************/
// function slideLeft() {
//     pos--;
//     if (pos === -1) {
//         pos = totalSlides - 1;
//     }
//
//     const slider = document.querySelector('#slider-wrap ul#slider');
//     if (slider) {
//         slider.style.left = `-${sliderWidth * pos}px`;
//     }
//
//     // *> optional
//     countSlides();
//     pagination();
// }
//
//
// /************
//  SLIDE RIGHT
//  *************/
// function slideRight() {
//     pos++;
//     if (pos === totalSlides) {
//         pos = 0;
//     }
//
//     const slider = document.querySelector('#slider-wrap ul#slider');
//     if (slider) {
//         slider.style.left = `-${sliderWidth * pos}px`;
//     }
//
//     // *> optional
//     countSlides();
//     pagination();
// }
//
//
// /************************
//  //*> OPTIONAL SETTINGS
//  ************************/
// function countSlides() {
//     const counter = document.querySelector('#counter');
//     if (counter) {
//         counter.innerHTML = `${pos + 1} / ${totalSlides}`;
//     }
// }
//
//
// function pagination() {
//     const dots = document.querySelectorAll('#pagination-wrap ul li');
//     dots.forEach((dot, index) => {
//         if (index === pos) {
//             dot.classList.add('active');
//         } else {
//             dot.classList.remove('active');
//         }
//     });
// }

console.log('image-slider.js');

slides = document.querySelector('#slides');
images = document.querySelectorAll('#slides img');
prevBtn = document.querySelector('.prev');
nextBtn = document.querySelector('.next');

index = 0;

function showSlide(i) {
  console.log('showslide');
  if (i < 0) index = images.length - 1;
  else if (i >= images.length) index = 0;
  else index = i;

  slides.style.transform = `translateX(-${index * 100}%)`;
}

prevBtn.addEventListener('click', () => showSlide(index - 1));
nextBtn.addEventListener('click', () => showSlide(index + 1));
