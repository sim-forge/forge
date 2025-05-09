<script>
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  
  export let activeTab = 'table';
  export let sequenceTitle = 'Untitled Sequence';
  export let isModified = false;
  
  const dispatch = createEventDispatcher();
  
  function setActiveTab(tab) {
    activeTab = tab;
    dispatch('tab-change', { tab });
  }
  
  function handleTitleChange(event) {
    sequenceTitle = event.target.value;
    dispatch('title-change', { title: sequenceTitle });
  }
  
  function handleSave() {
    dispatch('save');
  }
  
  function handleNew() {
    dispatch('new');
  }
  
  function handleOpen() {
    dispatch('open');
  }
  
  function handleSettings() {
    dispatch('settings');
  }
</script>

<div class="ribbon">
  <div class="ribbon-left">
    <div class="sequence-title">
      <input 
        type="text" 
        value={sequenceTitle} 
        on:input={handleTitleChange}
        placeholder="Untitled Sequence"
      />
      {#if isModified}
        <span class="modified-indicator" transition:fade>*</span>
      {/if}
    </div>
    
    <div class="ribbon-actions">
      <button class="ribbon-btn" on:click={handleNew}>New</button>
      <button class="ribbon-btn" on:click={handleOpen}>Open</button>
      <button class="ribbon-btn" on:click={handleSave}>Save</button>
    </div>
  </div>
  
  <div class="ribbon-tabs">
    <button 
      class="tab-btn" 
      class:active={activeTab === 'table'} 
      on:click={() => setActiveTab('table')}
    >
      Table
    </button>
    
    <button 
      class="tab-btn" 
      class:active={activeTab === 'graph'} 
      on:click={() => setActiveTab('graph')}
    >
      Graph
    </button>
    
    <button 
      class="tab-btn" 
      class:active={activeTab === 'prompt'} 
      on:click={() => setActiveTab('prompt')}
    >
      Prompt
    </button>
    
    <button 
      class="tab-btn" 
      class:active={activeTab === 'chat'} 
      on:click={() => setActiveTab('chat')}
    >
      Chat
    </button>
  </div>
  
  <div class="ribbon-right">
    <button class="settings-btn" on:click={handleSettings}>
      Settings
    </button>
  </div>
</div>

<style>
  .ribbon {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #2c3e50;
    color: white;
    padding: 0.5rem 1rem;
    height: 60px;
  }
  
  .ribbon-left {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .sequence-title {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  
  .sequence-title input {
    background-color: transparent;
    border: none;
    color: white;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 0.25rem 0;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
    width: 200px;
  }
  
  .sequence-title input:focus {
    outline: none;
    border-bottom-color: #3498db;
  }
  
  .modified-indicator {
    color: #e74c3c;
    font-weight: bold;
  }
  
  .ribbon-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .ribbon-btn {
    background-color: transparent;
    border: none;
    color: #ecf0f1;
    padding: 0.25rem 0.5rem;
    cursor: pointer;
    transition: color 0.2s;
    font-size: 0.9rem;
  }
  
  .ribbon-btn:hover {
    color: #3498db;
  }
  
  .ribbon-tabs {
    display: flex;
    gap: 0.25rem;
  }
  
  .tab-btn {
    background-color: transparent;
    border: none;
    color: #ecf0f1;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
    border-radius: 4px;
    font-weight: 500;
  }
  
  .tab-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .tab-btn.active {
    background-color: #3498db;
    color: white;
  }
  
  .ribbon-right {
    display: flex;
    align-items: center;
  }
  
  .settings-btn {
    background-color: transparent;
    border: 1px solid #ecf0f1;
    color: #ecf0f1;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
  }
  
  .settings-btn:hover {
    background-color: #ecf0f1;
    color: #2c3e50;
  }
</style>