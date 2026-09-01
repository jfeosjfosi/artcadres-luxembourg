// Scroll-reveal sobre, respecte prefers-reduced-motion. Aucune lib.
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var els = document.querySelectorAll(".reveal:not(.reveal-in)");

  function show(el) {
    el.classList.add("in");
  }

  function revealInView() {
    els.forEach(function (e) {
      if (e.classList.contains("in")) return;
      var r = e.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.92 && r.bottom > 0) {
        show(e);
      }
    });
  }

  if (reduce || !("IntersectionObserver" in window)) {
    els.forEach(show);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          show(en.target);
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -4% 0px" });
    els.forEach(function (e) { io.observe(e); });
    revealInView();
    window.addEventListener("load", revealInView);
    window.addEventListener("resize", revealInView);
  }

  document.querySelectorAll(".nav a").forEach(function (a) {
    a.addEventListener("click", function () {
      document.body.classList.remove("nav-open");
    });
  });

  document.querySelectorAll("img").forEach(function (img) {
    img.setAttribute("draggable", "false");
    img.addEventListener("dragstart", function (ev) { ev.preventDefault(); });
  });

  var stack = document.querySelector(".polaroids");
  if (stack && stack.children.length > 1) {
    function slots() {
      [].forEach.call(stack.children, function (card, i) {
        card.setAttribute("data-slot", String(i));
      });
    }
    slots();
    if (!reduce) {
      var busy = false;
      var EXIT_MS = 560;
      function cycle() {
        if (busy || document.hidden) return;
        var front = stack.firstElementChild;
        if (!front) return;
        busy = true;
        front.classList.add("is-exit");
        stack.appendChild(front);
        slots();
        window.setTimeout(function () {
          front.classList.add("is-tuck");
          window.requestAnimationFrame(function () {
            front.classList.remove("is-exit", "is-tuck");
            window.setTimeout(function () { busy = false; }, 720);
          });
        }, EXIT_MS);
      }
      window.setInterval(cycle, 3400);
    }
  }
})();
