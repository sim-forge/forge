<script>
  import { onMount } from 'svelte';
  import CognitionTable from '../components/table/CognitionTable.svelte';
  import { cognitionStore } from '../stores/cognitionStore';
  import { api } from '../utils/api';
  
  let apiStatus = 'Checking...';
  
  onMount(async () => {
    try {
      const response = await api.healthCheck();
      apiStatus = response.success ? 'Connected' : 'Error';
      
      // Load sequences
      await cognitionStore.loadSequences();
    } catch (error) {
      apiStatus = 'Disconnected';
      console.error('API connection error:', error);
    }
  });
</script>

<div class="home-page">
  <section class="welcome-section">
    <h1>Welcome to SimForge</h1>
    <p>A local-first, production-grade synthetic cognition tool</p>
    <div class="api-status">
      API Status: <span class={apiStatus === 'Connected' ? 'status-ok' : 'status-error'}>{apiStatus}</span>
    </div>
  </section>
  
  <section class="main-section">
    <div class="card">
      <h2>Quick Start</h2>
      <p>Create a new cognition sequence or open an existing one to get started.</p>
      <div class="button-group">
        <button class="primary">New Sequence</button>
        <button>Open Sequence</button>
      </div>
    </div>
    
    <div class="card">
      <h2>Sample Sequence</h2>
      <CognitionTable />
    </div>
  </section>
</div>

<style>
  .home-page {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .welcome-section {
    margin-bottom: 2rem;
  }
  
  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }
  
  .api-status {
    margin-top: 1rem;
    font-size: 0.875rem;
  }
  
  .status-ok {
    color: #2ecc71;
    font-weight: bold;
  }
  
  .status-error {
    color: #e74c3c;
    font-weight: bold;
  }
  
  .main-section {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 1.5rem;
  }
  
  .card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
  }
  
  h2 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #2c3e50;
  }
  
  .button-group {
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
  
  @media (max-width: 768px) {
    .main-section {
      grid-template-columns: 1fr;
    }
  }
</style>