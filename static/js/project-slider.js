// slider.js

// document.querySelectorAll('.project-x-slide').forEach(button => {
//     button.addEventListener('click', function () {
//         // console.log('test!')
//
//         const paction = this.dataset.sliderAction;
//         const psliderContainer = this.closest('.project-slider-container');
//         const pslider = psliderContainer.querySelector('.project-slider');
//         const pslides = pslider.querySelectorAll('.project-slide');
//         const ptotalSlides = pslides.length;
//
//         // Get current index from data attribute or default to 0
//         let pcurrentIndex = parseInt(pslider.dataset.currentIndex) || 0;
//
//         // Calculate new index based on action
//         if (paction === 'next') {
//             pcurrentIndex = Math.min(pcurrentIndex + 1, ptotalSlides - 1);
//         } else {
//             pcurrentIndex = Math.max(pcurrentIndex - 1, 0);
//         }
//
//         // Update slider position and store new index
//         pslider.style.transform = `translateX(-${pcurrentIndex * 100}%)`;
//         pslider.dataset.currentIndex = pcurrentIndex;
//     });
// });



// document.querySelectorAll('.project-x-slide').forEach(button => {
//     button.addEventListener('click', function () {
//         const paction = this.dataset.sliderAction;
//         const psliderContainer = this.closest('.project-slider-container');
//         const pslider = psliderContainer.querySelector('.project-slider');
//         const pslides = pslider.querySelectorAll('.project-slide');
//         const ptotalSlides = pslides.length;
//
//         let pcurrentIndex = parseInt(pslider.dataset.currentIndex) || 0;
//
//         if (paction === 'next') {
//             pcurrentIndex = (pcurrentIndex + 1) % ptotalSlides;
//         } else {
//             pcurrentIndex = (pcurrentIndex - 1 + ptotalSlides) % ptotalSlides;
//         }
//
//         // Remove active class from all slides
//         pslides.forEach(slide => slide.classList.remove('active'));
//
//         // Add active class to new current slide
//         pslides[pcurrentIndex].classList.add('active');
//
//         pslider.dataset.currentIndex = pcurrentIndex;
//     });
// });
