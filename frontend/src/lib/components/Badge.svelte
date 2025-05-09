<script>
  // Props
  export let variant = 'default'; // default, primary, success, warning, error, info
  export let size = 'md'; // sm, md, lg
  export let rounded = false;
  export let outline = false;
  export let icon = null;
  export let removable = false;
  
  // Event handler
  function handleRemove() {
    if (removable) {
      dispatch('remove');
    }
  }
  
  // Event dispatcher
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  
  // Computed classes
  $: variantClass = getVariantClass(variant, outline);
  $: sizeClass = getSizeClass(size);
  $: roundedClass = rounded ? 'rounded-full' : 'rounded';
  
  // Helper functions
  function getVariantClass(variant, outline) {
    const variants = {
      default: outline
        ? 'bg-transparent border border-neutral-300 text-neutral-700'
        : 'bg-neutral-100 text-neutral-800',
      primary: outline
        ? 'bg-transparent border border-primary-500 text-primary-700'
        : 'bg-primary-100 text-primary-800',
      success: outline
        ? 'bg-transparent border border-success-500 text-success-700'
        : 'bg-success-100 text-success-800',
      warning: outline
        ? 'bg-transparent border border-warning-500 text-warning-700'
        : 'bg-warning-100 text-warning-800',
      error: outline
        ? 'bg-transparent border border-error-500 text-error-700'
        : 'bg-error-100 text-error-800',
      info: outline
        ? 'bg-transparent border border-blue-500 text-blue-700'
        : 'bg-blue-100 text-blue-800',
    };
    
    return variants[variant] || variants.default;
  }
  
  function getSizeClass(size) {
    const sizes = {
      sm: 'text-xs px-2 py-0.5',
      md: 'text-sm px-2.5 py-0.5',
      lg: 'text-base px-3 py-1',
    };
    
    return sizes[size] || sizes.md;
  }
</script>

<span class="inline-flex items-center font-medium {variantClass} {sizeClass} {roundedClass}">
  {#if icon}
    <span class="mr-1 -ml-0.5">{icon}</span>
  {/if}
  
  <slot />
  
  {#if removable}
    <button
      type="button"
      class="ml-1 -mr-0.5 hover:text-opacity-75 focus:outline-none"
      on:click={handleRemove}
      aria-label="Remove"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
  {/if}
</span>