// Modern EduTrack JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts with beautiful animation (EXCEPT on study material pages)
    if (!window.location.pathname.includes('/study/')) {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            setTimeout(function() {
                alert.style.transition = 'all 0.5s ease';
                alert.style.transform = 'translateX(100%)';
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 500);
            }, 5000);
        });
    } else {
        console.log('Study material page detected - alert auto-removal disabled');
    }

    // Animate progress bars with intersection observer
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

    // Add staggered fade-in animation to cards
    const cards = document.querySelectorAll('.card, .course-card, .stats-card');
    cards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        
        setTimeout(function() {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
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

    // Enhanced form validation with visual feedback
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

    // Enhanced search functionality
    const searchForm = document.querySelector('form[method="GET"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            // Add search icon animation
            searchInput.addEventListener('focus', function() {
                const icon = searchForm.querySelector('.fa-search');
                if (icon) {
                    icon.style.transform = 'scale(1.2)';
                    icon.style.color = '#667eea';
                }
            });

            searchInput.addEventListener('blur', function() {
                const icon = searchForm.querySelector('.fa-search');
                if (icon) {
                    icon.style.transform = 'scale(1)';
                    icon.style.color = '';
                }
            });
        }
    }

    // Animated counter for stats
    const statNumbers = document.querySelectorAll('.stats-number');
    statNumbers.forEach(function(stat) {
        const finalNumber = parseInt(stat.textContent);
        if (!isNaN(finalNumber) && finalNumber > 0) {
            animateCounter(stat, 0, finalNumber, 2000);
        }
    });

    function animateCounter(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const currentNumber = Math.floor(progress * (end - start) + start);
            element.textContent = currentNumber + (element.textContent.includes('+') ? '+' : '') + (element.textContent.includes('%') ? '%' : '');
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Enhanced enrollment buttons
    const enrollButtons = document.querySelectorAll('a[href*="/enroll/"]');
    enrollButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enrolling...';
            btn.classList.add('disabled');
        });
    });

    // Beautiful grade table animations
    const gradeTables = document.querySelectorAll('.table');
    gradeTables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row, index) {
            row.style.opacity = '0';
            row.style.transform = 'translateX(-20px)';
            row.style.transition = 'all 0.4s ease';
            
            setTimeout(function() {
                row.style.opacity = '1';
                row.style.transform = 'translateX(0)';
            }, index * 50);
        });
    });

    // Enhanced course card hover effects
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-12px) scale(1.02)';
            this.style.boxShadow = '0 20px 60px rgba(0, 0, 0, 0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.1)';
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

    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }

    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            if (!this.classList.contains('disabled')) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });

    // Smooth reveal animations for sections
    const sections = document.querySelectorAll('section');
    const sectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    sections.forEach(function(section) {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'all 0.8s ease';
        sectionObserver.observe(section);
    });

    // Console welcome message
    console.log('%cWelcome to EduTrack! 🎓', 'color: #667eea; font-size: 18px; font-weight: bold;');
    console.log('%cBuilt with modern web technologies and lots of ❤️', 'color: #718096; font-size: 14px;');
});

