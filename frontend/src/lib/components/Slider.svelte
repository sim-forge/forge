<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { spring } from 'svelte/motion';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let value = 0;
  export let min = 0;
  export let max = 100;
  export let step = 1;
  export let disabled = false;
  export let showTicks = false;
  export let tickValues = [];
  export let showLabels = false;
  export let labelValues = [];
  export let showValue = false;
  export let valuePosition = 'top'; // top, bottom, tooltip
  export let color = 'primary'; // primary, success, warning, error
  export let size = 'md'; // sm, md, lg
  export let range = false;
  export let rangeValue = [0, 0];
  export let formatValue = null;
  export let name = '';
  export let id = '';
  
  // Local state
  let slider;
  let track;
  let isDragging = false;
  let activeHandle = 0; // 0 for single, 0 or 1 for range
  let tooltipVisible = false;
  let tooltipPosition = 0;
  
  // Spring animation for smooth transitions
  const springValue = spring(value, {
    stiffness: 0.15,
    damping: 0.8
  });
  
  const springRangeValue = [
    spring(rangeValue[0], {
      stiffness: 0.15,
      damping: 0.8
    }),
    spring(rangeValue[1], {
      stiffness: 0.15,
      damping: 0.8
    })
  ];
  
  // Update spring when value changes
  $: {
    if (!isDragging) {
      springValue.set(value);
      if (range) {
        springRangeValue[0].set(rangeValue[0]);
        springRangeValue[1].set(rangeValue[1]);
      }
    }
  }
  
  // Computed values
  $: percentage = ((value - min) / (max - min)) * 100;
  $: rangePercentage = range ? [
    ((rangeValue[0] - min) / (max - min)) * 100,
    ((rangeValue[1] - min) / (max - min)) * 100
  ] : [0, 0];
  
  $: springPercentage = (($springValue - min) / (max - min)) * 100;
  $: springRangePercentage = range ? [
    (($springRangeValue[0] - min) / (max - min)) * 100,
    (($springRangeValue[1] - min) / (max - min)) * 100
  ] : [0, 0];
  
  // Computed classes
  $: colorClass = getColorClass(color);
  $: sizeClass = getSizeClass(size);
  
  // Helper functions
  function getColorClass(color) {
    const colors = {
      primary: 'bg-primary-500',
      success: 'bg-success-500',
      warning: 'bg-warning-500',
      error: 'bg-error-500'
    };
    
    return colors[color] || colors.primary;
  }
  
  function getSizeClass(size) {
    const sizes = {
      sm: {
        track: 'h-1',
        thumb: 'w-3 h-3',
        valueText: 'text-xs'
      },
      md: {
        track: 'h-2',
        thumb: 'w-4 h-4',
        valueText: 'text-sm'
      },
      lg: {
        track: 'h-3',
        thumb: 'w-6 h-6',
        valueText: 'text-base'
      }
    };
    
    return sizes[size] || sizes.md;
  }
  
  function formatDisplayValue(val) {
    if (typeof formatValue === 'function') {
      return formatValue(val);
    }
    
    return val;
  }
  
  function getTickValues() {
    if (tickValues.length > 0) {
      return tickValues;
    }
    
    const ticks = [];
    for (let i = min; i <= max; i += step) {
      ticks.push(i);
    }
    
    return ticks;
  }
  
  function getLabelValues() {
    if (labelValues.length > 0) {
      return labelValues;
    }
    
    return [min, max];
  }
  
  function getTickPosition(tick) {
    return ((tick - min) / (max - min)) * 100;
  }
  
  function clamp(val, minVal, maxVal) {
    return Math.min(Math.max(val, minVal), maxVal);
  }
  
  function roundToStep(val) {
    const remainder = (val - min) % step;
    if (remainder === 0) {
      return val;
    }
    
    if (remainder < step / 2) {
      return val - remainder;
    } else {
      return val + (step - remainder);
    }
  }
  
  // Handle mouse/touch events
  function handleTrackClick(event) {
    if (disabled) return;
    
    const rect = track.getBoundingClientRect();
    const clientX = event.clientX || (event.touches && event.touches[0].clientX);
    const position = (clientX - rect.left) / rect.width;
    const newValue = min + position * (max - min);
    const roundedValue = roundToStep(clamp(newValue, min, max));
    
    if (range) {
      // Find the closest handle
      const distToMin = Math.abs(roundedValue - rangeValue[0]);
      const distToMax = Math.abs(roundedValue - rangeValue[1]);
      
      if (distToMin <= distToMax) {
        activeHandle = 0;
        rangeValue[0] = roundedValue;
      } else {
        activeHandle = 1;
        rangeValue[1] = roundedValue;
      }
      
      // Ensure min <= max
      if (rangeValue[0] > rangeValue[1]) {
        if (activeHandle === 0) {
          rangeValue[0] = rangeValue[1];
        } else {
          rangeValue[1] = rangeValue[0];
        }
      }
      
      rangeValue = [...rangeValue];
      dispatch('change', { value: rangeValue });
    } else {
      value = roundedValue;
      dispatch('change', { value });
    }
  }
  
  function handleMouseDown(event, handleIndex = 0) {
    if (disabled) return;
    
    event.preventDefault();
    isDragging = true;
    activeHandle = handleIndex;
    
    // Add event listeners
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
    window.addEventListener('touchmove', handleMouseMove);
    window.addEventListener('touchend', handleMouseUp);
    
    // Show tooltip if needed
    if (valuePosition === 'tooltip') {
      tooltipVisible = true;
    }
  }
  
  function handleMouseMove(event) {
    if (!isDragging || disabled) return;
    
    const rect = track.getBoundingClientRect();
    const clientX = event.clientX || (event.touches && event.touches[0].clientX);
    const position = clamp((clientX - rect.left) / rect.width, 0, 1);
    const newValue = min + position * (max - min);
    const roundedValue = roundToStep(clamp(newValue, min, max));
    
    if (range) {
      if (activeHandle === 0) {
        rangeValue[0] = Math.min(roundedValue, rangeValue[1]);
      } else {
        rangeValue[1] = Math.max(roundedValue, rangeValue[0]);
      }
      
      rangeValue = [...rangeValue];
      dispatch('input', { value: rangeValue });
      
      // Update tooltip position
      tooltipPosition = activeHandle === 0 ? rangePercentage[0] : rangePercentage[1];
    } else {
      value = roundedValue;
      dispatch('input', { value });
      
      // Update tooltip position
      tooltipPosition = percentage;
    }
  }
  
  function handleMouseUp() {
    if (!isDragging) return;
    
    isDragging = false;
    
    // Remove event listeners
    window.removeEventListener('mousemove', handleMouseMove);
    window.removeEventListener('mouseup', handleMouseUp);
    window.removeEventListener('touchmove', handleMouseMove);
    window.removeEventListener('touchend', handleMouseUp);
    
    // Hide tooltip if needed
    if (valuePosition === 'tooltip') {
      tooltipVisible = false;
    }
    
    // Dispatch final change event
    if (range) {
      dispatch('change', { value: rangeValue });
    } else {
      dispatch('change', { value });
    }
  }
  
  // Handle keyboard events
  function handleKeyDown(event, handleIndex = 0) {
    if (disabled) return;
    
    let newValue;
    
    if (range) {
      newValue = rangeValue[handleIndex];
    } else {
      newValue = value;
    }
    
    switch (event.key) {
      case 'ArrowLeft':
      case 'ArrowDown':
        newValue = Math.max(newValue - step, min);
        break;
      case 'ArrowRight':
      case 'ArrowUp':
        newValue = Math.min(newValue + step, max);
        break;
      case 'Home':
        newValue = min;
        break;
      case 'End':
        newValue = max;
        break;
      default:
        return;
    }
    
    event.preventDefault();
    
    if (range) {
      if (handleIndex === 0) {
        rangeValue[0] = Math.min(newValue, rangeValue[1]);
      } else {
        rangeValue[1] = Math.max(newValue, rangeValue[0]);
      }
      
      rangeValue = [...rangeValue];
      dispatch('change', { value: rangeValue });
    } else {
      value = newValue;
      dispatch('change', { value });
    }
  }
  
  // Initialize component
  onMount(() => {
    // Ensure range values are valid
    if (range) {
      rangeValue[0] = clamp(rangeValue[0], min, max);
      rangeValue[1] = clamp(rangeValue[1], rangeValue[0], max);
      rangeValue = [...rangeValue];
    }
  });
