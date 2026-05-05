// Curseur custom : cercle qui suit la souris, grossit au hover des éléments interactifs.
// Désactivé sous 1024px et si prefers-reduced-motion: reduce.

const BREAKPOINT = 1024;
const LERP = 0.18;
const HOVER_SELECTOR = 'a, button, [data-cursor], input[type="submit"]';

export function initCustomCursor(): void {
	if (typeof window === "undefined") return;
	if (window.innerWidth < BREAKPOINT) return;
	if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

	const cursor = document.createElement("div");
	cursor.className = "custom-cursor is-active";
	document.body.appendChild(cursor);
	document.documentElement.classList.add("has-custom-cursor");

	let targetX = window.innerWidth / 2;
	let targetY = window.innerHeight / 2;
	let currentX = targetX;
	let currentY = targetY;
	cursor.style.transform = `translate(${currentX}px, ${currentY}px) translate(-50%, -50%)`;

	const onMove = (e: MouseEvent) => {
		targetX = e.clientX;
		targetY = e.clientY;
	};

	const tick = () => {
		currentX += (targetX - currentX) * LERP;
		currentY += (targetY - currentY) * LERP;
		cursor.style.transform = `translate(${currentX}px, ${currentY}px) translate(-50%, -50%)`;
		requestAnimationFrame(tick);
	};

	const onEnter = () => cursor.classList.add("is-hover");
	const onLeave = () => cursor.classList.remove("is-hover");

	window.addEventListener("mousemove", onMove);

	const bindHovers = () => {
		document.querySelectorAll(HOVER_SELECTOR).forEach((el) => {
			el.removeEventListener("mouseenter", onEnter);
			el.removeEventListener("mouseleave", onLeave);
			el.addEventListener("mouseenter", onEnter);
			el.addEventListener("mouseleave", onLeave);
		});
	};
	bindHovers();

	const mo = new MutationObserver(bindHovers);
	mo.observe(document.body, { childList: true, subtree: true });

	requestAnimationFrame(tick);
}
