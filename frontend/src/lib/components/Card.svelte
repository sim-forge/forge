<script>
  import { motion } from 'framer-motion';
  import { scaleTransition } from '../transitions';
  
  // Props
  export let variant = 'default'; // default, elevated, outline, flat
  export let padding = 'default'; // none, sm, default, lg
  export let hover = false;
  export let clickable = false;
  export let animate = true;
  export let width = 'auto'; // auto, full, specific value like '300px'
  export let height = 'auto';
  export let maxHeight = null;
  
  // Computed classes
  $: variantClass = getVariantClass(variant);
  $: paddingClass = getPaddingClass(padding);
  $: hoverClass = hover ? 'hover:shadow-lg hover:border-primary-200 transition-all duration-200' : '';
  $: clickableClass = clickable ? 'cursor-pointer' : '';
  $: widthClass = width === 'full' ? 'w-full' : '';
  $: heightClass = height === 'full' ? 'h-full' : '';
  $: styleAttr = `
    ${width !== 'auto' && width !== 'full' ? `width: ${width};` : ''}
    ${height !== 'auto' && height !== 'full' ? `height: ${height};` : ''}
    ${maxHeight ? `max-height: ${maxHeight};` : ''}
  `;
  
  // Helper functions
  function getVariantClass(variant) {
    const variants = {
      default: 'bg-bg-primary border border-border-light shadow-sm',
      elevated: 'bg-bg-primary border border-border-light shadow-md',
      outline: 'bg-transparent border border-border-medium',
      flat: 'bg-bg-secondary border-none',
    };
    
    return variants[variant] || variants.default;
  }
  
  function getPaddingClass(padding) {
    const paddings = {
      none: 'p-0',
      sm: 'p-3',
      default: 'p-4',
      lg: 'p-6',
    };
    
    return paddings[padding] || paddings.default;
  }
  
  // Animation variants
  const cardAnimation = {
    initial: { opacity: 0, scale: 0.97 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.97 },
    transition: { duration: 0.2 },
  };
</script>

{#if animate}
  <motion.div
    class="card rounded-lg overflow-hidden {variantClass} {paddingClass} {hoverClass} {clickableClass} {widthClass} {heightClass}"
    style={styleAttr}
    initial="initial"
    animate="animate"
    exit="exit"
    variants={cardAnimation}
    on:click
  >
    <slot />
  </motion.div>
{:else}
  <div
    class="card rounded-lg overflow-hidden {variantClass} {paddingClass} {hoverClass} {clickableClass} {widthClass} {heightClass}"
    style={styleAttr}
    on:click
  >
    <slot />
  </div>
{/if}

<style>
  .card {
    display: flex;
    flex-direction: column;
  }
</style>