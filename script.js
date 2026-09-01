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
      function cycle() {
        if (busy || document.hidden) return;
        var front = stack.firstElementChild;
        if (!front) return;
        busy = true;
        front.classList.add("is-exit");
        window.setTimeout(function () {
          front.classList.add("is-tuck");
          window.setTimeout(function () {
            stack.appendChild(front);
            slots();
            void front.offsetWidth;
            front.classList.remove("is-exit", "is-tuck");
            window.setTimeout(function () { busy = false; }, 700);
          }, 650);
        }, 650);
      }
      window.setInterval(cycle, 3600);
    }
  }

  var faqItems = document.querySelectorAll(".faq-item");
  if (faqItems.length && !reduce) {
    faqItems.forEach(function (item) {
      var body = item.querySelector(".faq-a");
      var sum = item.querySelector("summary");
      if (!body || !sum) return;
      function closeItem(el) {
        var b = el.querySelector(".faq-a");
        el.classList.remove("is-open");
        if (b) b.style.gridTemplateRows = "0fr";
        window.clearTimeout(el._faqT);
        el._faqT = window.setTimeout(function () {
          el.removeAttribute("open");
        }, 460);
      }
      function openItem(el) {
        window.clearTimeout(el._faqT);
        el.setAttribute("open", "");
        el.classList.add("is-open");
        var b = el.querySelector(".faq-a");
        if (!b) return;
        b.style.gridTemplateRows = "0fr";
        window.requestAnimationFrame(function () {
          window.requestAnimationFrame(function () {
            b.style.gridTemplateRows = "1fr";
          });
        });
      }
      sum.addEventListener("click", function (ev) {
        ev.preventDefault();
        var willOpen = !item.classList.contains("is-open");
        faqItems.forEach(function (other) {
          if (other !== item && other.classList.contains("is-open")) closeItem(other);
        });
        if (willOpen) openItem(item);
        else closeItem(item);
      });
    });
  }
})();
