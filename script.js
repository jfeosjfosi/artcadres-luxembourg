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

  document.querySelectorAll(".nav-dd").forEach(function (dd) {
    var btn = dd.querySelector(".nav-dd__btn");
    if (!btn) return;
    btn.addEventListener("click", function (ev) {
      if (window.matchMedia("(max-width: 1399px)").matches) return;
      ev.preventDefault();
      var open = !dd.classList.contains("is-open");
      document.querySelectorAll(".nav-dd.is-open").forEach(function (other) {
        other.classList.remove("is-open");
        var b = other.querySelector(".nav-dd__btn");
        if (b) b.setAttribute("aria-expanded", "false");
      });
      dd.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (ev) {
    document.querySelectorAll(".nav-dd.is-open").forEach(function (dd) {
      if (!dd.contains(ev.target)) {
        dd.classList.remove("is-open");
        var b = dd.querySelector(".nav-dd__btn");
        if (b) b.setAttribute("aria-expanded", "false");
      }
    });
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "Escape") return;
    document.querySelectorAll(".nav-dd.is-open").forEach(function (dd) {
      dd.classList.remove("is-open");
      var b = dd.querySelector(".nav-dd__btn");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  });

  document.querySelectorAll("img").forEach(function (img) {
    img.setAttribute("draggable", "false");
    img.addEventListener("dragstart", function (ev) { ev.preventDefault(); });
  });

  var stack = document.querySelector(".polaroids");
  if (stack && stack.children.length > 1) {
    var EASE = "cubic-bezier(0.65, 0, 0.35, 1)";
    var DUR = 1150;
    // Slots de devant -> fond : recul progressif (bas-droite), plus petit, légère rotation.
    var POSES = [
      { x: 0.02, y: 0.00, r: -5, s: 1.00 },
      { x: 0.085, y: 0.055, r: 4, s: 0.955 },
      { x: 0.15, y: 0.11, r: -2, s: 0.91 },
      { x: 0.215, y: 0.165, r: 3, s: 0.865 },
      { x: 0.28, y: 0.22, r: 2, s: 0.82 }
    ];
    function tf(x, y, r, s) {
      return "translate3d(" + x + "px," + y + "px,0) rotate(" + r + "deg) scale(" + s + ")";
    }
    function poseAt(i) {
      var p = POSES[Math.min(i, POSES.length - 1)];
      return tf(p.x * stack.clientWidth, p.y * stack.clientHeight, p.r, p.s);
    }
    function layout() {
      [].forEach.call(stack.children, function (card, i) {
        card.setAttribute("data-slot", String(i));
        card.style.transform = poseAt(i);
        card.style.zIndex = String(100 - i);
        card.style.willChange = "transform";
      });
    }
    layout();
    if (!reduce && stack.animate) {
      var busy = false;
      function cycle() {
        if (busy || document.hidden) return;
        var cards = [].slice.call(stack.children);
        var n = cards.length;
        if (n < 2) return;
        busy = true;
        var front = cards[0];
        var W = stack.clientWidth, H = stack.clientHeight;
        var p0 = POSES[0];
        // La carte de devant se soulève nettement hors de la pile (haut-droite), puis file au fond.
        var outT = tf(p0.x * W + 0.34 * W, p0.y * H - 0.11 * H, p0.r - 9, 1.05);
        front.style.zIndex = "200";
        var fAnim = front.animate([
          { transform: poseAt(0), offset: 0 },
          { transform: outT, offset: 0.5 },
          { transform: poseAt(n - 1), offset: 1 }
        ], { duration: DUR, easing: "cubic-bezier(0.55, 0, 0.25, 1)", fill: "forwards" });
        // Une fois détachée de la pile, on la passe derrière : le swap de z devient invisible.
        window.setTimeout(function () { front.style.zIndex = "1"; }, Math.round(DUR * 0.55));
        // Toutes les autres avancent d'un cran, en même temps (c'est ce qui rend le mouvement fluide).
        for (var i = 1; i < n; i++) {
          cards[i].style.zIndex = String(100 - (i - 1));
          cards[i].animate([
            { transform: poseAt(i) },
            { transform: poseAt(i - 1) }
          ], { duration: DUR, easing: EASE, fill: "forwards" });
        }
        var done = false;
        function finish() {
          if (done) return;
          done = true;
          try {
            [].forEach.call(stack.children, function (c) {
              c.getAnimations().forEach(function (a) { a.cancel(); });
            });
          } catch (e) {}
          stack.appendChild(front);
          layout();
          busy = false;
        }
        if (fAnim.finished) fAnim.finished.then(finish, finish);
        else fAnim.onfinish = finish;
        window.setTimeout(finish, DUR + 140);
      }
      window.setInterval(cycle, 4200);
      window.addEventListener("resize", function () { if (!busy) layout(); });
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
