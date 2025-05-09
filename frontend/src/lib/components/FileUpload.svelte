<script>
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  import { formatBytes } from '../utils';
  import Progress from './Progress.svelte';
  
  // Event dispatcher
  const dispatch = createEventDispatcher();
  
  // Props
  export let id = 'file-upload';
  export let name = 'file';
  export let label = 'Upload file';
  export let accept = '';
  export let multiple = false;
  export let maxSize = 0; // in bytes, 0 means no limit
  export let maxFiles = 0; // 0 means no limit
  export let disabled = false;
  export let required = false;
  export let dropzone = true;
  export let preview = true;
  export let previewSize = 'md'; // sm, md, lg
  export let progress = 0;
  export let showProgress = false;
  export let error = '';
  export let helperText = '';
  export let value = []; // array of files
  
  // Local state
  let fileInput;
  let dropArea;
  let dragCounter = 0;
  let isDragging = false;
  
  // Computed classes
  $: previewSizeClass = getPreviewSizeClass(previewSize);
  $: hasError = error !== '';
  
  // Helper functions
  function getPreviewSizeClass(size) {
    const sizes = {
      sm: 'w-16 h-16',
      md: 'w-24 h-24',
      lg: 'w-32 h-32'
    };
    
    return sizes[size] || sizes.md;
  }
  
  function isImage(file) {
    return file.type.startsWith('image/');
  }
  
  function getFileIcon(file) {
    const extension = file.name.split('.').pop().toLowerCase();
    
    const icons = {
      pdf: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
            </svg>`,
      doc: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
            </svg>`,
      docx: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
            </svg>`,
      xls: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd" />
            </svg>`,
      xlsx: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd" />
            </svg>`,
      csv: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5 4a3 3 0 00-3 3v6a3 3 0 003 3h10a3 3 0 003-3V7a3 3 0 00-3-3H5zm-1 9v-1h5v2H5a1 1 0 01-1-1zm7 1h4a1 1 0 001-1v-1h-5v2zm0-4h5V8h-5v2zM9 8H4v2h5V8z" clip-rule="evenodd" />
            </svg>`,
      zip: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 3h8v1H6V7zm0 2h8v1H6V9zm0 2h4v1H6v-1z" clip-rule="evenodd" />
            </svg>`,
      rar: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 3h8v1H6V7zm0 2h8v1H6V9zm0 2h4v1H6v-1z" clip-rule="evenodd" />
            </svg>`,
      txt: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
            </svg>`,
      json: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
            </svg>`,
      mp3: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
            </svg>`,
      mp4: `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
            </svg>`,
    };
    
    return icons[extension] || `<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                              </svg>`;
  }
  
  // Handle file selection
  function handleFileSelect(event) {
    const files = event.target.files;
    processFiles(files);
  }
  
  // Process selected files
  function processFiles(files) {
    if (!files || files.length === 0) return;
    
    // Check max files limit
    if (maxFiles > 0 && value.length + files.length > maxFiles) {
      error = `You can only upload a maximum of ${maxFiles} files.`;
      return;
    }
    
    // Process each file
    const newFiles = [];
    const errors = [];
    
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      
      // Check file size
      if (maxSize > 0 && file.size > maxSize) {
        errors.push(`File "${file.name}" exceeds the maximum size of ${formatBytes(maxSize)}.`);
        continue;
      }
      
      // Check file type
      if (accept && !isFileTypeAccepted(file, accept)) {
        errors.push(`File "${file.name}" has an invalid file type.`);
        continue;
      }
      
      // Add file to the list
      newFiles.push(file);
    }
    
    // Update error message if any
    if (errors.length > 0) {
      error = errors.join(' ');
    } else {
      error = '';
    }
    
    // Update value
    if (multiple) {
      value = [...value, ...newFiles];
    } else {
      value = newFiles.slice(0, 1);
    }
    
    // Dispatch change event
    dispatch('change', { files: value });
  }
  
  // Check if file type is accepted
  function isFileTypeAccepted(file, accept) {
    if (!accept) return true;
    
    const acceptedTypes = accept.split(',').map(type => type.trim());
    const fileType = file.type;
    const fileExtension = `.${file.name.split('.').pop().toLowerCase()}`;
    
    return acceptedTypes.some(type => {
      // Check for wildcard
      if (type === '*' || type === '*/*') return true;
      
      // Check for MIME type wildcard
      if (type.endsWith('/*') && fileType.startsWith(type.replace('/*', '/'))) return true;
      
      // Check for specific MIME type
      if (type === fileType) return true;
      
      // Check for file extension
      if (type.startsWith('.') && type.toLowerCase() === fileExtension) return true;
      
      return false;
    });
  }
  
  // Remove a file
  function removeFile(index) {
    value = value.filter((_, i) => i !== index);
    dispatch('change', { files: value });
  }
  
  // Clear all files
  function clearFiles() {
    value = [];
    if (fileInput) fileInput.value = '';
    dispatch('change', { files: value });
  }
  
  // Handle drag events
  function handleDragEnter(event) {
    event.preventDefault();
    event.stopPropagation();
    dragCounter++;
    isDragging = true;
  }
  
  function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    dragCounter--;
    if (dragCounter === 0) {
      isDragging = false;
    }
  }
  
  function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
  }
  
  function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    isDragging = false;
    dragCounter = 0;
    
    const files = event.dataTransfer.files;
    processFiles(files);
  }
  
  // Initialize component
  onMount(() => {
    if (dropzone && dropArea) {
      dropArea.addEventListener('dragenter', handleDragEnter);
      dropArea.addEventListener('dragleave', handleDragLeave);
      dropArea.addEventListener('dragover', handleDragOver);
      dropArea.addEventListener('drop', handleDrop);
    }
  });
  
  // Cleanup
  onDestroy(() => {
    if (dropzone && dropArea) {
      dropArea.removeEventListener('dragenter', handleDragEnter);
      dropArea.removeEventListener('dragleave', handleDragLeave);
      dropArea.removeEventListener('dragover', handleDragOver);
      dropArea.removeEventListener('drop', handleDrop);
    }
  });
</script>

<div class="file-upload">
  <label for={id} class="block text-sm font-medium text-text-secondary mb-1">
    {label}
    {#if required}
      <span class="text-error-500">*</span>
    {/if}
  </label>
  
  {#if dropzone}
    <div
      bind:this={dropArea}
      class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md transition-colors duration-200 {isDragging ? 'border-primary-500 bg-primary-50 dark:bg-primary-900' : 'border-border-light'} {hasError ? 'border-error-500' : ''} {disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'}"
      on:click={() => !disabled && fileInput.click()}
    >
      <div class="space-y-1 text-center">
        <svg class="mx-auto h-12 w-12 text-text-tertiary" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
          <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <div class="flex text-sm text-text-tertiary">
          <span>{isDragging ? 'Drop files here' : 'Drag and drop files here, or click to select files'}</span>
          <input
            bind:this={fileInput}
            id={id}
            name={name}
            type="file"
            class="sr-only"
            {accept}
            {multiple}
            {disabled}
            {required}
            on:change={handleFileSelect}
          />
        </div>
        {#if accept}
          <p class="text-xs text-text-tertiary">
            Accepted file types: {accept}
          </p>
        {/if}
        {#if maxSize > 0}
          <p class="text-xs text-text-tertiary">
            Maximum file size: {formatBytes(maxSize)}
          </p>
        {/if}
      </div>
    </div>
  {:else}
    <div class="mt-1">
      <input
        bind:this={fileInput}
        id={id}
        name={name}
        type="file"
        class="block w-full text-sm text-text-primary file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100 focus:outline-none"
        {accept}
        {multiple}
        {disabled}
        {required}
        on:change={handleFileSelect}
      />
    </div>
  {/if}
  
  {#if showProgress && progress > 0}
    <div class="mt-2">
      <Progress value={progress} max={100} height="0.5rem" color="primary" showLabel={true} labelPosition="right" />
    </div>
  {/if}
  
  {#if hasError}
    <p class="mt-2 text-sm text-error-500">{error}</p>
  {:else if helperText}
    <p class="mt-2 text-sm text-text-tertiary">{helperText}</p>
  {/if}
  
  {#if preview && value.length > 0}
    <div class="mt-4">
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-sm font-medium text-text-secondary">Selected files ({value.length})</h3>
        {#if value.length > 0}
          <button
            type="button"
            class="text-sm text-error-600 hover:text-error-800 focus:outline-none focus:underline"
            on:click={clearFiles}
          >
            Clear all
          </button>
        {/if}
      </div>
      
      <ul class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {#each value as file, index}
          <li class="relative group">
            <div class="relative {previewSizeClass} rounded-lg border border-border-light overflow-hidden bg-bg-secondary flex items-center justify-center">
              {#if isImage(file)}
                <img
                  src={URL.createObjectURL(file)}
                  alt={file.name}
                  class="object-cover w-full h-full"
                />
              {:else}
                <div class="flex flex-col items-center justify-center p-2">
                  {@html getFileIcon(file)}
                  <span class="mt-1 text-xs text-text-tertiary truncate max-w-full">
                    {file.name.split('.').pop().toUpperCase()}
                  </span>
                </div>
              {/if}
              
              <button
                type="button"
                class="absolute top-1 right-1 bg-error-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-error-500"
                on:click={() => removeFile(index)}
                aria-label="Remove file"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            
            <div class="mt-1">
              <p class="text-xs text-text-secondary truncate" title={file.name}>
                {file.name}
              </p>
              <p class="text-xs text-text-tertiary">
                {formatBytes(file.size)}
              </p>
            </div>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</div>