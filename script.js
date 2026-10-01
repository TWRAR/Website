(function () {
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      var isDark = current ? current === "dark" : prefersDark;
      var next = isDark ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        localStorage.setItem("twrar-theme", next);
      } catch (e) {}
    });
  }

  var navToggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("site-nav");
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
})();

/* Footer copyright: the start year alone in the first year, then START–CURRENT. */
(function () {
  function run() {var y=new Date().getFullYear();document.querySelectorAll('[data-copyright-years]').forEach(function(e){var s=parseInt(e.getAttribute('data-start'),10);e.textContent=s>=y?String(y):s+'–'+y;});}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
