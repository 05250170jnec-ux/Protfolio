/* =========================================================
   Dechen Pem | Portfolio interactivity
   ========================================================= */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ---------- Safe localStorage helpers ---------- */
  const store = {
    get(key) { try { return localStorage.getItem(key); } catch (e) { return null; } },
    set(key, val) { try { localStorage.setItem(key, val); } catch (e) { /* ignore */ } }
  };

  /* ---------- Theme toggle (soft cream is the default, deep plum is the dark option) ---------- */
  const root = document.documentElement;
  const themeBtn = $("#theme-toggle");

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    themeBtn.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
    const meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "dark" ? "#1e1119" : "#fbf0e8");
  }

  applyTheme(store.get("theme") === "dark" ? "dark" : "light");

  themeBtn.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next);
    store.set("theme", next);
  });

  /* ---------- Mobile menu ---------- */
  const menuBtn = $("#menu-toggle");
  const navLinks = $("#nav-links");

  function setMenu(open) {
    navLinks.classList.toggle("open", open);
    menuBtn.setAttribute("aria-expanded", String(open));
    menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }

  menuBtn.addEventListener("click", () => setMenu(!navLinks.classList.contains("open")));
  $$("a", navLinks).forEach((a) => a.addEventListener("click", () => setMenu(false)));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });
  document.addEventListener("click", (e) => {
    if (!navLinks.contains(e.target) && !menuBtn.contains(e.target)) setMenu(false);
  });
  window.addEventListener("resize", () => { if (window.innerWidth > 820) setMenu(false); });

  /* ---------- Active link while scrolling ---------- */
  const sections = $$("main section[id]");
  const links = $$("a", navLinks);

  if ("IntersectionObserver" in window) {
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          links.forEach((l) => l.classList.toggle("active", l.getAttribute("href") === "#" + entry.target.id));
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach((s) => spy.observe(s));
  }

  /* ---------- Rotating headline word ---------- */
  const rotator = $("#rotator");
  const words = ["Network Enthusiast", "Web Developer in Training", "Lifelong Learner"];
  let wi = 0;
  if (rotator && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setInterval(() => {
      rotator.classList.add("fade");
      setTimeout(() => {
        wi = (wi + 1) % words.length;
        rotator.textContent = words[wi];
        rotator.classList.remove("fade");
      }, 350);
    }, 2800);
  }

  /* ---------- Build projects from data.js ---------- */
  const grid = $("#projects-grid");
  const filterBox = $("#project-filters");

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function renderProjects(filter) {
    grid.textContent = "";
    const list = (typeof projects !== "undefined" ? projects : [])
      .filter((p) => filter === "All" || p.tech.includes(filter));

    if (!list.length) {
      grid.appendChild(el("p", "empty-note",
        filter === "All" ? "Projects will be added here soon." : "No projects use " + filter + " yet."));
      return;
    }

    list.forEach((p) => {
      const card = el("article", "project-card");
      if (p.image) {
        const thumb = el("div", "project-thumb");
        const img = el("img");
        img.src = p.image;
        img.alt = p.imageAlt || p.title + " screenshot";
        img.loading = "lazy";
        thumb.appendChild(img);
        card.appendChild(thumb);
      }
      card.appendChild(el("h3", "", p.title));
      card.appendChild(el("p", "", p.description));

      const tech = el("ul", "chips");
      p.tech.forEach((t) => tech.appendChild(el("li", "", t)));
      card.appendChild(tech);

      const linkRow = el("div", "project-links");
      (p.links || []).forEach((l) => {
        const a = el("a", "", l.label);
        a.href = l.url; a.target = "_blank"; a.rel = "noopener noreferrer";
        a.setAttribute("aria-label", l.label + ": " + p.title);
        linkRow.appendChild(a);
      });
      if (linkRow.children.length) card.appendChild(linkRow);

      grid.appendChild(card);
    });
  }

  function buildFilters() {
    const all = typeof projects !== "undefined" ? projects : [];
    const techs = Array.from(new Set(all.flatMap((p) => p.tech)));
    filterBox.textContent = "";
    if (techs.length < 2) { filterBox.hidden = true; return; }

    ["All"].concat(techs).forEach((name, i) => {
      const b = el("button", "filter-btn" + (i === 0 ? " active" : ""), name);
      b.type = "button";
      b.addEventListener("click", () => {
        $$(".filter-btn", filterBox).forEach((x) => x.classList.remove("active"));
        b.classList.add("active");
        renderProjects(name);
      });
      filterBox.appendChild(b);
    });
  }

  buildFilters();
  renderProjects("All");

  /* ---------- Build education + certifications from data.js ---------- */
  const eduList = $("#education-list");
  const eduData = typeof education !== "undefined" ? education : [];

  if (!eduData.length) {
    eduList.style.paddingLeft = "0";
    eduList.classList.add("no-line");
    eduList.appendChild(el("p", "empty-note", "Education details will be added here soon."));
  } else {
    eduData.forEach((e) => {
      const item = el("article", "timeline-item reveal");
      item.appendChild(el("h3", "", e.qualification));
      item.appendChild(el("p", "where", e.institution));
      if (e.period) item.appendChild(el("p", "when", e.period));
      if (e.details) item.appendChild(el("p", "details", e.details));
      eduList.appendChild(item);
    });
  }

  const certData = typeof certifications !== "undefined" ? certifications : [];
  if (certData.length) {
    const certList = $("#cert-list");
    certData.forEach((c) => {
      const li = el("li", "reveal");
      const main = el("div", "cert-main");
      main.appendChild(el("strong", "", c.name));
      main.appendChild(el("span", "cert-meta", [c.issuer, c.date || c.year].filter(Boolean).join(" · ")));
      li.appendChild(main);

      if (c.links && c.links.length) {
        const row = el("div", "cert-links");
        c.links.forEach((l) => {
          const a = el("a", "", l.label);
          a.href = l.url; a.target = "_blank"; a.rel = "noopener noreferrer";
          a.setAttribute("aria-label", l.label + ": " + c.name);
          row.appendChild(a);
        });
        li.appendChild(row);
      }
      certList.appendChild(li);
    });
    $("#cert-block").hidden = false;
  }

  /* ---------- Reveal on scroll (after content is built) ---------- */
  const revealEls = $$(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("in"); obs.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    revealEls.forEach((r) => io.observe(r));
  } else {
    revealEls.forEach((r) => r.classList.add("in"));
  }

  /* ---------- Copy email ---------- */
  const copyBtn = $("#copy-email");
  copyBtn.addEventListener("click", async () => {
    const email = $("#email-link").textContent.trim();
    try {
      await navigator.clipboard.writeText(email);
      copyBtn.textContent = "Copied!";
    } catch (e) {
      copyBtn.textContent = "Press Ctrl+C";
      const range = document.createRange();
      range.selectNodeContents($("#email-link"));
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    }
    setTimeout(() => { copyBtn.textContent = "Copy"; }, 2000);
  });

  /* ---------- Contact form (opens the visitor's email app) ---------- */
  const form = $("#contact-form");
  const status = $("#form-status");
  const TO = "05250170.jnec@rub.edu.bt";

  function setError(input, msg) {
    const field = input.closest(".field");
    field.classList.toggle("invalid", Boolean(msg));
    $('.error[data-for="' + input.id + '"]').textContent = msg || "";
  }

  function validate() {
    const name = $("#cf-name"), email = $("#cf-email"), msg = $("#cf-message");
    let ok = true;

    if (name.value.trim().length < 2) { setError(name, "Please enter your name."); ok = false; } else setError(name);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) { setError(email, "Please enter a valid email address."); ok = false; } else setError(email);
    if (msg.value.trim().length < 10) { setError(msg, "Message should be at least 10 characters."); ok = false; } else setError(msg);

    return ok;
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    status.textContent = "";
    if (!validate()) { status.textContent = "Please fix the highlighted fields."; return; }

    const name = $("#cf-name").value.trim();
    const email = $("#cf-email").value.trim();
    const message = $("#cf-message").value.trim();

    const subject = "Portfolio message from " + name;
    const body = message + "\n\n— " + name + " (" + email + ")";
    window.location.href = "mailto:" + TO + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);

    status.textContent = "Opening your email app. Press send there to deliver your message.";
    form.reset();
  });

  ["#cf-name", "#cf-email", "#cf-message"].forEach((id) => {
    $(id).addEventListener("input", () => { if ($(id).closest(".field").classList.contains("invalid")) validate(); });
  });

  /* ---------- Back to top button ---------- */
  const toTop = $("#to-top");
  window.addEventListener("scroll", () => toTop.classList.toggle("show", window.scrollY > 600), { passive: true });
  toTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  /* ---------- Footer year ---------- */
  $("#year").textContent = new Date().getFullYear();
})();
