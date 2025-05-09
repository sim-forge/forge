<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { flip } from 'svelte/animate';
  import LoadingSpinner from '../common/LoadingSpinner.svelte';
  
  export let sequence = null;
  export let selectedRowId = null;
  
  const dispatch = createEventDispatcher();
  
  let messages = [];
  let newMessage = '';
  let isLoading = false;
  let chatContainer;
  
  // Sample system message to show on mount
  const systemMessage = {
    id: 'system-1',
    role: 'system',
    content: 'I am SimForge Assistant, ready to help you analyze and modify your cognition sequence. You can ask me questions about the sequence, request modifications, or get suggestions for improvements.',
    timestamp: new Date()
  };
  
  onMount(() => {
    // Add the system message
    messages = [systemMessage];
    
    // If a sequence is provided, add a welcome message
    if (sequence) {
      addMessage('assistant', `I'm analyzing the sequence "${sequence.title}". It contains ${sequence.rows.length} cognitive steps. How can I help you with this sequence?`);
    }
  });
  
  function addMessage(role, content) {
    const message = {
      id: `msg-${Date.now()}`,
      role,
      content,
      timestamp: new Date()
    };
    
    messages = [...messages, message];
    
    // Scroll to the bottom
    setTimeout(() => {
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    }, 100);
    
    return message;
  }
  
  async function handleSubmit() {
    if (!newMessage.trim()) return;
    
    const userMessage = addMessage('user', newMessage);
    newMessage = '';
    isLoading = true;
    
    try {
      // In a real implementation, this would call the API
      // For now, we'll just simulate a response
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      let responseContent = '';
      
      // Generate a contextual response based on the user message
      if (userMessage.content.toLowerCase().includes('help')) {
        responseContent = 'I can help you analyze your sequence, suggest improvements, or modify it based on your goals. What specific aspect would you like help with?';
      } else if (userMessage.content.toLowerCase().includes('fork')) {
        responseContent = 'To create a fork, select a row in the table and click the "Fork" button. This will create a new branch from that cognitive step, allowing you to explore alternative paths.';
      } else if (userMessage.content.toLowerCase().includes('export')) {
        responseContent = 'You can export your sequence by clicking the "Export" button in the table view. This will download a JSON file containing your sequence data.';
      } else if (userMessage.content.toLowerCase().includes('analyze') || userMessage.content.toLowerCase().includes('review')) {
        responseContent = `I've analyzed your sequence "${sequence?.title}". It contains ${sequence?.rows?.length || 0} cognitive steps. The sequence appears to be ${sequence?.rows?.length > 3 ? 'well-developed' : 'in early stages'}. Would you like me to suggest improvements for specific steps?`;
      } else {
        responseContent = 'I understand your request. To help you better, could you provide more specific details about what you'd like to do with your cognition sequence?';
      }
      
      addMessage('assistant', responseContent);
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage('system', 'Error: Failed to get a response. Please try again.');
    } finally {
      isLoading = false;
    }
  }
  
  function formatTimestamp(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
</script>

<div class="chat-agent">
  <div class="chat-header">
    <h3>SimForge Assistant</h3>
    <div class="chat-actions">
      <button class="btn btn-outline" on:click={() => dispatch('clear-chat')}>
        Clear Chat
      </button>
    </div>
  </div>
  
  <div class="chat-messages" bind:this={chatContainer}>
    {#each messages as message (message.id)}
      <div 
        class="message {message.role}" 
        animate:flip={{ duration: 300 }}
        transition:fly={{ y: 20, duration: 200 }}
      >
        <div class="message-content">
          {message.content}
        </div>
        <div class="message-meta">
          {formatTimestamp(message.timestamp)}
        </div>
      </div>
    {/each}
    
    {#if isLoading}
      <div class="message assistant loading" transition:fade>
        <div class="message-content">
          <LoadingSpinner size="20px" color="#3498db" thickness="2px" />
        </div>
      </div>
    {/if}
  </div>
  
  <form class="chat-input" on:submit|preventDefault={handleSubmit}>
    <input 
      type="text" 
      bind:value={newMessage} 
      placeholder="Ask a question about your sequence..."
      disabled={isLoading}
    />
    <button type="submit" class="send-btn" disabled={isLoading || !newMessage.trim()}>
      Send
    </button>
  </form>
</div>

<style>
  .chat-agent {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
  }
  
  .chat-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #2c3e50;
  }
  
  .chat-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .message {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    position: relative;
  }
  
  .message.user {
    align-self: flex-end;
    background-color: #3498db;
    color: white;
    border-bottom-right-radius: 0;
  }
  
  .message.assistant {
    align-self: flex-start;
    background-color: #f8f9fa;
    color: #2c3e50;
    border-bottom-left-radius: 0;
  }
  
  .message.system {
    align-self: center;
    background-color: #f8f9fa;
    color: #7f8c8d;
    font-style: italic;
    max-width: 90%;
  }
  
  .message.loading {
    padding: 0.5rem;
  }
  
  .message-content {
    word-break: break-word;
  }
  
  .message-meta {
    font-size: 0.75rem;
    opacity: 0.7;
    margin-top: 0.25rem;
    text-align: right;
  }
  
  .chat-input {
    display: flex;
    padding: 1rem;
    border-top: 1px solid #e9ecef;
  }
  
  .chat-input input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #e9ecef;
    border-radius: 4px 0 0 4px;
    font-family: inherit;
    font-size: 0.9rem;
  }
  
  .chat-input input:focus {
    outline: none;
    border-color: #3498db;
  }
  
  .send-btn {
    padding: 0.75rem 1.5rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .send-btn:hover:not(:disabled) {
    background-color: #2980b9;
  }
  
  .send-btn:disabled {
    background-color: #bdc3c7;
    cursor: not-allowed;
  }
  
  .btn {
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-weight: 500;
    font-size: 0.875rem;
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