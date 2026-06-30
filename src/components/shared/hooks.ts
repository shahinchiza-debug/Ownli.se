'use client';

import { useState, useRef, useEffect } from 'react';

/**
 * Shared scroll-reveal hook.
 * Adds the specified animation class and triggers 'visible' on intersection.
 */
export function useReveal(animateClass = 'reveal') {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const known = ['reveal', 'reveal-up-lg', 'reveal-left', 'reveal-right', 'reveal-scale', 'reveal-blur', 'reveal-clip', 'reveal-rotate', 'stagger-children', 'stagger-scale', 'process-stagger', 'stat-glow', 'line-draw', 'section-divider'];
    if (!known.some(c => el.classList.contains(c))) el.classList.add(animateClass);
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { el.classList.add('visible'); observer.unobserve(el); } },
      { threshold: 0.06, rootMargin: '0px 0px -32px 0px' }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  return ref;
}

/**
 * Animated number counter — counts from 0 → target on scroll.
 */
export function useCounter(target: number, duration = 1600) {
  const [count, setCount] = useState(0);
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return;
    started.current = true;
    const start = performance.now();
    const step = (now: number) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCount(Math.round(eased * target * 10) / 10);
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [target, duration]);

  return count;
}
