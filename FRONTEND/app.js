// Enhanced EcoFarm Quest - Comprehensive Learning & Community Application
class EnhancedEcoFarmQuest {
    constructor() {
        this.currentScreen = 'welcomeScreen';
        this.currentDashboardSection = 'overview';
        this.currentCommunityTab = 'discussions';
        this.currentAccountTab = 'profile';
        this.currentUser = null;
        this.selectedAvatar = null;
        this.learningData = null;
        this.communityData = null;
        this.accountData = null;
        this.currentCourse = null;
        this.currentQuiz = null;
        this.quizIndex = 0;
        this.accessToken = null;
        // Provide safe default/demo data so Account tabs render placeholders
        // even when real data hasn't loaded yet or is missing.
        this.accountData = {
            personalInfo: {
                name: 'Farmer',
                phone: '',
                email: '',
                location: '',
                farmSize: '',
                primaryCrops: [],
                farmingExperience: '',
                waterSource: 'borewell'
            },
            avatarOptions: [
                { id: 'cow', name: 'Gau Mata', type: 'Dairy Specialist', emoji: '🐄' },
                { id: 'chicken', name: 'Murgi', type: 'Poultry Expert', emoji: '🐔' },
                { id: 'goat', name: 'Bakri', type: 'Livestock Guardian', emoji: '🐐' },
                { id: 'rabbit', name: 'Khargosh', type: 'Small Farm Helper', emoji: '🐰' }
            ],
            currentAvatar: 'cow',
            settings: {
                notifications: {
                    questReminders: true,
                    communityUpdates: true,
                    weatherAlerts: true,
                    achievementNotifications: true
                },
                privacy: {
                    profileVisibility: 'community',
                    achievementSharing: true,
                    progressSharing: true,
                    locationSharing: false
                },
                preferences: { language: 'en', theme: 'auto' }
            }
        };

        // Minimal demo currentUser to avoid UI flashes of undefined
        this.currentUser = {
            id: null,
            name: 'Farmer',
            email: '',
            phone: '',
            location: '',
            farmSize: '',
            primaryCrops: [],
            farmingExperience: '',
            waterSource: 'borewell',
            avatar: this.accountData.avatarOptions[0],
            learningStats: {
                knowledge_points: 0,
                current_level: 1,
                completed_courses: 0
            },
            settings: this.accountData.settings
        };

        this.init();
    }

    async init() {
        console.log('🌱 Initializing Enhanced EcoFarm Quest...');
        // Populate UI with safe placeholders immediately to avoid flashes of undefined
        this.populateAccountPlaceholders();

        // Load application data
        await this.loadApplicationData();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initialize UI components
        this.initializeUI();
        
        // Start background effects
        this.initializeBackgroundEffects();
        
        console.log('✅ EcoFarm Quest Enhanced loaded successfully!');
    }

    populateAccountPlaceholders() {
        try {
            // Profile avatar
            const profileAvatar = document.getElementById('profileAvatarEdit');
            const name = document.getElementById('profileName');
            const email = document.getElementById('profileEmail');
            const avatar = this.currentUser?.avatar || (this.accountData && this.accountData.avatarOptions && this.accountData.avatarOptions[0]) || { id: 'cow', emoji: '🐄' };
            if (profileAvatar) profileAvatar.innerHTML = `<div class="animal-character ${avatar.id}-avatar breathing">${avatar.emoji}</div>`;

            // Dashboard avatar
            const dashboardAvatar = document.getElementById('dashboardAvatar');
            if (dashboardAvatar) dashboardAvatar.innerHTML = `<div class="animal-character ${avatar.id}-avatar breathing">${avatar.emoji}</div>`;

            // Selected avatar preview/name/type
            const selPrev = document.getElementById('selectedAvatarPreview');
            const selName = document.getElementById('selectedAvatarName');
            const selType = document.getElementById('selectedAvatarType');
            if (name) name.value = this.userData.name;
            if (selPrev) selPrev.textContent = avatar.emoji || '🐄';
            if (selName) selName.textContent = avatar.name || 'Gau Mata';
            if (selType) selType.textContent = avatar.type || 'Farm Companion';

            // Fill avatar options grid if empty
            const avatarOptionsGrid = document.getElementById('avatarOptionsGrid');
            if (avatarOptionsGrid && avatarOptionsGrid.innerHTML.trim() === '') {
                if (this.accountData && Array.isArray(this.accountData.avatarOptions)) {
                    avatarOptionsGrid.innerHTML = this.accountData.avatarOptions.map(a => `
                        <div class="avatar-option enhanced-card" data-avatar-id="${a.id}">
                            <div class="avatar-option-icon">${a.emoji}</div>
                            <div class="avatar-option-name">${a.name}</div>
                            <div class="avatar-option-type">${a.type}</div>
                        </div>
                    `).join('');
                }
            }

            // Ensure profile fields show placeholders
            this.updateElementValue('profileName', this.currentUser?.name || this.accountData.personalInfo.name || 'Farmer');
            this.updateElementValue('profileEmail', this.currentUser?.email || this.accountData.personalInfo.email || '');
            this.updateElementValue('profilePhone', this.currentUser?.phone || this.accountData.personalInfo.phone || '');
            this.updateElementValue('profileLocation', this.currentUser?.location || this.accountData.personalInfo.location || '');
            this.updateElementValue('profileFarmSize', this.currentUser?.farmSize || this.accountData.personalInfo.farmSize || '');
        } catch (e) {
            console.warn('populateAccountPlaceholders error', e);
        }
    }

    async loadApplicationData() {
        // Attempt to restore session
        this.restoreSession();

        // Load demo data when we don't have learning/community/account data yet
        // (we may have a demo currentUser object initialized earlier just for placeholders)
        if (!this.currentUser || !this.learningData || !this.communityData || !this.accountData) {
            await this.loadDemoData();
        }
    }

