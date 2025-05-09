<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { clickOutside } from '../utils/clickOutside';
  import { hexToRgba, getContrastColor } from '../utils';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let value = '#000000';
  export let label = '';
  export let name = '';
  export let id = name;
  export let disabled = false;
  export let required = false;
  export let error = '';
  export let helperText = '';
  export let showAlpha = false;
  export let alpha = 1;
  export let format = 'hex'; // hex, rgb, rgba, hsl, hsla
  export let presetColors = [
    '#000000', '#ffffff', '#f44336', '#e91e63', '#9c27b0', '#673ab7',
    '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50',
    '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722',
    '#795548', '#9e9e9e', '#607d8b'
  ];
  
  // Local state
  let isOpen = false;
  let colorPicker;
  let hueSlider;
  let alphaSlider;
  let saturationPicker;
  let hue = 0;
  let saturation = 0;
  let lightness = 0;
  let isDraggingHue = false;
  let isDraggingAlpha = false;
  let isDraggingSaturation = false;
  
  // Computed values
  $: rgbColor = hexToRgb(value);
  $: hslColor = rgbToHsl(rgbColor.r, rgbColor.g, rgbColor.b);
  $: hue = hslColor.h;
  $: saturation = hslColor.s;
  $: lightness = hslColor.l;
  $: hueColor = hslToHex(hue, 1, 0.5);
  $: formattedColor = formatColor(value, alpha, format);
  $: contrastColor = getContrastColor(value);
  
  // Helper functions
  function hexToRgb(hex) {
    // Remove # if present
    hex = hex.replace('#', '');
    
    // Handle shorthand hex
    if (hex.length === 3) {
      hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
    
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    
    return { r, g, b };
  }
  
  function rgbToHex(r, g, b) {
    return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
  }
  
  function rgbToHsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    
    if (max === min) {
      h = s = 0; // achromatic
    } else {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
      }
      
      h /= 6;
    }
    
    return { h, s, l };
  }
  
  function hslToRgb(h, s, l) {
    let r, g, b;
    
    if (s === 0) {
      r = g = b = l; // achromatic
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
      };
      
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
    }
    
    return {
      r: Math.round(r * 255),
      g: Math.round(g * 255),
      b: Math.round(b * 255)
    };
  }
  
  function hslToHex(h, s, l) {
    const rgb = hslToRgb(h, s, l);
    return rgbToHex(rgb.r, rgb.g, rgb.b);
  }
  
  function formatColor(hex, alpha, format) {
    const rgb = hexToRgb(hex);
    
    switch (format) {
      case 'hex':
        return hex;
      case 'rgb':
        return `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
      case 'rgba':
        return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`;
      case 'hsl': {
        const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
        return `hsl(${Math.round(hsl.h * 360)}, ${Math.round(hsl.s * 100)}%, ${Math.round(hsl.l * 100)}%)`;
      }
      case 'hsla': {
        const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
        return `hsla(${Math.round(hsl.h * 360)}, ${Math.round(hsl.s * 100)}%, ${Math.round(hsl.l * 100)}%, ${alpha})`;
      }
      default:
        return hex;
    }
  }
  
  function parseColor(colorStr) {
    // Handle hex
    if (colorStr.startsWith('#')) {
      return { hex: colorStr, alpha: 1 };
    }
    
    // Handle rgb/rgba
    if (colorStr.startsWith('rgb')) {
      const values = colorStr.match(/\d+(\.\d+)?/g);
      if (values && values.length >= 3) {
        const r = parseInt(values[0]);
        const g = parseInt(values[1]);
        const b = parseInt(values[2]);
        const a = values.length > 3 ? parseFloat(values[3]) : 1;
        
        return {
          hex: rgbToHex(r, g, b),
          alpha: a
        };
      }
    }
    
    // Handle hsl/hsla
    if (colorStr.startsWith('hsl')) {
      const values = colorStr.match(/\d+(\.\d+)?/g);
      if (values && values.length >= 3) {
        const h = parseInt(values[0]) / 360;
        const s = parseInt(values[1]) / 100;
        const l = parseInt(values[2]) / 100;
        const a = values.length > 3 ? parseFloat(values[3]) : 1;
        
        const rgb = hslToRgb(h, s, l);
        
        return {
          hex: rgbToHex(rgb.r, rgb.g, rgb.b),
          alpha: a
        };
      }
    }
    
    // Default to black if parsing fails
    return { hex: '#000000', alpha: 1 };
  }
  
  // Toggle color picker
  function togglePicker() {
    if (!disabled) {
      isOpen = !isOpen;
    }
  }
  
  // Close color picker
  function closePicker() {
    isOpen = false;
  }
  
  // Handle hue slider
  function handleHueMouseDown(event) {
    event.preventDefault();
    isDraggingHue = true;
    
    window.addEventListener('mousemove', handleHueMouseMove);
    window.addEventListener('mouseup', handleHueMouseUp);
    window.addEventListener('touchmove', handleHueMouseMove);
    window.addEventListener('touchend', handleHueMouseUp);
    
    handleHueMouseMove(event);
  }
  
  function handleHueMouseMove(event) {
    if (!isDraggingHue) return;
    
    const rect = hueSlider.getBoundingClientRect();
    const clientX = event.clientX || (event.touches && event.touches[0].clientX);
    
    let position = (clientX - rect.left) / rect.width;
    position = Math.max(0, Math.min(1, position));
    
    hue = position;
    updateColorFromHSL();
  }
  
  function handleHueMouseUp() {
    isDraggingHue = false;
    
    window.removeEventListener('mousemove', handleHueMouseMove);
    window.removeEventListener('mouseup', handleHueMouseUp);
    window.removeEventListener('touchmove', handleHueMouseMove);
    window.removeEventListener('touchend', handleHueMouseUp);
  }
  
  // Handle alpha slider
  function handleAlphaMouseDown(event) {
    event.preventDefault();
    isDraggingAlpha = true;
    
    window.addEventListener('mousemove', handleAlphaMouseMove);
    window.addEventListener('mouseup', handleAlphaMouseUp);
    window.addEventListener('touchmove', handleAlphaMouseMove);
    window.addEventListener('touchend', handleAlphaMouseUp);
    
    handleAlphaMouseMove(event);
  }
  
  function handleAlphaMouseMove(event) {
    if (!isDraggingAlpha) return;
    
    const rect = alphaSlider.getBoundingClientRect();
    const clientX = event.clientX || (event.touches && event.touches[0].clientX);
    
    let position = (clientX - rect.left) / rect.width;
    position = Math.max(0, Math.min(1, position));
    
    alpha = position;
    dispatch('change', { value, alpha, formattedColor });
  }
  
  function handleAlphaMouseUp() {
    isDraggingAlpha = false;
    
    window.removeEventListener('mousemove', handleAlphaMouseMove);
    window.removeEventListener('mouseup', handleAlphaMouseUp);
    window.removeEventListener('touchmove', handleAlphaMouseMove);
    window.removeEventListener('touchend', handleAlphaMouseUp);
  }
  
  // Handle saturation/lightness picker
  function handleSaturationMouseDown(event) {
    event.preventDefault();
    isDraggingSaturation = true;
    
    window.addEventListener('mousemove', handleSaturationMouseMove);
    window.addEventListener('mouseup', handleSaturationMouseUp);
    window.addEventListener('touchmove', handleSaturationMouseMove);
    window.addEventListener('touchend', handleSaturationMouseUp);
    
    handleSaturationMouseMove(event);
  }
  
  function handleSaturationMouseMove(event) {
    if (!isDraggingSaturation) return;
    
    const rect = saturationPicker.getBoundingClientRect();
    const clientX = event.clientX || (event.touches && event.touches[0].clientX);
    const clientY = event.clientY || (event.touches && event.touches[0].clientY);
    
    let x = (clientX - rect.left) / rect.width;
    let y = (clientY - rect.top) / rect.height;
    
    x = Math.max(0, Math.min(1, x));
    y = Math.max(0, Math.min(1, y));
    
    saturation = x;
    lightness = 1 - y;
    
    updateColorFromHSL();
  }
  
  function handleSaturationMouseUp() {
    isDraggingSaturation = false;
    
    window.removeEventListener('mousemove', handleSaturationMouseMove);
    window.removeEventListener('mouseup', handleSaturationMouseUp);
    window.removeEventListener('touchmove', handleSaturationMouseMove);
    window.removeEventListener('touchend', handleSaturationMouseUp);
  }
  
  // Update color from HSL values
  function updateColorFromHSL() {
    const rgb = hslToRgb(hue, saturation, lightness);
    value = rgbToHex(rgb.r, rgb.g, rgb.b);
    dispatch('change', { value, alpha, formattedColor });
  }
  
  // Handle input change
  function handleInputChange(event) {
    const colorStr = event.target.value;
    const { hex, alpha: newAlpha } = parseColor(colorStr);
    
    value = hex;
    if (showAlpha) {
      alpha = newAlpha;
    }
    
    dispatch('change', { value, alpha, formattedColor });
  }
  
  // Handle preset color selection
  function selectPresetColor(color) {
    value = color;
    dispatch('change', { value, alpha, formattedColor });
  }
  
  // Initialize component
  onMount(() => {
    // Ensure value is a valid hex color
    if (!value.startsWith('#')) {
      const { hex, alpha: newAlpha } = parseColor(value);
      value = hex;
      if (showAlpha) {
        alpha = newAlpha;
      }
    }
  });
