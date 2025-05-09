<script>
  import { toastStore } from '../services/toastService';
  import Toast from './Toast.svelte';
  
  // Group toasts by position
  $: groupedToasts = groupToastsByPosition($toastStore);
  
  // Helper function to group toasts by position
  function groupToastsByPosition(toasts) {
    const groups = {
      'top-right': [],
      'top-left': [],
      'bottom-right': [],
      'bottom-left': [],
      'top-center': [],
      'bottom-center': []
    };
    
    toasts.forEach(toast => {
      const position = toast.position || 'top-right';
      if (groups[position]) {
        groups[position].push(toast);
      } else {
        groups['top-right'].push(toast);
      }
    });
    
    return groups;
  }
  
  // Handle toast close
  function handleClose(event) {
    const { id } = event.detail;
    toastStore.remove(id);
  }
</script>

<!-- Top Right -->
{#if groupedToasts['top-right'].length > 0}
  <div class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full">
    {#each groupedToasts['top-right'] as toast (toast.id)}
      <Toast
        {...toast}
        position=""
        on:close={handleClose}
      />
    {/each}
  </div>
{/if}

<!-- Top Left -->
{#if groupedToasts['top-left'].length > 0}
  <div class="fixed top-4 left-4 z-50 flex flex-col gap-2 max-w-sm w-full">
    {#each groupedToasts['top-left'] as toast (toast.id)}
      <Toast
        {...toast}
        position=""
        on:close={handleClose}
      />
    {/each}
  </div>
{/if}

<!-- Bottom Right -->
{#if groupedToasts['bottom-right'].length > 0}
  <div class="fixed bottom-4 right-4 z-50 flex flex-col-reverse gap-2 max-w-sm w-full">
    {#each groupedToasts['bottom-right'] as toast (toast.id)}
      <Toast
        {...toast}
        position=""
        on:close={handleClose}
      />
    {/each}
  </div>
{/if}

<!-- Bottom Left -->
{#if groupedToasts['bottom-left'].length > 0}
  <div class="fixed bottom-4 left-4 z-50 flex flex-col-reverse gap-2 max-w-sm w-full">
    {#each groupedToasts['bottom-left'] as toast (toast.id)}
      <Toast
        {...toast}
        position=""
        on:close={handleClose}
      />
    {/each}
  </div>
{/if}

<!-- Top Center -->
{#if groupedToasts['top-center'].length > 0}
  <div class="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 flex flex-col gap-2 max-w-sm w-full">
    {#each groupedToasts['top-center'] as toast (toast.id)}
      <Toast
        {...toast}
        position=""
        on:close={handleClose}
      />
    {/each}
  </div>
{/if}

<!-- Bottom Center -->
{#if groupedToasts['bottom-center'].length > 0}
  <div class="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50 flex flex-col-reverse gap-2 max-w-sm w-full">
    {#each groupedToasts['bottom-center'] as toast (toast.id)}
      <Toast
        {...toast}
        position=""
        on:close={handleClose}
      />
    {/each}
  </div>
{/if}