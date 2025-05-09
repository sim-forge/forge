<script>
  export let size = '40px';
  export let color = '#3498db';
  export let thickness = '4px';
</script>

<div class="spinner" style="width: {size}; height: {size}; border-width: {thickness}; border-top-color: {color};"></div>

<style>
  .spinner {
    border-radius: 50%;
    border-style: solid;
    border-color: rgba(0, 0, 0, 0.1);
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>