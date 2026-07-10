// Hero 3D de /freelance-web-kaolack — « Le sel de Kaolack, grain par grain ».
// ~6 000 particules s'assemblent en KAOLACK, réagissent au curseur et au scroll.
// Chargé en différé (dynamic import), desktop uniquement, jamais sur reduced-motion.
// Contrainte : rester décoratif — le contenu SEO du hero vit au-dessus, dans le DOM.

import * as THREE from "three";

const WORD = "KAOLACK";
const MAX_POINTS = 9000;
const TERRACOTTA = "#C2410C";
const TERRACOTTA_BRIGHT = "#E8703F"; // accent lisible sur fond dark warm

function isDarkTheme(): boolean {
	return !document.documentElement.classList.contains("theme-light");
}

function inkHex(): string {
	// Encre du thème actif : crème sur dark warm, noir café sur light.
	return isDarkTheme() ? "#FEF3E2" : "#2A1810";
}

// Sprite circulaire doux pour des grains ronds (PointsMaterial rend des carrés sinon).
function makeGrainTexture(): THREE.Texture {
	const c = document.createElement("canvas");
	c.width = c.height = 64;
	const g = c.getContext("2d")!;
	const grad = g.createRadialGradient(32, 32, 0, 32, 32, 32);
	grad.addColorStop(0, "rgba(255,255,255,1)");
	grad.addColorStop(0.5, "rgba(255,255,255,0.85)");
	grad.addColorStop(1, "rgba(255,255,255,0)");
	g.fillStyle = grad;
	g.fillRect(0, 0, 64, 64);
	const tex = new THREE.CanvasTexture(c);
	tex.colorSpace = THREE.SRGBColorSpace;
	return tex;
}

// Échantillonne le mot dans un canvas offscreen → positions (px, origine centre canvas).
function sampleWord(w: number, h: number): { x: number; y: number }[] {
	const c = document.createElement("canvas");
	c.width = w;
	c.height = h;
	const g = c.getContext("2d", { willReadFrequently: true })!;

	// Le mot occupe le tiers droit du hero, décalé pour ne pas croiser le H1.
	const areaW = w * 0.4;
	const centerX = w * 0.745;
	const centerY = h * 0.5;

	let fontSize = 200;
	g.font = `600 ${fontSize}px Fraunces, Georgia, serif`;
	fontSize = Math.floor((fontSize * areaW) / g.measureText(WORD).width);
	fontSize = Math.min(fontSize, Math.floor(h * 0.34));
	g.font = `600 ${fontSize}px Fraunces, Georgia, serif`;
	g.textAlign = "center";
	g.textBaseline = "middle";
	g.fillStyle = "#fff";
	g.fillText(WORD, centerX, centerY);

	const data = g.getImageData(0, 0, w, h).data;
	// Pas d'échantillonnage adaptatif : viser ~MAX_POINTS quel que soit l'écran.
	const pts: { x: number; y: number }[] = [];
	for (let step = 2; step <= 6; step++) {
		pts.length = 0;
		for (let y = 0; y < h; y += step) {
			for (let x = 0; x < w; x += step) {
				if (data[(y * w + x) * 4 + 3] > 128) {
					// Léger jitter pour casser la grille mécanique → grain organique.
					pts.push({ x: x - w / 2 + Math.random() * 1.6 - 0.8, y: h / 2 - y + Math.random() * 1.6 - 0.8 });
				}
			}
		}
		if (pts.length <= MAX_POINTS) break;
	}
	return pts;
}

