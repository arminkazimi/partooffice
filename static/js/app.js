const main = document.getElementById('main')
const logoButton = document.getElementById('logo-btn')
const menu = document.getElementById('menu')
const officeTpl = document.getElementById('office-menu');
const partoTpl = document.getElementById('parto-menu');


// slider configs:
const sliderConfig = {}
let slides = document.querySelector('#slides');
let images = document.querySelectorAll('#slides img');
let prevBtn = document.getElementById('armin-prev');
let nextBtn = document.getElementById('armin-next');
let numberBtns = document.querySelectorAll('.page-number .slider-btns');
let captions = [];
let captionElement;
let index = 0;

let cells;
let backBtn;
let jobsFormListenerAttached = false;

let app = {
    _site: 'office',
    _section: 'projects',
    _isDetail: false,
    _ignoreSections: new Set(['description', 'contacts', 'jobs', 'design-order', 'education']),
    _sectionsWithSlider: new Set(['production', 'details']),
    get site() {
        return this._site;
    },
    set site(newSite) {
        this._site = newSite;
    },

    get isDetail() {
        return this._isDetail;
    },
    set isDetail(isDetail) {
        this._isDetail = isDetail;
    },

    get section() {
        return this._section;
    },
    set section(newSection) {
        if (this._section === newSection) return;
        this._section = newSection;
        // renderActiveSection()

        // if (this._ignoreSections.has(newSection)) {
        //     console.log("section change ignored for:", newSection);
        //     return;
        // }
        // if (this._sectionsWithSlider.has(newSection)) {
        //     console.log("section changed to:", newSection);
        // }
    }
};

const initTiles = () => {
    cells = document.querySelectorAll('.cell');

    cells.forEach(cell => {
        cell.addEventListener('click', () => cellClickHandler(Number(cell.dataset.id)));
    });
};

const cellClickHandler = (id) => {
    console.log('thjis is detail ID:', id)
    app.isDetail = true;
    renderActiveSection()
    initImageSlider()

    backBtn = document.getElementById('back');
    backBtn.addEventListener('click', backClickHandler)
};

const getJobsPayload = (form) => ({
    name: form?.querySelector('#jobs-fullname')?.value?.trim() || '',
    email: form?.querySelector('#jobs-email')?.value?.trim() || '',
    phone_number: form?.querySelector('#jobs-phone')?.value?.trim() || '',
});

const getJobsEndpoint = (form) => form?.dataset?.endpoint || '/api/jobs/';

const renderJobsStatus = (form, message, isError = false) => {
    const status = form?.querySelector('#jobs-status');
    if (!status) return;
    status.textContent = message;
    status.classList.toggle('error', Boolean(isError));
};

const toggleJobsSubmittingState = (form, isSubmitting) => {
    const submitBtn = form?.querySelector('#jobs-submit');
    if (!submitBtn) return;
    submitBtn.disabled = isSubmitting;
    submitBtn.textContent = isSubmitting ? 'Saving...' : 'Save';
};

const getCookie = (name) => {
    if (!document.cookie) return null;
    const token = document.cookie
        .split(';')
        .map(cookie => cookie.trim())
        .find(cookie => cookie.startsWith(`${name}=`));
    return token ? decodeURIComponent(token.split('=')[1]) : null;
};

const submitJobsForm = async (event) => {
    const form = event.target?.closest('#jobs-form');
    if (!form) return;
    event.preventDefault();

    const payload = getJobsPayload(form);
    const csrfToken = getCookie('csrftoken');

    toggleJobsSubmittingState(form, true);
    renderJobsStatus(form, '');

    try {
        const res = await fetch(getJobsEndpoint(form), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
            },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            const errorText = `Save failed (HTTP ${res.status})`;
            renderJobsStatus(form, errorText, true);
            throw new Error(errorText);
        }

        renderJobsStatus(form, 'Saved successfully.');
        form.reset();
    } catch (err) {
        renderJobsStatus(form, 'Save failed, please try again.', true);
        console.error('jobs submit failed', err);
    } finally {
        toggleJobsSubmittingState(form, false);
    }
};

