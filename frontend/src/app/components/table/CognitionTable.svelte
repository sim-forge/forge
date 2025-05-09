<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { flip } from 'svelte/animate';
  import { cognitionStore } from '../../stores/cognitionStore';
  import TableRow from './TableRow.svelte';
  import TableHeader from './TableHeader.svelte';
  
  export let sequence = null;
  export let editable = true;
  export let showControls = true;
  
  const dispatch = createEventDispatcher();
  
  let selectedRows = new Set();
  let isLoading = false;
  let tableElement;
  
  // Fallback to sample data if no sequence is provided
  $: activeSequence = sequence || {
    id: "sample",
    title: "Sample Cognition Sequence",
    description: "This is a sample sequence for demonstration purposes",
    rows: [
      {
        id: "row1",
        goal: "Understand the problem",
        beliefs: [
          { content: "The problem is complex", confidence: 0.9 },
          { content: "Multiple approaches exist", confidence: 0.8 }
        ],
        operation: "Reflect",
        output: "Found 3 potential approaches"
      },
      {
        id: "row2",
        goal: "Select an approach",
        beliefs: [
          { content: "Approach A is most efficient", confidence: 0.7 },
          { content: "Approach B is most reliable", confidence: 0.8 }
        ],
        operation: "Act",
        output: "Selected Approach B for reliability"
      }
    ]
  };
  
  $: rows = activeSequence?.rows || [];
  $: hasSelection = selectedRows.size > 0;
  
  onMount(async () => {
    if (!sequence && $cognitionStore.sequences.length > 0) {
      sequence = $cognitionStore.sequences[0];
    }
  });
  
  function handleRowSelect(event) {
    const { rowId, selected } = event.detail;
    
    if (selected) {
      selectedRows.add(rowId);
    } else {
      selectedRows.delete(rowId);
    }
    
    selectedRows = selectedRows; // Trigger reactivity
  }
  
  async function addRow() {
    isLoading = true;
    
    try {
      // In a real implementation, this would call the API
      const newRow = {
        id: crypto.randomUUID(),
        goal: "New goal",
        beliefs: [
          { content: "New belief", confidence: 0.8 }
        ],
        operation: "Reflect",
        output: "New output"
      };
      
      // Add the row to the sequence
      activeSequence.rows = [...activeSequence.rows, newRow];
      
      // Scroll to the new row
      setTimeout(() => {
        const newRowElement = tableElement?.querySelector(`[data-row-id="${newRow.id}"]`);
        if (newRowElement) {
          newRowElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    } catch (error) {
      console.error('Error adding row:', error);
    } finally {
      isLoading = false;
    }
  }
  
  async function deleteSelectedRows() {
    if (selectedRows.size === 0) return;
    
    isLoading = true;
    
    try {
      // Filter out the selected rows
      activeSequence.rows = activeSequence.rows.filter(row => !selectedRows.has(row.id));
      
      // Clear the selection
      selectedRows.clear();
    } catch (error) {
      console.error('Error deleting rows:', error);
    } finally {
      isLoading = false;
    }
  }
  
  async function regenerateSelectedRows() {
    if (selectedRows.size === 0) return;
    
    isLoading = true;
    
    try {
      // In a real implementation, this would call the API
      // For now, we'll just update the rows with mock data
      activeSequence.rows = activeSequence.rows.map(row => {
        if (selectedRows.has(row.id)) {
          return {
            ...row,
            goal: `Regenerated goal for ${row.id}`,
            beliefs: [
              { content: "Regenerated belief", confidence: 0.9 }
            ],
            operation: "Act",
            output: "Regenerated output"
          };
        }
        return row;
      });
    } catch (error) {
      console.error('Error regenerating rows:', error);
    } finally {
      isLoading = false;
    }
  }
  
  async function forkSelectedRows() {
    if (selectedRows.size === 0) return;
    
    isLoading = true;
    
    try {
      // Get the first selected row (for now, we only fork one row at a time)
      const rowToFork = activeSequence.rows.find(row => selectedRows.has(row.id));
      
      if (!rowToFork) {
        throw new Error('Selected row not found');
      }
      
      // In a real implementation, this would call the API
      const forkedRow = {
        id: crypto.randomUUID(),
        goal: `Forked from ${rowToFork.goal}`,
        beliefs: [
          { content: "Forked belief", confidence: 0.7 }
        ],
        operation: "Fork",
        output: "Forked output",
        parent_id: rowToFork.id
      };
      
      // Add the forked row to the sequence
      activeSequence.rows = [...activeSequence.rows, forkedRow];
      
      // Scroll to the forked row
      setTimeout(() => {
        const forkedRowElement = tableElement?.querySelector(`[data-row-id="${forkedRow.id}"]`);
        if (forkedRowElement) {
          forkedRowElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    } catch (error) {
      console.error('Error forking row:', error);
    } finally {
      isLoading = false;
    }
  }
  
  function exportSequence() {
    try {
      // Create a JSON string of the sequence
      const sequenceJson = JSON.stringify(activeSequence, null, 2);
      
      // Create a blob and download link
      const blob = new Blob([sequenceJson], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      // Create a download link and click it
      const a = document.createElement('a');
      a.href = url;
      a.download = `${activeSequence.title || 'sequence'}_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      
      // Clean up
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting sequence:', error);
    }
  }
</script>

<div class="cognition-table-container" bind:this={tableElement}>
  {#if isLoading}
    <div class="loading-overlay" transition:fade>
      <div class="spinner"></div>
    </div>
  {/if}
  
  <h2>{activeSequence.title}</h2>
  
  {#if showControls}
    <div class="table-controls">
      <div class="left-controls">
        <button class="btn btn-primary" on:click={addRow}>
          Add Row
        </button>
        
        <button class="btn btn-danger" on:click={deleteSelectedRows} disabled={!hasSelection}>
          Delete
        </button>
        
        <button class="btn btn-secondary" on:click={regenerateSelectedRows} disabled={!hasSelection}>
          Regenerate
        </button>
        
        <button class="btn btn-info" on:click={forkSelectedRows} disabled={!hasSelection}>
          Fork
        </button>
      </div>
      
      <div class="right-controls">
        <button class="btn btn-outline" on:click={exportSequence}>
          Export
        </button>
      </div>
    </div>
  {/if}
  
  <div class="table-wrapper">
    <table class="cognition-table">
      <thead>
        <tr>
          {#if editable}
            <th class="select-col"></th>
          {/if}
          <th>Goal</th>
          <th>Beliefs</th>
          <th>Operation</th>
          <th>Output</th>
          {#if editable}
            <th class="actions-col"></th>
          {/if}
        </tr>
      </thead>
      
      <tbody>
        {#if rows.length === 0}
          <tr transition:fade>
            <td colspan={editable ? 6 : 4} class="empty-state">
              <div class="empty-message">
                <p>No rows yet. Add a row to get started.</p>
              </div>
            </td>
          </tr>
        {:else}
          {#each rows as row (row.id)}
            <tr animate:flip={{ duration: 300 }} data-row-id={row.id}>
              {#if editable}
                <td class="select-col">
                  <input 
                    type="checkbox" 
                    checked={selectedRows.has(row.id)}
                    on:change={(e) => handleRowSelect({ detail: { rowId: row.id, selected: e.target.checked } })}
                  />
                </td>
              {/if}
              <td>{row.goal}</td>
              <td>
                <ul>
                  {#each row.beliefs as belief}
                    <li>
                      {belief.content} 
                      <span class="confidence">({(belief.confidence * 100).toFixed(0)}%)</span>
                    </li>
                  {/each}
                </ul>
              </td>
              <td>{row.operation}</td>
              <td>{row.output}</td>
              {#if editable}
                <td class="actions-col">
                  <button class="btn-icon" on:click={() => dispatch('edit', { rowId: row.id })}>
                    Edit
                  </button>
                </td>
              {/if}
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>

<style>
  .cognition-table-container {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  h2 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #2c3e50;
  }
  
  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 255, 255, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
    border-radius: 8px;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top-color: #3498db;
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .table-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .left-controls, .right-controls {
    display: flex;
    gap: 0.5rem;
  }
  
  .table-wrapper {
    flex: 1;
    overflow: auto;
  }
  
  .cognition-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
  }
  
  th {
    background-color: #f8f9fa;
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 1;
  }
  
  .select-col, .actions-col {
    width: 50px;
    text-align: center;
  }
  
  ul {
    margin: 0;
    padding-left: 1.25rem;
  }
  
  .confidence {
    color: #6c757d;
    font-size: 0.875rem;
  }
  
  .empty-state {
    padding: 3rem;
    text-align: center;
    color: #6c757d;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s ease;
  }
  
  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .btn-primary {
    background-color: #3498db;
    color: white;
  }
  
  .btn-primary:hover:not(:disabled) {
    background-color: #2980b9;
  }
  
  .btn-danger {
    background-color: #e74c3c;
    color: white;
  }
  
  .btn-danger:hover:not(:disabled) {
    background-color: #c0392b;
  }
  
  .btn-secondary {
    background-color: #7f8c8d;
    color: white;
  }
  
  .btn-secondary:hover:not(:disabled) {
    background-color: #6c7a7a;
  }
  
  .btn-info {
    background-color: #9b59b6;
    color: white;
  }
  
  .btn-info:hover:not(:disabled) {
    background-color: #8e44ad;
  }
  
  .btn-outline {
    background-color: transparent;
    border: 1px solid #bdc3c7;
    color: #2c3e50;
  }
  
  .btn-outline:hover:not(:disabled) {
    background-color: #f8f9fa;
  }
  
  .btn-icon {
    padding: 0.25rem 0.5rem;
    background-color: transparent;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    color: #2c3e50;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .btn-icon:hover {
    background-color: #f8f9fa;
  }
</style>