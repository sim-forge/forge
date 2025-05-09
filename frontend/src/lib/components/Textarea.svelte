<script>
  import { createEventDispatcher } from 'svelte';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
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
  export let rows = 4;
  export let maxlength = null;
  export let fullWidth = false;
  export let resizable = true;
  export let showCount = false;
  
  // Computed classes
  $: widthClass = fullWidth ? 'w-full' : '';
  $: errorClass = error ? 'border-error-500 focus:ring-error-500 focus:border-error-500' : 'border-border-medium focus:ring-primary-500 focus:border-primary-500';
  $: disabledClass = disabled ? 'opacity-60 cursor-not-allowed bg-bg-tertiary' : '';
  $: resizableClass = resizable ? '' : 'resize-none';
  
  // Character count
  $: charCount = value ? value.length : 0;
  $: showMaxLength = showCount && maxlength;
  
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
</script>

<div class="textarea-wrapper {widthClass}">
  {#if label}
    <label for={id} class="block text-text-secondary text-sm font-medium mb-1">
      {label}
      {#if required}
        <span class="text-error-500">*</span>
      {/if}
    </label>
  {/if}
  
  <textarea
    {id}
    {name}
    {placeholder}
    {disabled}
    {readonly}
    {required}
    {rows}
    {maxlength}
    autofocus={autofocus ? true : null}
    bind:value
    on:input={handleInput}
    on:change={handleChange}
    on:focus={handleFocus}
    on:blur={handleBlur}
    class="block rounded-md shadow-sm py-2 px-4 {widthClass} {errorClass} {disabledClass} {resizableClass} bg-bg-primary text-text-primary placeholder-text-tertiary focus:outline-none focus:ring-2 transition-colors duration-200"
  ></textarea>
  
  <div class="flex justify-between mt-1">
    {#if error}
      <p class="text-xs text-error-500">{error}</p>
    {:else if helperText}
      <p class="text-xs text-text-tertiary">{helperText}</p>
    {:else}
      <span></span>
    {/if}
    
    {#if showCount}
      <p class="text-xs text-text-tertiary">
        {charCount}{#if showMaxLength} / {maxlength}{/if}
      </p>
    {/if}
  </div>
</div>

<style>
  .textarea-wrapper {
    margin-bottom: 1rem;
  }
  
  textarea {
    border-width: 1px;
    min-height: 2.5rem;
    line-height: 1.5;
  }
</style>