// Menu DOM
const menu = document.querySelector(".menu");
const overlayMenu = document.querySelector(".overlay-menu");
const closeOverlayMenu = document.querySelector(".overlay-menu__close");

// Suggest DOM
const suggest = document.querySelector(".suggest");
const searchInput = document.querySelector("#word");
const arabicPattern = /[\u0600-\u06FF]/;
const ENTER_KEY_CODE = 13;

// Search Form DOM
const searchForm = document.getElementById("form-search");
const btnSearchForm = document.getElementById("searchBtn");

// Handling Menu
menu.addEventListener("click", function (e) {
  e.preventDefault();
  overlayMenu.classList.add("overlay-menu__show");
});

closeOverlayMenu.addEventListener("click", function (e) {
  e.preventDefault();
  overlayMenu.classList.remove("overlay-menu__show");
});

// Helper Functions
const goToWordPage = function (word) {
  return `${location.origin}${location.pathname.slice(0, 4)}word/${word}`;
};

// Handling send ajax request for suggestion
if (searchInput) {
  searchInput.addEventListener("keyup", async function (e) {
    const value = e.target.value.trim().toLowerCase();

    if (value === "") {
      suggest.innerHTML = "";
      suggest.classList.remove("suggest__show");
      e.target.classList.remove("search-form__input--suggest");
      e.target.classList.remove("search-form__input--en");
      return false;
    } else if (!arabicPattern.test(value)) {
      e.target.classList.add("search-form__input--en");
    }

    if (e.keyCode === ENTER_KEY_CODE) {
      location.href = goToWordPage(value);
      return;
    }

    try {
      const response = await fetch(`${location.origin}/${location.pathname.slice(1,3)}/suggest/${value}/`);
      if (!response.ok) {
        throw new Error("Word Not Found");
      }
      const { html } = await response.json();
      suggest.classList.add("suggest__show");
      e.target.classList.add("search-form__input--suggest");
      suggest.innerHTML = "";
      suggest.insertAdjacentHTML("afterbegin", html);
      return true;
    } catch (error) {
      suggest.innerHTML = "";
      e.target.classList.remove("search-form__input--suggest");
      suggest.classList.remove("suggest__show");
      console.log(error.message);
    }
  });
}

if (searchForm) {
  searchForm.addEventListener("submit", function (e) {
    e.preventDefault();
  });
}

if (btnSearchForm) {
  btnSearchForm.addEventListener("click", function (e) {
    e.preventDefault();
    const query = searchInput.value.trim().toLowerCase();
    if (query) {
      location.href = goToWordPage(query);
    }
  });
}
