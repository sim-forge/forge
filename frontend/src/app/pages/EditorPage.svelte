<script>
  import { onMount } from 'svelte';
  import AppLayout from '../components/layout/AppLayout.svelte';
  import { cognitionStore } from '../stores/cognitionStore';
  import { toast } from 'svelte-french-toast';
  
  onMount(() => {
    // Initialize with sample data
    cognitionStore.initializeWithSampleData();
    
    // Show welcome toast
    toast.success('Welcome to SimForge!', {
      duration: 3000,
      position: 'top-right'
    });
  });
</script>

<AppLayout />

<style>
  :global(html, body) {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
</style>