(() => {
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('#nav-toggle');
  const nav = document.querySelector('#nav-links');
  const year = document.querySelector('#year');
  const pointerGlow = document.querySelector('#pointer-glow');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const backToTop = document.querySelector('#back-to-top');

  backToTop?.addEventListener('click', (event) => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
    history.replaceState(null, '', window.location.pathname + window.location.search);
  });

  if (year) year.textContent = new Date().getFullYear();

  const syncHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 18);
  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    toggle.setAttribute('aria-label', open ? 'Open navigation' : 'Close navigation');
    nav?.classList.toggle('is-open', !open);
    document.body.style.overflow = open ? '' : 'hidden';
  });

  nav?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      toggle?.setAttribute('aria-expanded', 'false');
      toggle?.setAttribute('aria-label', 'Open navigation');
      nav.classList.remove('is-open');
      document.body.style.overflow = '';
    });
  });

  if (!reducedMotion) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -35px' });

    document.querySelectorAll('.reveal').forEach((el, index) => {
      el.style.transitionDelay = `${Math.min(index % 4, 3) * 60}ms`;
      observer.observe(el);
    });

    window.addEventListener('pointermove', (event) => {
      if (!pointerGlow) return;
      pointerGlow.style.transform = `translate3d(${event.clientX}px, ${event.clientY}px, 0)`;
    }, { passive: true });

    document.querySelectorAll('.project-card').forEach((card) => {
      card.addEventListener('pointermove', (event) => {
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--x', `${event.clientX - rect.left}px`);
        card.style.setProperty('--y', `${event.clientY - rect.top}px`);
      });
    });
  } else {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('is-visible'));
  }
})();
