<script>
  // Props
  export let value = 0;
  export let max = 100;
  export let height = '0.5rem';
  export let color = 'primary'; // primary, success, warning, error, info, neutral
  export let showLabel = false;
  export let labelPosition = 'right'; // right, top, bottom, inside
  export let labelFormat = 'percent'; // percent, value, custom
  export let customLabel = '';
  export let striped = false;
  export let animated = false;
  export let rounded = true;
  export let indeterminate = false;
  
  // Computed values
  $: percentage = Math.min(100, Math.max(0, (value / max) * 100));
  $: displayLabel = getDisplayLabel(value, max, labelFormat, customLabel);
  
  // Computed classes
  $: colorClass = getColorClass(color);
  $: stripedClass = striped ? 'progress-striped' : '';
  $: animatedClass = animated ? 'progress-animated' : '';
  $: roundedClass = rounded ? 'rounded-full' : 'rounded-none';
  $: indeterminateClass = indeterminate ? 'progress-indeterminate' : '';
  
  // Helper functions
  function getColorClass(color) {
    const colors = {
      primary: 'bg-primary-500',
      success: 'bg-success-500',
      warning: 'bg-warning-500',
      error: 'bg-error-500',
      info: 'bg-blue-500',
      neutral: 'bg-neutral-500'
    };
    
    return colors[color] || colors.primary;
  }
  
  function getDisplayLabel(value, max, format, custom) {
    if (custom) return custom;
    
    switch (format) {
      case 'percent':
        return `${Math.round((value / max) * 100)}%`;
      case 'value':
        return `${value}/${max}`;
      default:
        return `${Math.round((value / max) * 100)}%`;
    }
  }
</script>

<div class="progress-container">
  {#if showLabel && (labelPosition === 'top')}
    <div class="text-sm text-text-secondary mb-1">{displayLabel}</div>
  {/if}
  
  <div class="relative {roundedClass} overflow-hidden bg-neutral-200 dark:bg-neutral-700" style="height: {height};">
    {#if !indeterminate}
      <div
        class="h-full {colorClass} {stripedClass} {animatedClass} {roundedClass} transition-all duration-300 ease-in-out"
        style="width: {percentage}%;"
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin="0"
        aria-valuemax={max}
      >
        {#if showLabel && (labelPosition === 'inside')}
          <div class="absolute inset-0 flex items-center justify-center text-xs text-white font-medium">
            {displayLabel}
          </div>
        {/if}
      </div>
    {:else}
      <div
        class="h-full {colorClass} {indeterminateClass} {roundedClass}"
        role="progressbar"
        aria-valuemin="0"
        aria-valuemax="100"
      ></div>
    {/if}
  </div>
  
  {#if showLabel && (labelPosition === 'bottom')}
    <div class="text-sm text-text-secondary mt-1">{displayLabel}</div>
  {/if}
  
  {#if showLabel && (labelPosition === 'right')}
    <div class="flex items-center">
      <div class="relative {roundedClass} overflow-hidden bg-neutral-200 dark:bg-neutral-700 flex-1" style="height: {height};">
        {#if !indeterminate}
          <div
            class="h-full {colorClass} {stripedClass} {animatedClass} {roundedClass} transition-all duration-300 ease-in-out"
            style="width: {percentage}%;"
          ></div>
        {:else}
          <div
            class="h-full {colorClass} {indeterminateClass} {roundedClass}"
          ></div>
        {/if}
      </div>
      <div class="ml-3 text-sm text-text-secondary min-w-[3rem] text-right">{displayLabel}</div>
    </div>
  {/if}
</div>

<style>
  .progress-striped {
    background-image: linear-gradient(
      45deg,
      rgba(255, 255, 255, 0.15) 25%,
      transparent 25%,
      transparent 50%,
      rgba(255, 255, 255, 0.15) 50%,
      rgba(255, 255, 255, 0.15) 75%,
      transparent 75%,
      transparent
    );
    background-size: 1rem 1rem;
  }
  
  .progress-animated {
    animation: progress-bar-stripes 1s linear infinite;
  }
  
  .progress-indeterminate {
    width: 50%;
    animation: indeterminate 1.5s infinite ease-in-out;
  }
  
  @keyframes progress-bar-stripes {
    from {
      background-position: 1rem 0;
    }
    to {
      background-position: 0 0;
    }
  }
  
  @keyframes indeterminate {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(200%);
    }
  }
</style>