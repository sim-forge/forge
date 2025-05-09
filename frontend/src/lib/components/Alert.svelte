<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let type = 'info'; // info, success, warning, error
  export let title = '';
  export let message = '';
  export let dismissible = false;
  export let autoDismiss = false;
  export let autoDismissTimeout = 5000; // ms
  export let icon = true;
  export let variant = 'filled'; // filled, outlined, subtle
  export let actions = [];
  
  // Local state
  let timeoutId;
  
  // Computed classes
  $: typeClass = getTypeClass(type, variant);
  $: iconSvg = getIconSvg(type);
  
  // Helper functions
  function getTypeClass(type, variant) {
    const types = {
      filled: {
        info: 'bg-primary-500 text-white',
        success: 'bg-success-500 text-white',
        warning: 'bg-warning-500 text-white',
        error: 'bg-error-500 text-white',
      },
      outlined: {
        info: 'bg-transparent border border-primary-500 text-primary-700',
        success: 'bg-transparent border border-success-500 text-success-700',
        warning: 'bg-transparent border border-warning-500 text-warning-700',
        error: 'bg-transparent border border-error-500 text-error-700',
      },
      subtle: {
        info: 'bg-primary-50 text-primary-800 dark:bg-primary-900 dark:text-primary-200',
        success: 'bg-success-50 text-success-800 dark:bg-success-900 dark:text-success-200',
        warning: 'bg-warning-50 text-warning-800 dark:bg-warning-900 dark:text-warning-200',
        error: 'bg-error-50 text-error-800 dark:bg-error-900 dark:text-error-200',
      },
    };
    
    return types[variant]?.[type] || types.subtle.info;
  }
  
  function getIconSvg(type) {
    const icons = {
      info: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>`,
      success: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>`,
      warning: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>`,
      error: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>`,
    };
    
    return icons[type] || icons.info;
  }
  
  // Dismiss alert
  function dismiss() {
    dispatch('dismiss');
  }
  
  // Handle action click
  function handleActionClick(action) {
    if (action.onClick) {
      action.onClick();
    }
    
    if (action.dismiss) {
      dismiss();
    }
  }
  
  // Initialize auto-dismiss
  onMount(() => {
    if (autoDismiss) {
      timeoutId = setTimeout(dismiss, autoDismissTimeout);
    }
    
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  });
</script>

<div
  class="alert rounded-lg p-4 {typeClass}"
  role="alert"
  in:fly={{ y: -20, duration: 300 }}
  out:fade={{ duration: 200 }}
>
  <div class="flex">
    {#if icon}
      <div class="flex-shrink-0 mr-3">
        {@html iconSvg}
      </div>
    {/if}
    
    <div class="flex-1">
      {#if title}
        <h3 class="text-sm font-medium">{title}</h3>
      {/if}
      
      {#if message}
        <div class={title ? 'mt-1 text-sm opacity-90' : 'text-sm'}>
          {message}
        </div>
      {/if}
      
      <slot />
      
      {#if actions.length > 0}
        <div class="mt-3 flex space-x-2">
          {#each actions as action}
            <button
              type="button"
              class="inline-flex items-center px-3 py-1.5 text-xs font-medium rounded-md {action.variant === 'primary' ? 'bg-white bg-opacity-20 hover:bg-opacity-30' : 'bg-transparent hover:bg-white hover:bg-opacity-10'} focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
              on:click={() => handleActionClick(action)}
            >
              {action.label}
            </button>
          {/each}
        </div>
      {/if}
    </div>
    
    {#if dismissible}
      <div class="ml-auto pl-3">
        <button
          type="button"
          class="inline-flex rounded-md focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
          aria-label="Dismiss"
          on:click={dismiss}
        >
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    {/if}
  </div>
</div>