    async loadDemoData() {
        // Demo data for non-authenticated users
        this.learningData = {
            courses: [
                {
                    id: "irrigation_mastery",
                    title: "Smart Irrigation Mastery",
                    category: "water",
                    description: "Learn advanced irrigation techniques for optimal water usage",
                    duration: "3 hours",
                    difficulty: 3,
                    progress: 65,
                    lessons: 8,
                    completed: 5,
                    certificate: "Water Management Expert",
                    thumbnail: "🌊",
                    color: "#2196F3"
                },
                {
                    id: "soil_health",
                    title: "Soil Health Fundamentals",
                    category: "soil",
                    description: "Master soil testing, composting, and nutrient management",
                    duration: "4 hours",
                    difficulty: 2,
                    progress: 90,
                    lessons: 10,
                    completed: 9,
                    certificate: "Soil Guardian",
                    thumbnail: "🌱",
                    color: "#4CAF50"
                },
                {
                    id: "pest_control",
                    title: "Integrated Pest Management",
                    category: "pest",
                    description: "Natural and biological pest control methods",
                    duration: "2.5 hours",
                    difficulty: 3,
                    progress: 30,
                    lessons: 6,
                    completed: 2,
                    certificate: "Pest Control Specialist",
                    thumbnail: "🐛",
                    color: "#FF5722"
                },
                {
                    id: "organic_farming",
                    title: "Organic Farming Practices",
                    category: "sustainable",
                    description: "Complete guide to organic and sustainable farming",
                    duration: "5 hours",
                    difficulty: 4,
                    progress: 0,
                    lessons: 12,
                    completed: 0,
                    certificate: "Organic Farming Master",
                    thumbnail: "🌿",
                    color: "#8BC34A"
                },
                {
                    id: "crop_rotation",
                    title: "Crop Rotation Strategies",
                    category: "soil",
                    description: "Maximize yield through strategic crop rotation",
                    duration: "2 hours",
                    difficulty: 2,
                    progress: 100,
                    lessons: 5,
                    completed: 5,
                    certificate: "Rotation Expert",
                    thumbnail: "🔄",
                    color: "#9C27B0"
                }
            ],
            quizzes: [
                {
                    courseId: "irrigation_mastery",
                    questions: [
                        {
                            question: "Which irrigation method is most water-efficient?",
                            options: ["Flood Irrigation", "Sprinkler System", "Drip Irrigation", "Manual Watering"],
                            correct: 2,
                            explanation: "Drip irrigation delivers water directly to plant roots, reducing waste by up to 50%."
                        },
                        {
                            question: "What is the ideal time for irrigation?",
                            options: ["Noon", "Evening", "Early morning", "Late night"],
                            correct: 2,
                            explanation: "Early morning irrigation reduces evaporation and allows plants to absorb water efficiently."
                        }
                    ]
                }
            ],
            stats: {
                totalCourses: 5,
                completedCourses: 1,
                totalLessons: 41,
                completedLessons: 21,
                learningStreak: 7,
                knowledgePoints: 1250,
                currentLevel: 3,
                nextLevelPoints: 1500,
                certificates: 1
            }
        };

        this.communityData = {
            discussions: [
                {
                    id: "irrigation_tips",
                    title: "Smart Irrigation Tips & Tricks",
                    category: "water",
                    author: "Rajesh Kumar",
                    authorAvatar: "🐄",
                    participants: 23,
                    messages: 156,
                    lastMessage: "Just installed drip irrigation - seeing 40% water savings!",
                    lastUser: "Rajesh Kumar",
                    lastTime: "2 minutes ago",
                    pinned: true,
                    likes: 45,
                    content: "Has anyone tried the new smart irrigation controllers? Looking for recommendations."
                },
                {
                    id: "organic_success",
                    title: "Organic Farming Success Stories",
                    category: "sustainable",
                    author: "Priya Devi",
                    authorAvatar: "🐔",
                    participants: 31,
                    messages: 203,
                    lastMessage: "My organic tomatoes are selling at premium prices!",
                    lastUser: "Priya Devi",
                    lastTime: "15 minutes ago",
                    pinned: false,
                    likes: 67,
                    content: "Share your organic farming success stories and tips here!"
                },
                {
                    id: "pest_natural",
                    title: "Natural Pest Control Methods",
                    category: "pest",
                    author: "Anil Singh",
                    authorAvatar: "🐐",
                    participants: 18,
                    messages: 89,
                    lastMessage: "Neem oil works wonders for aphids",
                    lastUser: "Anil Singh",
                    lastTime: "1 hour ago",
                    pinned: false,
                    likes: 34,
                    content: "Let's discuss effective natural pest control methods that don't harm the environment."
                }
            ],
            achievements: [
                {
                    category: "Learning Achievements",
                    achievements: [
                        {
                            id: "first_course",
                            name: "Knowledge Seeker",
                            description: "Complete your first course",
                            icon: "📚",
                            unlocked: true,
                            unlockedDate: "2025-09-15",
                            progress: 100
                        },
                        {
                            id: "quiz_master",
                            name: "Quiz Master",
                            description: "Score 100% on 5 quizzes",
                            icon: "🎯",
                            unlocked: true,
                            unlockedDate: "2025-09-20",
                            progress: 100
                        },
                        {
                            id: "learning_streak",
                            name: "Consistent Learner",
                            description: "Maintain 7-day learning streak",
                            icon: "🔥",
                            unlocked: true,
                            unlockedDate: "2025-09-25",
                            progress: 100
                        }
                    ]
                },
                {
                    category: "Community Achievements",
                    achievements: [
                        {
                            id: "helpful_farmer",
                            name: "Helpful Farmer",
                            description: "Help 10 fellow farmers",
                            icon: "🤝",
                            unlocked: true,
                            unlockedDate: "2025-09-18",
                            progress: 100
                        },
                        {
                            id: "discussion_leader",
                            name: "Discussion Leader",
                            description: "Start 5 meaningful discussions",
                            icon: "💬",
                            unlocked: false,
                            progress: 60,
                            requirement: "3 more discussions needed"
                        }
                    ]
                }
            ],
            leaderboard: [
                {
                    rank: 1,
                    name: "Rajesh Kumar",
                    avatar: "🐄",
                    points: 2450,
                    location: "Green Valley Village"
                },
                {
                    rank: 2,
                    name: "Priya Devi",
                    avatar: "🐔",
                    points: 2380,
                    location: "Sunrise Farm"
                },
                {
                    rank: 3,
                    name: "Anil Singh",
                    avatar: "🐐",
                    points: 2320,
                    location: "Eco Fields"
                },
                {
                    rank: 4,
                    name: "Farmer John",
                    avatar: "🐄",
                    points: 1250,
                    location: "Green Valley Village"
                }
            ]
        };

        this.accountData = {
            personalInfo: {
                name: "Farmer John",
                phone: "+91 98765 43210",
                email: "farmer@example.com",
                location: "Green Valley Village",
                farmSize: "5 acres",
                primaryCrops: ["Rice", "Wheat", "Vegetables"],
                farmingExperience: "15 years",
                waterSource: "borewell"
            },
            avatarOptions: [
                { id: "cow", name: "Gau Mata", type: "Dairy Specialist", emoji: "🐄" },
                { id: "chicken", name: "Murgi", type: "Poultry Expert", emoji: "🐔" },
                { id: "goat", name: "Bakri", type: "Livestock Guardian", emoji: "🐐" },
                { id: "rabbit", name: "Khargosh", type: "Small Farm Helper", emoji: "🐰" }
            ],
            currentAvatar: "cow",
            settings: {
                notifications: {
                    questReminders: true,
                    communityUpdates: true,
                    weatherAlerts: true,
                    achievementNotifications: true
                },
                privacy: {
                    profileVisibility: "community",
                    achievementSharing: true,
                    progressSharing: true,
                    locationSharing: false
                },
                preferences: {
                    language: "en",
                    theme: "auto"
                }
            }
        };

        // If we have a token, try to load real user profile; otherwise use demo user
        if (this.accessToken) {
            try {
                const me = await this.apiGet('/api/auth/me');
                if (me?.data?.user) {
                    this.currentUser = this.mapServerUserToClient(me.data.user);
                }
            } catch (e) {
                // Fallback to demo user on failure
                this.useDemoUser();
            }
        } else {
            this.useDemoUser();
        }
    }

    // --- Auth & API helpers ---
    mapServerUserToClient(user) {
        return {
            id: user.id,
            name: user.name || '',
            email: user.email || '',
            phone: user.phone || '',
            location: user.location || '',
            farmSize: user.farm_size || user.farmSize || '',
            primaryCrops: user.primary_crops || user.primaryCrops || [],
            farmingExperience: user.farming_experience || user.farmingExperience || '',
            waterSource: user.water_source || user.waterSource || '',
            avatar: user.avatar || this.accountData.avatarOptions.find(a => a.id === this.accountData.currentAvatar),
            learningStats: user.learning_stats || user.learningStats || this.learningData?.stats,
            settings: user.settings || this.accountData.settings
        };
    }

    useDemoUser() {
        this.currentUser = {
            ...this.accountData.personalInfo,
            avatar: this.accountData.avatarOptions.find(a => a.id === this.accountData.currentAvatar),
            learningStats: this.learningData.stats,
            settings: this.accountData.settings
        };
    }

    storeSession(token) {
        this.accessToken = token;
        try { localStorage.setItem('access_token', token); } catch (_) {}
    }

    clearSession() {
        this.accessToken = null;
        try { localStorage.removeItem('access_token'); } catch (_) {}
    }

    restoreSession() {
        try { this.accessToken = localStorage.getItem('access_token'); } catch (_) { this.accessToken = null; }
    }

    async apiRequest(path, options = {}) {
        const headers = options.headers || {};
        if (this.accessToken) {
            headers['Authorization'] = `Bearer ${this.accessToken}`;
        }
        headers['Content-Type'] = 'application/json';
        const res = await fetch(path, { ...options, headers });
        const contentType = res.headers.get('content-type') || '';
        const bodyText = await res.text();
        if (!res.ok) {
            // Try to parse JSON error body if present
            let parsed = null;
            try {
                parsed = JSON.parse(bodyText || '{}');
            } catch (e) {
                parsed = bodyText || null;
            }
            const err = new Error((parsed && parsed.message) ? parsed.message : `Request failed: ${res.status}`);
            // Attach extra info for debugging
            err.status = res.status;
            err.body = parsed;
            err.raw = bodyText;
            throw err;
        }

        if (contentType.includes('application/json')) {
            return JSON.parse(bodyText);
        }
        // Fallback: return raw text
        return bodyText;
    }

    apiGet(path) { return this.apiRequest(path, { method: 'GET' }); }
    apiPost(path, body) { return this.apiRequest(path, { method: 'POST', body: JSON.stringify(body) }); }

