document.addEventListener('DOMContentLoaded', () => {
  // ---------- Icons ----------
  if (window.lucide) lucide.createIcons();

  // ---------- AOS ----------
  if (window.AOS) {
    AOS.init({ once: true, duration: 700, easing: 'ease-out-cubic', offset: 60 });
  }

  // ---------- Navbar scroll state ----------
  const navbar = document.getElementById('navbar');
  const onScroll = () => {
    if (window.scrollY > 20) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // ---------- Mobile menu ----------
  const menuBtn = document.getElementById('menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  menuBtn?.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });
  mobileMenu?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => mobileMenu.classList.add('hidden'));
  });

  // ---------- Active nav link on scroll ----------
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  const setActiveLink = () => {
    let current = sections[0]?.id;
    const scrollPos = window.scrollY + 120;
    sections.forEach((section) => {
      if (scrollPos >= section.offsetTop) current = section.id;
    });
    navLinks.forEach((link) => {
      const isActive = link.getAttribute('href') === `#${current}`;
      link.classList.toggle('text-accent-light', isActive);
      link.classList.toggle('text-white/70', !isActive);
    });
  };
  setActiveLink();
  window.addEventListener('scroll', setActiveLink, { passive: true });

  // ---------- Typing effect ----------
  const typedEl = document.getElementById('typed-role');
  const roles = ['Web Developer', 'Problem Solver', 'Builder'];
  let roleIndex = 0, charIndex = 0, deleting = false;

  function typeLoop() {
    if (!typedEl) return;
    const word = roles[roleIndex];

    if (!deleting) {
      charIndex++;
      typedEl.textContent = word.slice(0, charIndex);
      if (charIndex === word.length) {
        deleting = true;
        setTimeout(typeLoop, 1400);
        return;
      }
    } else {
      charIndex--;
      typedEl.textContent = word.slice(0, charIndex);
      if (charIndex === 0) {
        deleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
      }
    }
    setTimeout(typeLoop, deleting ? 45 : 90);
  }
  typeLoop();

  // ---------- Mouse glow (only within dark sections) ----------
  const glow = document.getElementById('mouse-glow');
  const darkSections = document.querySelectorAll('#home, #contact');
  let overDark = false;

  darkSections.forEach((sec) => {
    sec.addEventListener('mouseenter', () => { overDark = true; glow.style.opacity = '1'; });
    sec.addEventListener('mouseleave', () => { overDark = false; glow.style.opacity = '0'; });
  });

  window.addEventListener('mousemove', (e) => {
    if (!overDark) return;
    glow.style.transform = `translate(${e.clientX - 210}px, ${e.clientY - 210}px)`;
  }, { passive: true });

  // ---------- Scroll progress bar ----------
  const progressBar = document.getElementById('scroll-progress');
  const updateProgress = () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = `${pct}%`;
  };
  updateProgress();
  window.addEventListener('scroll', updateProgress, { passive: true });
  window.addEventListener('resize', updateProgress);

  // ---------- Scroll to top ----------
  const toTop = document.getElementById('to-top');
  toTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ---------- Skill bars animate on view ----------
  const skillBars = document.querySelectorAll('.skill-bar');
  const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        bar.style.width = `${bar.dataset.level}%`;
        skillObserver.unobserve(bar);
      }
    });
  }, { threshold: 0.4 });
  skillBars.forEach((bar) => skillObserver.observe(bar));

  // ---------- Contact form ----------
  const form = document.getElementById('contact-form');
  const submitBtn = document.getElementById('contact-submit');
  const status = document.getElementById('form-status');

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    document.querySelectorAll('.form-error').forEach((el) => (el.textContent = ''));
    status.textContent = '';

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    submitBtn.disabled = true;
    const originalHTML = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span>Sending…</span>';

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (!res.ok) {
        if (data.errors) {
          Object.entries(data.errors).forEach(([field, msg]) => {
            const el = document.querySelector(`.form-error[data-for="${field}"]`);
            if (el) el.textContent = msg;
          });
        }
        status.textContent = 'Please fix the errors above.';
        status.classList.remove('text-emerald-400');
        status.classList.add('text-red-400');
      } else {
        status.textContent = data.message || 'Message sent!';
        status.classList.remove('text-red-400');
        status.classList.add('text-emerald-400');
        form.reset();
      }
    } catch (err) {
      status.textContent = 'Something went wrong. Please try again.';
      status.classList.add('text-red-400');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalHTML;
      if (window.lucide) lucide.createIcons();
    }
  });
});
