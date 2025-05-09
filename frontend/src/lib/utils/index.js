/**
 * Utility functions for SimForge
 */

/**
 * Format date to a readable string
 * @param {Date|string} date - The date to format
 * @param {Object} options - Formatting options
 * @returns {string} - The formatted date
 */
export function formatDate(date, options = {}) {
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };
  
  const dateObj = date instanceof Date ? date : new Date(date);
  return dateObj.toLocaleDateString(undefined, { ...defaultOptions, ...options });
}

/**
 * Format a relative time
 * @param {Date} date - The date to format
 * @returns {string} - The formatted relative time
 */
export function formatRelativeTime(date) {
  if (!date) return '';
  
  const now = new Date();
  const dateObj = date instanceof Date ? date : new Date(date);
  const diffInSeconds = Math.floor((now - dateObj) / 1000);
  
  if (diffInSeconds < 60) {
    return 'just now';
  }
  
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return `${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''} ago`;
  }
  
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
  }
  
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 7) {
    return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
  }
  
  const diffInWeeks = Math.floor(diffInDays / 7);
  if (diffInWeeks < 4) {
    return `${diffInWeeks} week${diffInWeeks > 1 ? 's' : ''} ago`;
  }
  
  const diffInMonths = Math.floor(diffInDays / 30);
  if (diffInMonths < 12) {
    return `${diffInMonths} month${diffInMonths > 1 ? 's' : ''} ago`;
  }
  
  const diffInYears = Math.floor(diffInDays / 365);
  return `${diffInYears} year${diffInYears > 1 ? 's' : ''} ago`;
}

// Generate a random ID
export function generateId(length = 8) {
  return Math.random().toString(36).substring(2, 2 + length);
}

// Debounce function to limit how often a function can be called
export function debounce(func, wait = 300) {
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

// Throttle function to limit how often a function can be called
export function throttle(func, limit = 300) {
  let inThrottle;
  
  return function executedFunction(...args) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}

// Deep clone an object
export function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

// Check if two objects are equal
export function isEqual(obj1, obj2) {
  return JSON.stringify(obj1) === JSON.stringify(obj2);
}

// Truncate text with ellipsis
export function truncateText(text, maxLength = 100) {
  if (!text || text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

// Format number with commas
export function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Convert string to title case
export function toTitleCase(str) {
  return str.replace(
    /\w\S*/g,
    (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  );
}

// Get initials from a name
export function getInitials(name) {
  if (!name) return '';
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase();
}

// Convert hex color to rgba
export function hexToRgba(hex, alpha = 1) {
  if (!hex) return '';
  
  // Remove # if present
  hex = hex.replace('#', '');
  
  // Parse the hex values
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// Get contrast color (black or white) based on background color
export function getContrastColor(hexColor) {
  if (!hexColor) return '#000000';
  
  // Remove # if present
  hexColor = hexColor.replace('#', '');
  
  // Parse the hex values
  const r = parseInt(hexColor.substring(0, 2), 16);
  const g = parseInt(hexColor.substring(2, 4), 16);
  const b = parseInt(hexColor.substring(4, 6), 16);
  
  // Calculate luminance
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
  // Return black for bright colors, white for dark colors
  return luminance > 0.5 ? '#000000' : '#FFFFFF';
}

// Format bytes to human-readable size
export function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Download data as a file
export function downloadFile(data, filename, type = 'text/plain') {
  const blob = new Blob([data], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  
  // Clean up
  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 0);
}

// Copy text to clipboard
export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy text: ', err);
    return false;
  }
}

// Parse JSON safely
export function safeJsonParse(str, fallback = {}) {
  try {
    return JSON.parse(str);
  } catch (e) {
    return fallback;
  }
}

// Get random item from array
export function getRandomItem(array) {
  return array[Math.floor(Math.random() * array.length)];
}

// Shuffle array
export function shuffleArray(array) {
  const newArray = [...array];
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
  }
  return newArray;
}

// Group array by key
export function groupBy(array, key) {
  return array.reduce((result, item) => {
    const groupKey = typeof key === 'function' ? key(item) : item[key];
    (result[groupKey] = result[groupKey] || []).push(item);
    return result;
  }, {});
}

// Create a range of numbers
export function range(start, end) {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

// Wait for a specified time
export function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Check if object is empty
export function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

// Get URL parameters as an object
export function getUrlParams() {
  const params = new URLSearchParams(window.location.search);
  const result = {};
  
  for (const [key, value] of params.entries()) {
    result[key] = value;
  }
  
  return result;
}

// Format operation type for display
export function formatOperationType(type) {
  const typeMap = {
    'Reflect': '🤔 Reflect',
    'Plan': '📝 Plan',
    'Act': '🚀 Act',
    'Fork': '🔀 Fork'
  };
  
  return typeMap[type] || type;
}

// Get color for operation type
export function getOperationTypeColor(type, theme = 'light') {
  const colorMap = {
    light: {
      'Reflect': '#8b5cf6', // Purple
      'Plan': '#3b82f6',    // Blue
      'Act': '#10b981',     // Green
      'Fork': '#f59e0b'     // Amber
    },
    dark: {
      'Reflect': '#a78bfa', // Lighter purple for dark mode
      'Plan': '#60a5fa',    // Lighter blue for dark mode
      'Act': '#34d399',     // Lighter green for dark mode
      'Fork': '#fbbf24'     // Lighter amber for dark mode
    }
  };
  
  const themeColors = colorMap[theme] || colorMap.light;
  return themeColors[type] || '#6b7280'; // Default gray
}