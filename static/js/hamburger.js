const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".mobile-menu");

hamburger.addEventListener("click", () => {

  /* Toggle active class */
  hamburger.classList.toggle("hambur-active");
  navMenu.classList.toggle("hambur-active");

  /* Toggle aria-expanded value */
  let menuOpen = navMenu.classList.contains("hambur-active");
  console.log(menuOpen)
  let newMenuOpenStatus = menuOpen;
  hamburger.setAttribute("aria-expanded", newMenuOpenStatus);
})

// close mobile menu
document.querySelectorAll(".nav-link").forEach(n => n.addEventListener("click", () => {
  hamburger.classList.remove("hambur-active");
  navMenu.classList.remove("hambur-active");
//   Need to add Toggle aria-expanded value here as well because it stays as true when you click a menu item
}))