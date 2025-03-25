function setActive(link) {
    // Remove 'x-active' from all .nav-link elements
    var links = document.querySelectorAll('.sidebar .nav-link');
    links.forEach(function (elem) {
        elem.classList.remove('disabled');
    });
    links = document.querySelectorAll('.mobile-menu .nav-link');
    links.forEach(function (elem) {
        elem.classList.remove('disabled');
    });
    // Add 'x-active' to the current link
    link.textContent = 'loading...'
    var elems = document.querySelectorAll('#' + link.id);
    elems.forEach(function (elem) {
        elem.classList.add('x-active');
        elem.classList.add('disabled');
    });
    return false;
}


var currentTab; // Current tab is set to be the first tab (0)

// let radioContainerOne = null;
let selectedButtonOne = null; // Track the currently selected button

// let radioContainerTwo = null;
let selectedButtonTwo = null; // Track the currently selected button

document.addEventListener("htmx:afterSwap", function (event) {
    //clear x-active cllas from sidebar items

    // const triggeringLink = event.detail.pathInfo;
    const targetUrl = event.detail.pathInfo.responsePath
    // console.dir(event.detail.pathInfo.responsePath);
    if (targetUrl !== "/toggle/") {
        var links = document.querySelectorAll('.sidebar .nav-link');
        links.forEach(function (elem) {
            elem.classList.remove('x-active');
        });
    }

    // Call functions based on the clicked URL
    // console.log(targetUrl + ' is loaded!')
    //parto side
    if (targetUrl === "/description/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#description');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'Description'
        });
        // const element = document.getElementById('description')
        // element.textContent = 'Description';
        // element.classList.add('x-active');

    } else if (targetUrl === "/event/list/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#events');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'Events'
        });
        // const element = document.getElementById('events')
        // element.textContent = 'Events';
        // element.classList.add('x-active');

    } else if (targetUrl === "/contacts/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#contacts');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'Contacts'
        });
        // const element = document.getElementById('contacts')
        // element.textContent = 'Contacts';
        // element.classList.add('x-active');

    } else if (targetUrl === "/jobs/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#jobs');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'Jobs'
        });
        // const element = document.getElementById('jobs')
        // element.textContent = 'Jobs';
        // element.classList.add('x-active');

        // office side
    } else if (targetUrl === "/project/list/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#projects');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'Projects'
        });
        // const element = document.getElementById('projects')
        // element.textContent = 'Projects';
        // element.classList.add('x-active');

    } else if (targetUrl === "/product/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#production');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'production'
        });
        // const element = document.getElementById('production')
        // element.textContent = 'Production';
        // element.classList.add('x-active');

        // initProduction(); // Call your existing function
    } else if (targetUrl === "/education/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#education');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'Education'
        });
        // const element = document.getElementById('education')
        // element.textContent = 'Education';
        // element.classList.add('x-active');

    } else if (targetUrl === "/design/create/") {
        console.log(targetUrl + ' is loaded!!!')
        var links = document.querySelectorAll('#design-order');
        links.forEach(function (elem) {
            elem.classList.add('x-active');
            elem.textContent = 'Design Order'
        });
        // const element = document.getElementById('design-order')
        // element.textContent = 'Design Order';
        // element.classList.add('x-active');
        currentTab = 0;
        showTab(currentTab); // Display the current tab


        // Get the container that holds all the buttons
        const radioContainerOne = document.querySelector('.radio-container-1');
        const radioContainerTwo = document.querySelector('.radio-container-2');
// let radioContainerOne = null;
        let selectedButtonOne = null; // Track the currently selected button

// let radioContainerTwo = null;
        let selectedButtonTwo = null; // Track the currently selected button
        // Add event listener to the container
        radioContainerOne.addEventListener('click', (event) => {
            // Check if the clicked element has the class 'x-btn-primary'
            if (event.target.classList.contains('x-btn-primary')) {
                // Deselect the previously selected button
                if (selectedButtonOne) {
                    selectedButtonOne.classList.remove('clicked');
                }
                // Select the clicked button
                event.target.classList.add('clicked');
                selectedButtonOne = event.target; // Update the selected button
            }
        });

// Add event listener to the container
        radioContainerTwo.addEventListener('click', (event) => {
            // Check if the clicked element has the class 'x-btn-primary'
            if (event.target.classList.contains('x-btn-primary')) {
                // Deselect the previously selected button
                if (selectedButtonTwo) {
                    selectedButtonTwo.classList.remove('clicked');
                }

                // Select the clicked button
                event.target.classList.add('clicked');
                selectedButtonTwo = event.target; // Update the selected button
            }
        });
    }
    return false;
});


//design order form:


function showTab(n) {
    // This function will display the specified tab of the form ...
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
    }
    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form... :
    if (currentTab >= x.length) {
        //...the form gets submitted:
        document.getElementById("regForm").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, i, is_radio = false, radioCheckd = false, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        // If a field is empty...
        if (y[i].value == "") {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            // and set the current valid status to false:
            valid = false;
        }
        // Handle radio input type

        if (y[i].type === "radio") {
            is_radio = true
            radioCheckd = radioCheckd || y[i].checked;
            console.log(y[i].checked)
        }

    }
    if (radioCheckd === false && is_radio === true) {
        valid = false;
    }
    // console.log(radioCheckd)
    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active";
}




