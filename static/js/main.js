// ============================
// ARTICLEHUB MAIN JAVASCRIPT
// ============================

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ============ AUTO-HIDE FLASH MESSAGES ============
    // Automatically hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Create Bootstrap alert instance and close it
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5000 milliseconds = 5 seconds
    });

    
    // ============ SCROLL TO TOP BUTTON ============
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    
    if (scrollTopBtn) {
        // Show button when user scrolls down 100px
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 100) {
                scrollTopBtn.style.display = 'block';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        });
        
        // Scroll to top when button is clicked
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    
    // ============ CHARACTER COUNTER FOR POST CONTENT ============
    const postContent = document.getElementById('postContent');
    const charCount = document.getElementById('charCount');
    
    if (postContent && charCount) {
        // Update character count on page load
        charCount.textContent = postContent.value.length;
        
        // Update character count as user types
        postContent.addEventListener('input', function() {
            const currentLength = postContent.value.length;
            charCount.textContent = currentLength;
            
            // Change color based on character count
            if (currentLength < 20) {
                charCount.style.color = '#dc3545'; // Red for too short
            } else if (currentLength < 50) {
                charCount.style.color = '#ffc107'; // Yellow for okay
            } else {
                charCount.style.color = '#198754'; // Green for good
            }
        });
    }

    
    // ============ FORM VALIDATION ============
    const postForm = document.getElementById('postForm');
    
    if (postForm) {
        postForm.addEventListener('submit', function(event) {
            const title = document.querySelector('input[name="title"]');
            const content = document.querySelector('textarea[name="content"]');
            const category = document.querySelector('select[name="category"]');
            
            let isValid = true;
            let errorMessage = '';
            
            // Validate title
            if (title && title.value.trim().length < 5) {
                isValid = false;
                errorMessage += 'Title must be at least 5 characters long.\n';
                title.classList.add('is-invalid');
            } else if (title) {
                title.classList.remove('is-invalid');
            }
            
            // Validate content
            if (content && content.value.trim().length < 20) {
                isValid = false;
                errorMessage += 'Content must be at least 20 characters long.\n';
                content.classList.add('is-invalid');
            } else if (content) {
                content.classList.remove('is-invalid');
            }
            
            // Validate category
            if (category && !category.value) {
                isValid = false;
                errorMessage += 'Please select a category.\n';
                category.classList.add('is-invalid');
            } else if (category) {
                category.classList.remove('is-invalid');
            }
            
            // If validation fails, prevent form submission
            if (!isValid) {
                event.preventDefault();
                alert(errorMessage);
                return false;
            }
        });
    }

    
    // ============ CONFIRM DELETE ACTIONS ============
    // Add confirmation to all delete forms
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const confirmed = confirm('Are you sure you want to delete this? This action cannot be undone.');
            if (!confirmed) {
                event.preventDefault();
                return false;
            }
        });
    });

    
    // ============ REAL-TIME EMAIL VALIDATION ============
    const emailInputs = document.querySelectorAll('input[type="email"]');
    
    emailInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (input.value && !emailPattern.test(input.value)) {
                input.classList.add('is-invalid');
                
                // Add error message if not exists
                if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('invalid-feedback')) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.textContent = 'Please enter a valid email address.';
                    input.parentNode.appendChild(errorDiv);
                }
            } else {
                input.classList.remove('is-invalid');
            }
        });
    });

    
    // ============ PASSWORD STRENGTH INDICATOR ============
    const passwordInput = document.querySelector('input[name="password"]');
    
    if (passwordInput && passwordInput.form.querySelector('input[name="confirm_password"]')) {
        passwordInput.addEventListener('input', function() {
            const password = passwordInput.value;
            const strength = calculatePasswordStrength(password);
            
            // Remove existing strength indicator
            const existingIndicator = passwordInput.parentNode.querySelector('.password-strength');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            // Add new strength indicator
            if (password.length > 0) {
                const strengthDiv = document.createElement('div');
                strengthDiv.className = 'password-strength mt-1';
                
                let strengthText = '';
                let strengthColor = '';
                
                if (strength < 3) {
                    strengthText = 'Weak password';
                    strengthColor = 'text-danger';
                } else if (strength < 5) {
                    strengthText = 'Medium password';
                    strengthColor = 'text-warning';
                } else {
                    strengthText = 'Strong password';
                    strengthColor = 'text-success';
                }
                
                strengthDiv.innerHTML = `<small class="${strengthColor}">${strengthText}</small>`;
                passwordInput.parentNode.appendChild(strengthDiv);
            }
        });
    }

    
    // ============ SMOOTH SCROLL FOR ANCHOR LINKS ============
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            const href = link.getAttribute('href');
            
            // Only handle if href is not just "#"
            if (href !== '#' && href.length > 1) {
                event.preventDefault();
                
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    
    // ============ NAVBAR ACTIVE LINK HIGHLIGHTING ============
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(function(link) {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentLocation) {
            link.classList.add('active');
        }
    });

});


// ============ HELPER FUNCTIONS ============

/**
 * Calculate password strength
 * Returns a score from 0-6 based on password characteristics
 */
function calculatePasswordStrength(password) {
    let strength = 0;
    
    // Check length
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    
    // Check for lowercase
    if (/[a-z]/.test(password)) strength++;
    
    // Check for uppercase
    if (/[A-Z]/.test(password)) strength++;
    
    // Check for numbers
    if (/[0-9]/.test(password)) strength++;
    
    // Check for special characters
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    return strength;
}


/**
 * Format date to readable string
 */
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}


/**
 * Truncate text to specified length
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength) + '...';
}


/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}


/**
 * Show loading spinner
 */
function showLoading(element) {
    if (element) {
        element.classList.add('loading');
        element.disabled = true;
    }
}


/**
 * Hide loading spinner
 */
function hideLoading(element) {
    if (element) {
        element.classList.remove('loading');
        element.disabled = false;
    }
}


// ============ CONSOLE MESSAGE ============
console.log('%cArticleHub Blog Platform', 'color: #0d6efd; font-size: 20px; font-weight: bold;');
console.log('%cBuilt with Flask, Bootstrap & JavaScript', 'color: #6c757d; font-size: 12px;');
console.log('%cWeb Technology (BIT233) Project', 'color: #198754; font-size: 12px;');