    setupEventListeners() {
        // Form submissions
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin();
            });
        }

        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegister();
            });
        }

        // Password visibility toggle
        document.querySelectorAll('.toggle-password').forEach((btn) => {
            btn.addEventListener('click', () => {
                const targetId = btn.getAttribute('data-target');
                const input = document.getElementById(targetId);
                if (!input) return;
                const isPassword = input.getAttribute('type') === 'password';
                input.setAttribute('type', isPassword ? 'text' : 'password');
                btn.textContent = isPassword ? '🙈' : '👁️';
            });
        });

        // Modal close events
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target.id);
            }
        });

        // Keyboard events
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal:not(.hidden)');
                if (openModal) {
                    this.closeModal(openModal.id);
                }
            }
        });

        // Search functionality
        const discussionSearch = document.getElementById('discussionSearch');
        if (discussionSearch) {
            discussionSearch.addEventListener('input', (e) => {
                this.searchDiscussions(e.target.value);
            });
        }

        // Filter functionality
        const discussionFilter = document.getElementById('discussionFilter');
        if (discussionFilter) {
            discussionFilter.addEventListener('change', (e) => {
                this.filterDiscussions(e.target.value);
            });
        }
    }

    initializeUI() {
        this.renderLearningSection();
        this.renderCommunitySection();
        this.renderAccountSection();
        this.updateUserInterface();
    }

    initializeBackgroundEffects() {
        // Background particles are handled by CSS animations
        // This method can be extended for more complex effects
        const particles = document.querySelectorAll('.particle');
        particles.forEach((particle, index) => {
            particle.style.animationDelay = `${index * 3}s`;
        });
    }

    // Screen Navigation
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
        this.currentScreen = screenId;

        if (screenId === 'dashboardScreen') {
            this.updateUserInterface();
        }
    }

    showDashboardSection(sectionId) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${sectionId}"]`).classList.add('active');

        // Update sections
        document.querySelectorAll('.dashboard-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId + 'Section').classList.add('active');
        
        this.currentDashboardSection = sectionId;

        // Section-specific updates
        if (sectionId === 'learning') {
            this.renderLearningSection();
        } else if (sectionId === 'community') {
            this.renderCommunitySection();
        } else if (sectionId === 'account') {
            this.renderAccountSection();
            // Ensure an account sub-tab is visible when entering the Account section
            try {
                const desiredTab = this.currentAccountTab || 'profile';
                console.debug('Activating account tab on section show:', desiredTab);
                this.showAccountTab(desiredTab);
            } catch (e) { console.warn('Error activating account tab on showDashboardSection', e); }
        }
    }

    // Authentication
    switchAuthTab(tabName) {
        // Clear existing active state
        const authTabs = document.querySelectorAll('.auth-tab');
        authTabs.forEach(tab => tab.classList.remove('active'));

        // Attempt to find the tab button that started this action by inspecting its onclick attribute
        const activatedAuthTab = Array.from(authTabs).find(t => {
            const onclickAttr = t.getAttribute('onclick') || '';
            return onclickAttr.includes(`'${tabName}'`) || onclickAttr.includes(`"${tabName}"`);
        });
        if (activatedAuthTab) activatedAuthTab.classList.add('active');

        document.querySelectorAll('.auth-form').forEach(form => {
            form.classList.remove('active');
        });
        document.getElementById(tabName + 'Form').classList.add('active');
    }

    async handleLogin() {
        const emailEl = document.querySelector('#loginForm input[type="email"]') || document.querySelector('input[name="email"]');
        const passEl = document.querySelector('#loginForm input[type="password"]') || document.querySelector('#loginPassword') || document.querySelector('input[name="password"]');
        const email = (emailEl && emailEl.value) ? emailEl.value.trim() : '';
        const password = (passEl && passEl.value) ? passEl.value : '';

        if (!email || !password) {
            this.showNotification('Please enter email and password', 'error');
            return;
        }

        try {
            console.debug('Login payload:', { email, password: password ? '***' : '' });
            const resp = await this.apiPost('/api/auth/login', { email, password });
            const token = resp?.data?.access_token;
            if (!token) throw new Error('Missing access token');
            this.storeSession(token);

            // Load fresh user profile for this account
            const me = await this.apiGet('/api/auth/me');
            this.currentUser = this.mapServerUserToClient(me?.data?.user || {});

            this.showNotification('Login successful!', 'success');
            this.showScreen('dashboardScreen');
            this.updateUserInterface();
        } catch (err) {
            this.clearSession();
            // If apiRequest attached status/body info, show it in console and in the notification
            console.error('Login error details:', err);
            const details = err && (err.body || err.raw || err.status) ? ` (${JSON.stringify(err.body || err.raw || err.status)})` : '';
            this.showNotification('Login failed: ' + (err.message || 'Unknown error') + details, 'error');
        }
    }

    async handleRegister() {
        const form = document.getElementById('registerForm');

        // Prefer selecting inputs by name to avoid accidental mismatches
        const nameInput = (form && form.querySelector('input[name="name"]')) || document.querySelector('input[name="name"]');
        const emailInput = (form && form.querySelector('input[name="email"]')) || document.querySelector('input[name="email"]') || document.querySelector('#registerForm input[type="email"]');
        const passwordInput = (form && (form.querySelector('input[name="password"]') || form.querySelector('input[type="password"]'))) || document.querySelector('#registerPassword') || document.querySelector('input[type="password"]');
        const phoneInput = (form && form.querySelector('input[name="phone"]')) || document.querySelector('input[name="phone"]');
        const locationInput = (form && form.querySelector('input[name="location"]')) || document.querySelector('input[name="location"]');
        const farmSizeInput = (form && (form.querySelector('select[name="farm_size"]') || form.querySelector('input[name="farm_size"]'))) || document.querySelector('select[name="farm_size"]') || document.querySelector('input[name="farm_size"]');

        const name = (nameInput?.value || '').trim();
        let email = (emailInput?.value || '').trim();
        const password = (passwordInput?.value || '').trim();
        const phone = (phoneInput?.value || '').trim();
        const location = (locationInput?.value || '').trim();
        const farmSize = (farmSizeInput?.value || '').trim();

        // Normalize email to lowercase for client-side validation consistency
        email = email.toLowerCase();

        // Debug logs (helpful when reproducing client-side failures)
        console.debug('Register payload:', { name, email, password: password ? '***' : '', phone, location, farmSize });

        const missing = [];
        if (!name) missing.push('name');
        if (!email) missing.push('email');
        if (!password) missing.push('password');
        if (missing.length) {
            const human = missing.join(', ');
            const message = `Please fill in: ${human}`;
            // Show inline form error if present
            const regErr = document.getElementById('registerError');
            if (regErr) {
                regErr.textContent = message;
                regErr.style.display = 'block';
            }
            this.showNotification(message, 'error');
            console.warn('Registration blocked - missing fields:', missing);
            return;
        }

        // Client-side password strength to match backend policy
        const strongEnough = password.length >= 8 && /[A-Z]/.test(password) && /[a-z]/.test(password) && /\d/.test(password);
        if (!strongEnough) {
            this.showNotification('Password must be 8+ chars with upper, lower, and a number', 'error');
            return;
        }

        // Backend requires phone, location, farm_size. Provide fallbacks if missing.
        const body = {
            name,
            email,
            password,
            phone: phone || '+0000000000',
            location: location || 'Unknown',
            farm_size: farmSize || '1 acre',
        };

        try {
            const resp = await this.apiPost('/api/auth/register', body);
            const token = resp?.data?.access_token;
            if (token) this.storeSession(token);

            if (this.accessToken) {
                const me = await this.apiGet('/api/auth/me');
                this.currentUser = this.mapServerUserToClient(me?.data?.user || {});
            } else {
                this.useDemoUser();
                this.currentUser.name = name;
                this.currentUser.email = email;
            }

            this.showNotification('Registration successful! Welcome to EcoFarm Quest!', 'success');
            this.showScreen('dashboardScreen');
            this.updateUserInterface();
        } catch (err) {
            this.showNotification('Registration failed: ' + (err.message || 'Unknown error'), 'error');
        }
    }

    // Enhanced Learning Section
    renderLearningSection() {
        this.renderCourseCards();
        this.updateLearningStats();
    }

    renderCourseCards() {
        const coursesGrid = document.getElementById('coursesGrid');
        if (!coursesGrid) return;

        coursesGrid.innerHTML = '';

        const courses = (this.learningData && Array.isArray(this.learningData.courses)) ? this.learningData.courses : [];
        if (!courses.length) {
            coursesGrid.innerHTML = '<div class="notice">No courses available at the moment.</div>';
            return;
        }

        courses.forEach(course => {
            const courseCard = document.createElement('div');
            courseCard.className = 'course-card enhanced-card';
            courseCard.dataset.category = course.category;

            const difficultyStars = '⭐'.repeat(course.difficulty);
            const progressPercent = course.progress;

            courseCard.innerHTML = `
                <div class="course-header">
                    <div class="course-thumbnail" style="color: ${course.color}">${course.thumbnail}</div>
                    <div class="course-info">
                        <h3 class="course-title">${course.title}</h3>
                        <div class="course-category">${this.getCategoryName(course.category)}</div>
                    </div>
                </div>
                <p class="course-description">${course.description}</p>
                <div class="course-meta">
                    <span class="course-duration">⏱️ ${course.duration}</span>
                    <span class="course-difficulty">Difficulty: ${difficultyStars}</span>
                </div>
                <div class="course-progress-section">
                    <div class="course-progress-bar">
                        <div class="course-progress-fill" style="width: ${progressPercent}%"></div>
                    </div>
                    <div class="course-lessons-info">
                        <span>Progress: ${progressPercent}%</span>
                        <span>${course.completed}/${course.lessons} lessons</span>
                    </div>
                </div>
                <div class="course-certificate">
                    <span>🏅 Certificate: ${course.certificate}</span>
                </div>
                <div class="course-actions">
                    <button class="btn btn--outline enhanced-btn" onclick="app.previewCourse('${course.id}')">
                        📖 Preview
                    </button>
                    <button class="btn btn--primary enhanced-btn" onclick="app.startCourse('${course.id}')">
                        ${progressPercent > 0 ? 'Continue' : 'Start'} Course
                    </button>
                </div>
            `;

            coursesGrid.appendChild(courseCard);
        });
    }

    updateLearningStats() {
        const stats = this.learningData.stats;
        this.updateElementText('totalLessons', stats.completedLessons);
        this.updateElementText('streakDays', stats.learningStreak);
        this.updateElementText('currentLevel', stats.currentLevel);
        this.updateElementText('nextLevelPoints', stats.nextLevelPoints - stats.knowledgePoints);
        this.updateElementText('knowledgePoints', stats.knowledgePoints);
        this.updateElementText('coursesCompleted', `${stats.completedCourses} / ${stats.totalCourses}`);
        this.updateElementText('certificatesEarned', stats.certificates);
        this.updateElementText('learningStreak', `${stats.learningStreak} days`);

        // Update progress bar
        const progressPercent = (stats.knowledgePoints / stats.nextLevelPoints) * 100;
        this.updateProgressBar('knowledgeBar', progressPercent);
    }

    filterCourses(category) {
        // Clear active state for category buttons
        const categoryBtns = document.querySelectorAll('.category-btn');
        categoryBtns.forEach(btn => btn.classList.remove('active'));

        // Find the button that triggered the filter by checking its onclick attribute
        const activatedCategoryBtn = Array.from(categoryBtns).find(b => {
            const onclickAttr = b.getAttribute('onclick') || '';
            return onclickAttr.includes(`'${category}'`) || onclickAttr.includes(`"${category}"`);
        });
        if (activatedCategoryBtn) activatedCategoryBtn.classList.add('active');

        document.querySelectorAll('.course-card').forEach(card => {
            const cardCategory = card.dataset.category;
            const show = category === 'all' || cardCategory === category;
            card.style.display = show ? 'block' : 'none';
        });
    }

    getCategoryName(category) {
        const names = {
            water: 'Water Management',
            soil: 'Soil Management',
            pest: 'Crop Protection',
            sustainable: 'Sustainable Agriculture'
        };
        return names[category] || 'General';
    }

    startCourse(courseId) {
        const course = this.learningData.courses.find(c => c.id === courseId);
        if (!course) return;

        this.currentCourse = course;
        this.showCourseModal(course);
    }

    previewCourse(courseId) {
        const course = this.learningData.courses.find(c => c.id === courseId);
        if (!course) return;

        this.showCoursePreview(course);
    }

    showCourseModal(course) {
        document.getElementById('courseModalTitle').textContent = course.title;
        
        const courseDetails = document.getElementById('courseDetails');
        courseDetails.innerHTML = `
            <div class="course-modal-content">
                <div class="course-overview">
                    <h4>📖 Course Overview</h4>
                    <p>${course.description}</p>
                    <div class="course-modal-meta">
                        <p><strong>Duration:</strong> ${course.duration}</p>
                        <p><strong>Difficulty:</strong> ${'⭐'.repeat(course.difficulty)}</p>
                        <p><strong>Lessons:</strong> ${course.lessons}</p>
                        <p><strong>Certificate:</strong> ${course.certificate}</p>
                    </div>
                </div>
                <div class="course-curriculum">
                    <h4>📝 Curriculum</h4>
                    <ul>
                        <li>Introduction to ${course.title}</li>
                        <li>Basic Concepts and Principles</li>
                        <li>Practical Applications</li>
                        <li>Best Practices and Tips</li>
                        <li>Real-world Case Studies</li>
                        <li>Final Assessment and Quiz</li>
                    </ul>
                </div>
                <div class="course-actions-modal">
                    <button class="btn btn--secondary enhanced-btn" onclick="app.closeModal('courseModal')">
                        Cancel
                    </button>
                    <button class="btn btn--primary enhanced-btn" onclick="app.beginCourseLesson('${course.id}')">
                        ${course.progress > 0 ? 'Continue Learning' : 'Start Learning'}
                    </button>
                </div>
            </div>
        `;

        document.getElementById('courseModal').classList.remove('hidden');
    }

    beginCourseLesson(courseId) {
        this.closeModal('courseModal');
        
        // Check if course has quiz
        const quiz = this.learningData.quizzes.find(q => q.courseId === courseId);
        if (quiz) {
            this.startQuiz(quiz);
        } else {
            this.showNotification('Lesson started! Complete the interactive content.', 'success');
            this.simulateCourseProgress(courseId);
        }
    }

    startQuiz(quiz) {
        this.currentQuiz = quiz;
        this.quizIndex = 0;
        this.renderQuizQuestion();
        document.getElementById('quizModal').classList.remove('hidden');
    }

    renderQuizQuestion() {
        if (!this.currentQuiz || this.quizIndex >= this.currentQuiz.questions.length) {
            this.completeQuiz();
            return;
        }

        const question = this.currentQuiz.questions[this.quizIndex];
        const quizContainer = document.getElementById('quizContainer');

        document.getElementById('quizModalTitle').textContent = `Quiz - Question ${this.quizIndex + 1}`;

        quizContainer.innerHTML = `
            <div class="quiz-progress">
                <div class="quiz-progress-bar">
                    <div class="progress-fill" style="width: ${((this.quizIndex + 1) / this.currentQuiz.questions.length) * 100}%"></div>
                </div>
                <p>Question ${this.quizIndex + 1} of ${this.currentQuiz.questions.length}</p>
            </div>
            <div class="quiz-question-content">
                <h4>${question.question}</h4>
                <div class="quiz-options">
                    ${question.options.map((option, index) => `
                        <button class="quiz-option enhanced-btn" onclick="app.selectQuizAnswer(${index})" data-index="${index}">
                            ${option}
                        </button>
                    `).join('')}
                </div>
                <div id="quizFeedback" class="quiz-feedback" style="display: none;"></div>
                <div class="quiz-navigation" style="display: none;">
                    <button class="btn btn--primary enhanced-btn" onclick="app.nextQuizQuestion()">
                        ${this.quizIndex < this.currentQuiz.questions.length - 1 ? 'Next Question' : 'Complete Quiz'}
                    </button>
                </div>
            </div>
        `;
    }

    selectQuizAnswer(selectedIndex) {
        const question = this.currentQuiz.questions[this.quizIndex];
        const options = document.querySelectorAll('.quiz-option');
        const feedback = document.getElementById('quizFeedback');
        const navigation = document.querySelector('.quiz-navigation');

        // Disable further selection
        options.forEach(option => {
            option.disabled = true;
            option.style.pointerEvents = 'none';
        });

        // Show correct/incorrect styling
        options.forEach((option, index) => {
            if (index === question.correct) {
                option.classList.add('success-state');
                option.style.background = 'var(--color-success)';
                option.style.color = 'white';
            } else if (index === selectedIndex && index !== question.correct) {
                option.classList.add('error-state');
                option.style.background = 'var(--color-error)';
                option.style.color = 'white';
            }
        });

        // Show explanation
        feedback.innerHTML = `
            <div class="feedback-content">
                <h5>${selectedIndex === question.correct ? '✅ Correct!' : '❌ Incorrect'}</h5>
                <p>${question.explanation}</p>
            </div>
        `;
        feedback.style.display = 'block';
        navigation.style.display = 'block';

        // Track score
        if (!this.currentQuiz.score) this.currentQuiz.score = 0;
        if (selectedIndex === question.correct) {
            this.currentQuiz.score++;
        }
    }

    nextQuizQuestion() {
        this.quizIndex++;
        this.renderQuizQuestion();
    }

    completeQuiz() {
        const score = this.currentQuiz.score || 0;
        const totalQuestions = this.currentQuiz.questions.length;
        const percentage = Math.round((score / totalQuestions) * 100);

        this.closeModal('quizModal');

        // Update course progress
        const course = this.learningData.courses.find(c => c.id === this.currentQuiz.courseId);
        if (course) {
            course.progress = Math.min(100, course.progress + 25);
            course.completed = Math.min(course.lessons, course.completed + 1);
        }

        // Show completion notification
        this.showAchievement(
            'Quiz Completed!',
            `You scored ${score}/${totalQuestions} (${percentage}%). ${percentage >= 70 ? 'Well done!' : 'Keep practicing!'}`,
            percentage >= 70 ? '🎉' : '📚'
        );

        this.updateLearningStats();
        this.renderCourseCards();

        // Reset quiz state
        this.currentQuiz = null;
        this.quizIndex = 0;
    }

    simulateCourseProgress(courseId) {
        const course = this.learningData.courses.find(c => c.id === courseId);
        if (!course) return;

        // Simulate lesson completion
        setTimeout(() => {
            course.progress = Math.min(100, course.progress + 15);
            course.completed = Math.min(course.lessons, course.completed + 1);
            
            this.showNotification('Lesson completed! Great job!', 'success');
            this.updateLearningStats();
            this.renderCourseCards();

            // Check for course completion
            if (course.progress >= 100) {
                this.showAchievement(
                    'Course Completed!',
                    `Congratulations! You've earned the "${course.certificate}" certificate!`,
                    '🏆'
                );
            }
        }, 2000);
    }

    showCertificates() {
        const completedCourses = this.learningData.courses.filter(c => c.progress >= 100);
        if (completedCourses.length === 0) {
            this.showNotification('Complete your first course to earn certificates!', 'info');
            return;
        }

        let certificatesHTML = '<h4>🏅 Your Certificates</h4><div class="certificates-grid">';
        completedCourses.forEach(course => {
            certificatesHTML += `
                <div class="certificate-card">
                    <div class="certificate-icon">${course.thumbnail}</div>
                    <h5>${course.certificate}</h5>
                    <p>Completed: ${course.title}</p>
                    <button class="btn btn--outline enhanced-btn">Download Certificate</button>
                </div>
            `;
        });
        certificatesHTML += '</div>';

        this.showModal('Certificates', certificatesHTML);
    }

    continueLearning() {
        const incompleteCourse = this.learningData.courses.find(c => c.progress > 0 && c.progress < 100);
        if (incompleteCourse) {
            this.startCourse(incompleteCourse.id);
        } else {
            const firstCourse = this.learningData.courses.find(c => c.progress === 0);
            if (firstCourse) {
                this.startCourse(firstCourse.id);
            } else {
                this.showNotification('All courses completed! New content coming soon.', 'success');
            }
        }
    }

    // Enhanced Community Section
    renderCommunitySection() {
        this.renderDiscussions();
        this.renderAchievements();
        this.renderLeaderboard();
    }

    showCommunityTab(tabName) {
        const communityTabs = document.querySelectorAll('.community-tab');
        communityTabs.forEach(tab => tab.classList.remove('active'));

        const activatedCommunityTab = Array.from(communityTabs).find(t => {
            const onclickAttr = t.getAttribute('onclick') || '';
            return onclickAttr.includes(`'${tabName}'`) || onclickAttr.includes(`"${tabName}"`);
        });
        if (activatedCommunityTab) activatedCommunityTab.classList.add('active');

        document.querySelectorAll('.community-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName + 'Tab').classList.add('active');
        
        this.currentCommunityTab = tabName;

        if (tabName === 'discussions') {
            this.renderDiscussions();
        } else if (tabName === 'achievements') {
            this.renderAchievements();
        } else if (tabName === 'leaderboard') {
            this.renderLeaderboard();
        }
    }

    renderDiscussions() {
        const discussionsFeed = document.getElementById('discussionsFeed');
        if (!discussionsFeed) return;

        discussionsFeed.innerHTML = '';

        this.communityData.discussions.forEach(discussion => {
            const discussionCard = document.createElement('div');
            discussionCard.className = 'discussion-card enhanced-card';
            discussionCard.dataset.category = discussion.category;

            discussionCard.innerHTML = `
                <div class="discussion-header">
                    <h3 class="discussion-title">${discussion.title}</h3>
                    <div class="discussion-category">${this.getCategoryName(discussion.category)}</div>
                </div>
                <div class="discussion-meta">
                    <span>👤 ${discussion.author}</span>
                    <span>👥 ${discussion.participants} participants</span>
                    <span>⏰ ${discussion.lastTime}</span>
                </div>
                <div class="discussion-preview">
                    ${discussion.content}
                </div>
                <div class="discussion-stats">
                    <span>💬 ${discussion.messages} replies</span>
                    <span>❤️ ${discussion.likes} likes</span>
                    ${discussion.pinned ? '<span>📌 Pinned</span>' : ''}
                </div>
                <div class="discussion-actions">
                    <button class="btn btn--outline enhanced-btn" onclick="app.viewDiscussion('${discussion.id}')">
                        View Discussion
                    </button>
                    <button class="btn btn--secondary enhanced-btn" onclick="app.likeDiscussion('${discussion.id}')">
                        ❤️ Like
                    </button>
                </div>
            `;

            discussionsFeed.appendChild(discussionCard);
        });
    }

    searchDiscussions(searchTerm) {
        const discussions = document.querySelectorAll('.discussion-card');
        discussions.forEach(card => {
            const title = card.querySelector('.discussion-title').textContent.toLowerCase();
            const content = card.querySelector('.discussion-preview').textContent.toLowerCase();
            const matches = title.includes(searchTerm.toLowerCase()) || content.includes(searchTerm.toLowerCase());
            card.style.display = matches ? 'block' : 'none';
        });
    }

    filterDiscussions(category) {
        const discussions = document.querySelectorAll('.discussion-card');
        discussions.forEach(card => {
            const cardCategory = card.dataset.category;
            const show = category === 'all' || cardCategory === category;
            card.style.display = show ? 'block' : 'none';
        });
    }

    createNewPost() {
        console.log('Creating new post...'); // Debug log
        const newPostForm = document.getElementById('newPostForm');
        console.log('New post form:', newPostForm); // Debug log
        
        if (newPostForm) {
            newPostForm.classList.toggle('hidden');
            this.showNotification('New post form opened!', 'info');
        } else {
            // If form doesn't exist, create it dynamically
            this.showNewPostModal();
        }
    }

    showNewPostModal() {
        const modalHTML = `
            <div class="new-post-modal-content">
                <h4>✍️ Create New Discussion</h4>
                <div class="form-group">
                    <label class="form-label">Topic Title</label>
                    <input type="text" class="form-control" id="modalPostTitle" placeholder="What would you like to discuss?">
                </div>
                <div class="form-group">
                    <label class="form-label">Category</label>
                    <select class="form-control" id="modalPostCategory">
                        <option value="general">General Discussion</option>
                        <option value="water">Water Management</option>
                        <option value="soil">Soil Health</option>
                        <option value="pest">Pest Control</option>
                        <option value="sustainable">Sustainable Practices</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Message</label>
                    <textarea class="form-control" id="modalPostMessage" rows="4" placeholder="Share your thoughts, questions, or experiences..."></textarea>
                </div>
                <div class="form-actions">
                    <button class="btn btn--secondary enhanced-btn" onclick="app.closeModal('customModal')">Cancel</button>
                    <button class="btn btn--primary enhanced-btn" onclick="app.submitNewPostFromModal()">📝 Post Discussion</button>
                </div>
            </div>
        `;
        
        this.showModal('Create New Discussion', modalHTML);
    }

    submitNewPostFromModal() {
        const title = document.getElementById('modalPostTitle').value;
        const category = document.getElementById('modalPostCategory').value;
        const message = document.getElementById('modalPostMessage').value;

        if (!title || !message) {
            this.showNotification('Please fill in all required fields', 'error');
            return;
        }

        // Create new discussion
        const newDiscussion = {
            id: 'new_' + Date.now(),
            title: title,
            category: category,
            author: this.currentUser.name,
            authorAvatar: this.currentUser.avatar?.emoji || '👤',
            participants: 1,
            messages: 1,
            lastMessage: message.substring(0, 50) + '...',
            lastUser: this.currentUser.name,
            lastTime: 'Just now',
            pinned: false,
            likes: 0,
            content: message
        };

        // Add to discussions array
        this.communityData.discussions.unshift(newDiscussion);

        // Re-render discussions
        this.renderDiscussions();

        // Close modal and show success
        this.closeModal('customModal');
        this.showNotification('Discussion created successfully!', 'success');

        // Update achievement progress
        this.updateDiscussionLeaderProgress();
    }

    cancelNewPost() {
        const newPostForm = document.getElementById('newPostForm');
        if (newPostForm) {
            newPostForm.classList.add('hidden');
            // Clear form
            newPostForm.querySelectorAll('input, textarea, select').forEach(field => {
                field.value = '';
            });
        }
    }

    submitNewPost() {
        const title = document.getElementById('postTitle').value;
        const category = document.getElementById('postCategory').value;
        const message = document.getElementById('postMessage').value;

        if (!title || !message) {
            this.showNotification('Please fill in all required fields', 'error');
            return;
        }

        // Create new discussion
        const newDiscussion = {
            id: 'new_' + Date.now(),
            title: title,
            category: category,
            author: this.currentUser.name,
            authorAvatar: this.currentUser.avatar?.emoji || '👤',
            participants: 1,
            messages: 1,
            lastMessage: message.substring(0, 50) + '...',
            lastUser: this.currentUser.name,
            lastTime: 'Just now',
            pinned: false,
            likes: 0,
            content: message
        };

        // Add to discussions array
        this.communityData.discussions.unshift(newDiscussion);

        // Re-render discussions
        this.renderDiscussions();

        // Hide form and show success
        this.cancelNewPost();
        this.showNotification('Discussion created successfully!', 'success');

        // Update achievement progress
        this.updateDiscussionLeaderProgress();
    }

    updateDiscussionLeaderProgress() {
        const achievement = this.communityData.achievements
            .find(cat => cat.category === 'Community Achievements')
            ?.achievements.find(a => a.id === 'discussion_leader');

        if (achievement && !achievement.unlocked) {
            achievement.progress = Math.min(100, achievement.progress + 20);
            if (achievement.progress >= 100) {
                achievement.unlocked = true;
                achievement.unlockedDate = new Date().toISOString().split('T')[0];
                this.showAchievement(
                    'Achievement Unlocked!',
                    `${achievement.name}: ${achievement.description}`,
                    achievement.icon
                );
            }
        }
    }

    viewDiscussion(discussionId) {
        const discussion = this.communityData.discussions.find(d => d.id === discussionId);
        if (!discussion) return;

        const discussionHTML = `
            <div class="discussion-detail">
                <div class="discussion-header-detail">
                    <h3>${discussion.title}</h3>
                    <div class="discussion-meta-detail">
                        <span>${discussion.authorAvatar} ${discussion.author}</span>
                        <span>${discussion.lastTime}</span>
                    </div>
                </div>
                <div class="discussion-content-detail">
                    <p>${discussion.content}</p>
                </div>
                <div class="discussion-replies">
                    <h4>💬 Replies (${discussion.messages})</h4>
                    <div class="reply-item">
                        <strong>🐔 Priya Devi:</strong> Great topic! I've been using similar methods.
                    </div>
                    <div class="reply-item">
                        <strong>🐐 Anil Singh:</strong> Thanks for sharing your experience!
                    </div>
                </div>
                <div class="reply-form">
                    <textarea class="form-control" placeholder="Add your reply..." rows="3" id="replyText"></textarea>
                    <button class="btn btn--primary enhanced-btn" onclick="app.addReply('${discussionId}')">
                        Post Reply
                    </button>
                </div>
            </div>
        `;

        this.showModal(discussion.title, discussionHTML);
    }

    addReply(discussionId) {
        const replyText = document.getElementById('replyText');
        if (!replyText || !replyText.value.trim()) {
            this.showNotification('Please enter a reply message', 'error');
            return;
        }

        const discussion = this.communityData.discussions.find(d => d.id === discussionId);
        if (discussion) {
            discussion.messages++;
            discussion.participants++;
            this.showNotification('Reply added successfully!', 'success');
            this.closeModal('customModal');
            this.renderDiscussions();
        }
    }

    likeDiscussion(discussionId) {
        const discussion = this.communityData.discussions.find(d => d.id === discussionId);
        if (discussion) {
            discussion.likes++;
            this.showNotification('Discussion liked!', 'success');
            this.renderDiscussions();
        }
    }

    renderAchievements() {
        const achievementCategories = document.getElementById('achievementCategories');
        if (!achievementCategories) return;

        achievementCategories.innerHTML = '';

        this.communityData.achievements.forEach(category => {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'achievement-category';

            let achievementsHTML = `<h3>${category.category}</h3><div class="achievement-list">`;
            
            category.achievements.forEach(achievement => {
                const isUnlocked = achievement.unlocked;
                const progressText = isUnlocked ? '✅ Unlocked' : 
                    achievement.progress ? `${achievement.progress}% Complete` : '🔒 Locked';

                achievementsHTML += `
                    <div class="achievement-item ${isUnlocked ? 'unlocked' : ''}">
                        <div class="achievement-icon ${isUnlocked ? 'celebration' : ''}">${achievement.icon}</div>
                        <div class="achievement-name">${achievement.name}</div>
                        <div class="achievement-description">${achievement.description}</div>
                        <div class="achievement-progress">${progressText}</div>
                        ${achievement.requirement ? `<div class="achievement-requirement">${achievement.requirement}</div>` : ''}
                    </div>
                `;
            });

            achievementsHTML += '</div>';
            categoryDiv.innerHTML = achievementsHTML;
            achievementCategories.appendChild(categoryDiv);
        });
    }

    renderLeaderboard() {
        const leaderboardList = document.getElementById('leaderboardList');
        if (!leaderboardList) return;

        leaderboardList.innerHTML = '';

        this.communityData.leaderboard.forEach((farmer, index) => {
            const leaderboardItem = document.createElement('div');
            leaderboardItem.className = 'leaderboard-item enhanced-card';

            const rankClass = farmer.rank === 1 ? 'first' : farmer.rank === 2 ? 'second' : farmer.rank === 3 ? 'third' : '';

            leaderboardItem.innerHTML = `
                <div class="leaderboard-rank ${rankClass}">${farmer.rank}</div>
                <div class="leaderboard-avatar">${farmer.avatar}</div>
                <div class="leaderboard-info">
                    <div class="leaderboard-name">${farmer.name}</div>
                    <div class="leaderboard-score">${farmer.location}</div>
                </div>
                <div class="leaderboard-points">${farmer.points} pts</div>
            `;

            leaderboardList.appendChild(leaderboardItem);
        });
    }

    switchLeaderboard(type) {
        const leaderboardBtns = document.querySelectorAll('.leaderboard-category');
        leaderboardBtns.forEach(btn => btn.classList.remove('active'));

        const activatedLeaderboardBtn = Array.from(leaderboardBtns).find(b => {
            const onclickAttr = b.getAttribute('onclick') || '';
            return onclickAttr.includes(`'${type}'`) || onclickAttr.includes(`"${type}"`);
        });
        if (activatedLeaderboardBtn) activatedLeaderboardBtn.classList.add('active');

        // In a real app, this would load different leaderboard data
        this.showNotification(`Switched to ${type} leaderboard`, 'info');
    }

    refreshCommunity() {
        this.showNotification('Community data refreshed!', 'success');
        this.renderCommunitySection();
    }

    // Enhanced Account Section
    renderAccountSection() {
        this.renderProfileTab();
        this.renderAvatarTab();
        this.renderSettingsTab();
    }

    showAccountTab(tabName) {
        const accountTabs = document.querySelectorAll('.account-tab');
        accountTabs.forEach(tab => tab.classList.remove('active'));

        const activatedAccountTab = Array.from(accountTabs).find(t => {
            const onclickAttr = t.getAttribute('onclick') || '';
            return onclickAttr.includes(`'${tabName}'`) || onclickAttr.includes(`"${tabName}"`);
        });
    if (activatedAccountTab) activatedAccountTab.classList.add('active');
    // Add contrast class to animate text color for better visibility
    document.querySelectorAll('.account-tab').forEach(t => t.classList.remove('contrast'));
    if (activatedAccountTab) activatedAccountTab.classList.add('contrast');

        // Toggle active class and ensure visible display for account content
        document.querySelectorAll('.account-content').forEach(content => {
            content.classList.remove('active');
            // hide non-active sections to avoid accidental overlap
            content.style.display = 'none';
        });
        const activeEl = document.getElementById(tabName + 'Tab');
        if (activeEl) {
            activeEl.classList.add('active');
            activeEl.style.display = '';
        }
        
        this.currentAccountTab = tabName;

        if (tabName === 'profile') {
            this.renderProfileTab();
        } else if (tabName === 'avatar') {
            this.renderAvatarTab();
        } else if (tabName === 'settings') {
            this.renderSettingsTab();
        }
        // Ensure floating label overlay updates to keep label visible above any background pills
        try {
            this._ensureFloatingTabLabel(activatedAccountTab || null);
        } catch (e) {
            console.warn('Floating tab label error', e);
        }
    }

    // Create or update a floating label that sits above the background pill so the tab text
    // is always readable regardless of stacking issues or pseudo-element overlays.
    _ensureFloatingTabLabel(tabButton) {
        const id = 'floating-account-tab-label';
        let el = document.getElementById(id);
        if (!tabButton) {
            if (el) el.style.display = 'none';
            return;
        }

        const rect = tabButton.getBoundingClientRect();
        const text = tabButton.textContent || tabButton.innerText || '';

        if (!el) {
            el = document.createElement('div');
            el.id = id;
            el.className = 'floating-account-tab-label';
            document.body.appendChild(el);
        }
        el.style.display = 'block';
        el.textContent = text.trim();

        // Position the floating label centered over the tab button
        el.style.position = 'fixed';
        el.style.left = (rect.left + window.scrollX) + 'px';
        el.style.top = (rect.top + window.scrollY) + 'px';
        el.style.width = rect.width + 'px';
        el.style.height = rect.height + 'px';
        el.style.lineHeight = rect.height + 'px';
        el.style.transform = 'translateY(0)';
        el.style.textAlign = 'center';
        el.style.pointerEvents = 'none';
        el.style.zIndex = 999999; // very high to avoid stacking conflicts
        // For accessibility, replicate font and sizing from the tab
        const style = window.getComputedStyle(tabButton);
        el.style.fontSize = style.fontSize;
        el.style.fontWeight = style.fontWeight;
        el.style.fontFamily = style.fontFamily;
        el.style.padding = style.padding;
        el.style.borderRadius = style.borderRadius;
        el.style.background = 'transparent';
        el.style.color = '#000';
        el.style.whiteSpace = 'nowrap';
        el.style.overflow = 'hidden';
        el.style.textOverflow = 'ellipsis';
    }

    renderProfileTab() {
        console.debug('renderProfileTab called, currentUser:', this.currentUser);
        // Use safe fallback data when currentUser is missing
        const user = this.currentUser || (this.accountData && this.accountData.personalInfo) || {};
        this.updateElementValue('profileName', this.sanitizeValue(user.name, ''));
        this.updateElementValue('profileEmail', this.sanitizeValue(user.email, ''));
        this.updateElementValue('profilePhone', this.sanitizeValue(user.phone, ''));
        this.updateElementValue('profileLocation', this.sanitizeValue(user.location, ''));
        this.updateElementValue('profileFarmSize', this.sanitizeValue(user.farmSize || user.farm_size, ''));
        this.updateElementValue('profileExperience', this.sanitizeValue(user.farmingExperience || user.farming_experience, ''));
        this.updateElementValue('profileCrops', this.sanitizeValue((user.primaryCrops || user.primary_crops || []).join(', '), ''));
        this.updateElementValue('profileWaterSource', this.sanitizeValue(user.waterSource || user.water_source, 'borewell'));

        // Update avatar display
        this.updateProfileAvatar();

        // Ensure profile summary area exists and is populated
        try {
            const profileEl = document.getElementById('profileTab');
            if (profileEl) {
                profileEl.style.minHeight = profileEl.style.minHeight || '200px';
                let summary = profileEl.querySelector('.profile-summary');
                if (!summary) {
                    summary = document.createElement('div');
                    summary.className = 'profile-summary enhanced-card';
                    summary.style.marginBottom = '12px';
                    profileEl.prepend(summary);
                }
                const lastLogin = (this.currentUser && this.currentUser.last_login) ? new Date(this.currentUser.last_login).toLocaleString() : 'Never';
                const memberSince = (this.currentUser && this.currentUser.created_at) ? new Date(this.currentUser.created_at).toLocaleDateString() : 'Unknown';
                summary.innerHTML = `
                    <div class="profile-summary-grid">
                        <div><strong>Member Since</strong><div>${memberSince}</div></div>
                        <div><strong>Last Login</strong><div>${lastLogin}</div></div>
                        <div><strong>Account Status</strong><div>${this.currentUser?.is_active ? 'Active' : 'Inactive'}</div></div>
                    </div>
                `;
            }
        } catch (e) { console.warn('profile summary error', e); }
    }

    renderAvatarTab() {
        console.debug('renderAvatarTab called, currentUser.avatar:', this.currentUser?.avatar);
        const avatarOptionsGrid = document.getElementById('avatarOptionsGrid');
        if (!avatarOptionsGrid) return;
        // Ensure we have accountData and avatar options; fallback to default set if missing
        const avatars = (this.accountData && Array.isArray(this.accountData.avatarOptions) && this.accountData.avatarOptions.length) ? this.accountData.avatarOptions : [
            { id: 'cow', name: 'Gau Mata', type: 'Dairy Specialist', emoji: '🐄' },
            { id: 'chicken', name: 'Murgi', type: 'Poultry Expert', emoji: '🐔' }
        ];

        avatarOptionsGrid.innerHTML = '';

        avatars.forEach(avatar => {
            const avatarOption = document.createElement('div');
            avatarOption.className = `avatar-option enhanced-card ${avatar.id === this.currentUser?.avatar?.id ? 'selected' : ''}`;
            avatarOption.dataset.avatarId = avatar.id;

            avatarOption.innerHTML = `
                <div class="avatar-option-icon">${avatar.emoji || '🐄'}</div>
                <div class="avatar-option-name">${avatar.name || 'Companion'}</div>
                <div class="avatar-option-type">${avatar.type || 'Farm Helper'}</div>
            `;

            avatarOption.addEventListener('click', () => this.selectAvatar(avatar));
            avatarOptionsGrid.appendChild(avatarOption);
        });

        this.renderCustomizationOptions();
        this.updateAvatarPreview();
        try {
            const avatarEl = document.getElementById('avatarTab');
            if (avatarEl) {
                avatarEl.style.minHeight = avatarEl.style.minHeight || '200px';

                // ensure Save and Reset buttons are present
                let actions = avatarEl.querySelector('.avatar-actions');
                if (!actions) {
                    actions = document.createElement('div');
                    actions.className = 'avatar-actions';
                    actions.style.marginTop = '12px';
                    actions.innerHTML = `
                        <button class="btn btn--primary enhanced-btn" id="saveAvatarBtn">💾 Save Avatar</button>
                        <button class="btn btn--outline enhanced-btn" id="resetAvatarBtn">♻️ Reset Avatar</button>
                    `;
                    avatarEl.appendChild(actions);
                    // attach handlers
                    actions.querySelector('#saveAvatarBtn').addEventListener('click', () => this.saveAvatar());
                    actions.querySelector('#resetAvatarBtn').addEventListener('click', () => this.resetAvatar());
                }
            }
        } catch (e) { console.warn('avatar actions error', e); }
    }

    saveAvatar() {
        // In a real app, persist to server. For now, show a success toast and update UI
        this.showNotification(`Avatar saved: ${this.currentUser?.avatar?.name || 'Custom'}`, 'success');
        // Optionally persist to localStorage for session
        try { localStorage.setItem('selectedAvatar', JSON.stringify(this.currentUser.avatar)); } catch (e) {}
    }

    resetAvatar() {
        const defaultAvatar = (this.accountData && this.accountData.avatarOptions && this.accountData.avatarOptions[0]) || { id: 'cow', name: 'Gau Mata', emoji: '🐄' };
        this.selectAvatar(defaultAvatar);
        this.showNotification('Avatar reset to default', 'info');
    }

    renderCustomizationOptions() {
        const customizationOptions = document.getElementById('customizationOptions');
        if (!customizationOptions) return;

        const accessories = ['🎩', '👒', '🌺', '🔔', '🎀', '💍', '⭕', '🏷️'];
        
        customizationOptions.innerHTML = '';

        accessories.forEach(accessory => {
            const option = document.createElement('div');
            option.className = 'customization-option';
            option.textContent = accessory;
            option.addEventListener('click', () => this.selectCustomization(accessory));
            customizationOptions.appendChild(option);
        });
    }

    selectAvatar(avatar) {
        // Update selection visual
        document.querySelectorAll('.avatar-option').forEach(option => {
            option.classList.remove('selected');
        });
        document.querySelector(`[data-avatar-id="${avatar.id}"]`).classList.add('selected');

        // Update current user avatar
        this.currentUser.avatar = avatar;
        this.selectedAvatar = avatar;

        // Update preview
        this.updateAvatarPreview();
        this.updateProfileAvatar();

        this.showNotification(`Avatar changed to ${avatar.name}!`, 'success');
    }

    selectCustomization(accessory) {
        // Update selection visual
        const options = document.querySelectorAll('.customization-option');
        options.forEach(option => option.classList.remove('selected'));

        // Find the option element whose text matches the accessory and mark it selected
        const matched = Array.from(options).find(o => (o.textContent || '').trim() === (accessory || '').trim());
        if (matched) matched.classList.add('selected');

        // Store customization
        if (!this.currentUser.avatar.customization) {
            this.currentUser.avatar.customization = {};
        }
        this.currentUser.avatar.customization.accessory = accessory;

        this.updateAvatarPreview();
        this.showNotification('Customization applied!', 'success');
    }

    updateAvatarPreview() {
        const preview = document.getElementById('selectedAvatarPreview');
        const name = document.getElementById('selectedAvatarName');
        const type = document.getElementById('selectedAvatarType');

        const avatar = this.currentUser?.avatar || {};

        if (preview) {
            preview.textContent = avatar.emoji || '🐄';
            const avatarId = avatar.id || 'cow';
            preview.className = `animal-character ${avatarId}-avatar breathing`;
        }

        if (name) {
            name.textContent = avatar.name || 'Gau Mata';
        }

        if (type) {
            type.textContent = avatar.type || 'Farm Companion';
        }
    }

    updateProfileAvatar() {
        const profileAvatar = document.getElementById('profileAvatarEdit');
        const avatar = this.currentUser?.avatar || { id: 'cow', emoji: '🐄' };
        const avatarId = avatar?.id || 'cow';
        const avatarEmoji = avatar?.emoji || '🐄';
        if (profileAvatar) {
            profileAvatar.innerHTML = `<div class="animal-character ${avatarId}-avatar breathing">${avatarEmoji}</div>`;
        }

        // Update dashboard avatar too
        const dashboardAvatar = document.getElementById('dashboardAvatar');
        if (dashboardAvatar) {
            dashboardAvatar.innerHTML = `<div class="animal-character ${avatarId}-avatar breathing">${avatarEmoji}</div>`;
        }
    }

    renderSettingsTab() {
        console.debug('renderSettingsTab called, currentUser.settings:', this.currentUser?.settings);
        // Update settings form with current values
        const settings = this.currentUser.settings;

        this.updateElementValue('questReminders', settings.notifications?.questReminders, 'checkbox');
        this.updateElementValue('communityUpdates', settings.notifications?.communityUpdates, 'checkbox');
        this.updateElementValue('weatherAlerts', settings.notifications?.weatherAlerts, 'checkbox');
        this.updateElementValue('achievementNotifications', settings.notifications?.achievementNotifications, 'checkbox');

        this.updateElementValue('profileVisibility', settings.privacy?.profileVisibility);
        this.updateElementValue('achievementSharing', settings.privacy?.achievementSharing, 'checkbox');
        this.updateElementValue('progressSharing', settings.privacy?.progressSharing, 'checkbox');
        this.updateElementValue('locationSharing', settings.privacy?.locationSharing, 'checkbox');

        this.updateElementValue('languageSetting', settings.preferences?.language);
        this.updateElementValue('themeSetting', settings.preferences?.theme);
    }

    saveProfile() {
        // Get updated values from form
        this.currentUser.name = this.getElementValue('profileName');
        this.currentUser.email = this.getElementValue('profileEmail');
        this.currentUser.phone = this.getElementValue('profilePhone');
        this.currentUser.location = this.getElementValue('profileLocation');
        this.currentUser.farmSize = this.getElementValue('profileFarmSize');
        this.currentUser.farmingExperience = this.getElementValue('profileExperience');
        this.currentUser.primaryCrops = this.getElementValue('profileCrops').split(',').map(c => c.trim());
        this.currentUser.waterSource = this.getElementValue('profileWaterSource');

        // Save settings
        if (!this.currentUser.settings) this.currentUser.settings = { notifications: {}, privacy: {}, preferences: {} };

        this.currentUser.settings.notifications.questReminders = this.getElementValue('questReminders', 'checkbox');
        this.currentUser.settings.notifications.communityUpdates = this.getElementValue('communityUpdates', 'checkbox');
        this.currentUser.settings.notifications.weatherAlerts = this.getElementValue('weatherAlerts', 'checkbox');
        this.currentUser.settings.notifications.achievementNotifications = this.getElementValue('achievementNotifications', 'checkbox');

        this.currentUser.settings.privacy.profileVisibility = this.getElementValue('profileVisibility');
        this.currentUser.settings.privacy.achievementSharing = this.getElementValue('achievementSharing', 'checkbox');
        this.currentUser.settings.privacy.progressSharing = this.getElementValue('progressSharing', 'checkbox');
        this.currentUser.settings.privacy.locationSharing = this.getElementValue('locationSharing', 'checkbox');

        this.currentUser.settings.preferences.language = this.getElementValue('languageSetting');
        this.currentUser.settings.preferences.theme = this.getElementValue('themeSetting');

        // Show success notification - this was missing before
        this.showNotification('Profile saved successfully! All changes have been updated.', 'success');
        this.updateUserInterface();
    }

    exportData() {
        const userData = {
            profile: this.currentUser,
            learningProgress: this.learningData.stats,
            achievements: this.communityData.achievements,
            exportDate: new Date().toISOString()
        };

        const dataStr = JSON.stringify(userData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `ecofarm-quest-data-${new Date().toISOString().split('T')[0]}.json`;
        link.click();

        URL.revokeObjectURL(url);
        this.showNotification('Data exported successfully!', 'success');
    }

    exportUserData() {
        this.exportData();
    }

    createBackup() {
        this.exportData();
        this.showNotification('Backup created and downloaded!', 'success');
    }

    restoreData() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const userData = JSON.parse(e.target.result);
                    // In a real app, validate and restore data
                    this.showNotification('Data restored successfully!', 'success');
                } catch (error) {
                    this.showNotification('Invalid backup file!', 'error');
                }
            };
            reader.readAsText(file);
        };
        input.click();
    }

    resetAllProgress() {
        if (confirm('Are you sure you want to reset all progress? This cannot be undone.')) {
            // Reset learning progress
            this.learningData.courses.forEach(course => {
                course.progress = 0;
                course.completed = 0;
            });
            this.learningData.stats.completedCourses = 0;
            this.learningData.stats.completedLessons = 0;
            this.learningData.stats.knowledgePoints = 0;
            this.learningData.stats.certificates = 0;

            // Reset achievements
            this.communityData.achievements.forEach(category => {
                category.achievements.forEach(achievement => {
                    achievement.unlocked = false;
                    achievement.progress = 0;
                });
            });

            this.showNotification('All progress reset successfully!', 'success');
            this.updateUserInterface();
        }
    }

    deleteAccount() {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            if (confirm('This will permanently delete all your data. Type "DELETE" to confirm.')) {
                this.showNotification('Account deletion initiated. You will be logged out.', 'info');
                setTimeout(() => {
                    this.showScreen('welcomeScreen');
                }, 2000);
            }
        }
    }

    toggleFAQ(element) {
        const faqItem = element.parentElement;
        faqItem.classList.toggle('open');
    }

    contactSupport(type) {
        const messages = {
            email: 'Email support form opened!',
            chat: 'Live chat started!',
            phone: 'Calling support...'
        };
        this.showNotification(messages[type] || 'Support contact initiated', 'info');
    }

    showTutorial() {
        this.showNotification('Tutorial opened in new window!', 'info');
    }

    showLogoutConfirmation() {
        document.getElementById('logoutModal').classList.remove('hidden');
    }

    confirmLogout() {
        this.closeModal('logoutModal');
        this.showNotification('Logged out successfully!', 'success');
        this.currentUser = null;
        this.clearSession();
        // Optional: reset in-memory demo data to avoid leaking prev state
        this.learningData = null;
        this.communityData = null;
        this.accountData = null;
        setTimeout(() => {
            this.showScreen('welcomeScreen');
        }, 1000);
    }

    // Utility Methods
    updateUserInterface() {
        if (!this.currentUser) return;

        // Update user info displays
    this.updateElementText('farmerName', this.sanitizeValue(this.currentUser.name?.split(' ')[0], 'Farmer'));
    this.updateElementText('farmerLevel', this.sanitizeValue(this.currentUser.learningStats?.currentLevel, 1));
    this.updateElementText('farmerTitle', this.sanitizeValue(this.getLevelTitle(this.currentUser.learningStats?.currentLevel || 1), 'Farmer'));

        // Update learning stats
        if (this.currentUser.learningStats) {
            this.updateLearningStats();
        }

        // Update avatar displays
        this.updateProfileAvatar();
    }

    getLevelTitle(level) {
        const titles = {
            1: 'Beginner Farmer',
            2: 'Sprouting Farmer', 
            3: 'Growing Farmer',
            4: 'Sustainable Farmer',
            5: 'Eco Master'
        };
        return titles[level] || 'Expert Farmer';
    }

    updateElementText(id, text) {
        const element = document.getElementById(id);
        if (element) element.textContent = text;
    }

    sanitizeValue(value, fallback = '') {
        // Avoid rendering the literal strings 'undefined' or 'null' which may come from malformed data
        if (value === undefined || value === null) return fallback;
        if (typeof value === 'string' && (value.trim() === '' || value.trim().toLowerCase() === 'undefined' || value.trim().toLowerCase() === 'null')) return fallback;
        return value;
    }

    updateElementValue(id, value, type = 'text') {
        const element = document.getElementById(id);
        if (!element) return;

        if (type === 'checkbox') {
            element.checked = Boolean(value);
        } else {
            element.value = value || '';
        }
    }

    getElementValue(id, type = 'text') {
        const element = document.getElementById(id);
        if (!element) return null;

        if (type === 'checkbox') {
            return element.checked;
        } else {
            return element.value;
        }
    }

    updateProgressBar(id, percentage) {
        const bar = document.getElementById(id);
        if (bar) {
            bar.style.width = Math.max(0, Math.min(100, percentage)) + '%';
        }
    }

    // Modal Management
    showModal(title, content) {
        // Create a generic modal if it doesn't exist
        let modal = document.getElementById('customModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'customModal';
            modal.className = 'modal hidden';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 id="customModalTitle">${title}</h3>
                        <button class="modal-close enhanced-btn" onclick="app.closeModal('customModal')">×</button>
                    </div>
                    <div class="modal-body" id="customModalBody">
                        ${content}
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        } else {
            document.getElementById('customModalTitle').textContent = title;
            document.getElementById('customModalBody').innerHTML = content;
        }

        modal.classList.remove('hidden');
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
        }
    }

    // Notifications
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${this.getNotificationIcon(type)}</span>
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Add styles if not already present
        if (!document.getElementById('notificationStyles')) {
            const styles = document.createElement('style');
            styles.id = 'notificationStyles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    z-index: 3000;
                    background: var(--color-surface);
                    border: 2px solid var(--color-border);
                    border-radius: var(--radius-base);
                    padding: var(--space-16);
                    box-shadow: var(--shadow-lg);
                    animation: slideInRight 0.3s ease;
                    max-width: 400px;
                }
                .notification.success { border-color: var(--color-success); }
                .notification.error { border-color: var(--color-error); }
                .notification.warning { border-color: var(--color-warning); }
                .notification.info { border-color: var(--color-info); }
                .notification-content {
                    display: flex;
                    align-items: center;
                    gap: var(--space-8);
                }
                .notification-message { flex: 1; }
                .notification-close {
                    background: none;
                    border: none;
                    cursor: pointer;
                    font-size: var(--font-size-lg);
                }
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || 'ℹ️';
    }

    showAchievement(title, description, icon) {
        document.getElementById('achievementName').textContent = title;
        document.getElementById('achievementDescription').textContent = description;
        document.getElementById('achievementIcon').textContent = icon;
        
        const modal = document.getElementById('achievementModal');
        modal.classList.remove('hidden');

        // Add celebration animation
        const iconEl = document.getElementById('achievementIcon');
        iconEl.classList.add('celebration');
        setTimeout(() => iconEl.classList.remove('celebration'), 2000);
    }
}