const initJobsForm = () => {
    if (jobsFormListenerAttached) return;
    document.addEventListener('submit', submitJobsForm);
    jobsFormListenerAttached = true;
};
const backClickHandler = () => {
    app.isDetail = false;
    renderActiveSection()
    initTiles();
    
};

const initImageSlider = () => {
    slides = document.querySelector('#slides');
    images = document.querySelectorAll('#slides img');
    prevBtn = document.getElementById('armin-prev');
    nextBtn = document.getElementById('armin-next');
    numberBtns = document.querySelectorAll('.page-number .slider-btns');
    captionElement = document.querySelector('.caption');

    index = 0;

    const captionTemplate = document.getElementById('captions');
    const captionNodes = captionTemplate.content.querySelectorAll('p');

    captions = Array.from(captionNodes).map(p => p.innerHTML);
    numberBtns.forEach(numberBtn => {
        numberBtn.addEventListener('click', () => showSlide(Number(numberBtn.dataset.index)));
    });

    prevBtn.addEventListener('click', () => showSlide(index - 1));
    nextBtn.addEventListener('click', () => showSlide(index + 1));

    // showSlide(0)
};

const showSlide = (i) => {
    if (i < 0) index = images.length - 1;
    else if (i >= images.length) index = 0;
    else index = i;

    slides.style.transform = `translateX(-${index * 100}%)`;

    if (captions[index]) {
        captionElement.innerHTML = captions[index];
    }

    numberBtns.forEach(btn => btn.classList.remove('active-number'));
    const activeBtn = document.querySelector(`.slider-btns[data-index="${index}"]`);
    if (activeBtn) activeBtn.classList.add('active-number');


};

async function fetchProjects() {
    try {
        const res = await fetch('api/projects/'); // e.g. /api/projects/
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        console.log('projects list', data);
        // render into DOM...
    } catch (err) {
        console.error('fetchProjects error', err);
    }
}

const DOMContentLoadedHandler = () => {
    console.log('DOM is ready!');
    // You can safely access elements here
    fetchProjects();
    initJobsForm();
    // setupFormListener();
};

const renderMenu = () => {
    menu.innerHTML = '';
    if (app.site === 'office') {
        menu.appendChild(partoTpl.content.cloneNode(true)); // show Parto menu
        app.site = 'parto';
        app.section = 'description';
    } else {
        menu.appendChild(officeTpl.content.cloneNode(true)); // show office menu
        app.site = 'office';
        app.section = 'projects';
    }
};


const toggleSiteHandler = () => {

    renderMenu()

};

const renderActiveSection = () => {
    let currentTemplate;
    if (app.isDetail) currentTemplate = document.getElementById('details-section');
    else currentTemplate = document.getElementById(`${app.section}-section`);
    console.log(currentTemplate)
    main.innerHTML = '';
    main.appendChild(currentTemplate.content.cloneNode(true));
};


const menuClickHandler = (event) => {
    const item = event.target.closest('button');
    if (!item || !menu.contains(item)) return; // clicked outside items

    event.preventDefault(); // if links with href you want to override

    // You can use id or data-action
    app.section = item.dataset.action;
    app.isDetail = false;
    renderActiveSection();

    console.log('section:', app.section)
    if (app.site === 'office') {
        switch (app.section) {
            case 'projects':
                // handle projects
                initTiles();
                console.log('projects clicked', item);
                break;
            case 'production':
                initImageSlider();
                console.log('production clicked', item);
                break;
            case 'design-order':
                console.log('design-order clicked', item);
                break;
            case 'education':
                console.log('education clicked', item);
                break;
            // ...

            default:
                console.log('unknown item', item);
        }
    }

    if (app.site === 'parto') {
        switch (app.section) {
            case 'description':
                // handle projects
                console.log('description clicked', item);
                break;
            case 'events':
                initTiles();
                console.log('events clicked', item);
                break;
            case 'contacts':
                console.log('contacts clicked', item);
                break;
            case 'jobs':
                initJobsForm();
                console.log('jobs clicked', item);
                break;
            // ...

            default:
                console.log('unknown item', action);
        }
    }
};

document.addEventListener('DOMContentLoaded', DOMContentLoadedHandler);
logoButton.addEventListener('click', toggleSiteHandler);
menu.addEventListener('click', (event) => menuClickHandler(event));
