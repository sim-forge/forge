<script>
  // Props
  export let items = [];
  export let separator = '/';
  export let homeIcon = true;
  export let maxItems = 0; // 0 means show all
  export let collapsible = false;
  export let activeClass = 'text-text-primary font-medium';
  export let inactiveClass = 'text-text-tertiary hover:text-text-secondary';
  
  // Computed values
  $: visibleItems = getVisibleItems(items, maxItems, collapsible);
  
  // Helper functions
  function getVisibleItems(items, maxItems, collapsible) {
    if (!maxItems || items.length <= maxItems || !collapsible) {
      return items;
    }
    
    // Always show first and last items
    const firstItem = items[0];
    const lastItem = items[items.length - 1];
    
    // Calculate how many middle items to show
    const middleCount = maxItems - 2;
    
    if (middleCount <= 0) {
      // If we can only show 2 or fewer items, just show first and last
      return [
        firstItem,
        { label: '...', href: null, active: false, ellipsis: true },
        lastItem
      ];
    }
    
    // Show some middle items
    const middleItems = items.slice(1, -1);
    
    if (middleItems.length <= middleCount) {
      // If we have fewer middle items than we can show, show them all
      return items;
    }
    
    // Determine which middle items to show
    const visibleMiddleItems = [];
    
    if (middleCount === 1) {
      // If we can only show one middle item, show an ellipsis
      visibleMiddleItems.push({ label: '...', href: null, active: false, ellipsis: true });
    } else {
      // Show some middle items with ellipsis
      const itemsFromStart = Math.floor(middleCount / 2);
      const itemsFromEnd = middleCount - itemsFromStart - 1;
      
      // Add items from the start
      for (let i = 0; i < itemsFromStart; i++) {
        visibleMiddleItems.push(middleItems[i]);
      }
      
      // Add ellipsis
      visibleMiddleItems.push({ label: '...', href: null, active: false, ellipsis: true });
      
      // Add items from the end
      for (let i = middleItems.length - itemsFromEnd; i < middleItems.length; i++) {
        visibleMiddleItems.push(middleItems[i]);
      }
    }
    
    return [firstItem, ...visibleMiddleItems, lastItem];
  }
</script>

<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol class="flex items-center space-x-2 text-sm">
    {#each visibleItems as item, index}
      <li class="flex items-center">
        {#if index > 0}
          <span class="mx-2 text-text-tertiary" aria-hidden="true">
            {#if typeof separator === 'string'}
              {separator}
            {:else}
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
            {/if}
          </span>
        {/if}
        
        {#if item.ellipsis}
          <span class="text-text-tertiary">
            {item.label}
          </span>
        {:else if item.href && !item.active}
          <a
            href={item.href}
            class={`${inactiveClass} ${index === 0 && homeIcon ? 'flex items-center' : ''}`}
            aria-current={item.active ? 'page' : undefined}
          >
            {#if index === 0 && homeIcon}
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
              </svg>
            {/if}
            {item.label}
          </a>
        {:else}
          <span
            class={item.active ? activeClass : inactiveClass}
            aria-current={item.active ? 'page' : undefined}
          >
            {#if index === 0 && homeIcon}
              <span class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                </svg>
                {item.label}
              </span>
            {:else}
              {item.label}
            {/if}
          </span>
        {/if}
      </li>
    {/each}
  </ol>
</nav>