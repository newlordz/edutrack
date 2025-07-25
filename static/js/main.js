// Main JavaScript for EduLearn

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Animate progress bars when they come into view
    const progressBars = document.querySelectorAll('.progress-bar');
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    };

    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const targetWidth = progressBar.style.width;
                progressBar.style.width = '0%';
                setTimeout(function() {
                    progressBar.style.width = targetWidth;
                }, 100);
            }
        });
    }, observerOptions);

    progressBars.forEach(function(bar) {
        progressObserver.observe(bar);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('fade-in');
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
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

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                
                // Re-enable button after 3 seconds in case of errors
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Submit';
                }, 3000);
            }
        });
    });

    // Store original button text
    document.querySelectorAll('button[type="submit"]').forEach(function(btn) {
        btn.setAttribute('data-original-text', btn.innerHTML);
    });

    // Course search functionality
    const searchForm = document.querySelector('form[method="GET"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            // Add search icon animation
            searchInput.addEventListener('focus', function() {
                const icon = searchForm.querySelector('.fa-search');
                if (icon) {
                    icon.classList.add('text-primary');
                }
            });

            searchInput.addEventListener('blur', function() {
                const icon = searchForm.querySelector('.fa-search');
                if (icon) {
                    icon.classList.remove('text-primary');
                }
            });
        }
    }

    // Dashboard stats counter animation
    const statNumbers = document.querySelectorAll('.card-body h3, .card-body h4');
    statNumbers.forEach(function(stat) {
        const finalNumber = parseInt(stat.textContent);
        if (!isNaN(finalNumber) && finalNumber > 0) {
            animateCounter(stat, 0, finalNumber, 1000);
        }
    });

    function animateCounter(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const currentNumber = Math.floor(progress * (end - start) + start);
            element.textContent = currentNumber;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Add loading state to enrollment buttons
    const enrollButtons = document.querySelectorAll('a[href*="/enroll/"]');
    enrollButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enrolling...';
            btn.classList.add('disabled');
        });
    });

    // Grade table enhancements
    const gradeTables = document.querySelectorAll('.table');
    gradeTables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row, index) {
            row.style.animationDelay = (index * 0.05) + 's';
            row.classList.add('fade-in');
        });
    });

    // Course card hover effects
    const courseCards = document.querySelectorAll('.card');
    courseCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Mobile menu enhancements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            setTimeout(function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.style.maxHeight = navbarCollapse.scrollHeight + 'px';
                } else {
                    navbarCollapse.style.maxHeight = '0px';
                }
            }, 50);
        });
    }

    // Console welcome message
    console.log('%cWelcome to EduLearn! 🎓', 'color: #0d6efd; font-size: 18px; font-weight: bold;');
    console.log('%cBuilt with Flask, Bootstrap, and lots of ❤️', 'color: #6c757d; font-size: 14px;');
});

// Utility functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(function() {
        alertDiv.remove();
    }, 5000);
}

// Export for global use
window.EduLearn = {
    showNotification: showNotification
};
