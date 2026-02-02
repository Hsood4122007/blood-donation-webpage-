// Advanced GSAP Animations for BloodLife Platform

document.addEventListener('DOMContentLoaded', function() {
    // Ensure GSAP and ScrollTrigger are loaded
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
        console.warn('GSAP or ScrollTrigger not loaded');
        return;
    }

    // Register plugins
    gsap.registerPlugin(ScrollTrigger);

    // Global animation defaults
    gsap.defaults({
        duration: 0.8,
        ease: "power2.out"
    });

    // Hero Section Animations
    function initHeroAnimations() {
        const hero = document.querySelector('.hero');
        if (!hero) return;

        // Background elements animation
        gsap.to('.hero .absolute:nth-child(2) .absolute:nth-child(1)', {
            x: -50,
            y: -30,
            duration: 8,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut"
        });

        gsap.to('.hero .absolute:nth-child(2) .absolute:nth-child(2)', {
            x: 30,
            y: 40,
            duration: 10,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut",
            delay: 1
        });

        // Hero content stagger animation
        const heroElements = gsap.utils.toArray('.hero-content > div > *');
        gsap.from(heroElements, {
            opacity: 0,
            y: 50,
            stagger: 0.15,
            duration: 1,
            ease: "back.out(1.4)",
            scrollTrigger: {
                trigger: '.hero',
                start: "top 80%",
                toggleActions: "play none none reverse"
            }
        });

        // Hero media card animation
        gsap.from('.hero-media-card', {
            opacity: 0,
            x: 100,
            rotation: 5,
            duration: 1.2,
            ease: "elastic.out(1, 0.5)",
            scrollTrigger: {
                trigger: '.hero-media',
                start: "top 70%",
                toggleActions: "play none none reverse"
            }
        });
    }

    // Story Block Animations
    function initStoryAnimations() {
        // Story points animation
        gsap.utils.toArray('.story-point').forEach((point, i) => {
            gsap.from(point, {
                opacity: 0,
                y: 30,
                duration: 0.8,
                delay: i * 0.1,
                scrollTrigger: {
                    trigger: point,
                    start: "top 85%",
                    toggleActions: "play none none reverse"
                }
            });
        });

        // Steps animation
        gsap.utils.toArray('.steps > li').forEach((step, i) => {
            gsap.from(step, {
                opacity: 0,
                x: -50,
                duration: 0.6,
                delay: i * 0.15,
                scrollTrigger: {
                    trigger: step,
                    start: "top 90%",
                    toggleActions: "play none none reverse"
                }
            });
        });

        // Media cards floating effect
        gsap.utils.toArray('.story-media .rounded-2xl').forEach(card => {
            gsap.to(card, {
                y: -15,
                duration: 3,
                repeat: -1,
                yoyo: true,
                ease: "sine.inOut"
            });
        });
    }

    // Impact Section Animations
    function initImpactAnimations() {
        // Animated counters
        const counters = document.querySelectorAll('.impact-number');
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count-to')) || 0;
            
            ScrollTrigger.create({
                trigger: counter,
                start: "top 85%",
                onEnter: () => {
                    animateCounter(counter, target);
                },
                once: true
            });
        });

        // Impact cards entrance
        gsap.utils.toArray('.impact-card').forEach((card, i) => {
            gsap.from(card, {
                opacity: 0,
                y: 50,
                scale: 0.9,
                duration: 0.8,
                delay: i * 0.1,
                scrollTrigger: {
                    trigger: card,
                    start: "top 90%",
                    toggleActions: "play none none reverse"
                }
            });
        });
    }

    // Counter animation function
    function animateCounter(element, target) {
        const duration = 2;
        const increment = target / (duration * 60);
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        };
        
        updateCounter();
    }

    // Form Animations
    function initFormAnimations() {
        // Registration form step transitions
        const steps = document.querySelectorAll('#donor-registration-form .step');
        if (steps.length > 0) {
            // Add smooth transitions between steps
            document.addEventListener('stepChange', (e) => {
                const { fromStep, toStep } = e.detail;
                gsap.fromTo(toStep, 
                    { opacity: 0, x: 50 },
                    { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }
                );
            });
        }

        // Input field focus animations
        gsap.utils.toArray('input, select, textarea').forEach(input => {
            input.addEventListener('focus', () => {
                gsap.to(input, {
                    scale: 1.02,
                    duration: 0.2,
                    ease: "power1.out"
                });
            });

            input.addEventListener('blur', () => {
                gsap.to(input, {
                    scale: 1,
                    duration: 0.2,
                    ease: "power1.out"
                });
            });
        });

        // Button hover effects
        gsap.utils.toArray('button:not(.gsap-ignore)').forEach(button => {
            button.addEventListener('mouseenter', () => {
                gsap.to(button, {
                    scale: 1.05,
                    duration: 0.3,
                    ease: "back.out(1.7)"
                });
            });

            button.addEventListener('mouseleave', () => {
                gsap.to(button, {
                    scale: 1,
                    duration: 0.3,
                    ease: "power2.out"
                });
            });
        });
    }

    // Search Results Animations
    function initSearchAnimations() {
        // Donor card entrance animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    gsap.fromTo(entry.target, 
                        { opacity: 0, y: 30, scale: 0.95 },
                        { 
                            opacity: 1, 
                            y: 0, 
                            scale: 1,
                            duration: 0.6,
                            delay: index * 0.1,
                            ease: "back.out(1.4)"
                        }
                    );
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        // Observe donor cards
        gsap.utils.toArray('#results-container > div').forEach(card => {
            observer.observe(card);
        });
    }

    // Navbar Animation
    function initNavbarAnimation() {
        const navbar = document.querySelector('.navbar');
        if (!navbar) return;

        // Navbar scroll effect with smooth transition
        let lastScrollY = window.scrollY;
        
        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 50) {
                gsap.to(navbar, {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    backdropFilter: 'blur(10px)',
                    duration: 0.3,
                    ease: "power2.out"
                });
            } else {
                gsap.to(navbar, {
                    backgroundColor: 'transparent',
                    backdropFilter: 'none',
                    duration: 0.3,
                    ease: "power2.out"
                });
            }
            
            lastScrollY = currentScrollY;
        });
    }

    // Page Load Entrance Animations
    function initPageLoadAnimations() {
        // Staggered entrance for all animated elements
        const animatedElements = gsap.utils.toArray('.animate-on-scroll');
        
        animatedElements.forEach((element, i) => {
            // Skip if already animated
            if (element.dataset.animated) return;
            
            gsap.fromTo(element,
                { opacity: 0, y: 30 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    delay: i * 0.05,
                    ease: "power2.out",
                    onComplete: () => {
                        element.dataset.animated = "true";
                    },
                    scrollTrigger: {
                        trigger: element,
                        start: "top 90%",
                        toggleActions: "play none none reverse"
                    }
                }
            );
        });
    }

    // Initialize all animations
    function initAllAnimations() {
        initHeroAnimations();
        initStoryAnimations();
        initImpactAnimations();
        initFormAnimations();
        initNavbarAnimation();
        initPageLoadAnimations();
        
        // Listen for dynamic content
        document.addEventListener('searchResultsLoaded', initSearchAnimations);
    }

    // Run initialization
    initAllAnimations();

    // Export functions for external use
    window.BloodLifeAnimations = {
        initSearchAnimations,
        animateCounter
    };
});

// Utility functions for other scripts
window.animateDonorCardEntrance = function(cardElement) {
    if (typeof gsap !== 'undefined') {
        gsap.fromTo(cardElement,
            { opacity: 0, y: 30, scale: 0.95 },
            { 
                opacity: 1, 
                y: 0, 
                scale: 1,
                duration: 0.6,
                ease: "back.out(1.4)"
            }
        );
    }
};