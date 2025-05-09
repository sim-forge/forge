<script>
  import { createEventDispatcher } from 'svelte';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let totalItems = 0;
  export let pageSize = 10;
  export let currentPage = 1;
  export let siblingCount = 1;
  export let showFirstLast = true;
  export let showPrevNext = true;
  export let showPageSize = false;
  export let pageSizeOptions = [5, 10, 25, 50, 100];
  export let disabled = false;
  export let variant = 'default'; // default, simple, minimal
  
  // Computed values
  $: totalPages = Math.ceil(totalItems / pageSize);
  $: pageRange = getPageRange(currentPage, totalPages, siblingCount);
  
  // Computed classes
  $: variantClass = getVariantClass(variant);
  
  // Helper functions
  function getVariantClass(variant) {
    const variants = {
      default: {
        container: 'flex items-center',
        button: 'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
        active: 'z-10 bg-primary-50 border-primary-500 text-primary-600',
        inactive: 'bg-bg-primary border-border-light text-text-primary hover:bg-bg-secondary',
        disabled: 'opacity-50 cursor-not-allowed',
      },
      simple: {
        container: 'flex items-center',
        button: 'relative inline-flex items-center px-3 py-1.5 text-sm font-medium',
        active: 'z-10 text-primary-600 underline',
        inactive: 'text-text-primary hover:text-primary-600',
        disabled: 'opacity-50 cursor-not-allowed',
      },
      minimal: {
        container: 'flex items-center',
        button: 'relative inline-flex items-center p-1 text-sm font-medium rounded-full w-8 h-8 justify-center',
        active: 'z-10 bg-primary-500 text-white',
        inactive: 'text-text-primary hover:bg-bg-secondary',
        disabled: 'opacity-50 cursor-not-allowed',
      },
    };
    
    return variants[variant] || variants.default;
  }
  
  function getPageRange(currentPage, totalPages, siblingCount) {
    const totalPageNumbers = siblingCount * 2 + 3; // siblings + current + first + last
    
    // Case 1: If the number of pages is less than the page numbers we want to show
    if (totalPageNumbers >= totalPages) {
      return range(1, totalPages);
    }
    
    const leftSiblingIndex = Math.max(currentPage - siblingCount, 1);
    const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages);
    
    const shouldShowLeftDots = leftSiblingIndex > 2;
    const shouldShowRightDots = rightSiblingIndex < totalPages - 1;
    
    // Case 2: No left dots to show, but right dots to be shown
    if (!shouldShowLeftDots && shouldShowRightDots) {
      const leftItemCount = 1 + 2 * siblingCount;
      const leftRange = range(1, leftItemCount);
      
      return [...leftRange, 'DOTS', totalPages];
    }
    
    // Case 3: No right dots to show, but left dots to be shown
    if (shouldShowLeftDots && !shouldShowRightDots) {
      const rightItemCount = 1 + 2 * siblingCount;
      const rightRange = range(totalPages - rightItemCount + 1, totalPages);
      
      return [1, 'DOTS', ...rightRange];
    }
    
    // Case 4: Both left and right dots to be shown
    if (shouldShowLeftDots && shouldShowRightDots) {
      const middleRange = range(leftSiblingIndex, rightSiblingIndex);
      
      return [1, 'DOTS', ...middleRange, 'DOTS', totalPages];
    }
  }
  
  function range(start, end) {
    const length = end - start + 1;
    return Array.from({ length }, (_, i) => start + i);
  }
  
  // Handle page change
  function goToPage(page) {
    if (disabled || page === currentPage || page < 1 || page > totalPages) {
      return;
    }
    
    currentPage = page;
    dispatch('pageChange', { page, pageSize });
  }
  
  // Handle page size change
  function handlePageSizeChange(event) {
    const newPageSize = Number(event.target.value);
    pageSize = newPageSize;
    currentPage = 1; // Reset to first page
    dispatch('pageSizeChange', { page: currentPage, pageSize });
  }
</script>

<div class="pagination {variantClass.container}">
  {#if showPageSize}
    <div class="mr-4">
      <select
        class="block w-full rounded-md border-border-light shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
        on:change={handlePageSizeChange}
        disabled={disabled}
        aria-label="Items per page"
      >
        {#each pageSizeOptions as option}
          <option value={option} selected={pageSize === option}>
            {option} per page
          </option>
        {/each}
      </select>
    </div>
  {/if}
  
  <nav class="pagination-nav" aria-label="Pagination">
    {#if showFirstLast}
      <button
        type="button"
        class="{variantClass.button} rounded-l-md {currentPage === 1 || disabled ? variantClass.disabled : variantClass.inactive}"
        on:click={() => goToPage(1)}
        disabled={currentPage === 1 || disabled}
        aria-label="Go to first page"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
    
    {#if showPrevNext}
      <button
        type="button"
        class="{variantClass.button} {!showFirstLast ? 'rounded-l-md' : ''} {currentPage === 1 || disabled ? variantClass.disabled : variantClass.inactive}"
        on:click={() => goToPage(currentPage - 1)}
        disabled={currentPage === 1 || disabled}
        aria-label="Previous page"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
    
    {#each pageRange as page}
      {#if page === 'DOTS'}
        <span class="{variantClass.button} border-border-light bg-bg-primary text-text-tertiary">
          &hellip;
        </span>
      {:else}
        <button
          type="button"
          class="{variantClass.button} {page === currentPage ? variantClass.active : variantClass.inactive} {disabled ? variantClass.disabled : ''}"
          aria-current={page === currentPage ? 'page' : undefined}
          on:click={() => goToPage(page)}
          disabled={disabled}
        >
          {page}
        </button>
      {/if}
    {/each}
    
    {#if showPrevNext}
      <button
        type="button"
        class="{variantClass.button} {!showFirstLast ? 'rounded-r-md' : ''} {currentPage === totalPages || disabled ? variantClass.disabled : variantClass.inactive}"
        on:click={() => goToPage(currentPage + 1)}
        disabled={currentPage === totalPages || disabled}
        aria-label="Next page"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
    
    {#if showFirstLast}
      <button
        type="button"
        class="{variantClass.button} rounded-r-md {currentPage === totalPages || disabled ? variantClass.disabled : variantClass.inactive}"
        on:click={() => goToPage(totalPages)}
        disabled={currentPage === totalPages || disabled}
        aria-label="Go to last page"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10.293 15.707a1 1 0 010-1.414L14.586 10l-4.293-4.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          <path fill-rule="evenodd" d="M4.293 15.707a1 1 0 010-1.414L8.586 10 4.293 5.707a1 1 0 011.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clip-rule="evenodd" />
        </svg>
      </button>
    {/if}
  </nav>
  
  <div class="ml-4 text-sm text-text-tertiary">
    {#if totalItems > 0}
      <span>
        Showing <span class="font-medium">{Math.min((currentPage - 1) * pageSize + 1, totalItems)}</span> to <span class="font-medium">{Math.min(currentPage * pageSize, totalItems)}</span> of <span class="font-medium">{totalItems}</span> results
      </span>
    {:else}
      <span>No results</span>
    {/if}
  </div>
</div>