// Simple scroll-based animations for sections and images
(function () {
  function onScroll() {
    const fadeElems = document.querySelectorAll(".scroll-fade");
    const parallaxElems = document.querySelectorAll(".scroll-parallax");
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;

    fadeElems.forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < viewportHeight * 0.85) {
        el.classList.add("visible");
      }
    });

    const scrollY = window.scrollY || window.pageYOffset;
    parallaxElems.forEach((el) => {
      const speed = 0.12;
      const offset = (scrollY - el.offsetTop) * speed;
      el.style.transform = `translateY(${offset}px)`;
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("load", onScroll);

  // Home page search functionality
  document.addEventListener('DOMContentLoaded', function() {
    const homeSearchForm = document.getElementById('home-search-form');
    
    if (homeSearchForm) {
      homeSearchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const bloodGroup = document.getElementById('home-blood-group').value;
        const pincode = document.getElementById('home-pincode').value;
        
        if (!bloodGroup) {
          alert('Please select a blood group');
          return;
        }
        
        // Redirect to search page with parameters
        let url = '/accounts/search/?blood_group=' + encodeURIComponent(bloodGroup);
        if (pincode) {
          url += '&pincode=' + encodeURIComponent(pincode);
        }
        
        window.location.href = url;
      });
    }
  });

  // Enhanced GSAP animations
  if (typeof gsap !== 'undefined') {
    // Hero section entrance animation
    gsap.from('.hero h1', {
      opacity: 0,
      y: 50,
      duration: 1,
      delay: 0.2,
      ease: 'power3.out'
    });
    
    gsap.from('.hero-copy', {
      opacity: 0,
      y: 30,
      duration: 1,
      delay: 0.4,
      ease: 'power2.out'
    });
    
    // Staggered button animations
    gsap.from('.hero-actions a', {
      opacity: 0,
      y: 20,
      duration: 0.8,
      delay: 0.6,
      stagger: 0.1,
      ease: 'back.out(1.7)'
    });
    
    // Animated counter for impact section
    const counters = document.querySelectorAll('.impact-number');
    counters.forEach(counter => {
      const target = parseInt(counter.getAttribute('data-count-to'));
      const duration = 2;
      const increment = target / (duration * 60);
      let current = 0;
      
      const updateCounter = () => {
        current += increment;
        if (current < target) {
          counter.textContent = Math.floor(current);
          requestAnimationFrame(updateCounter);
        } else {
          counter.textContent = target;
        }
      };
      
      // Start counter when element comes into view
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            updateCounter();
            observer.unobserve(entry.target);
          }
        });
      });
      
      observer.observe(counter);
    });
  }
})();


