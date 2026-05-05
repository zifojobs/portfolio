// Compteur animé pour les éléments [data-counter] avec data-counter-target.
// Animation easeOut de 0 à la valeur cible quand l'élément entre dans le viewport.

const DURATION = 1200;

const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);

export function initCounters(): void {
	if (typeof window === "undefined") return;
	if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

	const elements = document.querySelectorAll<HTMLElement>("[data-counter]");
	if (elements.length === 0) return;

	const observer = new IntersectionObserver(
		(entries) => {
			entries.forEach((entry) => {
				if (!entry.isIntersecting) return;
				const el = entry.target as HTMLElement;
				const target = Number(el.dataset.counterTarget ?? "0");
				const suffix = el.dataset.counterSuffix ?? "";
				const start = performance.now();

				const tick = (now: number) => {
					const t = Math.min(1, (now - start) / DURATION);
					const value = Math.round(target * easeOut(t));
					el.textContent = `${value}${suffix}`;
					if (t < 1) requestAnimationFrame(tick);
				};
				requestAnimationFrame(tick);
				observer.unobserve(el);
			});
		},
		{ threshold: 0.5 }
	);

	elements.forEach((el) => observer.observe(el));
}
