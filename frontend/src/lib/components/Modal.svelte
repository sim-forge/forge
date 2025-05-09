<script>
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  import { fade, scale } from 'svelte/transition';
  import { modalTransition } from '../transitions';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let open = false;
  export let title = '';
  export let size = 'md'; // sm, md, lg, xl, full
  export let closeOnEsc = true;
  export let closeOnClickOutside = true;
  export let showCloseButton = true;
  export let preventScroll = true;
  
  // Local state
  let modalElement;
  let previouslyFocused;
  
  // Computed classes
  $: sizeClass = getSizeClass(size);
  
  // Helper functions
  function getSizeClass(size) {
    const sizes = {
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
      xl: 'max-w-xl',
      '2xl': 'max-w-2xl',
      '3xl': 'max-w-3xl',
      '4xl': 'max-w-4xl',
      '5xl': 'max-w-5xl',
      '6xl': 'max-w-6xl',
      '7xl': 'max-w-7xl',
      full: 'max-w-full',
    };
    
    return sizes[size] || sizes.md;
  }
  
  // Close modal
  function closeModal() {
    open = false;
    dispatch('close');
  }
  
  // Handle click outside
  function handleClickOutside(event) {
    if (closeOnClickOutside && modalElement && !modalElement.contains(event.target)) {
      closeModal();
    }
  }
  
  // Handle keydown
  function handleKeydown(event) {
    if (closeOnEsc && event.key === 'Escape') {
      closeModal();
    }
  }
  
  // Prevent scroll on body when modal is open
  $: if (typeof document !== 'undefined') {
    if (open && preventScroll) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }
  
  // Focus trap and accessibility
  onMount(() => {
    if (open) {
      previouslyFocused = document.activeElement;
      
      // Set focus to the modal
      setTimeout(() => {
        const focusableElements = modalElement.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length > 0) {
          focusableElements[0].focus();
        } else {
          modalElement.focus();
        }
      }, 0);
    }
  });
  
  // Cleanup
  onDestroy(() => {
    if (typeof document !== 'undefined') {
      document.body.style.overflow = '';
    }
  });
  
  // Watch for open changes
  $: if (open && typeof document !== 'undefined') {
    previouslyFocused = document.activeElement;
    
    // Set focus to the modal
    setTimeout(() => {
      const focusableElements = modalElement?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      if (focusableElements?.length > 0) {
        focusableElements[0].focus();
      } else if (modalElement) {
        modalElement.focus();
      }
    }, 0);
  } else if (!open && previouslyFocused && typeof document !== 'undefined') {
    // Return focus to previously focused element
    previouslyFocused.focus();
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
  <div
    class="fixed inset-0 z-50 overflow-y-auto"
    aria-labelledby={title ? 'modal-title' : null}
    role="dialog"
    aria-modal="true"
  >
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-neutral-900 bg-opacity-50 transition-opacity"
      on:click={handleClickOutside}
      transition:fade={modalTransition.overlay}
    ></div>
    
    <!-- Modal container -->
    <div class="flex min-h-screen items-center justify-center p-4 text-center sm:p-0">
      <!-- Modal content -->
      <div
        bind:this={modalElement}
        class="relative transform overflow-hidden rounded-lg bg-bg-primary text-left shadow-xl transition-all w-full {sizeClass}"
        transition:scale={modalTransition.content}
        tabindex="-1"
      >
        {#if title || showCloseButton}
          <div class="flex items-center justify-between px-6 py-4 border-b border-border-light">
            {#if title}
              <h3 id="modal-title" class="text-lg font-medium text-text-primary">
                {title}
              </h3>
            {:else}
              <div></div>
            {/if}
            
            {#if showCloseButton}
              <button
                type="button"
                class="rounded-md bg-transparent text-text-tertiary hover:text-text-secondary focus:outline-none focus:ring-2 focus:ring-primary-500"
                on:click={closeModal}
                aria-label="Close"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            {/if}
          </div>
        {/if}
        
        <div class="px-6 py-4">
          <slot />
        </div>
        
        <slot name="footer">
          <!-- Default footer slot -->
        </slot>
      </div>
    </div>
  </div>
{/if}