<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { slide } from 'svelte/transition';
  import { clickOutside } from '../utils/clickOutside';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let items = [];
  export let trigger = null;
  export let label = '';
  export let placement = 'bottom-start'; // top-start, top-end, bottom-start, bottom-end
  export let width = 'auto'; // auto, sm, md, lg, full
  export let maxHeight = '300px';
  export let showArrow = true;
  export let disabled = false;
  
  // Local state
  let isOpen = false;
  let dropdownContainer;
  
  // Computed classes
  $: placementClass = getPlacementClass(placement);
  $: widthClass = getWidthClass(width);
  
  // Helper functions
  function getPlacementClass(placement) {
    const placements = {
      'top-start': 'bottom-full left-0 mb-2',
      'top-end': 'bottom-full right-0 mb-2',
      'bottom-start': 'top-full left-0 mt-2',
      'bottom-end': 'top-full right-0 mt-2',
    };
    
    return placements[placement] || placements['bottom-start'];
  }
  
  function getWidthClass(width) {
    const widths = {
      auto: 'min-w-[200px]',
      sm: 'w-48',
      md: 'w-64',
      lg: 'w-80',
      full: 'w-full',
    };
    
    return widths[width] || widths.auto;
  }
  
  // Toggle dropdown
  function toggleDropdown() {
    if (!disabled) {
      isOpen = !isOpen;
    }
  }
  
  // Close dropdown
  function closeDropdown() {
    isOpen = false;
  }
  
  // Handle item click
  function handleItemClick(item) {
    if (item.disabled) return;
    
    dispatch('select', { item });
    
    if (!item.keepOpen) {
      closeDropdown();
    }
  }
  
  // Handle keydown
  function handleKeydown(event) {
    if (event.key === 'Escape') {
      closeDropdown();
    }
  }
  
  // Initialize component
  onMount(() => {
    // Add keydown listener
    window.addEventListener('keydown', handleKeydown);
    
    return () => {
      window.removeEventListener('keydown', handleKeydown);
    };
  });
</script>

<div
  class="dropdown-container relative inline-block"
  bind:this={dropdownContainer}
  use:clickOutside
  on:clickOutside={closeDropdown}
>
  {#if trigger}
    <div on:click={toggleDropdown} class:cursor-pointer={!disabled} class:opacity-60={disabled}>
      {trigger}
    </div>
  {:else}
    <button
      type="button"
      class="inline-flex items-center justify-between px-4 py-2 text-sm font-medium rounded-md border border-border-light bg-bg-primary text-text-primary hover:bg-bg-secondary focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors duration-200"
      class:opacity-60={disabled}
      class:cursor-not-allowed={disabled}
      disabled={disabled}
      on:click={toggleDropdown}
      aria-haspopup="true"
      aria-expanded={isOpen}
    >
      {label}
      
      {#if showArrow}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 -mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      {/if}
    </button>
  {/if}
  
  {#if isOpen}
    <div
      class="dropdown-menu absolute z-10 {placementClass} {widthClass} rounded-md shadow-lg bg-bg-primary border border-border-light overflow-hidden"
      transition:slide={{ duration: 200 }}
      style="max-height: {maxHeight}; overflow-y: auto;"
      role="menu"
      aria-orientation="vertical"
    >
      <div class="py-1">
        {#each items as item, index}
          {#if item.type === 'divider'}
            <div class="border-t border-border-light my-1" role="separator"></div>
          {:else if item.type === 'header'}
            <div class="px-4 py-2 text-xs font-semibold text-text-tertiary uppercase tracking-wider">
              {item.label}
            </div>
          {:else}
            <button
              type="button"
              class="w-full text-left px-4 py-2 text-sm {item.disabled ? 'opacity-50 cursor-not-allowed' : 'hover:bg-bg-secondary cursor-pointer'} {item.danger ? 'text-error-600' : 'text-text-primary'} focus:outline-none focus:bg-bg-secondary transition-colors duration-150"
              role="menuitem"
              disabled={item.disabled}
              on:click={() => handleItemClick(item)}
            >
              <div class="flex items-center">
                {#if item.icon}
                  <span class="mr-3 text-text-tertiary">{item.icon}</span>
                {/if}
                
                <span>{item.label}</span>
                
                {#if item.badge}
                  <span class="ml-auto px-2 py-0.5 text-xs rounded-full bg-primary-100 text-primary-800">
                    {item.badge}
                  </span>
                {/if}
                
                {#if item.checked}
                  <span class="ml-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary-500" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </span>
                {/if}
              </div>
              
              {#if item.description}
                <p class="mt-1 text-xs text-text-tertiary">
                  {item.description}
                </p>
              {/if}
            </button>
          {/if}
        {/each}
      </div>
    </div>
  {/if}
</div>