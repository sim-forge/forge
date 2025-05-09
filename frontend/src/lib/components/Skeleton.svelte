<script>
  // Props
  export let variant = 'rectangle'; // rectangle, circle, text
  export let width = '100%';
  export let height = '1rem';
  export let rounded = false;
  export let animate = true;
  export let count = 1;
  export let className = '';
  
  // Computed classes
  $: variantClass = getVariantClass(variant);
  $: roundedClass = getRoundedClass(variant, rounded);
  $: animateClass = animate ? 'animate-pulse' : '';
  
  // Helper functions
  function getVariantClass(variant) {
    const variants = {
      rectangle: '',
      circle: 'rounded-full',
      text: 'rounded'
    };
    
    return variants[variant] || variants.rectangle;
  }
  
  function getRoundedClass(variant, rounded) {
    if (variant === 'circle') return '';
    if (variant === 'text') return '';
    
    return rounded ? 'rounded-lg' : 'rounded';
  }
  
  // Generate skeleton items
  function generateSkeletons(count) {
    return Array.from({ length: count }, (_, i) => i);
  }
  
  // Skeleton items
  $: skeletons = generateSkeletons(count);
</script>

<div class="skeleton-container {className}">
  {#each skeletons as _, i}
    <div
      class="skeleton bg-neutral-200 dark:bg-neutral-700 {variantClass} {roundedClass} {animateClass}"
      style="width: {width}; height: {height}; {i > 0 ? 'margin-top: 0.5rem;' : ''}"
    ></div>
  {/each}
</div>

<style>
  .skeleton {
    position: relative;
    overflow: hidden;
  }
  
  .skeleton::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    transform: translateX(-100%);
    background-image: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0) 0,
      rgba(255, 255, 255, 0.2) 20%,
      rgba(255, 255, 255, 0.5) 60%,
      rgba(255, 255, 255, 0)
    );
    animation: shimmer 2s infinite;
  }
  
  @keyframes shimmer {
    100% {
      transform: translateX(100%);
    }
  }
  
  :global(.dark) .skeleton::after {
    background-image: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0) 0,
      rgba(255, 255, 255, 0.05) 20%,
      rgba(255, 255, 255, 0.1) 60%,
      rgba(255, 255, 255, 0)
    );
  }
</style>