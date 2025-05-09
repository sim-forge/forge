<script>
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';
  
  // Props
  export let content = '';
  export let position = 'top'; // top, right, bottom, left
  export let trigger = 'hover'; // hover, click, focus
  export let delay = 300; // ms
  export let maxWidth = '200px';
  export let theme = 'dark'; // dark, light
  export let arrow = true;
  export let disabled = false;
  
  // Local state
  let tooltipVisible = false;
  let tooltipElement;
  let triggerElement;
  let timeoutId;
  
  // Computed classes
  $: positionClass = getPositionClass(position);
  $: themeClass = getThemeClass(theme);
  
  // Helper functions
  function getPositionClass(position) {
    const positions = {
      top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
      right: 'left-full top-1/2 transform -translate-y-1/2 ml-2',
      bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
      left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    };
    
    return positions[position] || positions.top;
  }
  
  function getThemeClass(theme) {
    const themes = {
      dark: 'bg-neutral-800 text-white',
      light: 'bg-white text-neutral-800 border border-neutral-200',
    };
    
    return themes[theme] || themes.dark;
  }
  
  function getArrowClass(position) {
    const arrows = {
      top: 'bottom-[-6px] left-1/2 transform -translate-x-1/2 border-t-neutral-800 border-r-transparent border-b-transparent border-l-transparent',
      right: 'left-[-6px] top-1/2 transform -translate-y-1/2 border-t-transparent border-r-neutral-800 border-b-transparent border-l-transparent',
      bottom: 'top-[-6px] left-1/2 transform -translate-x-1/2 border-t-transparent border-r-transparent border-b-neutral-800 border-l-transparent',
      left: 'right-[-6px] top-1/2 transform -translate-y-1/2 border-t-transparent border-r-transparent border-b-transparent border-l-neutral-800',
    };
    
    if (theme === 'light') {
      arrows.top = 'bottom-[-6px] left-1/2 transform -translate-x-1/2 border-t-white border-r-transparent border-b-transparent border-l-transparent';
      arrows.right = 'left-[-6px] top-1/2 transform -translate-y-1/2 border-t-transparent border-r-white border-b-transparent border-l-transparent';
      arrows.bottom = 'top-[-6px] left-1/2 transform -translate-x-1/2 border-t-transparent border-r-transparent border-b-white border-l-transparent';
      arrows.left = 'right-[-6px] top-1/2 transform -translate-y-1/2 border-t-transparent border-r-transparent border-b-transparent border-l-white';
    }
    
    return arrows[position] || arrows.top;
  }
  
  // Show tooltip
  function showTooltip() {
    if (disabled || !content) return;
    
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      tooltipVisible = true;
      
      // Position tooltip
      if (tooltipElement && triggerElement) {
        const triggerRect = triggerElement.getBoundingClientRect();
        const tooltipRect = tooltipElement.getBoundingClientRect();
        
        // Adjust position if tooltip is outside viewport
        if (position === 'top' || position === 'bottom') {
          const leftOffset = triggerRect.left + triggerRect.width / 2 - tooltipRect.width / 2;
          const rightEdge = leftOffset + tooltipRect.width;
          
          if (leftOffset < 10) {
            tooltipElement.style.left = '10px';
            tooltipElement.style.transform = 'translateY(0)';
          } else if (rightEdge > window.innerWidth - 10) {
            tooltipElement.style.left = 'auto';
            tooltipElement.style.right = '10px';
            tooltipElement.style.transform = 'translateY(0)';
          }
        } else if (position === 'left' || position === 'right') {
          const topOffset = triggerRect.top + triggerRect.height / 2 - tooltipRect.height / 2;
          const bottomEdge = topOffset + tooltipRect.height;
          
          if (topOffset < 10) {
            tooltipElement.style.top = '10px';
            tooltipElement.style.transform = 'translateX(0)';
          } else if (bottomEdge > window.innerHeight - 10) {
            tooltipElement.style.top = 'auto';
            tooltipElement.style.bottom = '10px';
            tooltipElement.style.transform = 'translateX(0)';
          }
        }
      }
    }, delay);
  }
  
  // Hide tooltip
  function hideTooltip() {
    clearTimeout(timeoutId);
    tooltipVisible = false;
  }
  
  // Toggle tooltip
  function toggleTooltip() {
    if (tooltipVisible) {
      hideTooltip();
    } else {
      showTooltip();
    }
  }
  
  // Event handlers
  function handleMouseEnter() {
    if (trigger === 'hover') {
      showTooltip();
    }
  }
  
  function handleMouseLeave() {
    if (trigger === 'hover') {
      hideTooltip();
    }
  }
  
  function handleFocus() {
    if (trigger === 'focus') {
      showTooltip();
    }
  }
  
  function handleBlur() {
    if (trigger === 'focus') {
      hideTooltip();
    }
  }
  
  function handleClick() {
    if (trigger === 'click') {
      toggleTooltip();
    }
  }
  
  // Handle click outside
  function handleClickOutside(event) {
    if (
      trigger === 'click' &&
      tooltipVisible &&
      triggerElement &&
      !triggerElement.contains(event.target) &&
      tooltipElement &&
      !tooltipElement.contains(event.target)
    ) {
      hideTooltip();
    }
  }
  
  // Initialize component
  onMount(() => {
    // Add click outside listener
    if (trigger === 'click') {
      document.addEventListener('click', handleClickOutside);
    }
    
    return () => {
      if (trigger === 'click') {
        document.removeEventListener('click', handleClickOutside);
      }
    };
  });
  
  // Cleanup
  onDestroy(() => {
    clearTimeout(timeoutId);
  });
</script>

<div class="tooltip-container inline-block relative">
  <div
    bind:this={triggerElement}
    on:mouseenter={handleMouseEnter}
    on:mouseleave={handleMouseLeave}
    on:focus={handleFocus}
    on:blur={handleBlur}
    on:click={handleClick}
  >
    <slot />
  </div>
  
  {#if tooltipVisible}
    <div
      bind:this={tooltipElement}
      class="tooltip absolute z-50 px-2 py-1 text-sm rounded shadow-lg whitespace-normal {positionClass} {themeClass}"
      style="max-width: {maxWidth};"
      transition:fade={{ duration: 150 }}
      role="tooltip"
    >
      {content}
      
      {#if arrow}
        <div class="tooltip-arrow absolute w-0 h-0 border-solid border-[6px] {getArrowClass(position)}"></div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .tooltip-container {
    display: inline-block;
  }
</style>