// Utility functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; transform: translateX(100%); transition: all 0.3s ease;';
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : type === 'danger' ? 'times-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Animate in
    setTimeout(() => {
        alertDiv.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(function() {
        alertDiv.style.transform = 'translateX(100%)';
        setTimeout(() => {
            alertDiv.remove();
        }, 300);
    }, 5000);
}

// Enhanced Chatbot Functionality
class EduTrackChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.typingTimeout = null;
        this.conversationContext = {
            userRole: null,
            currentTopic: null,
            lastQuestion: null,
            sessionStart: new Date()
        };
        this.knowledgeBase = this.initializeKnowledgeBase();
        this.init();
    }

    init() {
        this.createChatbotHTML();
        this.bindEvents();
        this.addWelcomeMessage();
        this.startPulseAnimation();
    }

    initializeKnowledgeBase() {
        return {
            greetings: {
                patterns: ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'sup', 'yo'],
                responses: [
                    "Hello! 👋 I'm your EduTrack assistant. I can help you with:\n\n📚 **Courses** - Browse our 20+ courses\n📊 **Grades** - Check your progress\n💡 **Study Tips** - Get learning advice\n🎯 **Learning Support** - Overcome challenges\n\nWhat would you like to explore today?",
                    "Hi there! 🎓 Welcome to EduTrack. Here are some popular topics:\n\n• How many courses do we offer?\n• What courses are available?\n• How to check my grades?\n• Get study tips\n• Help with learning\n\nWhat interests you most?",
                    "Hey! I'm here to help you succeed! 🚀\n\nQuick options:\n📖 Browse courses\n📈 Check grades\n💡 Get study tips\n❓ Ask for help\n\nWhat can I assist you with today?"
                ]
            },
            courses: {
                patterns: ['course', 'courses', 'class', 'classes', 'subject', 'subjects', 'enroll', 'enrollment', 'how many', 'available', 'catalog', 'curriculum', 'syllabus'],
                responses: [
                    "We currently have **20 courses** available across different skill levels and technologies! Here's what we offer:\n\n📚 **Programming & Development (8 courses):**\n• Python Programming, Flask Web Development, JavaScript, React Native\n• Database Design, DevOps, Blockchain, Web Security\n\n🎯 **Data & AI (4 courses):**\n• Data Science, Machine Learning, AI Basics, Data Visualization\n\n💻 **Design & Marketing (3 courses):**\n• UI/UX Design, Digital Marketing, Content Creation\n\n🛠️ **Specialized Skills (5 courses):**\n• Cybersecurity, Cloud Computing, Project Management, Mobile Games, E-commerce\n\nWould you like me to tell you more about any specific course?",
                    
                    "We offer **20 comprehensive courses**! Here's the breakdown:\n\n🎓 **By Difficulty Level:**\n• Beginner: 4 courses (Python, Database, UI/UX, Digital Marketing, Content Creation)\n• Intermediate: 11 courses (Flask, Data Science, JavaScript, React Native, etc.)\n• Advanced: 5 courses (Advanced JavaScript, Machine Learning, AI, DevOps, Blockchain)\n\n⏱️ **By Duration:**\n• 6-8 weeks: 6 courses\n• 10-12 weeks: 10 courses\n• 14-16 weeks: 4 courses\n\nWhich category interests you most?",
                    
                    "**20 courses** are available in our catalog! Here are some highlights:\n\n🔥 **Most Popular:**\n• Introduction to Python Programming\n• Web Development with Flask\n• Data Science Fundamentals\n• UI/UX Design Principles\n\n🆕 **Latest Additions:**\n• Blockchain Development\n• Artificial Intelligence Basics\n• Mobile Game Development\n• E-commerce Development\n\nWhat type of course are you looking for?"
                ]
            },
            grades: {
                patterns: ['grade', 'grades', 'score', 'scores', 'performance', 'progress', 'result', 'results', 'gpa', 'average', 'marks', 'assessment'],
                responses: [
                    "I can help you check your grades and track your progress! You can view your grades in the Grades section of your dashboard.",
                    "To see your grades, go to the Grades page in your dashboard. Would you like me to explain how the grading system works?",
                    "Your grades reflect your learning progress. Are you having trouble with a specific subject or assignment?"
                ]
            },
            help: {
                patterns: ['help', 'support', 'assist', 'problem', 'issue', 'trouble', 'difficult', 'stuck', 'confused', 'need help'],
                responses: [
                    "I'm here to help! What specific issue are you facing? I can assist with course navigation, technical problems, or learning questions.",
                    "Don't worry, I can help you resolve this. Can you describe the problem you're experiencing?",
                    "I'm your learning assistant. Let me know what you need help with, and I'll guide you through it."
                ]
            },
            technical: {
                patterns: ['login', 'password', 'account', 'profile', 'settings', 'logout', 'register', 'sign up', 'sign in', 'reset password', 'forgot password'],
                responses: [
                    "For account-related issues, you can use the login/register buttons in the navigation. Need help with a specific account feature?",
                    "Account management is handled through the main interface. What specific account issue are you experiencing?",
                    "I can guide you through account features. Are you having trouble logging in or managing your profile?"
                ]
            },
            learning: {
                patterns: ['learn', 'study', 'practice', 'understand', 'confused', 'difficult', 'hard', 'challenging', 'complex', 'complicated', 'don\'t understand'],
                responses: [
                    "Learning can be challenging, but I'm here to support you! What specific concept are you finding difficult?",
                    "Don't worry about getting stuck - it's part of the learning process. What topic are you working on?",
                    "I can help you break down complex topics. What subject or concept would you like to understand better?"
                ]
            },
            motivation: {
                patterns: ['motivation', 'motivated', 'tired', 'bored', 'give up', 'quit', 'difficult', 'overwhelmed', 'stress', 'anxiety', 'frustrated', 'discouraged'],
                responses: [
                    "Remember, every expert was once a beginner! Take it one step at a time. What's your current learning goal?",
                    "You've got this! Learning is a journey, not a race. What small win can you celebrate today?",
                    "It's normal to feel overwhelmed sometimes. Let's break down what you're working on into smaller, manageable steps."
                ]
            },
            features: {
                patterns: ['feature', 'features', 'what can you do', 'capabilities', 'functions', 'abilities', 'skills'],
                responses: [
                    "I can help you with course information, grades, learning support, technical issues, and general guidance. What would you like to know more about?",
                    "My capabilities include answering questions about courses, helping with learning challenges, providing motivation, and guiding you through the platform. How can I assist you?",
                    "I'm your learning companion! I can help with course selection, study tips, progress tracking, and overcoming learning obstacles."
                ]
            },
            schedule: {
                patterns: ['schedule', 'time', 'when', 'duration', 'how long', 'deadline', 'due date', 'timeline'],
                responses: [
                    "Course schedules vary by program. Most courses run for 8-16 weeks. Would you like to know about a specific course's schedule?",
                    "Course durations range from 6 to 16 weeks. What type of schedule are you looking for?",
                    "I can help you find courses that fit your timeline. Are you looking for short-term or long-term programs?"
                ]
            },
            instructors: {
                patterns: ['instructor', 'teacher', 'professor', 'tutor', 'mentor', 'who teaches', 'faculty'],
                responses: [
                    "Our instructors are industry experts with years of experience. Would you like to know about a specific course's instructor?",
                    "We have experienced instructors for each course. What subject area are you interested in?",
                    "Our teaching team includes professionals from various industries. Which course would you like to learn more about?"
                ]
            },
            career: {
                patterns: ['career', 'job', 'employment', 'work', 'profession', 'salary', 'income', 'opportunities', 'future'],
                responses: [
                    "Our courses are designed to prepare you for real-world careers! What field are you interested in?",
                    "Many of our graduates find great opportunities in tech, data, design, and marketing. What career path interests you?",
                    "I can help you understand career opportunities in different fields. What industry are you considering?"
                ]
            },
            pricing: {
                patterns: ['price', 'cost', 'fee', 'payment', 'money', 'expensive', 'cheap', 'affordable', 'budget'],
                responses: [
                    "Course pricing varies by program and duration. Would you like to know about specific course costs?",
                    "We offer various pricing options to fit different budgets. What type of course are you interested in?",
                    "I can help you find courses within your budget. What price range are you considering?"
                ]
            },
            platform: {
                patterns: ['platform', 'website', 'app', 'mobile', 'desktop', 'online', 'offline', 'access'],
                responses: [
                    "EduTrack is accessible on web browsers and mobile devices. You can learn anywhere, anytime!",
                    "Our platform works on computers, tablets, and phones. Do you have a preferred device?",
                    "You can access your courses from any device with internet. What's your preferred learning environment?"
                ]
            },
            community: {
                patterns: ['community', 'students', 'peers', 'network', 'discussion', 'forum', 'group', 'collaborate'],
                responses: [
                    "You'll be part of a vibrant learning community! Connect with peers, share experiences, and collaborate on projects.",
                    "Our platform includes discussion forums and group projects. Would you like to know more about community features?",
                    "Learning is better together! You can interact with other students and instructors through our community features."
                ]
            },
            certificates: {
                patterns: ['certificate', 'certification', 'diploma', 'degree', 'accreditation', 'recognition'],
                responses: [
                    "Complete courses to earn certificates that showcase your skills to employers!",
                    "Our certificates are recognized by industry professionals. What certification are you interested in?",
                    "Earn valuable credentials that can boost your career prospects. Which course would you like to get certified in?"
                ]
            },
            feedback: {
                patterns: ['feedback', 'review', 'rating', 'testimonial', 'opinion', 'experience', 'satisfaction'],
                responses: [
                    "We value your feedback! You can rate courses and share your learning experience.",
                    "Student feedback helps us improve our courses. Would you like to share your thoughts?",
                    "Your opinion matters! We use feedback to enhance the learning experience for everyone."
                ]
            }
        };
    }

    createChatbotHTML() {
        const chatbotHTML = `
            <div class="chatbot-container">
                <button class="chatbot-fab" id="chatbotFab" title="Chat with EduTrack Assistant">
                    <i class="fas fa-comments"></i>
                    <div class="chatbot-notification" id="chatbotNotification" style="display: none;">3</div>
                </button>
            </div>
            
            <div class="chatbot-modal" id="chatbotModal">
                <div class="chatbot-content">
                    <div class="chatbot-header">
                        <h5>EduTrack Assistant</h5>
                        <div class="status">
                            <div class="status-dot"></div>
                            Online
                        </div>
                        <button class="chatbot-close" id="chatbotClose">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="chatbot-body">
                        <div class="chat-messages" id="chatMessages"></div>
                        <div class="quick-actions" id="quickActions" style="display: none;">
                            <div class="quick-actions-title">Quick Actions:</div>
                            <div class="quick-actions-buttons">
                                <button class="quick-action-btn" data-action="courses">
                                    <i class="fas fa-book"></i> Browse Courses
                                </button>
                                <button class="quick-action-btn" data-action="grades">
                                    <i class="fas fa-chart-line"></i> Check Grades
                                </button>
                                <button class="quick-action-btn" data-action="help">
                                    <i class="fas fa-question-circle"></i> Get Help
                                </button>
                                <button class="quick-action-btn" data-action="tips">
                                    <i class="fas fa-lightbulb"></i> Study Tips
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="chat-input">
                        <input type="text" id="chatInput" placeholder="Ask me anything about learning..." maxlength="500">
                        <button id="chatSend">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    bindEvents() {
        const fab = document.getElementById('chatbotFab');
        const modal = document.getElementById('chatbotModal');
        const close = document.getElementById('chatbotClose');
        const input = document.getElementById('chatInput');
        const send = document.getElementById('chatSend');

        fab.addEventListener('click', () => this.toggleChat());
        close.addEventListener('click', () => this.closeChat());
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.closeChat();
        });

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        send.addEventListener('click', () => this.sendMessage());

        // Add hover effects
        fab.addEventListener('mouseenter', () => {
            fab.style.transform = 'translateY(-8px) scale(1.1)';
        });

        fab.addEventListener('mouseleave', () => {
            fab.style.transform = 'translateY(0) scale(1)';
        });

        // Quick action buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-action-btn')) {
                const action = e.target.getAttribute('data-action');
                this.handleQuickAction(action);
            }
        });


    }

    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    openChat() {
        const modal = document.getElementById('chatbotModal');
        const fab = document.getElementById('chatbotFab');
        const notification = document.getElementById('chatbotNotification');

        this.isOpen = true;
        modal.style.display = 'flex';
        
        // Trigger animations
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);

        // Hide notification when opened
        notification.style.display = 'none';
        fab.classList.remove('pulse');



        // Focus input
        setTimeout(() => {
            document.getElementById('chatInput').focus();
        }, 300);

        // Scroll to bottom
        this.scrollToBottom();
    }

    closeChat() {
        const modal = document.getElementById('chatbotModal');
        this.isOpen = false;
        modal.classList.remove('show');
        
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }

    addWelcomeMessage() {
        const welcomeMessage = {
            type: 'bot',
            content: 'Hello! 👋 I\'m your EduTrack assistant. I can help you with courses, grades, learning support, and more. What would you like to know?',
            time: new Date()
        };
        this.addMessage(welcomeMessage);
    }

    sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;

        // Add user message
        const userMessage = {
            type: 'user',
            content: message,
            time: new Date()
        };
        this.addMessage(userMessage);

        // Clear input
        input.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        // Process message and generate intelligent response
        setTimeout(() => {
            this.hideTypingIndicator();
            const response = this.processMessage(message);
            this.addMessage({
                type: 'bot',
                content: response,
                time: new Date()
            });
        }, 1000 + Math.random() * 1500);
    }

    processMessage(message) {
        const lowerMessage = message.toLowerCase();
        
        // Update conversation context
        this.conversationContext.lastQuestion = lowerMessage;
        
        // Check for questions about the chatbot itself
        if (lowerMessage.includes('who are you') || lowerMessage.includes('what are you') || lowerMessage.includes('your name') || lowerMessage.includes('what is your name')) {
            return "I'm the EduTrack Assistant! 🤖 I'm an AI-powered chatbot designed to help you navigate your learning journey. I can answer questions about courses, grades, study tips, and provide support whenever you need it. Think of me as your personal learning companion!";
        }
        
        // Check for gratitude expressions
        if (lowerMessage.includes('thank') || lowerMessage.includes('thanks') || lowerMessage.includes('appreciate') || lowerMessage.includes('grateful')) {
            return "You're very welcome! 😊 I'm here to help make your learning journey easier and more enjoyable. Is there anything else you'd like to know or explore?";
        }
        
        // Check for goodbye/farewell
        if (lowerMessage.includes('bye') || lowerMessage.includes('goodbye') || lowerMessage.includes('see you') || lowerMessage.includes('later') || lowerMessage.includes('farewell')) {
            return "Goodbye! 👋 It was great chatting with you. Remember, I'm always here when you need help with your learning journey. Good luck with your studies! 🎓";
        }
        
        // Check for compliments
        if (lowerMessage.includes('good') || lowerMessage.includes('great') || lowerMessage.includes('awesome') || lowerMessage.includes('amazing') || lowerMessage.includes('excellent') || lowerMessage.includes('wonderful')) {
            return "Thank you! 😊 I'm glad I could help. Is there anything specific you'd like to explore or learn more about?";
        }
        
        // Check for confusion or unclear messages
        if ((lowerMessage.includes('what') && lowerMessage.includes('mean')) || lowerMessage.includes('confused') || lowerMessage.includes('unclear') || lowerMessage.includes('don\'t understand')) {
            return "I understand that might be confusing! Let me try to help clarify. Could you rephrase your question or tell me what specific topic you'd like to learn about? I'm here to make things clearer for you!";
        }
        
        // Check for urgency or immediate help needed
        if (lowerMessage.includes('urgent') || lowerMessage.includes('emergency') || lowerMessage.includes('asap') || lowerMessage.includes('quick') || lowerMessage.includes('immediately')) {
            return "I understand you need help quickly! 🚨 What specific issue are you facing? I'll do my best to provide immediate assistance. You can also use the Quick Actions buttons for faster access to common features.";
        }
        
        // Check for "how many" questions specifically
        if (lowerMessage.includes('how many') && (lowerMessage.includes('course') || lowerMessage.includes('available'))) {
            this.conversationContext.currentTopic = 'course_count';
            return "We currently have **20 courses** available in our catalog! Here's the breakdown:\n\n📊 **Course Statistics:**\n• Total Courses: 20\n• Beginner Level: 4 courses\n• Intermediate Level: 11 courses\n• Advanced Level: 5 courses\n\n📚 **Categories:**\n• Programming & Development: 8 courses\n• Data & AI: 4 courses\n• Design & Marketing: 3 courses\n• Specialized Skills: 5 courses\n\nWould you like me to show you the complete course list or tell you about specific courses?";
        }
        
        // Handle follow-up responses based on context
        if (this.conversationContext.currentTopic === 'course_count' && 
            (lowerMessage.includes('yes') || lowerMessage.includes('show') || lowerMessage.includes('complete') || lowerMessage.includes('list') || lowerMessage.includes('sure'))) {
            this.conversationContext.currentTopic = 'courses';
            return this.getCompleteCourseList();
        }
        
        // Handle specific course inquiries
        const courseInfo = this.getSpecificCourseInfo(lowerMessage);
        if (courseInfo) {
            this.conversationContext.currentTopic = 'specific_course';
            return courseInfo;
        }
        
        // Check for compound questions (multiple topics)
        const topics = [];
        for (const [category, data] of Object.entries(this.knowledgeBase)) {
            for (const pattern of data.patterns) {
                if (lowerMessage.includes(pattern)) {
                    topics.push(category);
                }
            }
        }
        
        if (topics.length > 1) {
            return `I see you're asking about multiple topics! Let me help you with each one:\n\n${topics.map(topic => `• **${topic.charAt(0).toUpperCase() + topic.slice(1)}** - ${this.getContextualResponse(topic, lowerMessage).split('\n')[0]}`).join('\n')}\n\nWhich topic would you like to explore first?`;
        }
        
        // Check for specific patterns and generate contextual responses with improved matching
        let bestMatch = null;
        let bestScore = 0;
        
        for (const [category, data] of Object.entries(this.knowledgeBase)) {
            for (const pattern of data.patterns) {
                if (lowerMessage.includes(pattern)) {
                    // Calculate match score based on pattern length and position
                    const score = pattern.length + (lowerMessage.indexOf(pattern) === 0 ? 10 : 0);
                    if (score > bestScore) {
                        bestScore = score;
                        bestMatch = category;
                    }
                }
            }
        }
        
        if (bestMatch) {
            this.conversationContext.currentTopic = bestMatch;
            return this.getContextualResponse(bestMatch, lowerMessage);
        }

        // If no specific pattern matches, provide a helpful general response
        return this.getGeneralResponse(lowerMessage);
    }

    getContextualResponse(category, message) {
        const responses = this.knowledgeBase[category].responses;
        let response = responses[Math.floor(Math.random() * responses.length)];

        // Add follow-up questions based on context
        if (category === 'courses') {
            response += "\n\nWould you like me to suggest some courses based on your interests?";
        } else if (category === 'grades') {
            response += "\n\nIs there a specific subject you'd like to improve in?";
        } else if (category === 'learning') {
            response += "\n\nWhat learning style works best for you?";
        }

        // Show quick actions for certain categories
        setTimeout(() => {
            this.showQuickActions(category);
        }, 500);

        return response;
    }

    showQuickActions(category) {
        const quickActions = document.getElementById('quickActions');
        if (category === 'courses' || category === 'grades' || category === 'help' || category === 'learning' || category === 'motivation') {
            quickActions.style.display = 'block';
            // Don't auto-scroll, let user control the view
        }
    }

    getGeneralResponse(message) {
        // Check if we have context from previous conversation
        if (this.conversationContext.currentTopic === 'course_count') {
            return "I'd be happy to show you the complete course list! Here are all 20 courses we offer:\n\n" + this.getCompleteCourseList();
        }
        
        // Check for vague responses like "anything", "whatever", "idk", etc.
        const vagueWords = ['anything', 'whatever', 'idk', 'i don\'t know', 'not sure', 'maybe', 'whatever'];
        const messageLower = message.toLowerCase();
        
        for (let word of vagueWords) {
            if (messageLower.includes(word)) {
                return `I'd be happy to help you explore! Here are some popular topics:\n\n📚 **Courses** - Browse our 20+ courses\n📊 **Grades** - Check your progress\n💡 **Study Tips** - Get learning advice\n🎯 **Learning Paths** - Find your direction\n\nWhat interests you most? Or you can ask me about:\n• Specific courses (like "Python" or "Data Science")\n• Your current grades\n• Study strategies\n• Learning goals`;
            }
        }
        
        // If someone mentioned a course but we don't have specific info, offer to help
        if (message.includes('course') || message.includes('class')) {
            return "I'd be happy to tell you more about that course! Could you please specify which course you're interested in? I can provide details about instructors, duration, difficulty level, and what you'll learn.";
        }
        
        const generalResponses = [
            "That's an interesting question! I'm here to help with your learning journey. Could you tell me more about what you're working on?",
            "I'd love to help you with that! Are you looking for course information, learning support, or something else?",
            "Thanks for reaching out! I can assist with courses, grades, study tips, and technical support. What area would you like to explore?",
            "I'm here to support your educational goals! What specific aspect of learning would you like to discuss?",
            "That's a great topic! I can help you navigate your learning path. What would you like to know more about?"
        ];

        return generalResponses[Math.floor(Math.random() * generalResponses.length)];
    }

    handleQuickAction(action) {
        const quickActions = document.getElementById('quickActions');
        quickActions.style.display = 'none';

        let response = '';
        switch (action) {
            case 'courses':
                response = "We have **20 courses** available! Here's our complete catalog:\n\n📚 **Programming & Development:**\n• Introduction to Python Programming (Beginner, 8 weeks)\n• Web Development with Flask (Intermediate, 12 weeks)\n• Advanced JavaScript (Advanced, 8 weeks)\n• Database Design and SQL (Beginner, 6 weeks)\n• DevOps Fundamentals (Advanced, 10 weeks)\n• Blockchain Development (Advanced, 14 weeks)\n• Web Security (Advanced, 10 weeks)\n• E-commerce Development (Intermediate, 12 weeks)\n\n🎯 **Data & AI:**\n• Data Science Fundamentals (Intermediate, 10 weeks)\n• Machine Learning Basics (Advanced, 12 weeks)\n• Artificial Intelligence Basics (Advanced, 12 weeks)\n• Data Visualization (Intermediate, 8 weeks)\n\n💻 **Design & Marketing:**\n• UI/UX Design Principles (Beginner, 8 weeks)\n• Digital Marketing Strategy (Beginner, 8 weeks)\n• Content Creation (Beginner, 8 weeks)\n\n🛠️ **Specialized Skills:**\n• Cybersecurity Fundamentals (Intermediate, 10 weeks)\n• Cloud Computing with AWS (Intermediate, 12 weeks)\n• Project Management (Intermediate, 10 weeks)\n• Mobile App Development with React Native (Intermediate, 14 weeks)\n• Mobile Game Development (Intermediate, 16 weeks)\n• Network Administration (Intermediate, 10 weeks)\n\nWhich course interests you most?";
                break;
            case 'grades':
                response = "To check your grades:\n\n1️⃣ Go to your Dashboard\n2️⃣ Click on 'Grades' in the navigation\n3️⃣ View your performance across all courses\n\n📊 **Grade Categories:**\n• Assignments (40%)\n• Quizzes (25%)\n• Projects (25%)\n• Participation (10%)\n\nNeed help understanding your grades or improving performance?";
                break;
            case 'help':
                response = "I'm here to help! Here are common areas I can assist with:\n\n🔧 **Technical Issues:**\n• Login problems\n• Course access issues\n• Platform navigation\n\n📖 **Learning Support:**\n• Course explanations\n• Study strategies\n• Assignment help\n\n🎯 **Academic Guidance:**\n• Course selection\n• Progress tracking\n• Goal setting\n\nWhat specific help do you need?";
                break;
            case 'tips':
                response = this.getStudyTip();
                break;
        }

        this.addMessage({
            type: 'bot',
            content: response,
            time: new Date()
        });
    }

    getSpecificCourseInfo(message) {
        const courseDatabase = {
            'mobile game development': {
                title: "Mobile Game Development",
                instructor: "Ms. Lisa Rodriguez",
                duration: "16 weeks",
                difficulty: "Intermediate",
                description: "Create mobile games using Unity and C# programming language.",
                maxStudents: 20,
                highlights: [
                    "🎮 Learn Unity game engine fundamentals",
                    "💻 Master C# programming for games",
                    "📱 Develop for iOS and Android platforms",
                    "🎨 Create game mechanics and UI",
                    "🚀 Publish games to app stores"
                ],
                prerequisites: "Basic programming knowledge recommended",
                skills: "Unity, C#, Game Design, Mobile Development"
            },
            'python': {
                title: "Introduction to Python Programming",
                instructor: "Dr. Sarah Johnson",
                duration: "8 weeks",
                difficulty: "Beginner",
                description: "Learn the fundamentals of Python programming including variables, data types, control structures, and functions.",
                maxStudents: 30,
                highlights: [
                    "🐍 Master Python syntax and basics",
                    "📊 Work with data structures",
                    "🔧 Build practical applications",
                    "📚 Learn best practices",
                    "🎯 Complete hands-on projects"
                ],
                prerequisites: "No prior programming experience required",
                skills: "Python, Programming Fundamentals, Problem Solving"
            },
            'flask': {
                title: "Web Development with Flask",
                instructor: "Prof. Michael Chen",
                duration: "12 weeks",
                difficulty: "Intermediate",
                description: "Build dynamic web applications using Flask framework, HTML, CSS, and JavaScript.",
                maxStudents: 25,
                highlights: [
                    "🌐 Build full-stack web applications",
                    "🔧 Master Flask framework",
                    "🎨 Create responsive user interfaces",
                    "🗄️ Work with databases",
                    "🚀 Deploy applications online"
                ],
                prerequisites: "Basic Python knowledge required",
                skills: "Flask, HTML/CSS, JavaScript, Web Development"
            },
            'data science': {
                title: "Data Science Fundamentals",
                instructor: "Dr. Emily Rodriguez",
                duration: "10 weeks",
                difficulty: "Intermediate",
                description: "Introduction to data analysis, visualization, and machine learning concepts using Python.",
                maxStudents: 20,
                highlights: [
                    "📊 Learn data analysis techniques",
                    "📈 Master data visualization",
                    "🤖 Introduction to machine learning",
                    "🔍 Statistical analysis methods",
                    "📋 Real-world data projects"
                ],
                prerequisites: "Basic Python and statistics knowledge",
                skills: "Python, Pandas, Matplotlib, Statistics, Machine Learning"
            },
            'javascript': {
                title: "Advanced JavaScript",
                instructor: "Ms. Lisa Wang",
                duration: "8 weeks",
                difficulty: "Advanced",
                description: "Master advanced JavaScript concepts including ES6+, async programming, and modern frameworks.",
                maxStudents: 15,
                highlights: [
                    "⚡ Modern JavaScript (ES6+)",
                    "🔄 Async programming patterns",
                    "🏗️ Advanced frameworks",
                    "🛠️ Build tools and testing",
                    "🚀 Performance optimization"
                ],
                prerequisites: "Intermediate JavaScript knowledge required",
                skills: "JavaScript, ES6+, Async Programming, Modern Frameworks"
            }
        };

        // Check for course matches
        for (const [key, course] of Object.entries(courseDatabase)) {
            if (message.includes(key)) {
                return `🎮 **${course.title}**\n\n👨‍🏫 **Instructor:** ${course.instructor}\n⏱️ **Duration:** ${course.duration}\n📊 **Difficulty:** ${course.difficulty}\n👥 **Max Students:** ${course.maxStudents}\n\n📝 **Description:**\n${course.description}\n\n✨ **What You'll Learn:**\n${course.highlights.map(h => `• ${h}`).join('\n')}\n\n📋 **Prerequisites:** ${course.prerequisites}\n🎯 **Skills You'll Gain:** ${course.skills}\n\nWould you like to enroll in this course or learn about other courses?`;
            }
        }

        return null; // No specific course found
    }

    getCompleteCourseList() {
        return "Here's the **complete course list** with all 20 courses:\n\n📚 **Programming & Development (8 courses):**\n• Introduction to Python Programming (Beginner, 8 weeks)\n• Web Development with Flask (Intermediate, 12 weeks)\n• Advanced JavaScript (Advanced, 8 weeks)\n• Database Design and SQL (Beginner, 6 weeks)\n• DevOps Fundamentals (Advanced, 10 weeks)\n• Blockchain Development (Advanced, 14 weeks)\n• Web Security (Advanced, 10 weeks)\n• E-commerce Development (Intermediate, 12 weeks)\n\n🎯 **Data & AI (4 courses):**\n• Data Science Fundamentals (Intermediate, 10 weeks)\n• Machine Learning Basics (Advanced, 12 weeks)\n• Artificial Intelligence Basics (Advanced, 12 weeks)\n• Data Visualization (Intermediate, 8 weeks)\n\n💻 **Design & Marketing (3 courses):**\n• UI/UX Design Principles (Beginner, 8 weeks)\n• Digital Marketing Strategy (Beginner, 8 weeks)\n• Content Creation (Beginner, 8 weeks)\n\n🛠️ **Specialized Skills (5 courses):**\n• Cybersecurity Fundamentals (Intermediate, 10 weeks)\n• Cloud Computing with AWS (Intermediate, 12 weeks)\n• Project Management (Intermediate, 10 weeks)\n• Mobile App Development with React Native (Intermediate, 14 weeks)\n• Mobile Game Development (Intermediate, 16 weeks)\n• Network Administration (Intermediate, 10 weeks)\n\nWhich course would you like to learn more about?";
    }

    getStudyTip() {
        const studyTips = [
            "🎯 **Active Learning Tip:** Instead of just reading, try explaining concepts to yourself or others. This helps reinforce understanding!",
            
            "⏰ **Time Management:** Use the Pomodoro Technique - study for 25 minutes, then take a 5-minute break. It keeps your mind fresh!",
            
            "📝 **Note-Taking Strategy:** Use the Cornell Method - divide your page into sections for notes, key points, and summary. It's super effective!",
            
            "🧠 **Memory Technique:** Connect new information to things you already know. Creating associations makes learning stick better!",
            
            "🎵 **Environment Matters:** Find a quiet, comfortable study space. Good lighting and minimal distractions boost focus!",
            
            "📚 **Spaced Repetition:** Review material at increasing intervals (1 day, 3 days, 1 week). This strengthens long-term memory!",
            
            "💡 **Practice Makes Perfect:** Apply what you learn through projects and exercises. Hands-on practice is the best teacher!",
            
            "🎪 **Make it Fun:** Turn studying into a game or challenge. Learning is more effective when you're engaged and enjoying it!"
        ];

        return studyTips[Math.floor(Math.random() * studyTips.length)];
    }

    addMessage(message) {
        this.messages.push(message);
        this.renderMessage(message);
        // Scroll to bottom for both user and bot messages
        this.scrollToBottom();
    }

    renderMessage(message) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.type}-message`;

        const time = message.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        if (message.type === 'user') {
            messageDiv.innerHTML = `
                <div class="message-content">
                    ${this.escapeHtml(message.content)}
                </div>
                <div class="message-avatar">U</div>
                <div class="message-time">${time}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-avatar">A</div>
                <div class="message-content">
                    ${this.escapeHtml(message.content)}
                </div>
                <div class="message-time">${time}</div>
            `;
            
            // Add a subtle animation for bot messages to indicate new content
            messageDiv.style.opacity = '0';
            messageDiv.style.transform = 'translateY(10px)';
            setTimeout(() => {
                messageDiv.style.transition = 'all 0.3s ease';
                messageDiv.style.opacity = '1';
                messageDiv.style.transform = 'translateY(0)';
            }, 10);
        }

        messagesContainer.appendChild(messageDiv);
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator-container';
        typingDiv.id = 'typingIndicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">A</div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        messagesContainer.appendChild(typingDiv);
        // Don't auto-scroll, let user control the view
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }



    startPulseAnimation() {
        const fab = document.getElementById('chatbotFab');
        const notification = document.getElementById('chatbotNotification');
        
        // Show notification after 3 seconds
        setTimeout(() => {
            notification.style.display = 'flex';
            fab.classList.add('pulse');
        }, 3000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize existing functionality
    // ... existing code ...

    // Initialize chatbot
    setTimeout(() => {
        window.edutrackChatbot = new EduTrackChatbot();
    }, 100);
});

// Export for global use
window.EduTrack = {
    showNotification: showNotification,
    chatbot: window.edutrackChatbot
};