export async function initHeroKaolack3D(canvas: HTMLCanvasElement): Promise<void> {
	// Les glyphes Fraunces doivent être prêts avant l'échantillonnage.
	try { await document.fonts.ready; } catch { /* on échantillonne avec le fallback */ }

	const section = canvas.closest("section") ?? canvas.parentElement!;
	let W = section.clientWidth;
	let H = section.clientHeight;
	if (W === 0 || H === 0) return;

	const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false, powerPreference: "low-power" });
	renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
	renderer.setSize(W, H, false);

	const scene = new THREE.Scene();
	// Caméra calée pour que 1 unité monde = 1 px écran sur le plan z=0.
	const FOV = 40;
	const camera = new THREE.PerspectiveCamera(FOV, W / H, 1, 5000);
	const camDist = () => H / (2 * Math.tan((FOV * Math.PI) / 360));
	camera.position.z = camDist();

	const samples = sampleWord(W, H);
	if (samples.length < 100) { renderer.dispose(); return; }
	const n = Math.min(samples.length, MAX_POINTS);

	// Buffers physiques : position courante, vitesse, cible (lettres), départ (dispersion).
	const pos = new Float32Array(n * 3);
	const vel = new Float32Array(n * 3);
	const target = new Float32Array(n * 3);
	const scatter = new Float32Array(n * 3);
	const drift = new Float32Array(n * 3); // direction de dispersion au scroll
	const delay = new Float32Array(n);
	const isAccent = new Uint8Array(n);

	const minX = Math.min(...samples.slice(0, n).map((s) => s.x));
	const spanX = Math.max(...samples.slice(0, n).map((s) => s.x)) - minX || 1;

	for (let i = 0; i < n; i++) {
		const s = samples[i];
		target[i * 3] = s.x;
		target[i * 3 + 1] = s.y;
		target[i * 3 + 2] = (Math.random() - 0.5) * 12;

		// Départ : nuage dispersé sur tout le hero, légèrement en profondeur.
		scatter[i * 3] = (Math.random() - 0.5) * W * 1.2;
		scatter[i * 3 + 1] = (Math.random() - 0.5) * H * 1.3;
		scatter[i * 3 + 2] = (Math.random() - 0.5) * 500;

		pos[i * 3] = scatter[i * 3];
		pos[i * 3 + 1] = scatter[i * 3 + 1];
		pos[i * 3 + 2] = scatter[i * 3 + 2];

		const dir = Math.random() * Math.PI * 2;
		drift[i * 3] = Math.cos(dir) * (60 + Math.random() * 220);
		drift[i * 3 + 1] = 120 + Math.random() * 260; // le sel s'envole vers le haut
		drift[i * 3 + 2] = (Math.random() - 0.5) * 160;

		// Assemblage balayé de gauche à droite + aléa, wow < 3 s.
		delay[i] = ((s.x - minX) / spanX) * 1.1 + Math.random() * 0.35;
		isAccent[i] = Math.random() < 0.1 ? 1 : 0;
	}

	const colors = new Float32Array(n * 3);
	function paintColors() {
		const ink = new THREE.Color(inkHex());
		const accent = new THREE.Color(isDarkTheme() ? TERRACOTTA_BRIGHT : TERRACOTTA);
		for (let i = 0; i < n; i++) {
			const c = isAccent[i] ? accent : ink;
			colors[i * 3] = c.r;
			colors[i * 3 + 1] = c.g;
			colors[i * 3 + 2] = c.b;
		}
		geometry.attributes.color && (geometry.attributes.color.needsUpdate = true);
	}

	const geometry = new THREE.BufferGeometry();
	geometry.setAttribute("position", new THREE.BufferAttribute(pos, 3));
	geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
	paintColors();

	const material = new THREE.PointsMaterial({
		size: 3.5,
		map: makeGrainTexture(),
		vertexColors: true,
		transparent: true,
		opacity: 0.95,
		depthWrite: false,
		sizeAttenuation: true,
	});

	const points = new THREE.Points(geometry, material);
	const group = new THREE.Group();
	group.add(points);
	scene.add(group);

	// Poussière ambiante : quelques grains libres sur tout le hero, très discrets.
	const dustN = 220;
	const dustPos = new Float32Array(dustN * 3);
	for (let i = 0; i < dustN; i++) {
		dustPos[i * 3] = (Math.random() - 0.5) * W * 1.1;
		dustPos[i * 3 + 1] = (Math.random() - 0.5) * H * 1.1;
		dustPos[i * 3 + 2] = (Math.random() - 0.5) * 300;
	}
	const dustGeo = new THREE.BufferGeometry();
	dustGeo.setAttribute("position", new THREE.BufferAttribute(dustPos, 3));
	const dustMat = new THREE.PointsMaterial({
		size: 2.4,
		map: material.map,
		transparent: true,
		opacity: 0.28,
		color: new THREE.Color(inkHex()),
		depthWrite: false,
	});
	scene.add(new THREE.Points(dustGeo, dustMat));

	// --- Interactions ---
	const mouse = { x: 0, y: 0, active: false };
	section.addEventListener("pointermove", (e: PointerEvent) => {
		const r = canvas.getBoundingClientRect();
		mouse.x = e.clientX - r.left - W / 2;
		mouse.y = H / 2 - (e.clientY - r.top);
		mouse.active = true;
	});
	section.addEventListener("pointerleave", () => (mouse.active = false));

	let scrollP = 0;
	function onScroll() {
		scrollP = Math.min(1, Math.max(0, window.scrollY / (H * 0.9)));
	}
	window.addEventListener("scroll", onScroll, { passive: true });

	// Pause quand le hero sort de l'écran ou onglet caché.
	let inView = true;
	new IntersectionObserver((entries) => (inView = entries[0].isIntersecting), { threshold: 0.01 }).observe(canvas);

	let resizeTimer: ReturnType<typeof setTimeout>;
	window.addEventListener("resize", () => {
		clearTimeout(resizeTimer);
		resizeTimer = setTimeout(() => {
			W = section.clientWidth;
			H = section.clientHeight;
			renderer.setSize(W, H, false);
			camera.aspect = W / H;
			camera.position.z = camDist();
			camera.updateProjectionMatrix();
			const fresh = sampleWord(W, H);
			for (let i = 0; i < n; i++) {
				const s = fresh[i % fresh.length];
				target[i * 3] = s.x;
				target[i * 3 + 1] = s.y;
			}
		}, 250);
	});

	// Bascule de thème : repeindre encre + poussière.
	new MutationObserver(() => {
		paintColors();
		dustMat.color.set(inkHex());
	}).observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

	// --- Boucle ---
	const t0 = performance.now();
	const SPRING = 0.055;
	const FRICTION = 0.86;
	const REPULSE_R = 95;
	const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);

	function frame() {
		requestAnimationFrame(frame);
		if (!inView || document.hidden) return;

		const t = (performance.now() - t0) / 1000;
		const posAttr = geometry.attributes.position as THREE.BufferAttribute;

		for (let i = 0; i < n; i++) {
			const i3 = i * 3;
			// Progression d'assemblage propre à chaque grain.
			const p = easeOut(Math.min(1, Math.max(0, (t - delay[i]) / 1.6)));

			// Cible du moment : dispersion → lettre, + houle légère, + envol au scroll.
			let bx = scatter[i3] + (target[i3] - scatter[i3]) * p + drift[i3] * scrollP;
			let by =
				scatter[i3 + 1] +
				(target[i3 + 1] - scatter[i3 + 1]) * p +
				Math.sin(t * 1.3 + target[i3] * 0.02) * 1.5 * p +
				drift[i3 + 1] * scrollP;
			let bz = scatter[i3 + 2] + (target[i3 + 2] - scatter[i3 + 2]) * p + drift[i3 + 2] * scrollP;

			// Ressort vers la cible.
			vel[i3] = (vel[i3] + (bx - pos[i3]) * SPRING) * FRICTION;
			vel[i3 + 1] = (vel[i3 + 1] + (by - pos[i3 + 1]) * SPRING) * FRICTION;
			vel[i3 + 2] = (vel[i3 + 2] + (bz - pos[i3 + 2]) * SPRING) * FRICTION;

			// Répulsion curseur (uniquement une fois assemblé, sinon ça brouille l'arrivée).
			if (mouse.active && p > 0.85) {
				const dx = pos[i3] - mouse.x;
				const dy = pos[i3 + 1] - mouse.y;
				const d2 = dx * dx + dy * dy;
				if (d2 < REPULSE_R * REPULSE_R && d2 > 0.01) {
					const d = Math.sqrt(d2);
					const f = ((REPULSE_R - d) / REPULSE_R) ** 2 * 5.5;
					vel[i3] += (dx / d) * f;
					vel[i3 + 1] += (dy / d) * f;
				}
			}

			pos[i3] += vel[i3];
			pos[i3 + 1] += vel[i3 + 1];
			pos[i3 + 2] += vel[i3 + 2];
		}
		posAttr.needsUpdate = true;

		// Perspective vivante : tilt de base + parallaxe curseur + respiration lente.
		group.rotation.y = -0.07 + (mouse.active ? (mouse.x / W) * 0.06 : 0) + Math.sin(t * 0.18) * 0.015;
		group.rotation.x = (mouse.active ? (-mouse.y / H) * 0.04 : 0) + Math.cos(t * 0.15) * 0.01;

		// Le mot s'efface en montant quand on scrolle.
		material.opacity = 0.95 * (1 - scrollP * 0.9);
		dustMat.opacity = 0.28 * (1 - scrollP);

		renderer.render(scene, camera);
	}
	frame();
}
