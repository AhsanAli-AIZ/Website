/* AIZ Pro — site behaviour
   ---------------------------------------------------------------
   Navigation, sticky sub-nav scroll-spy, tabs, accordions,
   scroll reveal, stat counters, contact-form preselect.
   All motion is gated on prefers-reduced-motion.
   --------------------------------------------------------------- */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Reveal animations are opt-in via this class, so that a page with no JS
  // (or with JS that failed to load) renders fully visible rather than blank.
  document.documentElement.classList.add("has-js");

  /* ---------- primary navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  function closeDropdowns() {
    document.querySelectorAll(".has-dropdown.open").forEach(function (i) {
      i.classList.remove("open");
      var a = i.querySelector(":scope > a");
      if (a) a.setAttribute("aria-expanded", "false");
    });
  }

  // First tap opens the panel, second tap follows the link so hub
  // pages stay reachable on touch devices.
  document.querySelectorAll(".has-dropdown > a").forEach(function (link) {
    link.addEventListener("click", function (e) {
      var item = link.parentElement;
      if (!item.classList.contains("open")) {
        e.preventDefault();
        closeDropdowns();
        item.classList.add("open");
        link.setAttribute("aria-expanded", "true");
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-dropdown")) closeDropdowns();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    closeDropdowns();
    if (nav) nav.classList.remove("open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  });

  /* ---------- sticky sub-nav scroll-spy ---------- */
  var subnav = document.querySelector(".subnav");
  if (subnav) {
    var subLinks = Array.prototype.slice.call(subnav.querySelectorAll("a[href^='#']"));
    var targets = subLinks
      .map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); })
      .filter(Boolean);

    if (targets.length) {
      var setActive = function (id) {
        subLinks.forEach(function (a) {
          a.classList.toggle("is-active", a.getAttribute("href") === "#" + id);
        });
      };

      var spy = new IntersectionObserver(function (entries) {
        // Prefer the highest intersecting section on screen.
        var visible = entries
          .filter(function (en) { return en.isIntersecting; })
          .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
        if (visible.length) setActive(visible[0].target.id);
      }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });

      targets.forEach(function (t) { spy.observe(t); });
      setActive(targets[0].id);
    }
  }

  /* ---------- tabs ---------- */
  document.querySelectorAll(".tabs").forEach(function (group) {
    var tabs = Array.prototype.slice.call(group.querySelectorAll("[role='tab']"));
    if (!tabs.length) return;

    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.setAttribute("tabindex", on ? "0" : "-1");
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !on;
      });
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
        else if (e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (e.key === "Home") next = tabs[0];
        else if (e.key === "End") next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); select(next); next.focus(); }
      });
    });

    select(tabs.find(function (t) { return t.getAttribute("aria-selected") === "true"; }) || tabs[0]);
  });

  /* ---------- accordions ---------- */
  document.querySelectorAll(".acc-trigger").forEach(function (trigger) {
    var panel = document.getElementById(trigger.getAttribute("aria-controls"));
    if (!panel) return;

    trigger.addEventListener("click", function () {
      var open = trigger.getAttribute("aria-expanded") === "true";
      trigger.setAttribute("aria-expanded", open ? "false" : "true");
      panel.hidden = open;
    });
  });

  /* ---------- scroll reveal ---------- */
  var revealables = document.querySelectorAll("[data-reveal]");
  function revealAll() {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  }

  if (revealables.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealAll();
    } else {
      var revealer = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
      revealables.forEach(function (el) { revealer.observe(el); });

      // Safety net: content must never stay invisible. If the observer has not
      // delivered by now — a background tab that never composited a frame, an
      // engine quirk — show everything regardless.
      setTimeout(revealAll, 2500);
    }
  }

  /* ---------- stat counters ---------- */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && !reduceMotion && "IntersectionObserver" in window) {
    var countObs = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        obs.unobserve(entry.target);

        var el = entry.target;
        var target = parseFloat(el.getAttribute("data-count"));
        var prefix = el.getAttribute("data-prefix") || "";
        var suffix = el.getAttribute("data-suffix") || "";
        var start = performance.now();
        var dur = 1100;

        (function tick(now) {
          var t = Math.min((now - start) / dur, 1);
          var eased = 1 - Math.pow(1 - t, 3);
          el.textContent = prefix + Math.round(target * eased) + suffix;
          if (t < 1) requestAnimationFrame(tick);
        })(start);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { countObs.observe(el); });
  }

  /* ---------- contact form: preselect from ?interest= ---------- */
  // Options carry explicit value attributes, so this matches on value
  // rather than on visible label text.
  var interestSelect = document.getElementById("interest");
  if (interestSelect) {
    var param = new URLSearchParams(window.location.search).get("interest");
    if (param) {
      var match = Array.prototype.slice.call(interestSelect.options).some(function (o) {
        return o.value === param;
      });
      if (match) interestSelect.value = param;
    }
  }
})();
