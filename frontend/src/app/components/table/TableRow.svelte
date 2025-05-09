<script>
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  
  export let row;
  export let editable = true;
  export let selected = false;
  
  const dispatch = createEventDispatcher();
  
  function handleSelect(event) {
    dispatch('select', {
      rowId: row.id,
      selected: event.target.checked
    });
  }
  
  function handleEdit() {
    dispatch('edit', { rowId: row.id });
  }
  
  function handleFork() {
    dispatch('fork', { rowId: row.id });
  }
  
  // Format confidence as percentage
  function formatConfidence(confidence) {
    return `${(confidence * 100).toFixed(0)}%`;
  }
  
  // Get operation color
  function getOperationColor(operation) {
    switch (operation) {
      case 'Reflect':
        return '#3498db'; // Blue
      case 'Act':
        return '#2ecc71'; // Green
      case 'Plan':
        return '#9b59b6'; // Purple
      case 'Fork':
        return '#e67e22'; // Orange
      default:
        return '#7f8c8d'; // Gray
    }
  }
</script>

<tr data-row-id={row.id} transition:fade={{ duration: 200 }}>
  {#if editable}
    <td class="select-col">
      <input 
        type="checkbox" 
        checked={selected}
        on:change={handleSelect}
      />
    </td>
  {/if}
  
  <td class="goal-cell">
    <div class="goal-content">
      {row.goal}
    </div>
  </td>
  
  <td class="beliefs-cell">
    {#if row.beliefs && row.beliefs.length > 0}
      <ul class="beliefs-list">
        {#each row.beliefs as belief}
          <li class="belief-item">
            <span class="belief-content">{belief.content}</span>
            <span class="belief-confidence" style="opacity: {belief.confidence}">
              {formatConfidence(belief.confidence)}
            </span>
          </li>
        {/each}
      </ul>
    {:else}
      <span class="empty-beliefs">No beliefs</span>
    {/if}
  </td>
  
  <td class="operation-cell">
    <div class="operation-badge" style="background-color: {getOperationColor(row.operation)}">
      {row.operation}
    </div>
  </td>
  
  <td class="output-cell">
    <div class="output-content">
      {row.output}
    </div>
  </td>
  
  {#if editable}
    <td class="actions-col">
      <div class="row-actions">
        <button class="btn-icon" on:click={handleEdit}>
          Edit
        </button>
        <button class="btn-icon" on:click={handleFork}>
          Fork
        </button>
      </div>
    </td>
  {/if}
</tr>

<style>
  tr {
    transition: background-color 0.2s;
  }
  
  tr:hover {
    background-color: #f8f9fa;
  }
  
  td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
    vertical-align: top;
  }
  
  .select-col {
    width: 40px;
    text-align: center;
    vertical-align: middle;
  }
  
  .actions-col {
    width: 100px;
    text-align: center;
    vertical-align: middle;
  }
  
  .goal-cell {
    width: 20%;
    font-weight: 500;
  }
  
  .beliefs-cell {
    width: 30%;
  }
  
  .operation-cell {
    width: 15%;
  }
  
  .output-cell {
    width: 35%;
  }
  
  .beliefs-list {
    margin: 0;
    padding-left: 1.25rem;
    list-style-type: disc;
  }
  
  .belief-item {
    margin-bottom: 0.25rem;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.5rem;
  }
  
  .belief-content {
    flex: 1;
  }
  
  .belief-confidence {
    color: #6c757d;
    font-size: 0.875rem;
    white-space: nowrap;
  }
  
  .empty-beliefs {
    color: #6c757d;
    font-style: italic;
  }
  
  .operation-badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    color: white;
    font-weight: 500;
    font-size: 0.875rem;
  }
  
  .row-actions {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
  }
  
  .btn-icon {
    padding: 0.25rem 0.5rem;
    background-color: transparent;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    color: #2c3e50;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.875rem;
  }
  
  .btn-icon:hover {
    background-color: #f8f9fa;
  }
</style>