</script>

<div class="color-picker-container" bind:this={colorPicker} use:clickOutside on:clickOutside={closePicker}>
  {#if label}
    <label for={id} class="block text-sm font-medium text-text-secondary mb-1">
      {label}
      {#if required}
        <span class="text-error-500">*</span>
      {/if}
    </label>
  {/if}
  
  <div class="relative">
    <div
      class="color-swatch flex items-center border border-border-light rounded-md overflow-hidden {disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}"
      on:click={togglePicker}
    >
      <div
        class="color-preview w-10 h-10"
        style="background-color: {value}; background-image: linear-gradient(45deg, #ccc 25%, transparent 25%), linear-gradient(-45deg, #ccc 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #ccc 75%), linear-gradient(-45deg, transparent 75%, #ccc 75%); background-size: 10px 10px; background-position: 0 0, 0 5px, 5px -5px, -5px 0px;"
      >
        <div
          class="w-full h-full"
          style="background-color: {showAlpha ? hexToRgba(value, alpha) : value};"
        ></div>
      </div>
      
      <input
        type="text"
        id={id}
        name={name}
        value={formattedColor}
        class="flex-1 px-3 py-2 border-l border-border-light bg-bg-primary text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500"
        on:input={handleInputChange}
        disabled={disabled}
        required={required}
      />
    </div>
    
    {#if isOpen}
      <div class="absolute z-10 mt-1 w-56 rounded-md shadow-lg bg-bg-primary border border-border-light">
        <div class="p-3">
          <!-- Saturation/Lightness picker -->
          <div
            bind:this={saturationPicker}
            class="saturation-picker w-full h-32 rounded-md mb-3 relative cursor-crosshair"
            style="background: linear-gradient(to right, #fff, {hueColor});"
            on:mousedown={handleSaturationMouseDown}
            on:touchstart={handleSaturationMouseDown}
          >
            <div class="absolute inset-0 bg-gradient-to-t from-black to-transparent rounded-md"></div>
            
            <div
              class="saturation-thumb absolute w-4 h-4 rounded-full border-2 border-white shadow-md transform -translate-x-1/2 -translate-y-1/2"
              style="left: {saturation * 100}%; top: {(1 - lightness) * 100}%; background-color: {value};"
            ></div>
          </div>
          
          <!-- Hue slider -->
          <div
            bind:this={hueSlider}
            class="hue-slider w-full h-4 rounded-md mb-3 relative cursor-pointer"
            style="background: linear-gradient(to right, #f00, #ff0, #0f0, #0ff, #00f, #f0f, #f00);"
            on:mousedown={handleHueMouseDown}
            on:touchstart={handleHueMouseDown}
          >
            <div
              class="hue-thumb absolute w-4 h-4 rounded-full border-2 border-white shadow-md transform -translate-x-1/2 -translate-y-1/2 top-1/2"
              style="left: {hue * 100}%; background-color: {hueColor};"
            ></div>
          </div>
          
          <!-- Alpha slider -->
          {#if showAlpha}
            <div
              bind:this={alphaSlider}
              class="alpha-slider w-full h-4 rounded-md mb-3 relative cursor-pointer"
              style="background-image: linear-gradient(45deg, #ccc 25%, transparent 25%), linear-gradient(-45deg, #ccc 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #ccc 75%), linear-gradient(-45deg, transparent 75%, #ccc 75%); background-size: 10px 10px; background-position: 0 0, 0 5px, 5px -5px, -5px 0px;"
              on:mousedown={handleAlphaMouseDown}
              on:touchstart={handleAlphaMouseDown}
            >
              <div
                class="absolute inset-0 rounded-md"
                style="background: linear-gradient(to right, transparent, {value});"
              ></div>
              
              <div
                class="alpha-thumb absolute w-4 h-4 rounded-full border-2 border-white shadow-md transform -translate-x-1/2 -translate-y-1/2 top-1/2"
                style="left: {alpha * 100}%; background-color: {hexToRgba(value, alpha)};"
              ></div>
            </div>
          {/if}
          
          <!-- Color value -->
          <div class="flex items-center mb-3">
            <div
              class="color-preview w-8 h-8 rounded-md mr-2"
              style="background-color: {showAlpha ? hexToRgba(value, alpha) : value};"
            ></div>
            
            <input
              type="text"
              value={formattedColor}
              class="flex-1 px-2 py-1 text-sm border border-border-light rounded-md bg-bg-primary text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500"
              on:input={handleInputChange}
            />
          </div>
          
          <!-- Preset colors -->
          {#if presetColors.length > 0}
            <div class="preset-colors grid grid-cols-7 gap-1">
              {#each presetColors as color}
                <button
                  type="button"
                  class="w-6 h-6 rounded-md border border-border-light overflow-hidden focus:outline-none focus:ring-2 focus:ring-primary-500"
                  style="background-color: {color};"
                  on:click={() => selectPresetColor(color)}
                  aria-label={color}
                >
                  {#if color === value}
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-auto" viewBox="0 0 20 20" fill={contrastColor}>
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  {/if}
                </button>
              {/each}
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>
  
  {#if error}
    <p class="mt-1 text-xs text-error-500">{error}</p>
  {:else if helperText}
    <p class="mt-1 text-xs text-text-tertiary">{helperText}</p>
  {/if}
</div>