// Global functions for onclick handlers
window.showScreen = (screenId) => app.showScreen(screenId);
window.switchAuthTab = (tabName) => app.switchAuthTab(tabName);
window.showDashboardSection = (sectionId) => app.showDashboardSection(sectionId);
window.showCommunityTab = (tabName) => app.showCommunityTab(tabName);
window.showAccountTab = (tabName) => app.showAccountTab(tabName);
window.filterCourses = (category) => app.filterCourses(category);
window.switchLeaderboard = (type) => app.switchLeaderboard(type);
window.closeModal = (modalId) => app.closeModal(modalId);
window.toggleFAQ = (element) => app.toggleFAQ(element);
window.createNewPost = () => app.createNewPost();
window.saveProfile = () => app.saveProfile();
window.exportData = () => app.exportData();
window.exportUserData = () => app.exportUserData();
window.createBackup = () => app.createBackup();
window.restoreData = () => app.restoreData();
window.resetAllProgress = () => app.resetAllProgress();
window.deleteAccount = () => app.deleteAccount();
window.contactSupport = (type) => app.contactSupport(type);
window.showTutorial = () => app.showTutorial();
window.showLogoutConfirmation = () => app.showLogoutConfirmation();
window.confirmLogout = () => app.confirmLogout();
window.showCertificates = () => app.showCertificates();
window.continueLearning = () => app.continueLearning();
window.refreshCommunity = () => app.refreshCommunity();

