<script>
  // Placeholder settings
  const settings = {
    llmProvider: 'OpenAI',
    apiKey: '********',
    model: 'gpt-4',
    temperature: 0.7,
    maxTokens: 2000,
    dataDirectory: '/data',
    theme: 'light'
  };
  
  function saveSettings() {
    alert('Settings saved (placeholder)');
  }
</script>

<div class="settings-page">
  <h1>Settings</h1>
  <p>Configure SimForge to your preferences</p>
  
  <div class="settings-container">
    <div class="settings-section">
      <h2>LLM Configuration</h2>
      
      <div class="form-group">
        <label for="llm-provider">Provider</label>
        <select id="llm-provider" value={settings.llmProvider}>
          <option value="OpenAI">OpenAI</option>
          <option value="Anthropic">Anthropic</option>
          <option value="Local">Local Model</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="api-key">API Key</label>
        <input type="password" id="api-key" value={settings.apiKey} />
      </div>
      
      <div class="form-group">
        <label for="model">Model</label>
        <select id="model" value={settings.model}>
          <option value="gpt-4">GPT-4</option>
          <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
          <option value="claude-3">Claude 3</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="temperature">Temperature</label>
        <input type="range" id="temperature" min="0" max="1" step="0.1" value={settings.temperature} />
        <span>{settings.temperature}</span>
      </div>
      
      <div class="form-group">
        <label for="max-tokens">Max Tokens</label>
        <input type="number" id="max-tokens" value={settings.maxTokens} />
      </div>
    </div>
    
    <div class="settings-section">
      <h2>Application Settings</h2>
      
      <div class="form-group">
        <label for="data-directory">Data Directory</label>
        <input type="text" id="data-directory" value={settings.dataDirectory} />
        <button class="small">Browse</button>
      </div>
      
      <div class="form-group">
        <label for="theme">Theme</label>
        <select id="theme" value={settings.theme}>
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="system">System Default</option>
        </select>
      </div>
    </div>
    
    <div class="settings-actions">
      <button class="primary" on:click={saveSettings}>Save Settings</button>
      <button>Reset to Defaults</button>
    </div>
  </div>
</div>

<style>
  .settings-page {
    max-width: 800px;
    margin: 0 auto;
  }
  
  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }
  
  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #2c3e50;
  }
  
  .settings-container {
    margin-top: 2rem;
  }
  
  .settings-section {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  input, select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  input[type="range"] {
    width: calc(100% - 3rem);
    margin-right: 0.5rem;
  }
  
  .settings-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 1.5rem;
  }
  
  button {
    padding: 0.75rem 1.25rem;
    background-color: #e9ecef;
    color: #2c3e50;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
  }
  
  button.small {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
  
  button.primary {
    background-color: #3498db;
    color: white;
  }
  
  button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  button.primary:hover {
    background-color: #2980b9;
  }
</style>