<script>
  import { createEventDispatcher } from 'svelte';
  import { motion } from 'framer-motion';
  import { buttonHoverTransition, buttonTapTransition } from '../transitions';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let type = 'button';
  export let variant = 'primary'; // primary, secondary, outline, ghost, danger
  export let size = 'md'; // sm, md, lg
  export let disabled = false;
  export let loading = false;
  export let icon = null;
  export let iconPosition = 'left'; // left, right
  export let fullWidth = false;
  export let rounded = false;
  export let href = null;
  export let external = false;
  export let animate = true;
  
  // Computed classes
  $: variantClass = getVariantClass(variant);
  $: sizeClass = getSizeClass(size);
  $: widthClass = fullWidth ? 'w-full' : '';
  $: roundedClass = rounded ? 'rounded-full' : 'rounded';
  $: disabledClass = disabled || loading ? 'opacity-60 cursor-not-allowed' : 'hover:shadow-md';
  
  // Helper functions
  function getVariantClass(variant) {
    const variants = {
      primary: 'bg-primary-500 hover:bg-primary-600 text-white border-transparent',
      secondary: 'bg-neutral-100 hover:bg-neutral-200 text-neutral-800 border-transparent',
      outline: 'bg-transparent hover:bg-neutral-50 text-primary-500 border-primary-500',
      ghost: 'bg-transparent hover:bg-neutral-100 text-neutral-700 border-transparent',
      danger: 'bg-error-500 hover:bg-error-600 text-white border-transparent',
    };
    
    return variants[variant] || variants.primary;
  }
  
  function getSizeClass(size) {
    const sizes = {
      sm: 'text-xs py-1.5 px-3',
      md: 'text-sm py-2 px-4',
      lg: 'text-base py-2.5 px-5',
    };
    
    return sizes[size] || sizes.md;
  }
  
  // Handle click
  function handleClick(event) {
    if (disabled || loading) {
      event.preventDefault();
      return;
    }
    
    dispatch('click', event);
  }
  
  // Animation variants
  const buttonAnimation = {
    hover: buttonHoverTransition,
    tap: buttonTapTransition,
  };
</script>

{#if href}
  <motion.a
    {href}
    target={external ? '_blank' : null}
    rel={external ? 'noopener noreferrer' : null}
    class="inline-flex items-center justify-center font-medium transition-all duration-200 border {variantClass} {sizeClass} {widthClass} {roundedClass} {disabledClass}"
    on:click={handleClick}
    whileHover={animate && !disabled && !loading ? 'hover' : null}
    whileTap={animate && !disabled && !loading ? 'tap' : null}
    variants={buttonAnimation}
  >
    {#if loading}
      <span class="mr-2 inline-block w-4 h-4 border-2 border-t-transparent border-white rounded-full animate-spin"></span>
    {:else if icon && iconPosition === 'left'}
      <span class="mr-2">{icon}</span>
    {/if}
    
    <slot />
    
    {#if icon && iconPosition === 'right'}
      <span class="ml-2">{icon}</span>
    {/if}
  </motion.a>
{:else}
  <motion.button
    {type}
    {disabled}
    class="inline-flex items-center justify-center font-medium transition-all duration-200 border {variantClass} {sizeClass} {widthClass} {roundedClass} {disabledClass}"
    on:click={handleClick}
    whileHover={animate && !disabled && !loading ? 'hover' : null}
    whileTap={animate && !disabled && !loading ? 'tap' : null}
    variants={buttonAnimation}
  >
    {#if loading}
      <span class="mr-2 inline-block w-4 h-4 border-2 border-t-transparent border-current rounded-full animate-spin"></span>
    {:else if icon && iconPosition === 'left'}
      <span class="mr-2">{icon}</span>
    {/if}
    
    <slot />
    
    {#if icon && iconPosition === 'right'}
      <span class="ml-2">{icon}</span>
    {/if}
  </motion.button>
{/if}

<style>
  /* Additional styles can be added here if needed */
</style>