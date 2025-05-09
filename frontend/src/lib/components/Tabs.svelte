<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { slide } from 'svelte/transition';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let tabs = [];
  export let activeTab = null;
  export let variant = 'default'; // default, pills, underline, minimal
  export let size = 'md'; // sm, md, lg
  export let fullWidth = false;
  export let vertical = false;
  export let contentClass = '';
  
  // Local state
  let tabsContainer;
  let indicator;
  let activeTabElement;
  
  // Computed classes
  $: variantClass = getVariantClass(variant);
  $: sizeClass = getSizeClass(size);
  $: layoutClass = vertical ? 'flex-col' : 'flex-row';
  $: widthClass = fullWidth && !vertical ? 'w-full' : '';
  $: tabWidthClass = fullWidth && !vertical ? 'flex-1' : '';
  
  // Helper functions
  function getVariantClass(variant) {
    const variants = {
      default: 'bg-bg-secondary rounded-lg p-1',
      pills: 'space-x-2',
      underline: 'border-b border-border-light',
      minimal: '',
    };
    
    return variants[variant] || variants.default;
  }
  
  function getSizeClass(size) {
    const sizes = {
      sm: 'text-xs',
      md: 'text-sm',
      lg: 'text-base',
    };
    
    return sizes[size] || sizes.md;
  }
  
  // Set active tab
  function setActiveTab(tab) {
    if (tab.disabled) return;
    
    activeTab = tab.id;
    dispatch('change', { tab });
    
    // Update indicator position
    updateIndicator();
  }
  
  // Update indicator position
  function updateIndicator() {
    if (variant !== 'underline' || !tabsContainer || !indicator) return;
    
    // Find the active tab element
    activeTabElement = tabsContainer.querySelector(`[data-tab-id="${activeTab}"]`);
    
    if (activeTabElement) {
      if (vertical) {
        indicator.style.top = `${activeTabElement.offsetTop}px`;
        indicator.style.height = `${activeTabElement.offsetHeight}px`;
        indicator.style.width = '2px';
        indicator.style.left = '0';
      } else {
        indicator.style.left = `${activeTabElement.offsetLeft}px`;
        indicator.style.width = `${activeTabElement.offsetWidth}px`;
        indicator.style.height = '2px';
        indicator.style.bottom = '0';
      }
    }
  }
  
  // Initialize component
  onMount(() => {
    // Set default active tab if not provided
    if (!activeTab && tabs.length > 0) {
      const firstEnabledTab = tabs.find(tab => !tab.disabled);
      if (firstEnabledTab) {
        activeTab = firstEnabledTab.id;
      }
    }
    
    // Update indicator position
    updateIndicator();
    
    // Add resize listener for indicator
    const resizeObserver = new ResizeObserver(() => {
      updateIndicator();
    });
    
    if (tabsContainer) {
      resizeObserver.observe(tabsContainer);
    }
    
    return () => {
      if (tabsContainer) {
        resizeObserver.unobserve(tabsContainer);
      }
    };
  });
  
  // Watch for activeTab changes
  $: if (activeTab) {
    // Wait for DOM update
    setTimeout(updateIndicator, 0);
  }
</script>

<div class="tabs-component {vertical ? 'flex' : ''}">
  <div
    bind:this={tabsContainer}
    class="tabs-list flex {layoutClass} {variantClass} {sizeClass} {widthClass}"
    role="tablist"
  >
    {#each tabs as tab}
      {@const isActive = activeTab === tab.id}
      <button
        type="button"
        role="tab"
        id={`tab-${tab.id}`}
        aria-selected={isActive}
        aria-controls={`panel-${tab.id}`}
        class="tab-item {sizeClass} {tabWidthClass} font-medium px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md transition-colors duration-200 {tab.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}"
        class:active={isActive}
        class:tab-default={variant === 'default' && isActive}
        class:tab-pills={variant === 'pills' && isActive}
        class:tab-underline={variant === 'underline' && isActive}
        class:tab-minimal={variant === 'minimal' && isActive}
        disabled={tab.disabled}
        data-tab-id={tab.id}
        on:click={() => setActiveTab(tab)}
      >
        {#if tab.icon}
          <span class="mr-2">{tab.icon}</span>
        {/if}
        
        {tab.label}
        
        {#if tab.badge}
          <span class="ml-2 px-2 py-0.5 text-xs rounded-full bg-primary-100 text-primary-800">
            {tab.badge}
          </span>
        {/if}
      </button>
    {/each}
    
    {#if variant === 'underline'}
      <div bind:this={indicator} class="indicator absolute bg-primary-500 transition-all duration-200"></div>
    {/if}
  </div>
  
  <div class="tabs-content mt-4 {vertical ? 'flex-1 ml-4' : ''} {contentClass}">
    {#each tabs as tab}
      {#if activeTab === tab.id}
        <div
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          transition:slide={{ duration: 200 }}
        >
          <slot name={tab.id} />
        </div>
      {/if}
    {/each}
  </div>
</div>

<style>
  .tabs-component {
    position: relative;
  }
  
  .tabs-list {
    position: relative;
  }
  
  .tab-default {
    background-color: var(--bg-primary);
    color: var(--text-primary);
  }
  
  .tab-pills {
    background-color: var(--primary-500);
    color: white;
  }
  
  .tab-underline {
    color: var(--primary-500);
  }
  
  .tab-minimal.active {
    color: var(--primary-500);
  }
  
  .indicator {
    position: absolute;
    transition: all 0.2s ease;
  }
</style>