<script>
  import { createEventDispatcher } from 'svelte';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let type = 'text';
  export let name = '';
  export let id = name;
  export let value = '';
  export let placeholder = '';
  export let label = '';
  export let helperText = '';
  export let error = '';
  export let disabled = false;
  export let readonly = false;
  export let required = false;
  export let autofocus = false;
  export let autocomplete = 'off';
  export let size = 'md'; // sm, md, lg
  export let fullWidth = false;
  export let icon = null;
  export let iconPosition = 'left'; // left, right
  export let clearable = false;
  
  // Computed classes
  $: sizeClass = getSizeClass(size);
  $: widthClass = fullWidth ? 'w-full' : '';
  $: errorClass = error ? 'border-error-500 focus:ring-error-500 focus:border-error-500' : 'border-border-medium focus:ring-primary-500 focus:border-primary-500';
  $: disabledClass = disabled ? 'opacity-60 cursor-not-allowed bg-bg-tertiary' : '';
  $: iconClass = icon ? (iconPosition === 'left' ? 'pl-10' : 'pr-10') : '';
  
  // Helper functions
  function getSizeClass(size) {
    const sizes = {
      sm: 'text-xs py-1.5 px-3',
      md: 'text-sm py-2 px-4',
      lg: 'text-base py-2.5 px-5',
    };
    
    return sizes[size] || sizes.md;
  }
  
  // Handle input
  function handleInput(event) {
    value = event.target.value;
    dispatch('input', { value, name, event });
  }
  
  // Handle change
  function handleChange(event) {
    dispatch('change', { value, name, event });
  }
  
  // Handle focus
  function handleFocus(event) {
    dispatch('focus', { value, name, event });
  }
  
  // Handle blur
  function handleBlur(event) {
    dispatch('blur', { value, name, event });
  }
  
  // Clear input
  function clearInput() {
    value = '';
    dispatch('input', { value, name });
    dispatch('clear');
  }
</script>

<div class="input-wrapper {widthClass}">
  {#if label}
    <label for={id} class="block text-text-secondary text-sm font-medium mb-1">
      {label}
      {#if required}
        <span class="text-error-500">*</span>
      {/if}
    </label>
  {/if}
  
  <div class="relative">
    {#if icon && iconPosition === 'left'}
      <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-text-tertiary">
        {icon}
      </div>
    {/if}
    
    <input
      {type}
      {id}
      {name}
      {placeholder}
      {disabled}
      {readonly}
      {required}
      {autocomplete}
      autofocus={autofocus ? true : null}
      bind:value
      on:input={handleInput}
      on:change={handleChange}
      on:focus={handleFocus}
      on:blur={handleBlur}
      class="block rounded-md shadow-sm {sizeClass} {widthClass} {errorClass} {disabledClass} {iconClass} bg-bg-primary text-text-primary placeholder-text-tertiary focus:outline-none focus:ring-2 transition-colors duration-200"
    />
    
    {#if icon && iconPosition === 'right'}
      <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-text-tertiary">
        {icon}
      </div>
    {/if}
    
    {#if clearable && value && !disabled && !readonly}
      <button
        type="button"
        class="absolute inset-y-0 right-0 flex items-center pr-3 text-text-tertiary hover:text-text-secondary"
        on:click={clearInput}
        aria-label="Clear input"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
  </div>
  
  {#if error}
    <p class="mt-1 text-xs text-error-500">{error}</p>
  {:else if helperText}
    <p class="mt-1 text-xs text-text-tertiary">{helperText}</p>
  {/if}
</div>

<style>
  .input-wrapper {
    margin-bottom: 1rem;
  }
  
  input {
    border-width: 1px;
  }
</style>