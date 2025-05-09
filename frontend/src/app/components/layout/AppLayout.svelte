<script>
  import { onMount } from 'svelte';
  import Ribbon from '../ribbon/Ribbon.svelte';
  import SettingsPanel from '../settings/SettingsPanel.svelte';
  import CognitionTable from '../table/CognitionTable.svelte';
  import ForkViewer from '../graph/ForkViewer.svelte';
  import PromptPlayground from '../prompt/PromptPlayground.svelte';
  import ChatAgent from '../chat/ChatAgent.svelte';
  import ContextPanel from '../context/ContextPanel.svelte';
  import { cognitionStore } from '../../stores/cognitionStore';
  
  let activeTab = 'table';
  let showSettings = false;
  let showContext = true;
  let context = '';
  let selectedRowId = null;
  let isModified = false;
  let sequenceTitle = 'Untitled Sequence';
  
  // Settings
  let settings = {
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
  
  // Prompt templates
  let promptTemplates = [
    {
      id: 'default',
      name: 'Default Template',
      description: 'Standard template for generating cognition sequences',
      system: 'You are SimForge, a synthetic cognition system. Generate a sequence of cognitive steps based on the provided context.',
      user: 'Generate a sequence of cognitive steps for solving the following problem: [PROBLEM DESCRIPTION]'
    },
    {
      id: 'creative',
      name: 'Creative Thinking',
      description: 'Template focused on creative problem-solving',
      system: 'You are SimForge, a synthetic cognition system specialized in creative thinking. Generate a sequence of cognitive steps that emphasize divergent thinking and novel approaches.',
      user: 'Generate a creative sequence of cognitive steps for addressing this challenge: [CHALLENGE DESCRIPTION]'
    }
  ];
  
  let currentTemplate = promptTemplates[0];
  let systemPrompt = currentTemplate.system;
  let userPrompt = currentTemplate.user;
  
  onMount(() => {
    // Load settings from localStorage if available
    const savedSettings = localStorage.getItem('simforge-settings');
    if (savedSettings) {
      settings = JSON.parse(savedSettings);
    }
    
    // Apply theme
    document.documentElement.setAttribute('data-theme', settings.theme);
    
    console.log('SimForge application mounted');
  });
  
  function handleTabChange(event) {
    activeTab = event.detail.tab;
  }
  
  function handleTitleChange(event) {
    sequenceTitle = event.detail.title;
    isModified = true;
  }
  
  function handleSave() {
    // In a real implementation, this would save to a file or database
    console.log('Saving sequence:', sequenceTitle);
    isModified = false;
  }
  
  function handleNew() {
    // In a real implementation, this would create a new sequence
    console.log('Creating new sequence');
    sequenceTitle = 'Untitled Sequence';
    isModified = false;
  }
  
  function handleOpen() {
    // In a real implementation, this would open a file dialog
    console.log('Opening sequence');
  }
  
  function handleSettings() {
    showSettings = true;
  }
  
  function handleSaveSettings(event) {
    settings = event.detail.settings;
    
    // Apply theme
    document.documentElement.setAttribute('data-theme', settings.theme);
    
    // Save settings to localStorage
    localStorage.setItem('simforge-settings', JSON.stringify(settings));
    
    showSettings = false;
  }
  
  function handleResetSettings() {
    settings = {
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
    
    // Apply theme
    document.documentElement.setAttribute('data-theme', settings.theme);
  }
  
  function handleContextUpdate(event) {
    context = event.detail.context;
  }
  
  function handleSelectNode(event) {
    selectedRowId = event.detail.nodeId;
  }
  
  function handleSelectTemplate(event) {
    currentTemplate = event.detail.template;
    systemPrompt = currentTemplate.system;
    userPrompt = currentTemplate.user;
  }
  
  function handleUpdateSystemPrompt(event) {
    systemPrompt = event.detail.systemPrompt;
  }
  
  function handleUpdateUserPrompt(event) {
    userPrompt = event.detail.userPrompt;
  }
  
  function handleSaveTemplate() {
    // In a real implementation, this would save the template
    console.log('Saving template:', { systemPrompt, userPrompt });
  }
  
  function handleGenerate() {
    // In a real implementation, this would call the API
    console.log('Generating sequence with:', { systemPrompt, userPrompt, context });
  }
</script>

<div class="app-container">
  <Ribbon 
    {activeTab}
    {sequenceTitle}
    {isModified}
    on:tab-change={handleTabChange}
    on:title-change={handleTitleChange}
    on:save={handleSave}
    on:new={handleNew}
    on:open={handleOpen}
    on:settings={handleSettings}
  />
  
  <main class="app-content">
    {#if showContext}
      <ContextPanel 
        {context}
        expanded={true}
        on:update={handleContextUpdate}
      />
    {/if}
    
    <div class="tab-content">
      {#if activeTab === 'table'}
        <CognitionTable 
          sequence={$cognitionStore.currentSequence}
          editable={true}
          showControls={true}
        />
      {:else if activeTab === 'graph'}
        <ForkViewer 
          sequence={$cognitionStore.currentSequence}
          {selectedRowId}
          on:select-node={handleSelectNode}
        />
      {:else if activeTab === 'prompt'}
        <PromptPlayground 
          templates={promptTemplates}
          {currentTemplate}
          {systemPrompt}
          {userPrompt}
          on:select-template={handleSelectTemplate}
          on:update-system={handleUpdateSystemPrompt}
          on:update-user={handleUpdateUserPrompt}
          on:save-template={handleSaveTemplate}
          on:generate={handleGenerate}
        />
      {:else if activeTab === 'chat'}
        <ChatAgent 
          sequence={$cognitionStore.currentSequence}
          {selectedRowId}
        />
      {/if}
    </div>
  </main>
  
  <footer class="app-footer">
    <p>SimForge v0.1.0 - A local-first synthetic cognition tool</p>
  </footer>
  
  <SettingsPanel 
    {settings}
    isOpen={showSettings}
    on:close={() => showSettings = false}
    on:save={handleSaveSettings}
    on:reset={handleResetSettings}
  />
</div>

<style>
  .app-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f5f7fa;
  }
  
  .app-content {
    flex: 1;
    padding: 1rem;
    overflow: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .tab-content {
    flex: 1;
    overflow: auto;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .app-footer {
    padding: 1rem 2rem;
    background-color: #2c3e50;
    color: white;
    text-align: center;
    font-size: 0.875rem;
  }
  
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    color: #2c3e50;
  }
  
  :global([data-theme="dark"]) {
    --background: #1a1a1a;
    --text: #f5f5f5;
    --text-muted: #a0a0a0;
    --primary: #3498db;
    --primary-dark: #2980b9;
    --secondary: #7f8c8d;
    --secondary-dark: #6c7a7a;
    --danger: #e74c3c;
    --danger-dark: #c0392b;
    --info: #9b59b6;
    --info-dark: #8e44ad;
    --surface-1: #2c2c2c;
    --surface-2: #3c3c3c;
    --surface-3: #4c4c4c;
    --border-color: #4c4c4c;
  }
  
  :global([data-theme="light"]) {
    --background: #f5f7fa;
    --text: #2c3e50;
    --text-muted: #7f8c8d;
    --primary: #3498db;
    --primary-dark: #2980b9;
    --secondary: #7f8c8d;
    --secondary-dark: #6c7a7a;
    --danger: #e74c3c;
    --danger-dark: #c0392b;
    --info: #9b59b6;
    --info-dark: #8e44ad;
    --surface-1: #ffffff;
    --surface-2: #f8f9fa;
    --surface-3: #e9ecef;
    --border-color: #e9ecef;
  }
</style>