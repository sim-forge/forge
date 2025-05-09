<script>
  export let showSelect = true;
  export let showActions = true;
</script>

<thead>
  <tr>
    {#if showSelect}
      <th class="select-col"></th>
    {/if}
    <th>Goal</th>
    <th>Beliefs</th>
    <th>Operation</th>
    <th>Output</th>
    {#if showActions}
      <th class="actions-col">Actions</th>
    {/if}
  </tr>
</thead>

<style>
  th {
    padding: 0.75rem;
    text-align: left;
    background-color: #f8f9fa;
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 1;
    border-bottom: 2px solid #e9ecef;
  }
  
  .select-col, .actions-col {
    width: 80px;
    text-align: center;
  }
</style>