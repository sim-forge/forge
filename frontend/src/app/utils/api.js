// API base URL
const API_BASE_URL = 'http://localhost:12000/api/v1';

/**
 * Handles API requests with standard error handling
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<any>} - Response data
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Default headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  try {
    const response = await fetch(url, {
      ...options,
      headers
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'API request failed');
    }
    
    return data;
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
}

/**
 * API client for SimForge
 */
export const api = {
  /**
   * Health check
   * @returns {Promise<Object>} Health status
   */
  healthCheck: () => apiRequest('/health'),
  
  /**
   * Generate cognition sequences
   * @param {Object} params - Generation parameters
   * @returns {Promise<Object>} Generated sequences
   */
  generateSequence: (params) => apiRequest('/cognition/generate', {
    method: 'POST',
    body: JSON.stringify(params)
  })
};