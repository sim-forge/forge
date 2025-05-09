<script>
  import { createEventDispatcher } from 'svelte';
  import { slide } from 'svelte/transition';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let items = [];
  export let multiple = false;
  export let defaultOpen = [];
  export let variant = 'default'; // default, bordered, minimal
  export let iconPosition = 'right'; // left, right
  export let customIcon = null;
  
  // Local state
  let openItems = [...defaultOpen];
  
  // Computed classes
  $: variantClass = getVariantClass(variant);
  
  // Helper functions
  function getVariantClass(variant) {
    const variants = {
      default: 'bg-bg-primary rounded-lg shadow-sm',
      bordered: 'border border-border-light rounded-lg',
      minimal: '',
    };
    
    return variants[variant] || variants.default;
  }
  
  // Toggle item
  function toggleItem(itemId) {
    if (multiple) {
      // Multiple items can be open
      if (openItems.includes(itemId)) {
        openItems = openItems.filter(id => id !== itemId);
      } else {
        openItems = [...openItems, itemId];
      }
    } else {
      // Only one item can be open
      if (openItems.includes(itemId)) {
        openItems = [];
      } else {
        openItems = [itemId];
      }
    }
    
    dispatch('change', { openItems });
  }
  
  // Check if item is open
  function isItemOpen(itemId) {
    return openItems.includes(itemId);
  }
</script>

<div class="accordion {variantClass}">
  {#each items as item, index}
    {@const isOpen = isItemOpen(item.id)}
    <div class="accordion-item {variant === 'minimal' ? '' : 'border-b border-border-light last:border-b-0'}">
      <button
        type="button"
        class="accordion-header w-full flex items-center justify-between py-3 px-4 text-left font-medium focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-t-lg"
        class:text-primary-600={isOpen}
        aria-expanded={isOpen}
        aria-controls={`accordion-panel-${item.id}`}
        on:click={() => toggleItem(item.id)}
      >
        <div class="flex items-center">
          {#if iconPosition === 'left'}
            <div class="mr-3 flex-shrink-0 transition-transform duration-200" class:rotate-90={isOpen}>
              {#if customIcon}
                {customIcon}
              {:else}
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              {/if}
            </div>
          {/if}
          
          <span>{item.title}</span>
        </div>
        
        {#if iconPosition === 'right'}
          <div class="ml-3 flex-shrink-0 transition-transform duration-200" class:rotate-180={isOpen}>
            {#if customIcon}
              {customIcon}
            {:else}
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            {/if}
          </div>
        {/if}
      </button>
      
      {#if isOpen}
        <div
          id={`accordion-panel-${item.id}`}
          transition:slide={{ duration: 200 }}
          class="accordion-panel px-4 pb-4 pt-1"
        >
          {#if item.content}
            <div class="text-text-secondary">
              {item.content}
            </div>
          {:else if item.slot}
            <slot name={item.slot} />
          {/if}
        </div>
      {/if}
    </div>
  {/each}
</div>