</script>

<div class="slider-container" bind:this={slider}>
  {#if showValue && valuePosition === 'top'}
    <div class="flex justify-between mb-2">
      {#if range}
        <div class="{sizeClass.valueText} text-text-secondary">
          {formatDisplayValue(rangeValue[0])}
        </div>
        <div class="{sizeClass.valueText} text-text-secondary">
          {formatDisplayValue(rangeValue[1])}
        </div>
      {:else}
        <div class="{sizeClass.valueText} text-text-secondary">
          {formatDisplayValue(value)}
        </div>
      {/if}
    </div>
  {/if}
  
  <div class="relative py-2">
    <div
      bind:this={track}
      class="slider-track {sizeClass.track} bg-neutral-200 dark:bg-neutral-700 rounded-full cursor-pointer {disabled ? 'opacity-50 cursor-not-allowed' : ''}"
      on:click={handleTrackClick}
    >
      {#if range}
        <div
          class="slider-range absolute top-0 bottom-0 rounded-full {colorClass}"
          style="left: {Math.min($springRangePercentage[0], $springRangePercentage[1])}%; right: {100 - Math.max($springRangePercentage[0], $springRangePercentage[1])}%;"
        ></div>
      {:else}
        <div
          class="slider-progress absolute top-0 bottom-0 left-0 rounded-full {colorClass}"
          style="width: {$springPercentage}%;"
        ></div>
      {/if}
      
      {#if showTicks}
        <div class="slider-ticks absolute w-full top-full mt-1">
          {#each getTickValues() as tick}
            <div
              class="slider-tick absolute w-1 h-1 bg-neutral-400 rounded-full transform -translate-x-1/2"
              style="left: {getTickPosition(tick)}%;"
            ></div>
          {/each}
        </div>
      {/if}
    </div>
    
    {#if range}
      <!-- Min handle -->
      <button
        type="button"
        class="slider-handle absolute top-1/2 transform -translate-y-1/2 -translate-x-1/2 {sizeClass.thumb} rounded-full bg-white border-2 {colorClass.replace('bg-', 'border-')} shadow focus:outline-none focus:ring-2 focus:ring-offset-2 {colorClass.replace('bg-', 'focus:ring-')} {disabled ? 'cursor-not-allowed' : 'cursor-grab'}"
        style="left: {$springRangePercentage[0]}%;"
        on:mousedown={(e) => handleMouseDown(e, 0)}
        on:touchstart={(e) => handleMouseDown(e, 0)}
        on:keydown={(e) => handleKeyDown(e, 0)}
        tabindex={disabled ? -1 : 0}
        role="slider"
        aria-valuemin={min}
        aria-valuemax={rangeValue[1]}
        aria-valuenow={rangeValue[0]}
        aria-disabled={disabled}
        aria-label={`Minimum value: ${rangeValue[0]}`}
        disabled={disabled}
      ></button>
      
      <!-- Max handle -->
      <button
        type="button"
        class="slider-handle absolute top-1/2 transform -translate-y-1/2 -translate-x-1/2 {sizeClass.thumb} rounded-full bg-white border-2 {colorClass.replace('bg-', 'border-')} shadow focus:outline-none focus:ring-2 focus:ring-offset-2 {colorClass.replace('bg-', 'focus:ring-')} {disabled ? 'cursor-not-allowed' : 'cursor-grab'}"
        style="left: {$springRangePercentage[1]}%;"
        on:mousedown={(e) => handleMouseDown(e, 1)}
        on:touchstart={(e) => handleMouseDown(e, 1)}
        on:keydown={(e) => handleKeyDown(e, 1)}
        tabindex={disabled ? -1 : 0}
        role="slider"
        aria-valuemin={rangeValue[0]}
        aria-valuemax={max}
        aria-valuenow={rangeValue[1]}
        aria-disabled={disabled}
        aria-label={`Maximum value: ${rangeValue[1]}`}
        disabled={disabled}
      ></button>
      
      {#if valuePosition === 'tooltip' && tooltipVisible}
        <div
          class="slider-tooltip absolute top-0 transform -translate-x-1/2 -translate-y-full mb-2 px-2 py-1 bg-neutral-800 text-white text-xs rounded shadow"
          style="left: {tooltipPosition}%;"
        >
          {formatDisplayValue(activeHandle === 0 ? rangeValue[0] : rangeValue[1])}
        </div>
      {/if}
    {:else}
      <!-- Single handle -->
      <button
        type="button"
        class="slider-handle absolute top-1/2 transform -translate-y-1/2 -translate-x-1/2 {sizeClass.thumb} rounded-full bg-white border-2 {colorClass.replace('bg-', 'border-')} shadow focus:outline-none focus:ring-2 focus:ring-offset-2 {colorClass.replace('bg-', 'focus:ring-')} {disabled ? 'cursor-not-allowed' : 'cursor-grab'}"
        style="left: {$springPercentage}%;"
        on:mousedown={handleMouseDown}
        on:touchstart={handleMouseDown}
        on:keydown={handleKeyDown}
        tabindex={disabled ? -1 : 0}
        role="slider"
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={value}
        aria-disabled={disabled}
        aria-label={`Value: ${value}`}
        disabled={disabled}
      ></button>
      
      {#if valuePosition === 'tooltip' && tooltipVisible}
        <div
          class="slider-tooltip absolute top-0 transform -translate-x-1/2 -translate-y-full mb-2 px-2 py-1 bg-neutral-800 text-white text-xs rounded shadow"
          style="left: {tooltipPosition}%;"
        >
          {formatDisplayValue(value)}
        </div>
      {/if}
    {/if}
  </div>
  
  {#if showLabels}
    <div class="slider-labels flex justify-between mt-1">
      {#each getLabelValues() as label}
        <div class="text-xs text-text-tertiary">
          {formatDisplayValue(label)}
        </div>
      {/each}
    </div>
  {/if}
  
  {#if showValue && valuePosition === 'bottom'}
    <div class="flex justify-between mt-2">
      {#if range}
        <div class="{sizeClass.valueText} text-text-secondary">
          {formatDisplayValue(rangeValue[0])}
        </div>
        <div class="{sizeClass.valueText} text-text-secondary">
          {formatDisplayValue(rangeValue[1])}
        </div>
      {:else}
        <div class="{sizeClass.valueText} text-text-secondary">
          {formatDisplayValue(value)}
        </div>
      {/if}
    </div>
  {/if}
  
  {#if name}
    {#if range}
      <input type="hidden" {name}="{name}_min" value={rangeValue[0]} />
      <input type="hidden" {name}="{name}_max" value={rangeValue[1]} />
    {:else}
      <input type="hidden" {name} {value} />
    {/if}
  {/if}
</div>

<style>
  .slider-container {
    width: 100%;
  }
  
  .slider-track {
    position: relative;
    width: 100%;
  }
  
  .slider-handle {
    z-index: 1;
  }
  
  .slider-tooltip {
    z-index: 2;
  }
</style>