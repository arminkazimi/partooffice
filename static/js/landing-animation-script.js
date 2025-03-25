window.addEventListener('DOMContentLoaded', () => {
    const rightSplit = document.querySelector('.split.right');
    const whiteLogo = document.querySelector('.white-logo');
    const primaryLogo = document.querySelector('.primary-logo');
    const splashBg = document.querySelector('.splash-bg');
    const logo = document.querySelector('.logo');
    const halfLeftSecondSplit = document.querySelector('.half-split.left.second');
    const halfRightSecondSplit = document.querySelector('.half-split.right.second');


    let animationStarted = false;

    // Start animation on click
    document.querySelector('.container-fluid').addEventListener('click', () => {
        if (animationStarted) return; // Prevent repeated clicks
        animationStarted = true;
            // var loadData = new CustomEvent('customEvent');


        // step 1
        rightSplit.classList.add('expand');

        // step 2
        setTimeout(() => {
            whiteLogo.classList.add('fade');
        }, 350);

        // step 4
        setTimeout(() => {
            halfLeftSecondSplit.classList.add('expand');
            halfRightSecondSplit.classList.add('expand');
        }, 950);

        // step 3
        setTimeout(() => {
            primaryLogo.classList.add('fade');
        }, 900);

        //step 5
        setTimeout(() => {
            rightSplit.classList.add('hidden');
            whiteLogo.classList.add('hidden');
            splashBg.classList.add('hidden');

            halfLeftSecondSplit.classList.add('hidden');
            halfRightSecondSplit.classList.add('hidden');
            primaryLogo.classList.add('hidden');

            // logo.dispatchEvent(loadData);
        }, 2500);

        //step 6 init data
        // setTimeout(() => {
        //     logo.dispatchEvent(loadData);
        // }, 2200);
    });
});



