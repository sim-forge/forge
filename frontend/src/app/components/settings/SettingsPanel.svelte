<script>
  import { createEventDispatcher } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  
  export let settings = {
    llmProvider: 'openai',
    llmModel: 'gpt-4o',
    apiKey: '',
    temperature: 0.7,
    maxTokens: 2000,
    theme: 'light',
    autoSave: true,
    dataStoragePath: './data',
    showLineNumbers: true
  };
  
  export let isOpen = false;
  
  const dispatch = createEventDispatcher();
  
  let activeTab = 'general';
  let isTestingConnection = false;
  let connectionStatus = null;
  
  const llmProviders = [
    { id: 'openai', name: 'OpenAI' },
    { id: 'local', name: 'Local LLM' },
    { id: 'anthropic', name: 'Anthropic' }
  ];
  
  const openaiModels = [
    { id: 'gpt-4o', name: 'GPT-4o' },
    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo' },
    { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo' }
  ];
  
  const localModels = [
    { id: 'llama3', name: 'Llama 3' },
    { id: 'mistral', name: 'Mistral' },
    { id: 'mixtral', name: 'Mixtral' }
  ];
  
  const anthropicModels = [
    { id: 'claude-3-opus', name: 'Claude 3 Opus' },
    { id: 'claude-3-sonnet', name: 'Claude 3 Sonnet' },
    { id: 'claude-3-haiku', name: 'Claude 3 Haiku' }
  ];
  
  $: availableModels = settings.llmProvider === 'openai' 
    ? openaiModels 
    : settings.llmProvider === 'local' 
      ? localModels 
      : anthropicModels;
  
  function setActiveTab(tab) {
    activeTab = tab;
  }
  
  function handleClose() {
    dispatch('close');
  }
  
  function handleSave() {
    dispatch('save', { settings });
    handleClose();
  }
  
  function handleReset() {
    dispatch('reset');
  }
  
  async function testConnection() {
    isTestingConnection = true;
    connectionStatus = null;
    
    try {
      // In a real implementation, this would call the API
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate a successful connection
      connectionStatus = {
        success: true,
        message: `Successfully connected to ${settings.llmProvider} API`
      };
    } catch (error) {
      connectionStatus = {
        success: false,
        message: `Failed to connect: ${error.message}`
      };
    } finally {
      isTestingConnection = false;
    }
  }
</script>

{#if isOpen}
  <div class="settings-overlay" transition:fade={{ duration: 200 }}>
    <div class="settings-panel" transition:fly={{ y: 20, duration: 300 }}>
      <div class="settings-header">
        <h2>Settings</h2>
        <button class="close-btn" on:click={handleClose}>×</button>
      </div>
      
      <div class="settings-content">
        <div class="settings-tabs">
          <button 
            class="tab-btn" 
            class:active={activeTab === 'general'} 
            on:click={() => setActiveTab('general')}
          >
            General
          </button>
          
          <button 
            class="tab-btn" 
            class:active={activeTab === 'llm'} 
            on:click={() => setActiveTab('llm')}
          >
            LLM
          </button>
          
          <button 
            class="tab-btn" 
            class:active={activeTab === 'appearance'} 
            on:click={() => setActiveTab('appearance')}
          >
            Appearance
          </button>
          
          <button 
            class="tab-btn" 
            class:active={activeTab === 'advanced'} 
            on:click={() => setActiveTab('advanced')}
          >
            Advanced
          </button>
        </div>
        
        <div class="settings-tab-content">
          {#if activeTab === 'general'}
            <div class="settings-section">
              <h3>General Settings</h3>
              
              <div class="setting-item">
                <label for="auto-save">
                  <input 
                    type="checkbox" 
                    id="auto-save" 
                    bind:checked={settings.autoSave}
                  />
                  Auto-save sequences
                </label>
                <span class="setting-description">
                  Automatically save sequences when changes are made
                </span>
              </div>
              
              <div class="setting-item">
                <label for="data-path">Data Storage Path</label>
                <input 
                  type="text" 
                  id="data-path" 
                  bind:value={settings.dataStoragePath}
                />
                <span class="setting-description">
                  Path where sequence data will be stored
                </span>
              </div>
            </div>
          {/if}
          
          {#if activeTab === 'llm'}
            <div class="settings-section">
              <h3>LLM Settings</h3>
              
              <div class="setting-item">
                <label for="llm-provider">LLM Provider</label>
                <select id="llm-provider" bind:value={settings.llmProvider}>
                  {#each llmProviders as provider}
                    <option value={provider.id}>{provider.name}</option>
                  {/each}
                </select>
              </div>
              
              <div class="setting-item">
                <label for="llm-model">Model</label>
                <select id="llm-model" bind:value={settings.llmModel}>
                  {#each availableModels as model}
                    <option value={model.id}>{model.name}</option>
                  {/each}
                </select>
              </div>
              
              <div class="setting-item">
                <label for="api-key">API Key</label>
                <input 
                  type="password" 
                  id="api-key" 
                  bind:value={settings.apiKey}
                  placeholder={settings.llmProvider === 'local' ? 'Not required for local LLM' : 'Enter API key'}
                  disabled={settings.llmProvider === 'local'}
                />
              </div>
              
              <div class="setting-item">
                <label for="temperature">Temperature</label>
                <div class="range-input">
                  <input 
                    type="range" 
                    id="temperature" 
                    bind:value={settings.temperature}
                    min="0" 
                    max="1" 
                    step="0.1"
                  />
                  <span>{settings.temperature}</span>
                </div>
                <span class="setting-description">
                  Controls randomness: 0 is deterministic, 1 is creative
                </span>
              </div>
              
              <div class="setting-item">
                <label for="max-tokens">Max Tokens</label>
                <input 
                  type="number" 
                  id="max-tokens" 
                  bind:value={settings.maxTokens}
                  min="100" 
                  max="8000"
                />
                <span class="setting-description">
                  Maximum number of tokens to generate
                </span>
              </div>
              
              <div class="setting-item">
                <button 
                  class="btn btn-primary" 
                  on:click={testConnection}
                  disabled={isTestingConnection || (settings.llmProvider !== 'local' && !settings.apiKey)}
                >
                  {#if isTestingConnection}
                    Testing...
                  {:else}
                    Test Connection
                  {/if}
                </button>
                
                {#if connectionStatus}
                  <div class="connection-status" class:success={connectionStatus.success} transition:fade>
                    {connectionStatus.message}
                  </div>
                {/if}
              </div>
            </div>
          {/if}
          
          {#if activeTab === 'appearance'}
            <div class="settings-section">
              <h3>Appearance</h3>
              
              <div class="setting-item">
                <label for="theme">Theme</label>
                <select id="theme" bind:value={settings.theme}>
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="system">System</option>
                </select>
              </div>
              
              <div class="setting-item">
                <label for="line-numbers">
                  <input 
                    type="checkbox" 
                    id="line-numbers" 
                    bind:checked={settings.showLineNumbers}
                  />
                  Show line numbers in code blocks
                </label>
              </div>
            </div>
          {/if}
          
          {#if activeTab === 'advanced'}
            <div class="settings-section">
              <h3>Advanced Settings</h3>
              
              <div class="setting-item">
                <button class="btn btn-danger" on:click={handleReset}>
                  Reset All Settings
                </button>
                <span class="setting-description">
                  Reset all settings to their default values
                </span>
              </div>
            </div>
          {/if}
        </div>
      </div>
      
      <div class="settings-footer">
        <button class="btn btn-outline" on:click={handleClose}>Cancel</button>
        <button class="btn btn-primary" on:click={handleSave}>Save Changes</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .settings-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .settings-panel {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    width: 90%;
    max-width: 800px;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
  }
  
  .settings-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .settings-header h2 {
    margin: 0;
    font-size: 1.5rem;
    color: #2c3e50;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #7f8c8d;
    cursor: pointer;
    padding: 0;
    line-height: 1;
  }
  
  .close-btn:hover {
    color: #2c3e50;
  }
  
  .settings-content {
    display: flex;
    flex: 1;
    overflow: hidden;
  }
  
  .settings-tabs {
    width: 200px;
    background-color: #f8f9fa;
    padding: 1rem 0;
    border-right: 1px solid #e9ecef;
    display: flex;
    flex-direction: column;
  }
  
  .tab-btn {
    background: none;
    border: none;
    text-align: left;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    transition: background-color 0.2s;
    color: #7f8c8d;
    font-weight: 500;
  }
  
  .tab-btn:hover {
    background-color: #e9ecef;
  }
  
  .tab-btn.active {
    background-color: #e9ecef;
    color: #2c3e50;
    border-left: 3px solid #3498db;
  }
  
  .settings-tab-content {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
  }
  
  .settings-section {
    margin-bottom: 2rem;
  }
  
  .settings-section h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #2c3e50;
    font-size: 1.2rem;
    border-bottom: 1px solid #e9ecef;
    padding-bottom: 0.5rem;
  }
  
  .setting-item {
    margin-bottom: 1.5rem;
  }
  
  .setting-item label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #2c3e50;
  }
  
  .setting-item input[type="text"],
  .setting-item input[type="password"],
  .setting-item input[type="number"],
  .setting-item select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    font-family: inherit;
    font-size: 0.9rem;
  }
  
  .setting-item input[type="checkbox"] {
    margin-right: 0.5rem;
  }
  
  .setting-description {
    display: block;
    font-size: 0.875rem;
    color: #7f8c8d;
    margin-top: 0.25rem;
  }
  
  .range-input {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .range-input input {
    flex: 1;
  }
  
  .connection-status {
    margin-top: 0.5rem;
    padding: 0.5rem;
    border-radius: 4px;
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .connection-status.success {
    background-color: #d4edda;
    color: #155724;
  }
  
  .settings-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid #e9ecef;
  }
  
  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
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
  
  .btn-danger {
    background-color: #e74c3c;
    color: white;
    border: none;
  }
  
  .btn-danger:hover:not(:disabled) {
    background-color: #c0392b;
  }
</style>