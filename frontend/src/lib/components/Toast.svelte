<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { toastTransition } from '../transitions';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let id = '';
  export let type = 'info'; // info, success, warning, error
  export let message = '';
  export let title = '';
  export let duration = 5000; // ms
  export let position = 'top-right'; // top-right, top-left, bottom-right, bottom-left, top-center, bottom-center
  export let showIcon = true;
  export let showCloseButton = true;
  export let showProgress = true;
  export let pauseOnHover = true;
  
  // Local state
  let progress = 100;
  let interval;
  let isPaused = false;
  
  // Computed classes
  $: typeClass = getTypeClass(type);
  $: positionClass = getPositionClass(position);
  $: iconSvg = getIconSvg(type);
  
  // Helper functions
  function getTypeClass(type) {
    const types = {
      info: 'bg-primary-50 border-primary-500 text-primary-700',
      success: 'bg-success-50 border-success-500 text-success-700',
      warning: 'bg-warning-50 border-warning-500 text-warning-700',
      error: 'bg-error-50 border-error-500 text-error-700',
    };
    
    return types[type] || types.info;
  }
  
  function getPositionClass(position) {
    const positions = {
      'top-right': 'top-4 right-4',
      'top-left': 'top-4 left-4',
      'bottom-right': 'bottom-4 right-4',
      'bottom-left': 'bottom-4 left-4',
      'top-center': 'top-4 left-1/2 transform -translate-x-1/2',
      'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2',
    };
    
    return positions[position] || positions['top-right'];
  }
  
  function getIconSvg(type) {
    const icons = {
      info: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>`,
      success: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>`,
      warning: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>`,
      error: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>`,
    };
    
    return icons[type] || icons.info;
  }
  
  // Close toast
  function closeToast() {
    clearInterval(interval);
    dispatch('close', { id });
  }
  
  // Pause progress
  function pauseProgress() {
    if (pauseOnHover) {
      isPaused = true;
    }
  }
  
  // Resume progress
  function resumeProgress() {
    if (pauseOnHover) {
      isPaused = false;
    }
  }
  
  // Initialize progress timer
  onMount(() => {
    if (duration > 0) {
      const step = 100 / (duration / 10); // Update every 10ms
      
      interval = setInterval(() => {
        if (!isPaused) {
          progress -= step;
          
          if (progress <= 0) {
            clearInterval(interval);
            closeToast();
          }
        }
      }, 10);
      
      return () => clearInterval(interval);
    }
  });
</script>

<div
  class="toast fixed {positionClass} max-w-sm w-full shadow-md rounded-lg border-l-4 {typeClass} overflow-hidden"
  role="alert"
  aria-live="assertive"
  aria-atomic="true"
  on:mouseenter={pauseProgress}
  on:mouseleave={resumeProgress}
  in:fly={toastTransition.in}
  out:fade={toastTransition.out}
>
  <div class="p-4 flex">
    {#if showIcon}
      <div class="flex-shrink-0 mr-3">
        {@html iconSvg}
      </div>
    {/if}
    
    <div class="flex-1">
      {#if title}
        <div class="font-medium">{title}</div>
      {/if}
      
      <div class={title ? 'mt-1 text-sm' : ''}>
        {message}
      </div>
    </div>
    
    {#if showCloseButton}
      <button
        type="button"
        class="ml-4 flex-shrink-0 text-text-tertiary hover:text-text-secondary focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md"
        on:click={closeToast}
        aria-label="Close"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
  </div>
  
  {#if showProgress && duration > 0}
    <div class="h-1 bg-white bg-opacity-20">
      <div
        class="h-full bg-white"
        style="width: {progress}%"
      ></div>
    </div>
  {/if}
</div>

<style>
  .toast {
    z-index: 9999;
  }
</style>