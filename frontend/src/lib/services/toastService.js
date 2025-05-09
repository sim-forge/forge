import { writable } from 'svelte/store';
import { v4 as uuidv4 } from 'uuid';

// Create toast store
const createToastStore = () => {
  const { subscribe, update } = writable([]);
  
  return {
    subscribe,
    
    // Add a new toast
    add: (toast) => {
      const id = toast.id || uuidv4();
      const newToast = {
        id,
        type: toast.type || 'info',
        message: toast.message || '',
        title: toast.title || '',
        duration: toast.duration !== undefined ? toast.duration : 5000,
        position: toast.position || 'top-right',
        showIcon: toast.showIcon !== undefined ? toast.showIcon : true,
        showCloseButton: toast.showCloseButton !== undefined ? toast.showCloseButton : true,
        showProgress: toast.showProgress !== undefined ? toast.showProgress : true,
        pauseOnHover: toast.pauseOnHover !== undefined ? toast.pauseOnHover : true,
      };
      
      update(toasts => [...toasts, newToast]);
      
      return id;
    },
    
    // Remove a toast by ID
    remove: (id) => {
      update(toasts => toasts.filter(toast => toast.id !== id));
    },
    
    // Clear all toasts
    clear: () => {
      update(() => []);
    },
    
    // Shorthand methods for different toast types
    info: (message, options = {}) => {
      return toastStore.add({
        type: 'info',
        message,
        ...options
      });
    },
    
    success: (message, options = {}) => {
      return toastStore.add({
        type: 'success',
        message,
        ...options
      });
    },
    
    warning: (message, options = {}) => {
      return toastStore.add({
        type: 'warning',
        message,
        ...options
      });
    },
    
    error: (message, options = {}) => {
      return toastStore.add({
        type: 'error',
        message,
        ...options
      });
    }
  };
};

// Export the toast store
export const toastStore = createToastStore();