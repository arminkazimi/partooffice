// slider.js

document.querySelectorAll('.xxx-slide').forEach(button => {
    button.addEventListener('click', function () {
        // console.log('test!')

        const action = this.dataset.sliderAction;
        const sliderContainer = this.closest('.slider-container');
        const slider = sliderContainer.querySelector('.slider');
        const slides = slider.querySelectorAll('.slide');
        const totalSlides = slides.length;

        // Get current index from data attribute or default to 0
        let currentIndex = parseInt(slider.dataset.currentIndex) || 0;

        // Calculate new index based on action
        if (action === 'next') {
            currentIndex = Math.min(currentIndex + 1, totalSlides - 1);
        } else {
            currentIndex = Math.max(currentIndex - 1, 0);
        }

        // Update slider position and store new index
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;
        slider.dataset.currentIndex = currentIndex;
    });
});