// Initialize app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', function() {
    app = new EnhancedEcoFarmQuest();
    
    // Add any demo functions for testing
    window.app = app; // Make app globally available for debugging
    
    console.log('🌱 Enhanced EcoFarm Quest fully loaded!');
    console.log('Features available:');
    console.log('- Interactive Learning Hub with courses and quizzes');
    console.log('- Working Community Discussions and Achievements');
    console.log('- Comprehensive Account Management');
    console.log('- Real-time notifications and progress tracking');
    console.log('🐛 Bug fixes applied:');
    console.log('- Fixed new post creation functionality');
    console.log('- Added save profile confirmation notifications');
    // ✅ Wait until HTML is fully loaded before initializing
window.addEventListener('DOMContentLoaded', () => {
  window.app = new EnhancedEcoFarmQuest();

  // Expose key methods globally (for onclick handlers)


  window.showAccountTab = (tab) => app.showAccountTab(tab);
  window.exportUserData = () => app.exportUserData?.();
  window.createBackup = () => app.createBackup?.();
  window.restoreData = () => app.restoreData?.();
  window.resetAllProgress = () => app.resetAllProgress?.();
  window.deleteAccount = () => app.deleteAccount?.();
  window.contactSupport = (type) => app.contactSupport?.(type);
  window.showTutorial = () => app.showTutorial?.();
  window.showLogoutConfirmation = () => app.showLogoutConfirmation?.();
  window.toggleFAQ = (el) => app.toggleFAQ?.(el);
});
});