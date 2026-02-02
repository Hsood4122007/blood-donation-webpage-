// Enhanced JavaScript for Blood Donation Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSmoothScrolling();
    initAnimatedElements();
    initDynamicColors();
    initParallaxEffects();
    initFormValidations();
    initInteractiveFeatures();
});

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Animate elements on scroll
function initAnimatedElements() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all animate-on-scroll elements
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Dynamic color system based on scroll position
function initDynamicColors() {
    const sections = document.querySelectorAll('section');
    const navbar = document.querySelector('.navbar');
    
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                const sectionId = section.id;
                updateNavbarColor(navbar, sectionId);
            }
        });
    });
}

function updateNavbarColor(navbar, sectionId) {
    // Remove all color classes
    navbar.classList.remove('bg-red-900', 'bg-blue-900', 'bg-purple-900', 'bg-pink-900');
    
    // Add color based on section
    switch(sectionId) {
        case 'story':
            navbar.classList.add('bg-red-900');
            break;
        case 'how-it-works':
            navbar.classList.add('bg-blue-900');
            break;
        case 'impact':
            navbar.classList.add('bg-purple-900');
            break;
        case 'join':
            navbar.classList.add('bg-pink-900');
            break;
        default:
            navbar.classList.remove('bg-red-900', 'bg-blue-900', 'bg-purple-900', 'bg-pink-900');
    }
}

// Parallax effects
function initParallaxEffects() {
    const parallaxElements = document.querySelectorAll('.parallax-element');
    
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.parallaxSpeed || 0.5;
            const yPos = -(scrollPosition * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Enhanced form validations
function initFormValidations() {
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });

    // Phone number validation
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validatePhoneNumber(this);
        });
    });

    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            showPasswordStrength(this);
        });
    });
}

function validateEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(input.value);
    
    if (!isValid && input.value) {
        input.classList.add('border-red-500');
        showError(input, 'Please enter a valid email address');
    } else {
        input.classList.remove('border-red-500');
        hideError(input);
    }
}

function validatePhoneNumber(input) {
    const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
    const isValid = phoneRegex.test(input.value);
    
    if (!isValid && input.value) {
        input.classList.add('border-red-500');
        showError(input, 'Please enter a valid phone number');
    } else {
        input.classList.remove('border-red-500');
        hideError(input);
    }
}

function showPasswordStrength(passwordInput) {
    const strength = calculatePasswordStrength(passwordInput.value);
    const strengthBar = passwordInput.parentNode.querySelector('.password-strength');
    
    if (strengthBar) {
        strengthBar.className = `password-strength ${getStrengthClass(strength)}`;
        strengthBar.style.width = `${strength * 25}%`;
    }
}

function calculatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    return Math.min(strength, 4);
}

function getStrengthClass(strength) {
    switch(strength) {
        case 0: return 'bg-red-500';
        case 1: return 'bg-orange-500';
        case 2: return 'bg-yellow-500';
        case 3: return 'bg-green-500';
        case 4: return 'bg-green-600';
        default: return 'bg-gray-500';
    }
}

function showError(input, message) {
    let errorElement = input.parentNode.querySelector('.error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message text-red-400 text-sm mt-1';
        input.parentNode.appendChild(errorElement);
    }
    errorElement.textContent = message;
}

function hideError(input) {
    const errorElement = input.parentNode.querySelector('.error-message');
    if (errorElement) {
        errorElement.remove();
    }
}

// Interactive features
function initInteractiveFeatures() {
    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = document.querySelector(this.dataset.target);
            const icon = this.querySelector('svg');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.innerHTML = `
                    <path d="M3.5 6.5L10 13L16.5 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M2.06135 10.4476C2.01946 10.2944 2 10.147 2 10C2 6.13401 4.68629 3 8 3C9.85883 3 11.459 3.8375 12.5797 5.20117M18.0614 10.4476C18.0195 10.2944 18 10.147 18 10C18 6.13401 15.3137 3 12 3C10.1412 3 8.54095 3.8375 7.42031 5.20117" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M13 10C13 12.2091 11.2091 14 9 14C6.79086 14 5 12.2091 5 10C5 7.79086 6.79086 6 9 6C11.2091 6 13 7.79086 13 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            } else {
                passwordInput.type = 'password';
                icon.innerHTML = `
                    <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M1 1l22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                `;
            }
        });
    });

    // Tooltip functionality
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip absolute bg-gray-900 text-white px-2 py-1 rounded text-sm z-50';
            tooltip.textContent = this.dataset.tooltip;
            
            // Position tooltip
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - 30) + 'px';
            
            document.body.appendChild(tooltip);
            
            this.tooltipElement = tooltip;
        });

        element.addEventListener('mouseleave', function() {
            if (this.tooltipElement) {
                this.tooltipElement.remove();
                this.tooltipElement = null;
            }
        });
    });

    // Counter animations for stats
    initCounterAnimations();
}

function initCounterAnimations() {
    const observerOptions = {
        threshold: 0.5
    };

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const targetValue = parseInt(counter.dataset.countTo);
                animateCounter(counter, targetValue);
                counterObserver.unobserve(counter);
            }
        });
    }, observerOptions);

    document.querySelectorAll('[data-count-to]').forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element, targetValue) {
    const duration = 2000;
    const frameDuration = 1000 / 60;
    const totalFrames = duration / frameDuration;
    let currentFrame = 0;
    let currentValue = 0;

    const increment = targetValue / totalFrames;

    function update() {
        if (currentFrame < totalFrames) {
            currentValue += increment;
            element.textContent = Math.ceil(currentValue);
            currentFrame++;
            requestAnimationFrame(update);
        } else {
            element.textContent = targetValue;
        }
    }

    update();
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add scroll event listeners with debouncing
const debouncedScrollHandler = debounce(() => {
    // Update any scroll-dependent UI elements
    updateScrollIndicator();
}, 10);

window.addEventListener('scroll', debouncedScrollHandler);

function updateScrollIndicator() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.style.width = scrolled + '%';
    }
}

// Export functions for use in other modules
window.BloodDonationApp = {
    initSmoothScrolling,
    initAnimatedElements,
    initDynamicColors,
    initParallaxEffects,
    initFormValidations,
    validateEmail,
    validatePhoneNumber,
    showPasswordStrength
};