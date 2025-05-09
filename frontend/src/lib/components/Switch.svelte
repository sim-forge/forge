<script>
  import { createEventDispatcher } from 'svelte';
  import { spring } from 'svelte/motion';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let checked = false;
  export let disabled = false;
  export let name = '';
  export let id = name;
  export let label = '';
  export let labelPosition = 'right'; // right, left
  export let size = 'md'; // sm, md, lg
  export let color = 'primary'; // primary, success, warning, error
  export let description = '';
  
  // Local state
  let switchElement;
  
  // Spring animation for the toggle
  const toggleSpring = spring(checked ? 1 : 0, {
    stiffness: 0.3,
    damping: 0.7
  });
  
  // Update spring when checked changes
  $: {
    toggleSpring.set(checked ? 1 : 0);
  }
  
  // Computed classes
  $: sizeClass = getSizeClass(size);
  $: colorClass = getColorClass(color);
  $: labelPositionClass = labelPosition === 'left' ? 'flex-row-reverse' : 'flex-row';
  $: labelSpacingClass = labelPosition === 'left' ? 'mr-3' : 'ml-3';
  
  // Helper functions
  function getSizeClass(size) {
    const sizes = {
      sm: {
        track: 'w-8 h-4',
        toggle: 'w-3 h-3',
        translateX: 16
      },
      md: {
        track: 'w-10 h-5',
        toggle: 'w-4 h-4',
        translateX: 20
      },
      lg: {
        track: 'w-12 h-6',
        toggle: 'w-5 h-5',
        translateX: 24
      }
    };
    
    return sizes[size] || sizes.md;
  }
  
  function getColorClass(color) {
    const colors = {
      primary: 'bg-primary-500',
      success: 'bg-success-500',
      warning: 'bg-warning-500',
      error: 'bg-error-500'
    };
    
    return colors[color] || colors.primary;
  }
  
  // Handle click
  function handleClick() {
    if (!disabled) {
      checked = !checked;
      dispatch('change', { checked });
    }
  }
  
  // Handle keydown
  function handleKeydown(event) {
    if (!disabled && (event.key === 'Enter' || event.key === ' ')) {
      event.preventDefault();
      checked = !checked;
      dispatch('change', { checked });
    }
  }
</script>

<label
  class="inline-flex items-center {labelPositionClass} {disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}"
>
  <div
    bind:this={switchElement}
    class="relative inline-flex flex-shrink-0 {sizeClass.track} rounded-full transition-colors ease-in-out duration-200 focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2"
    class:bg-neutral-200={!checked}
    class:{colorClass}={checked}
    on:click={handleClick}
    on:keydown={handleKeydown}
    tabindex={disabled ? -1 : 0}
    role="switch"
    aria-checked={checked}
    aria-disabled={disabled}
  >
    <span
      aria-hidden="true"
      class="pointer-events-none absolute mx-0.5 my-0.5 inline-block rounded-full bg-white shadow transform ring-0 transition-transform ease-in-out duration-200 {sizeClass.toggle}"
      style="transform: translateX({$toggleSpring * sizeClass.translateX}px)"
    ></span>
    
    <input
      type="checkbox"
      {name}
      {id}
      bind:checked
      {disabled}
      class="sr-only"
      aria-labelledby={label ? `${id}-label` : null}
    />
  </div>
  
  {#if label}
    <div class="{labelSpacingClass}">
      <span id="{id}-label" class="text-sm font-medium text-text-primary">{label}</span>
      
      {#if description}
        <p class="text-xs text-text-tertiary mt-0.5">{description}</p>
      {/if}
    </div>
  {/if}
</label>