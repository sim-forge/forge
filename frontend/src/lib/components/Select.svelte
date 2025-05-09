<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { slide } from 'svelte/transition';
  import { clickOutside } from '../utils/clickOutside';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let name = '';
  export let id = name;
  export let value = '';
  export let placeholder = 'Select an option';
  export let label = '';
  export let helperText = '';
  export let error = '';
  export let disabled = false;
  export let required = false;
  export let options = [];
  export let optionLabelKey = 'label';
  export let optionValueKey = 'value';
  export let size = 'md'; // sm, md, lg
  export let fullWidth = false;
  export let searchable = false;
  export let clearable = false;
  
  // Local state
  let isOpen = false;
  let searchTerm = '';
  let selectedLabel = '';
  let selectContainer;
  
  // Computed classes
  $: sizeClass = getSizeClass(size);
  $: widthClass = fullWidth ? 'w-full' : '';
  $: errorClass = error ? 'border-error-500 focus:ring-error-500 focus:border-error-500' : 'border-border-medium focus:ring-primary-500 focus:border-primary-500';
  $: disabledClass = disabled ? 'opacity-60 cursor-not-allowed bg-bg-tertiary' : '';
  
  // Filtered options
  $: filteredOptions = searchable && searchTerm
    ? options.filter(option => 
        getOptionLabel(option).toLowerCase().includes(searchTerm.toLowerCase())
      )
    : options;
  
  // Helper functions
  function getSizeClass(size) {
    const sizes = {
      sm: 'text-xs py-1.5 px-3',
      md: 'text-sm py-2 px-4',
      lg: 'text-base py-2.5 px-5',
    };
    
    return sizes[size] || sizes.md;
  }
  
  function getOptionLabel(option) {
    if (typeof option === 'string') return option;
    return option[optionLabelKey] || '';
  }
  
  function getOptionValue(option) {
    if (typeof option === 'string') return option;
    return option[optionValueKey] || '';
  }
  
  // Update selected label when value changes
  $: {
    const selectedOption = options.find(option => getOptionValue(option) === value);
    selectedLabel = selectedOption ? getOptionLabel(selectedOption) : '';
  }
  
  // Toggle dropdown
  function toggleDropdown() {
    if (!disabled) {
      isOpen = !isOpen;
      if (isOpen && searchable) {
        setTimeout(() => {
          const searchInput = selectContainer.querySelector('input[type="text"]');
          if (searchInput) searchInput.focus();
        }, 0);
      }
    }
  }
  
  // Close dropdown
  function closeDropdown() {
    isOpen = false;
    searchTerm = '';
  }
  
  // Select option
  function selectOption(option) {
    const newValue = getOptionValue(option);
    value = newValue;
    selectedLabel = getOptionLabel(option);
    dispatch('change', { value: newValue, name });
    closeDropdown();
  }
  
  // Clear selection
  function clearSelection() {
    value = '';
    selectedLabel = '';
    dispatch('change', { value: '', name });
    dispatch('clear');
  }
  
  // Handle search input
  function handleSearchInput(event) {
    searchTerm = event.target.value;
  }
  
  // Initialize component
  onMount(() => {
    // Set initial selected label
    const selectedOption = options.find(option => getOptionValue(option) === value);
    if (selectedOption) {
      selectedLabel = getOptionLabel(selectedOption);
    }
  });
</script>

<div class="select-wrapper {widthClass}" bind:this={selectContainer} use:clickOutside on:clickOutside={closeDropdown}>
  {#if label}
    <label for={id} class="block text-text-secondary text-sm font-medium mb-1">
      {label}
      {#if required}
        <span class="text-error-500">*</span>
      {/if}
    </label>
  {/if}
  
  <div class="relative">
    <button
      type="button"
      id={id}
      class="flex items-center justify-between rounded-md shadow-sm {sizeClass} {widthClass} {errorClass} {disabledClass} bg-bg-primary text-text-primary focus:outline-none focus:ring-2 transition-colors duration-200 border"
      on:click={toggleDropdown}
      disabled={disabled}
      aria-haspopup="listbox"
      aria-expanded={isOpen}
    >
      <span class={!value ? 'text-text-tertiary' : ''}>
        {value ? selectedLabel : placeholder}
      </span>
      
      <div class="flex items-center">
        {#if clearable && value}
          <button
            type="button"
            class="mr-1 text-text-tertiary hover:text-text-secondary"
            on:click|stopPropagation={clearSelection}
            aria-label="Clear selection"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </button>
        {/if}
        
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-text-tertiary" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </div>
    </button>
    
    {#if isOpen}
      <div
        transition:slide={{ duration: 200 }}
        class="absolute z-10 mt-1 w-full rounded-md shadow-lg bg-bg-primary border border-border-light max-h-60 overflow-auto"
      >
        {#if searchable}
          <div class="sticky top-0 p-2 bg-bg-primary border-b border-border-light">
            <input
              type="text"
              placeholder="Search..."
              class="w-full px-3 py-1.5 text-sm rounded-md border border-border-medium focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              on:input={handleSearchInput}
              value={searchTerm}
            />
          </div>
        {/if}
        
        <ul class="py-1" role="listbox">
          {#if filteredOptions.length === 0}
            <li class="px-4 py-2 text-text-tertiary text-sm">No options found</li>
          {:else}
            {#each filteredOptions as option}
              {@const optionValue = getOptionValue(option)}
              {@const optionLabel = getOptionLabel(option)}
              <li
                role="option"
                aria-selected={value === optionValue}
                class="px-4 py-2 text-sm cursor-pointer hover:bg-bg-secondary {value === optionValue ? 'bg-primary-50 text-primary-700' : 'text-text-primary'}"
                on:click={() => selectOption(option)}
              >
                {optionLabel}
              </li>
            {/each}
          {/if}
        </ul>
      </div>
    {/if}
  </div>
  
  {#if error}
    <p class="mt-1 text-xs text-error-500">{error}</p>
  {:else if helperText}
    <p class="mt-1 text-xs text-text-tertiary">{helperText}</p>
  {/if}
  
  <!-- Hidden input for form submission -->
  <input type="hidden" {name} {value} />
</div>

<style>
  .select-wrapper {
    margin-bottom: 1rem;
  }
</style>