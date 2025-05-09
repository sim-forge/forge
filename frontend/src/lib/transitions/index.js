/**
 * Animation transitions for SimForge
 * Using Framer Motion for smooth, cinematic animations
 */

// Fade transition
export const fadeTransition = {
  in: { opacity: 0 },
  animate: { opacity: 1 },
  out: { opacity: 0 },
  transition: { duration: 0.3, ease: "easeInOut" }
};

// Slide up transition
export const slideUpTransition = {
  in: { y: 20, opacity: 0 },
  animate: { y: 0, opacity: 1 },
  out: { y: -20, opacity: 0 },
  transition: { duration: 0.3, ease: "easeOut" }
};

// Slide in from right transition
export const slideRightTransition = {
  in: { x: 20, opacity: 0 },
  animate: { x: 0, opacity: 1 },
  out: { x: -20, opacity: 0 },
  transition: { duration: 0.3, ease: "easeOut" }
};

// Scale transition
export const scaleTransition = {
  in: { scale: 0.95, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  out: { scale: 0.95, opacity: 0 },
  transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] }
};

// Staggered children transition
export const staggeredTransition = {
  in: { opacity: 0 },
  animate: { opacity: 1 },
  out: { opacity: 0 },
  transition: { duration: 0.2 },
  childrenDelay: 0.05
};

// Table row transition
export const tableRowTransition = {
  in: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  out: { opacity: 0, y: -10 },
  transition: { duration: 0.2, ease: "easeOut" }
};

// Panel slide transition
export const panelSlideTransition = {
  in: { x: "100%" },
  animate: { x: "0%" },
  out: { x: "100%" },
  transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] }
};

// Notification toast transition
export const toastTransition = {
  in: { opacity: 0, y: -20 },
  animate: { opacity: 1, y: 0 },
  out: { opacity: 0, y: -20 },
  transition: { duration: 0.2, ease: "easeOut" }
};

// Modal transition
export const modalTransition = {
  overlay: {
    in: { opacity: 0 },
    animate: { opacity: 1 },
    out: { opacity: 0 },
    transition: { duration: 0.2 }
  },
  content: {
    in: { opacity: 0, scale: 0.95, y: 10 },
    animate: { opacity: 1, scale: 1, y: 0 },
    out: { opacity: 0, scale: 0.95, y: 10 },
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] }
  }
};

// Fork graph node transition
export const nodeTransition = {
  in: { opacity: 0, scale: 0.8 },
  animate: { opacity: 1, scale: 1 },
  out: { opacity: 0, scale: 0.8 },
  transition: { duration: 0.3, ease: "easeOut" }
};

// Fork graph edge transition
export const edgeTransition = {
  in: { opacity: 0, pathLength: 0 },
  animate: { opacity: 1, pathLength: 1 },
  out: { opacity: 0 },
  transition: { duration: 0.5, ease: "easeOut" }
};

// Button hover transition
export const buttonHoverTransition = {
  scale: 1.03,
  transition: { duration: 0.2 }
};

// Button tap transition
export const buttonTapTransition = {
  scale: 0.97,
  transition: { duration: 0.1 }
};

// Page transition
export const pageTransition = {
  initial: { opacity: 0 },
  enter: { opacity: 1 },
  exit: { opacity: 0 },
  transition: { duration: 0.3 }
};