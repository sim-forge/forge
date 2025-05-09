<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  import LoadingSpinner from '../common/LoadingSpinner.svelte';
  
  export let sequence = null;
  export let selectedRowId = null;
  
  const dispatch = createEventDispatcher();
  
  let graphContainer;
  let isLoading = true;
  let nodes = [];
  let edges = [];
  let network = null;
  
  $: if (sequence) {
    buildGraphData();
  }
  
  onMount(() => {
    if (typeof window !== 'undefined') {
      import('vis-network/standalone').then(vis => {
        if (sequence) {
          initializeGraph(vis);
        }
      }).catch(err => {
        console.error('Failed to load vis-network:', err);
        isLoading = false;
      });
    }
  });
  
  function buildGraphData() {
    if (!sequence || !sequence.rows) return;
    
    nodes = [];
    edges = [];
    
    // Create nodes for each row
    sequence.rows.forEach(row => {
      const operationColors = {
        'Reflect': '#3498db',
        'Act': '#2ecc71',
        'Plan': '#9b59b6',
        'Fork': '#e67e22'
      };
      
      nodes.push({
        id: row.id,
        label: truncateText(row.goal, 30),
        title: `<strong>${row.goal}</strong><br/>${row.operation}: ${truncateText(row.output, 100)}`,
        color: {
          background: operationColors[row.operation] || '#7f8c8d',
          border: selectedRowId === row.id ? '#e74c3c' : '#2c3e50',
          highlight: {
            background: operationColors[row.operation] || '#7f8c8d',
            border: '#e74c3c'
          }
        },
        borderWidth: selectedRowId === row.id ? 3 : 1,
        font: { color: 'white' }
      });
      
      // Create edges for parent-child relationships
      if (row.parent_id) {
        edges.push({
          from: row.parent_id,
          to: row.id,
          arrows: 'to',
          color: { color: '#95a5a6', highlight: '#7f8c8d' },
          width: 2
        });
      }
    });
    
    // If the graph is already initialized, update it
    if (network) {
      updateGraph();
    }
  }
  
  function initializeGraph(vis) {
    if (!graphContainer) return;
    
    const data = {
      nodes: new vis.DataSet(nodes),
      edges: new vis.DataSet(edges)
    };
    
    const options = {
      layout: {
        hierarchical: {
          direction: 'UD',
          sortMethod: 'directed',
          levelSeparation: 100,
          nodeSpacing: 150
        }
      },
      nodes: {
        shape: 'box',
        margin: 10,
        widthConstraint: {
          maximum: 200
        },
        borderWidth: 1,
        shadow: true
      },
      edges: {
        smooth: {
          type: 'cubicBezier',
          forceDirection: 'vertical'
        }
      },
      physics: {
        hierarchicalRepulsion: {
          nodeDistance: 150
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 300
      }
    };
    
    network = new vis.Network(graphContainer, data, options);
    
    network.on('click', function(params) {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        dispatch('select-node', { nodeId });
      }
    });
    
    isLoading = false;
  }
  
  function updateGraph() {
    if (!network) return;
    
    // Update the graph data
    network.setData({
      nodes: nodes,
      edges: edges
    });
    
    // If a node is selected, focus on it
    if (selectedRowId) {
      network.focus(selectedRowId, {
        scale: 1.0,
        animation: true
      });
    }
  }
  
  function truncateText(text, maxLength) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  }
</script>

<div class="fork-viewer">
  <div class="graph-container" bind:this={graphContainer}>
    {#if isLoading}
      <div class="loading-overlay" transition:fade>
        <LoadingSpinner />
        <p>Loading graph visualization...</p>
      </div>
    {/if}
  </div>
  
  <div class="graph-controls">
    <button class="btn btn-outline" on:click={() => dispatch('reset-view')}>
      Reset View
    </button>
    <button class="btn btn-outline" on:click={() => dispatch('export-graph')}>
      Export Graph
    </button>
  </div>
</div>

<style>
  .fork-viewer {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1rem;
  }
  
  .graph-container {
    flex: 1;
    position: relative;
    border: 1px solid #e9ecef;
    border-radius: 4px;
    background-color: #f8f9fa;
    min-height: 400px;
  }
  
  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.8);
    z-index: 10;
  }
  
  .loading-overlay p {
    margin-top: 1rem;
    color: #2c3e50;
  }
  
  .graph-controls {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 1rem;
  }
  
  .btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
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