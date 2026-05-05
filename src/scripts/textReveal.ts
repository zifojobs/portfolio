// Text reveal par mots sur les éléments [data-text-reveal].
// Utilise GSAP ScrollTrigger (déjà installé). One-shot.

import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function initTextReveal(): void {
	if (typeof window === "undefined") return;
	if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

	const elements = document.querySelectorAll<HTMLElement>("[data-text-reveal]");

	elements.forEach((el) => {
		const text = el.textContent ?? "";
		const words = text.split(/(\s+)/);

		el.innerHTML = words
			.map((w) => (w.trim() === "" ? w : `<span class="reveal-word">${w}</span>`))
			.join("");

		const wordEls = el.querySelectorAll<HTMLElement>(".reveal-word");

		gsap.to(wordEls, {
			opacity: 1,
			y: 0,
			duration: 0.7,
			stagger: 0.05,
			ease: "power3.out",
			scrollTrigger: {
				trigger: el,
				start: "top 85%",
				once: true,
			},
		});
	});
}
