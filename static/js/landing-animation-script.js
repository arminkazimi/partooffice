const logoContainer = document.getElementById('logo-container');
const wipe = document.getElementsByClassName('wipe')[0];
const xcontainer = document.getElementById('xcontainer');
const ghostLogo = document.getElementById('ghost-logo');
const projectsContent = document.getElementById('projects-content');

// const ghostLogoAnimation = () => {
//
// };

const wipeHandler = () => {
    logoContainer.removeEventListener('click', wipeHandler);
    // Cover the screen from left to right
    wipe.style.width = '100vw';
    ghostLogo.style.animation = 'showGhostLogo 540ms 650ms forwards';

    // setTimeout(ghostLogoAnimation, 500)
    setTimeout(() => {
        ghostLogo.style.clipPath = 'inset(0)';
        ghostLogo.style.animation = 'hideGhostLogo 540ms 650ms forwards';

        wipe.style.left = 'auto';
        wipe.style.right = '0';
        wipe.style.width = '0px';
        // Hide container after wipe
        logoContainer.style.transition = 'opacity 0.5s';
        logoContainer.style.opacity = '0';
        setTimeout(() => {
            logoContainer.style.display = 'none';
            projectsContent.style.display = 'grid';

        }, 500);
        setTimeout(() => {
            ghostLogo.style.display = 'none';
        }, 1200);
    }, 1200);

};

logoContainer.addEventListener('click', wipeHandler);


// window.addEventListener('DOMContentLoaded', () => {
//     const rightSplit = document.querySelector('.split.right');
//     const whiteLogo = document.querySelector('.white-logo');
//     const primaryLogo = document.querySelector('.primary-logo');
//     const splashBg = document.querySelector('.splash-bg');
//     const logo = document.querySelector('.logo');
//     const halfLeftSecondSplit = document.querySelector('.half-split.left.second');
//     const halfRightSecondSplit = document.querySelector('.half-split.right.second');
//
//
//     let animationStarted = false;
//
//     // Start animation on click
//     document.querySelector('.container-fluid').addEventListener('click', () => {
//         if (animationStarted) return; // Prevent repeated clicks
//         animationStarted = true;
//             // var loadData = new CustomEvent('customEvent');
//
//
//         // step 1
//         rightSplit.classList.add('expand');
//
//         // step 2
//         setTimeout(() => {
//             whiteLogo.classList.add('fade');
//         }, 350);
//
//         // step 4
//         setTimeout(() => {
//             halfLeftSecondSplit.classList.add('expand');
//             halfRightSecondSplit.classList.add('expand');
//         }, 950);
//
//         // step 3
//         setTimeout(() => {
//             primaryLogo.classList.add('fade');
//         }, 900);
//
//         //step 5
//         setTimeout(() => {
//             rightSplit.classList.add('hidden');
//             whiteLogo.classList.add('hidden');
//             splashBg.classList.add('hidden');
//
//             halfLeftSecondSplit.classList.add('hidden');
//             halfRightSecondSplit.classList.add('hidden');
//             primaryLogo.classList.add('hidden');
//
//             // logo.dispatchEvent(loadData);
//         }, 2500);
//
//         //step 6 init data
//         // setTimeout(() => {
//         //     logo.dispatchEvent(loadData);
//         // }, 2200);
//     });
// });
//
//
//
