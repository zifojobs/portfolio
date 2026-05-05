// Effet magnétique : les éléments avec [data-magnetic] sont attirés vers le curseur
// dans une zone de 80px. Désactivé sous 1024px et si reduced-motion.

const BREAKPOINT = 1024;
const ZONE = 80;
const STRENGTH = 0.25;
const MAX_OFFSET = 8;

export function initMagnetic(): void {
	if (typeof window === "undefined") return;
	if (window.innerWidth < BREAKPOINT) return;
	if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

	const elements = document.querySelectorAll<HTMLElement>("[data-magnetic]");

	elements.forEach((el) => {
		let raf = 0;
		let targetX = 0;
		let targetY = 0;
		let currentX = 0;
		let currentY = 0;

		const tick = () => {
			currentX += (targetX - currentX) * 0.2;
			currentY += (targetY - currentY) * 0.2;
			el.style.transform = `translate(${currentX}px, ${currentY}px)`;
			if (Math.abs(targetX - currentX) < 0.1 && Math.abs(targetY - currentY) < 0.1) {
				raf = 0;
				return;
			}
			raf = requestAnimationFrame(tick);
		};

		const onMove = (e: MouseEvent) => {
			const rect = el.getBoundingClientRect();
			const cx = rect.left + rect.width / 2;
			const cy = rect.top + rect.height / 2;
			const dx = e.clientX - cx;
			const dy = e.clientY - cy;
			const dist = Math.hypot(dx, dy);

			if (dist < rect.width / 2 + ZONE) {
				targetX = Math.max(-MAX_OFFSET, Math.min(MAX_OFFSET, dx * STRENGTH));
				targetY = Math.max(-MAX_OFFSET, Math.min(MAX_OFFSET, dy * STRENGTH));
			} else {
				targetX = 0;
				targetY = 0;
			}
			if (!raf) raf = requestAnimationFrame(tick);
		};

		const onLeave = () => {
			targetX = 0;
			targetY = 0;
			if (!raf) raf = requestAnimationFrame(tick);
		};

		window.addEventListener("mousemove", onMove);
		el.addEventListener("mouseleave", onLeave);
	});
}
