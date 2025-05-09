<script>
  import { onMount, setContext } from 'svelte';
  import { writable } from 'svelte/store';
  import { themes, defaultTheme } from './themes';
  
  // Create theme store
  const themeStore = writable(defaultTheme);
  
  // Set theme context for child components
  setContext('theme', themeStore);
  
  // Props
  export let initialTheme = 'light';
  
  // Local state
  let currentTheme = initialTheme;
  let mounted = false;
  
  // Set theme in localStorage and update CSS variables
  function setTheme(themeId) {
    const theme = themes[themeId] || defaultTheme;
    currentTheme = themeId;
    
    // Update store
    themeStore.set(theme);
    
    // Save to localStorage
    if (mounted && typeof localStorage !== 'undefined') {
      localStorage.setItem('simforge-theme', themeId);
    }
    
    // Apply CSS variables to document root
    if (typeof document !== 'undefined') {
      const root = document.documentElement;
      
      // Background colors
      root.style.setProperty('--bg-primary', theme.colors.background.primary);
      root.style.setProperty('--bg-secondary', theme.colors.background.secondary);
      root.style.setProperty('--bg-tertiary', theme.colors.background.tertiary);
      
      // Text colors
      root.style.setProperty('--text-primary', theme.colors.text.primary);
      root.style.setProperty('--text-secondary', theme.colors.text.secondary);
      root.style.setProperty('--text-tertiary', theme.colors.text.tertiary);
      root.style.setProperty('--text-inverse', theme.colors.text.inverse);
      
      // Border colors
      root.style.setProperty('--border-light', theme.colors.border.light);
      root.style.setProperty('--border-medium', theme.colors.border.medium);
      root.style.setProperty('--border-dark', theme.colors.border.dark);
      
      // Primary colors
      root.style.setProperty('--primary-50', theme.colors.primary[50]);
      root.style.setProperty('--primary-100', theme.colors.primary[100]);
      root.style.setProperty('--primary-200', theme.colors.primary[200]);
      root.style.setProperty('--primary-300', theme.colors.primary[300]);
      root.style.setProperty('--primary-400', theme.colors.primary[400]);
      root.style.setProperty('--primary-500', theme.colors.primary[500]);
      root.style.setProperty('--primary-600', theme.colors.primary[600]);
      root.style.setProperty('--primary-700', theme.colors.primary[700]);
      root.style.setProperty('--primary-800', theme.colors.primary[800]);
      root.style.setProperty('--primary-900', theme.colors.primary[900]);
      
      // Accent colors
      root.style.setProperty('--accent-500', theme.colors.accent[500]);
      
      // Status colors
      root.style.setProperty('--success-500', theme.colors.success[500]);
      root.style.setProperty('--warning-500', theme.colors.warning[500]);
      root.style.setProperty('--error-500', theme.colors.error[500]);
      
      // Shadow
      root.style.setProperty('--shadow-sm', theme.colors.shadow.sm);
      root.style.setProperty('--shadow-md', theme.colors.shadow.md);
      root.style.setProperty('--shadow-lg', theme.colors.shadow.lg);
      
      // Set data attribute for CSS selectors
      root.setAttribute('data-theme', themeId);
    }
  }
  
  // Initialize theme on mount
  onMount(() => {
    mounted = true;
    
    // Check for saved theme in localStorage
    if (typeof localStorage !== 'undefined') {
      const savedTheme = localStorage.getItem('simforge-theme');
      if (savedTheme && themes[savedTheme]) {
        currentTheme = savedTheme;
      }
    }
    
    // Check for system preference if no saved theme
    if (!currentTheme && typeof window !== 'undefined' && window.matchMedia) {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      currentTheme = prefersDark ? 'dark' : 'light';
    }
    
    // Set initial theme
    setTheme(currentTheme);
    
    // Listen for system theme changes
    if (typeof window !== 'undefined' && window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      
      const handleChange = (e) => {
        // Only change if user hasn't explicitly set a theme
        const savedTheme = localStorage.getItem('simforge-theme');
        if (!savedTheme) {
          setTheme(e.matches ? 'dark' : 'light');
        }
      };
      
      // Add event listener with compatibility for older browsers
      if (mediaQuery.addEventListener) {
        mediaQuery.addEventListener('change', handleChange);
      } else if (mediaQuery.addListener) {
        mediaQuery.addListener(handleChange);
      }
      
      return () => {
        // Clean up listener
        if (mediaQuery.removeEventListener) {
          mediaQuery.removeEventListener('change', handleChange);
        } else if (mediaQuery.removeListener) {
          mediaQuery.removeListener(handleChange);
        }
      };
    }
  });
  
  // Watch for theme changes from props
  $: if (mounted && initialTheme !== currentTheme) {
    setTheme(initialTheme);
  }
  
  // Expose theme functions to parent components
  export function toggleTheme() {
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    return nextTheme;
  }
  
  export function getTheme() {
    return currentTheme;
  }
</script>

<slot />

<style>
  :global(:root) {
    /* Default CSS variables (will be overridden by JS) */
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --bg-tertiary: #f3f4f6;
    
    --text-primary: #111827;
    --text-secondary: #374151;
    --text-tertiary: #6b7280;
    --text-inverse: #ffffff;
    
    --border-light: #e5e7eb;
    --border-medium: #d1d5db;
    --border-dark: #9ca3af;
    
    --primary-500: #1890ff;
    --accent-500: #8b5cf6;
    --success-500: #10b981;
    --warning-500: #f59e0b;
    --error-500: #ef4444;
    
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    
    /* Typography */
    --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --font-mono: 'JetBrains Mono', Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  }
  
  :global(body) {
    font-family: var(--font-sans);
    background-color: var(--bg-primary);
    color: var(--text-primary);
    transition: background-color 0.3s ease, color 0.3s ease;
    margin: 0;
    padding: 0;
  }
</style>