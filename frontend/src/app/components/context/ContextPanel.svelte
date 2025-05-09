<script>
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  
  export let context = '';
  export let expanded = false;
  
  const dispatch = createEventDispatcher();
  
  function handleContextChange(event) {
    context = event.target.value;
    dispatch('update', { context });
  }
  
  function toggleExpanded() {
    expanded = !expanded;
  }
</script>

<div class="context-panel" class:expanded>
  <div class="panel-header" on:click={toggleExpanded}>
    <h3>Context</h3>
    <button class="toggle-btn">
      {expanded ? '▼' : '▶'}
    </button>
  </div>
  
  {#if expanded}
    <div class="panel-content" transition:fade={{ duration: 200 }}>
      <textarea 
        class="context-input"
        placeholder="Enter context information here..."
        value={context}
        on:input={handleContextChange}
      ></textarea>
      
      <div class="panel-actions">
        <button class="btn btn-primary" on:click={() => dispatch('apply')}>
          Apply Context
        </button>
        <button class="btn btn-outline" on:click={() => dispatch('clear')}>
          Clear
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .context-panel {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    overflow: hidden;
  }
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    cursor: pointer;
    border-bottom: 1px solid #e9ecef;
  }
  
  .panel-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #2c3e50;
  }
  
  .toggle-btn {
    background: none;
    border: none;
    font-size: 1rem;
    color: #6c757d;
    cursor: pointer;
  }
  
  .panel-content {
    padding: 1rem;
  }
  
  .context-input {
    width: 100%;
    min-height: 120px;
    padding: 0.75rem;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    font-family: inherit;
    font-size: 0.9rem;
    resize: vertical;
    margin-bottom: 1rem;
  }
  
  .panel-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .btn-primary {
    background-color: #3498db;
    color: white;
    border: none;
  }
  
  .btn-primary:hover {
    background-color: #2980b9;
  }
  
  .btn-outline {
    background-color: transparent;
    border: 1px solid #bdc3c7;
    color: #2c3e50;
  }
  
  .btn-outline:hover {
    background-color: #f8f9fa;
  }
</style>