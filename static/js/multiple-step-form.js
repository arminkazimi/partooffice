// // Get the container that holds all the buttons
// const radioContainerOne = document.querySelector('.radio-container-1');
//
// let selectedButtonOne = null; // Track the currently selected button
//
// // Add event listener to the container
// radioContainerOne.addEventListener('click', (event) => {
//     // Check if the clicked element has the class 'x-btn-primary'
//     if (event.target.classList.contains('x-btn-primary')) {
//         // Deselect the previously selected button
//         if (selectedButtonOne) {
//             selectedButtonOne.classList.remove('clicked');
//         }
//
//         // Select the clicked button
//         event.target.classList.add('clicked');
//         selectedButtonOne = event.target; // Update the selected button
//     }
// });
//
//
// // Get the container that holds all the buttons
// const radioContainerTwo = document.querySelector('.radio-container-2');
//
// let selectedButtonTwo = null; // Track the currently selected button
//
// // Add event listener to the container
// radioContainerTwo.addEventListener('click', (event) => {
//     // Check if the clicked element has the class 'x-btn-primary'
//     if (event.target.classList.contains('x-btn-primary')) {
//         // Deselect the previously selected button
//         if (selectedButtonTwo) {
//             selectedButtonTwo.classList.remove('clicked');
//         }
//
//         // Select the clicked button
//         event.target.classList.add('clicked');
//         selectedButtonTwo = event.target; // Update the selected button
//     }
// });