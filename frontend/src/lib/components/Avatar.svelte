<script>
  import { getInitials } from '../utils';
  
  // Props
  export let src = '';
  export let alt = '';
  export let name = '';
  export let size = 'md'; // xs, sm, md, lg, xl
  export let shape = 'circle'; // circle, square, rounded
  export let status = ''; // online, offline, away, busy
  export let statusPosition = 'bottom-right'; // bottom-right, bottom-left, top-right, top-left
  export let border = false;
  export let borderColor = '';
  export let backgroundColor = '';
  export let textColor = '';
  export let icon = null;
  export let fallback = 'initials'; // initials, icon
  
  // Local state
  let imageError = false;
  
  // Computed classes
  $: sizeClass = getSizeClass(size);
  $: shapeClass = getShapeClass(shape);
  $: statusClass = getStatusClass(status);
  $: statusPositionClass = getStatusPositionClass(statusPosition);
  $: borderClass = border ? 'border-2 border-white dark:border-neutral-800' : '';
  $: customBorderStyle = borderColor ? `border: 2px solid ${borderColor};` : '';
  $: customBgStyle = backgroundColor ? `background-color: ${backgroundColor};` : '';
  $: customTextStyle = textColor ? `color: ${textColor};` : '';
  $: customStyle = `${customBorderStyle} ${customBgStyle} ${customTextStyle}`;
  
  // Helper functions
  function getSizeClass(size) {
    const sizes = {
      xs: {
        avatar: 'w-6 h-6 text-xs',
        status: 'w-1.5 h-1.5',
      },
      sm: {
        avatar: 'w-8 h-8 text-sm',
        status: 'w-2 h-2',
      },
      md: {
        avatar: 'w-10 h-10 text-base',
        status: 'w-2.5 h-2.5',
      },
      lg: {
        avatar: 'w-12 h-12 text-lg',
        status: 'w-3 h-3',
      },
      xl: {
        avatar: 'w-16 h-16 text-xl',
        status: 'w-4 h-4',
      },
    };
    
    return sizes[size] || sizes.md;
  }
  
  function getShapeClass(shape) {
    const shapes = {
      circle: 'rounded-full',
      square: 'rounded-none',
      rounded: 'rounded-lg',
    };
    
    return shapes[shape] || shapes.circle;
  }
  
  function getStatusClass(status) {
    const statuses = {
      online: 'bg-success-500',
      offline: 'bg-neutral-400',
      away: 'bg-warning-500',
      busy: 'bg-error-500',
    };
    
    return statuses[status] || '';
  }
  
  function getStatusPositionClass(position) {
    const positions = {
      'bottom-right': 'bottom-0 right-0',
      'bottom-left': 'bottom-0 left-0',
      'top-right': 'top-0 right-0',
      'top-left': 'top-0 left-0',
    };
    
    return positions[position] || positions['bottom-right'];
  }
  
  // Handle image error
  function handleImageError() {
    imageError = true;
  }
  
  // Get initials from name
  $: initials = getInitials(name);
</script>

<div class="avatar-container relative inline-flex">
  {#if src && !imageError}
    <img
      {src}
      {alt}
      class="avatar {sizeClass.avatar} {shapeClass} {borderClass} object-cover"
      style={customStyle}
      on:error={handleImageError}
    />
  {:else if fallback === 'initials' && name}
    <div
      class="avatar {sizeClass.avatar} {shapeClass} {borderClass} flex items-center justify-center bg-primary-100 text-primary-800 dark:bg-primary-800 dark:text-primary-200"
      style={customStyle}
      aria-label={name}
    >
      {initials}
    </div>
  {:else if fallback === 'icon' && icon}
    <div
      class="avatar {sizeClass.avatar} {shapeClass} {borderClass} flex items-center justify-center bg-neutral-100 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-300"
      style={customStyle}
      aria-label={alt || name}
    >
      {icon}
    </div>
  {:else}
    <div
      class="avatar {sizeClass.avatar} {shapeClass} {borderClass} flex items-center justify-center bg-neutral-100 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-300"
      style={customStyle}
      aria-label={alt || name}
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-1/2 w-1/2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    </div>
  {/if}
  
  {#if status}
    <span class="absolute {statusPositionClass} block {sizeClass.status} {statusClass} rounded-full ring-2 ring-white dark:ring-neutral-800"></span>
  {/if}
</div>