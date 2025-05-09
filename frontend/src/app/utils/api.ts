/**
 * API utility for communicating with the SimForge backend
 */

// Base API URL - configurable for different environments
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Default request options
const defaultOptions: RequestInit = {
  headers: {
    'Content-Type': 'application/json',
  },
};

/**
 * Generic API request function
 */
async function request<T>(
  endpoint: string,
  method: string = 'GET',
  data?: any,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const requestOptions: RequestInit = {
    ...defaultOptions,
    ...options,
    method,
  };
  
  if (data) {
    requestOptions.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(url, requestOptions);
    
    // Handle non-JSON responses
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const json = await response.json();
      
      if (!response.ok) {
        throw new Error(json.detail || 'An error occurred');
      }
      
      return json as T;
    } else {
      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `HTTP error ${response.status}`);
      }
      
      return {} as T;
    }
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * API endpoints
 */
export const api = {
  // Health check
  health: () => request<{ status: string }>('/health'),
  
  // Cognition sequences
  generateSequence: (data: any) => 
    request<any>('/api/generate', 'POST', data),
  
  forkRow: (data: any) => 
    request<any>('/api/fork', 'POST', data),
  
  // Schemas
  getSchemas: () => 
    request<any[]>('/api/schemas'),
  
  getSchema: (id: string) => 
    request<any>(`/api/schemas/${id}`),
  
  // Prompts
  getPromptTemplates: () => 
    request<any[]>('/api/prompts'),
  
  getPromptTemplate: (id: string) => 
    request<any>(`/api/prompts/${id}`),
  
  savePromptTemplate: (data: any) => 
    request<any>('/api/prompts', 'POST', data),
};

export default api;