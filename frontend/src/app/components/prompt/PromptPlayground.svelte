<script>
  import { createEventDispatcher } from 'svelte';
  import { fade, slide } from 'svelte/transition';
  import LoadingSpinner from '../common/LoadingSpinner.svelte';
  
  export let templates = [];
  export let currentTemplate = null;
  export let systemPrompt = '';
  export let userPrompt = '';
  export let isLoading = false;
  
  const dispatch = createEventDispatcher();
  
  let showTemplateSelector = false;
  
  function selectTemplate(template) {
    currentTemplate = template;
    systemPrompt = template.system || '';
    userPrompt = template.user || '';
    showTemplateSelector = false;
    dispatch('select-template', { template });
  }
  
  function handleSystemPromptChange(event) {
    systemPrompt = event.target.value;
    dispatch('update-system', { systemPrompt });
  }
  
  function handleUserPromptChange(event) {
    userPrompt = event.target.value;
    dispatch('update-user', { userPrompt });
  }
  
  function saveAsTemplate() {
    dispatch('save-template', { systemPrompt, userPrompt });
  }
  
  function generateSequence() {
    dispatch('generate', { systemPrompt, userPrompt });
  }
</script>

<div class="prompt-playground">
  <div class="playground-header">
    <h3>Prompt Playground</h3>
    
    <div class="template-controls">
      <button class="btn btn-outline" on:click={() => showTemplateSelector = !showTemplateSelector}>
        {currentTemplate ? currentTemplate.name : 'Select Template'} {showTemplateSelector ? '▼' : '▶'}
      </button>
      
      <button class="btn btn-outline" on:click={saveAsTemplate}>
        Save as Template
      </button>
    </div>
  </div>
  
  {#if showTemplateSelector}
    <div class="template-selector" transition:slide={{ duration: 200 }}>
      <ul class="template-list">
        {#each templates as template}
          <li class="template-item" on:click={() => selectTemplate(template)}>
            <span class="template-name">{template.name}</span>
            <span class="template-description">{template.description}</span>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
  
  <div class="prompt-editor">
    <div class="prompt-section">
      <label for="system-prompt">System Prompt</label>
      <textarea 
        id="system-prompt"
        class="prompt-input system-prompt"
        placeholder="Enter system prompt here..."
        value={systemPrompt}
        on:input={handleSystemPromptChange}
      ></textarea>
    </div>
    
    <div class="prompt-section">
      <label for="user-prompt">User Prompt</label>
      <textarea 
        id="user-prompt"
        class="prompt-input user-prompt"
        placeholder="Enter user prompt here..."
        value={userPrompt}
        on:input={handleUserPromptChange}
      ></textarea>
    </div>
  </div>
  
  <div class="playground-actions">
    <button class="btn btn-primary" on:click={generateSequence} disabled={isLoading || !systemPrompt || !userPrompt}>
      {#if isLoading}
        <LoadingSpinner size="20px" color="white" thickness="2px" />
        Generating...
      {:else}
        Generate Sequence
      {/if}
    </button>
  </div>
</div>

<style>
  .prompt-playground {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .playground-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .playground-header h3 {
    margin: 0;
    font-size: 1.2rem;
    color: #2c3e50;
  }
  
  .template-controls {
    display: flex;
    gap: 0.5rem;
  }
  
  .template-selector {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    margin-bottom: 1rem;
    max-height: 200px;
    overflow-y: auto;
  }
  
  .template-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  
  .template-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    border-bottom: 1px solid #e9ecef;
    transition: background-color 0.2s;
  }
  
  .template-item:last-child {
    border-bottom: none;
  }
  
  .template-item:hover {
    background-color: #e9ecef;
  }
  
  .template-name {
    display: block;
    font-weight: 500;
    margin-bottom: 0.25rem;
  }
  
  .template-description {
    display: block;
    font-size: 0.875rem;
    color: #6c757d;
  }
  
  .prompt-editor {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .prompt-section {
    display: flex;
    flex-direction: column;
  }
  
  label {
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }
  
  .prompt-input {
    width: 100%;
    min-height: 200px;
    padding: 0.75rem;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    font-family: inherit;
    font-size: 0.9rem;
    resize: vertical;
  }
  
  .system-prompt {
    background-color: #f8f9fa;
  }
  
  .playground-actions {
    display: flex;
    justify-content: flex-end;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .btn-primary {
    background-color: #3498db;
    color: white;
    border: none;
  }
  
  .btn-primary:hover:not(:disabled) {
    background-color: #2980b9;
  }
  
  .btn-outline {
    background-color: transparent;
    border: 1px solid #bdc3c7;
    color: #2c3e50;
  }
  
  .btn-outline:hover:not(:disabled) {
    background-color: #f8f9fa;
  }
  
  @media (max-width: 768px) {
    .prompt-editor {
      grid-template-columns: 1fr;
    }
  }
</style>