/**
 * API Integration Tests for EcoFarm Quest Frontend
 */

// Mock fetch globally
global.fetch = require('jest-fetch-mock');

describe('API Integration Tests', () => {
  let app;

  beforeEach(() => {
    fetch.resetMocks();
    localStorage.clear();
    app = new EnhancedEcoFarmQuest();
  });

  afterEach(() => {
    if (app) {
      app = null;
    }
  });

  describe('Authentication API', () => {
    test('should handle successful login API call', async () => {
      const mockResponse = {
        status: 'success',
        message: 'Login successful',
        data: {
          user: {
            id: '1',
            name: 'Test User',
            email: 'test@example.com',
            phone: '+1234567890',
            location: 'Test City',
            farm_size: '5 acres'
          },
          access_token: 'mock-jwt-token',
          refresh_token: 'mock-refresh-token'
        }
      };

      fetch.mockResponseOnce(JSON.stringify(mockResponse));

      // Mock /me endpoint
      const meResponse = {
        status: 'success',
        data: {
          user: {
            id: '1',
            name: 'Test User',
            email: 'test@example.com',
            phone: '+1234567890',
            location: 'Test City',
            farm_size: '5 acres',
            learning_stats: {
              total_courses: 5,
              completed_courses: 2,
              knowledge_points: 150,
              current_level: 3
            }
          }
        }
      };
      fetch.mockResponseOnce(JSON.stringify(meResponse));

      document.querySelector('#loginForm input[type="email"]').value = 'test@example.com';
      document.querySelector('#loginForm input[type="password"]').value = 'Test123456';

      await app.handleLogin();

      expect(fetch).toHaveBeenCalledTimes(2);
      expect(fetch).toHaveBeenCalledWith('/api/auth/login', expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        }),
        body: JSON.stringify({
          email: 'test@example.com',
          password: 'Test123456'
        })
      }));

      expect(app.accessToken).toBe('mock-jwt-token');
      expect(app.currentUser).toBeDefined();
      expect(app.currentUser.name).toBe('Test User');
    });

    test('should handle login API error', async () => {
      fetch.mockRejectOnce(new Error('Invalid credentials'));

      document.querySelector('#loginForm input[type="email"]').value = 'test@example.com';
      document.querySelector('#loginForm input[type="password"]').value = 'wrongpassword';

      await app.handleLogin();

      expect(app.accessToken).toBeNull();
      expect(app.currentUser).toBeNull();
    });

    test('should handle successful registration API call', async () => {
      const mockResponse = {
        status: 'success',
        message: 'User registered successfully',
        data: {
          user: {
            id: '2',
            name: 'New User',
            email: 'new@example.com',
            phone: '+1234567890',
            location: 'New City',
            farm_size: '10 acres'
          },
          access_token: 'mock-jwt-token',
          refresh_token: 'mock-refresh-token'
        }
      };

      fetch.mockResponseOnce(JSON.stringify(mockResponse));

      // Mock /me endpoint
      const meResponse = {
        status: 'success',
        data: {
          user: {
            id: '2',
            name: 'New User',
            email: 'new@example.com',
            phone: '+1234567890',
            location: 'New City',
            farm_size: '10 acres',
            learning_stats: {
              total_courses: 0,
              completed_courses: 0,
              knowledge_points: 0,
              current_level: 1
            }
          }
        }
      };
      fetch.mockResponseOnce(JSON.stringify(meResponse));

      document.querySelector('#registerForm input[name="name"]').value = 'New User';
      document.querySelector('#registerForm input[type="email"]').value = 'new@example.com';
      document.querySelector('#registerForm input[type="password"]').value = 'NewPass123';
      document.querySelector('#registerForm input[name="phone"]').value = '+1234567890';
      document.querySelector('#registerForm input[name="location"]').value = 'New City';
      document.querySelector('#registerForm input[name="farm_size"]').value = '10 acres';

      await app.handleRegister();

      expect(fetch).toHaveBeenCalledTimes(2);
      expect(fetch).toHaveBeenCalledWith('/api/auth/register', expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        }),
        body: JSON.stringify({
          name: 'New User',
          email: 'new@example.com',
          password: 'NewPass123',
          phone: '+1234567890',
          location: 'New City',
          farm_size: '10 acres'
        })
      }));

      expect(app.accessToken).toBe('mock-jwt-token');
      expect(app.currentUser).toBeDefined();
      expect(app.currentUser.name).toBe('New User');
    });

    test('should handle registration validation errors', async () => {
      const mockErrorResponse = {
        status: 'error',
        message: 'Password must be at least 8 characters long'
      };

      fetch.mockResponseOnce(JSON.stringify(mockErrorResponse), { status: 400 });

      document.querySelector('#registerForm input[name="name"]').value = 'Test User';
      document.querySelector('#registerForm input[type="email"]').value = 'test@example.com';
      document.querySelector('#registerForm input[type="password"]').value = 'weak';
      document.querySelector('#registerForm input[name="phone"]').value = '+1234567890';
      document.querySelector('#registerForm input[name="location"]').value = 'Test City';
      document.querySelector('#registerForm input[name="farm_size"]').value = '5 acres';

      await app.handleRegister();

      expect(app.accessToken).toBeNull();
      expect(app.currentUser).toBeNull();
    });
  });

  describe('User Profile API', () => {
    test('should fetch user profile with authentication', async () => {
      app.accessToken = 'mock-jwt-token';

      const mockResponse = {
        status: 'success',
        data: {
          user: {
            id: '1',
            name: 'Test User',
            email: 'test@example.com',
            phone: '+1234567890',
            location: 'Test City',
            farm_size: '5 acres',
            learning_stats: {
              total_courses: 5,
              completed_courses: 2,
              knowledge_points: 150,
              current_level: 3
            },
            settings: {
              notifications: {
                quest_reminders: true,
                community_updates: true
              }
            }
          }
        }
      };

      fetch.mockResponseOnce(JSON.stringify(mockResponse));

      const result = await app.apiGet('/api/auth/me');

      expect(fetch).toHaveBeenCalledWith('/api/auth/me', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer mock-jwt-token',
          'Content-Type': 'application/json'
        }
      });

      expect(result).toEqual(mockResponse);
    });

    test('should handle API errors gracefully', async () => {
      app.accessToken = 'invalid-token';

      fetch.mockRejectOnce(new Error('Unauthorized'));

      await expect(app.apiGet('/api/auth/me')).rejects.toThrow('Unauthorized');
    });
  });

  describe('Session Management', () => {
    test('should restore session from localStorage', async () => {
      localStorage.getItem.mockReturnValue('stored-token');

      const mockResponse = {
        status: 'success',
        data: {
          user: {
            id: '1',
            name: 'Stored User',
            email: 'stored@example.com'
          }
        }
      };

      fetch.mockResponseOnce(JSON.stringify(mockResponse));

      app.restoreSession();
      expect(app.accessToken).toBe('stored-token');

      // Simulate app initialization with stored token
      const me = await app.apiGet('/api/auth/me');
      expect(me.data.user.name).toBe('Stored User');
    });

    test('should clear session on logout', () => {
      app.accessToken = 'test-token';
      app.currentUser = { name: 'Test User' };

      app.clearSession();

      expect(app.accessToken).toBeNull();
      expect(localStorage.removeItem).toHaveBeenCalledWith('access_token');
    });
  });

  describe('Data Mapping', () => {
    test('should map server user data to client format', () => {
      const serverUser = {
        id: '1',
        name: 'Test User',
        email: 'test@example.com',
        phone: '+1234567890',
        location: 'Test City',
        farm_size: '5 acres',
        primary_crops: ['Rice', 'Wheat'],
        farming_experience: '5 years',
        water_source: 'borewell',
        learning_stats: {
          total_courses: 5,
          completed_courses: 2,
          knowledge_points: 150,
          current_level: 3
        },
        settings: {
          notifications: {
            quest_reminders: true
          }
        }
      };

      const clientUser = app.mapServerUserToClient(serverUser);

      expect(clientUser.id).toBe('1');
      expect(clientUser.name).toBe('Test User');
      expect(clientUser.email).toBe('test@example.com');
      expect(clientUser.phone).toBe('+1234567890');
      expect(clientUser.location).toBe('Test City');
      expect(clientUser.farmSize).toBe('5 acres');
      expect(clientUser.primaryCrops).toEqual(['Rice', 'Wheat']);
      expect(clientUser.farmingExperience).toBe('5 years');
      expect(clientUser.waterSource).toBe('borewell');
      expect(clientUser.learningStats).toEqual(serverUser.learning_stats);
      expect(clientUser.settings).toEqual(serverUser.settings);
    });

    test('should handle missing server fields gracefully', () => {
      const serverUser = {
        id: '1',
        name: 'Minimal User',
        email: 'minimal@example.com'
      };

      const clientUser = app.mapServerUserToClient(serverUser);

      expect(clientUser.id).toBe('1');
      expect(clientUser.name).toBe('Minimal User');
      expect(clientUser.email).toBe('minimal@example.com');
      expect(clientUser.phone).toBe('');
      expect(clientUser.location).toBe('');
      expect(clientUser.farmSize).toBe('');
      expect(clientUser.primaryCrops).toEqual([]);
      expect(clientUser.farmingExperience).toBe('');
      expect(clientUser.waterSource).toBe('');
    });
  });

  describe('Error Handling', () => {
    test('should handle network errors', async () => {
      fetch.mockRejectOnce(new Error('Network error'));

      await expect(app.apiGet('/api/test')).rejects.toThrow('Network error');
    });

    test('should handle HTTP error responses', async () => {
      fetch.mockResponseOnce('Unauthorized', { status: 401 });

      await expect(app.apiGet('/api/protected')).rejects.toThrow();
    });

    test('should handle malformed JSON responses', async () => {
      fetch.mockResponseOnce('Invalid JSON');

      await expect(app.apiGet('/api/test')).rejects.toThrow();
    });
  });
});
