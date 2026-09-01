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
    var EASE = "cubic-bezier(0.33, 0.05, 0.15, 1)";
    var DUR = 1080;
    var POSES = [
      { x: 0.15, y: 0.00, r: -6, z: 5 },
      { x: 0.21, y: 0.05, r: 5, z: 4 },
      { x: 0.11, y: 0.10, r: -3, z: 3 },
      { x: 0.23, y: 0.15, r: 4, z: 2 },
      { x: 0.13, y: 0.20, r: 2, z: 1 }
    ];
    function tf(x, y, r) {
      return "translate3d(" + x + "px," + y + "px,0) rotate(" + r + "deg)";
    }
    function pose(i) {
      var p = POSES[Math.min(i, POSES.length - 1)];
      var x = p.x * stack.clientWidth;
      var y = p.y * stack.clientHeight;
      return { transform: tf(x, y, p.r), z: String(p.z), x: x, y: y, r: p.r };
    }
    function layout(skip) {
      var n = 0;
      [].forEach.call(stack.children, function (card) {
        if (card === skip) {
          card.setAttribute("data-slot", "deal");
          return;
        }
        var p = pose(n);
        card.setAttribute("data-slot", String(n));
        card.style.zIndex = p.z;
        card.style.transform = p.transform;
        n += 1;
      });
    }
    layout();
    if (!reduce && stack.animate) {
      var busy = false;
      function cycle() {
        if (busy || document.hidden) return;
        var front = stack.firstElementChild;
        if (!front) return;
        busy = true;
        var from = pose(0);
        var to = pose(4);
        var w = stack.clientWidth;
        var peekX = from.x + (w < 420 ? 0.10 : 0.13) * w;
        var peekY = from.y + (to.y - from.y) * 0.45;
        var midY = peekY + (to.y - peekY) * 0.28;
        var anims = [];
        var done = false;

        front.classList.add("is-deal");
        front.style.zIndex = "10";

        var slot = 0;
        [].forEach.call(stack.children, function (card) {
          if (card === front) return;
          var start = pose(slot + 1);
          var end = pose(slot);
          card.setAttribute("data-slot", String(slot));
          card.style.zIndex = end.z;
          anims.push(card.animate(
            [{ transform: start.transform }, { transform: end.transform }],
            { duration: DUR, easing: EASE, fill: "forwards" }
          ));
          slot += 1;
        });

        var anim = front.animate([
          { transform: from.transform, offset: 0 },
          { transform: tf(peekX, peekY, 7), offset: 0.4 },
          { transform: tf(peekX * 0.97, midY, 4), offset: 0.52 },
          { transform: to.transform, offset: 1 }
        ], { duration: DUR, easing: EASE, fill: "forwards" });
        anims.push(anim);

        window.setTimeout(function () {
          if (front.classList.contains("is-deal")) front.style.zIndex = "1";
        }, Math.round(DUR * 0.44));

        function finish() {
          if (done) return;
          done = true;
          anims.forEach(function (a) {
            try { a.commitStyles(); a.cancel(); } catch (err) {}
          });
          stack.appendChild(front);
          front.classList.remove("is-deal");
          layout();
          busy = false;
        }
        if (anim.finished) anim.finished.then(finish, finish);
        else anim.onfinish = finish;
        window.setTimeout(finish, DUR + 100);
      }
      window.setInterval(cycle, 3600);
      window.addEventListener("resize", function () {
        if (!busy) layout();
      });
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
