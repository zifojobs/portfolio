/**
 * Smooth scroll global avec Lenis
 * Donne la sensation de défilement premium (style Framer / Linear / Vercel).
 */
import Lenis from "lenis";

export function initSmoothScroll() {
	const lenis = new Lenis({
		duration: 1.2,
		easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // easeOutExpo
		smoothWheel: true,
		touchMultiplier: 2,
	});

	function raf(time: number) {
		lenis.raf(time);
		requestAnimationFrame(raf);
	}
	requestAnimationFrame(raf);

	// Gérer les ancres (#offres, #etudes-de-cas, etc.) avec smooth scroll
	document.querySelectorAll('a[href^="#"]').forEach((link) => {
		link.addEventListener("click", (e) => {
			const href = (link as HTMLAnchorElement).getAttribute("href");
			if (!href || href === "#") return;
			const target = document.querySelector(href);
			if (target) {
				e.preventDefault();
				lenis.scrollTo(target as HTMLElement, { offset: -80 });
			}
		});
	});

	return lenis;
}
