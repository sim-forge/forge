/**
 * Click outside directive for Svelte
 * Usage: <div use:clickOutside on:clickOutside={handleClickOutside}>...</div>
 */
export function clickOutside(node) {
  const handleClick = event => {
    if (node && !node.contains(event.target) && !event.defaultPrevented) {
      node.dispatchEvent(
        new CustomEvent('clickOutside', {
          detail: { target: event.target }
        })
      );
    }
  };
  
  document.addEventListener('click', handleClick, true);
  
  return {
    destroy() {
      document.removeEventListener('click', handleClick, true);
    }
  };
}