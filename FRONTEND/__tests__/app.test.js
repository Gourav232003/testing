/**
 * Jest tests for EcoFarm Quest Frontend Application
 */

// Mock the DOM environment
document.body.innerHTML = `
  <div id="app">
    <div id="welcomeScreen" class="screen active">
      <form id="loginForm">
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <form id="registerForm">
        <input type="text" name="name" placeholder="Name" />
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <input type="text" name="phone" placeholder="Phone" />
        <input type="text" name="location" placeholder="Location" />
        <input type="text" name="farm_size" placeholder="Farm Size" />
        <button type="submit">Register</button>
      </form>
    </div>
    <div id="dashboardScreen" class="screen">
      <div id="farmerName">Test User</div>
      <div id="farmerLevel">1</div>
    </div>
  </div>
`;

// Import the app after DOM is set up
const { EnhancedEcoFarmQuest } = require('../app.js');

describe('EcoFarm Quest Application', () => {
  let app;

  beforeEach(() => {
    // Reset fetch mock
    fetch.resetMocks();
    
    // Clear localStorage
    localStorage.clear();
    
    // Create new app instance
    app = new EnhancedEcoFarmQuest();
  });

  afterEach(() => {
    // Clean up
    if (app) {
      app = null;
    }
  });

  describe('Initialization', () => {
    test('should initialize with default values', () => {
      expect(app.currentScreen).toBe('welcomeScreen');
      expect(app.currentUser).toBeNull();
      expect(app.accessToken).toBeNull();
    });

    test('should load application data on init', async () => {
      await app.loadApplicationData();
      expect(app.learningData).toBeDefined();
      expect(app.communityData).toBeDefined();
      expect(app.accountData).toBeDefined();
    });
  });

  describe('Authentication', () => {
    test('should handle login with valid credentials', async () => {
      // Mock successful login response
      fetch.mockResponseOnce(JSON.stringify({
        status: 'success',
        data: {
          access_token: 'mock-token',
          user: {
            id: '1',
            name: 'Test User',
            email: 'test@example.com'
          }
        }
      }));

      // Mock successful /me response
      fetch.mockResponseOnce(JSON.stringify({
        status: 'success',
        data: {
          user: {
            id: '1',
            name: 'Test User',
            email: 'test@example.com',
            phone: '+1234567890',
            location: 'Test City',
            farm_size: '5 acres'
          }
        }
      }));

      // Set up form values
      document.querySelector('#loginForm input[type="email"]').value = 'test@example.com';
      document.querySelector('#loginForm input[type="password"]').value = 'Test123456';

      await app.handleLogin();

      expect(app.accessToken).toBe('mock-token');
      expect(app.currentUser).toBeDefined();
      expect(app.currentUser.name).toBe('Test User');
    });

    test('should handle login failure', async () => {
      // Mock failed login response
      fetch.mockRejectOnce(new Error('Invalid credentials'));

      document.querySelector('#loginForm input[type="email"]').value = 'test@example.com';
      document.querySelector('#loginForm input[type="password"]').value = 'wrongpassword';

      await app.handleLogin();

      expect(app.accessToken).toBeNull();
      expect(app.currentUser).toBeNull();
    });

    test('should handle registration with valid data', async () => {
      // Mock successful registration response
      fetch.mockResponseOnce(JSON.stringify({
        status: 'success',
        data: {
          access_token: 'mock-token',
          user: {
            id: '1',
            name: 'New User',
            email: 'new@example.com'
          }
        }
      }));

      // Mock successful /me response
      fetch.mockResponseOnce(JSON.stringify({
        status: 'success',
        data: {
          user: {
            id: '1',
            name: 'New User',
            email: 'new@example.com',
            phone: '+1234567890',
            location: 'New City',
            farm_size: '10 acres'
          }
        }
      }));

      // Set up form values
      document.querySelector('#registerForm input[name="name"]').value = 'New User';
      document.querySelector('#registerForm input[type="email"]').value = 'new@example.com';
      document.querySelector('#registerForm input[type="password"]').value = 'NewPass123';
      document.querySelector('#registerForm input[name="phone"]').value = '+1234567890';
      document.querySelector('#registerForm input[name="location"]').value = 'New City';
      document.querySelector('#registerForm input[name="farm_size"]').value = '10 acres';

      await app.handleRegister();

      expect(app.accessToken).toBe('mock-token');
      expect(app.currentUser).toBeDefined();
      expect(app.currentUser.name).toBe('New User');
    });

    test('should validate password strength', async () => {
      // Set up form with weak password
      document.querySelector('#registerForm input[name="name"]').value = 'Test User';
      document.querySelector('#registerForm input[type="email"]').value = 'test@example.com';
      document.querySelector('#registerForm input[type="password"]').value = 'weak';
      document.querySelector('#registerForm input[name="phone"]').value = '+1234567890';
      document.querySelector('#registerForm input[name="location"]').value = 'Test City';
      document.querySelector('#registerForm input[name="farm_size"]').value = '5 acres';

      await app.handleRegister();

      // Should not make API call with weak password
      expect(fetch).not.toHaveBeenCalled();
    });
  });

  describe('Session Management', () => {
    test('should store and retrieve session token', () => {
      const token = 'test-token';
      app.storeSession(token);
      expect(app.accessToken).toBe(token);
      expect(localStorage.setItem).toHaveBeenCalledWith('access_token', token);
    });

    test('should clear session on logout', () => {
      app.accessToken = 'test-token';
      app.currentUser = { name: 'Test User' };
      
      app.clearSession();
      
      expect(app.accessToken).toBeNull();
      expect(localStorage.removeItem).toHaveBeenCalledWith('access_token');
    });

    test('should restore session from localStorage', () => {
      localStorage.getItem.mockReturnValue('stored-token');
      app.restoreSession();
      expect(app.accessToken).toBe('stored-token');
    });
  });

  describe('API Requests', () => {
    test('should make authenticated API requests', async () => {
      app.accessToken = 'test-token';
      
      fetch.mockResponseOnce(JSON.stringify({ status: 'success' }));
      
      await app.apiGet('/api/test');
      
      expect(fetch).toHaveBeenCalledWith('/api/test', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer test-token',
          'Content-Type': 'application/json'
        }
      });
    });

    test('should handle API errors gracefully', async () => {
      fetch.mockRejectOnce(new Error('Network error'));
      
      await expect(app.apiGet('/api/test')).rejects.toThrow('Network error');
    });
  });

  describe('User Interface', () => {
    test('should update user interface elements', () => {
      app.currentUser = {
        name: 'John Doe',
        learningStats: { currentLevel: 5 }
      };
      
      app.updateUserInterface();
      
      expect(document.getElementById('farmerName').textContent).toBe('John');
      expect(document.getElementById('farmerLevel').textContent).toBe('5');
    });

    test('should show notifications', () => {
      app.showNotification('Test message', 'success');
      
      const notification = document.querySelector('.notification');
      expect(notification).toBeDefined();
      expect(notification.textContent).toContain('Test message');
    });
  });

  describe('Screen Navigation', () => {
    test('should switch between screens', () => {
      app.showScreen('dashboardScreen');
      expect(app.currentScreen).toBe('dashboardScreen');
      
      const dashboardScreen = document.getElementById('dashboardScreen');
      expect(dashboardScreen.classList.contains('active')).toBe(true);
    });
  });
});
