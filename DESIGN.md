# SpiderWeb — Sistema de Diseño

Documentación completa del sistema de diseño utilizado en SpiderWeb API Service.
Cubre los dos registros visuales del proyecto: el **Design System base** (`styles.css`) y el **Sistema Táctico** (`tactical.css` / `index.css`), así como el mecanismo de **modo oscuro / claro**.

---

## Índice

1. [Archivos CSS](#archivos-css)
2. [Tipografía](#tipografía)
3. [Paleta de colores — Design System base](#paleta-de-colores--design-system-base)
4. [Paleta de colores — Sistema Táctico](#paleta-de-colores--sistema-táctico)
5. [Espaciado y bordes redondeados](#espaciado-y-bordes-redondeados)
6. [Sombras y efectos glow](#sombras-y-efectos-glow)
7. [Gradientes](#gradientes)
8. [Componentes base (Design System)](#componentes-base-design-system)
9. [Componentes tácticos (Tactical System)](#componentes-tácticos-tactical-system)
10. [Componentes de Landing (index.css)](#componentes-de-landing-indexcss)
11. [Modo oscuro / claro](#modo-oscuro--claro)
12. [Variables RGB auxiliares](#variables-rgb-auxiliares)
13. [Responsive / Breakpoints](#responsive--breakpoints)
14. [Uso en futuros proyectos](#uso-en-futuros-proyectos)

---

## Archivos CSS

| Archivo | Propósito |
|---|---|
| `public/css/styles.css` | Design System base: tokens, layout, navbar, botones, cards, forms, tablas, badges, código, hero, dashboard, explorer, storage, 404, footer, animaciones, modo claro |
| `public/css/tactical.css` | Sistema táctico global: login, register, 404, admin-login y vistas sin landing |
| `public/css/index.css` | Landing page táctica: hero, features, API, network, devex, contacto, footer, modal de términos |
| `public/theme.js` | Script de toggle dark/light; se carga antes del DOM para evitar FOUC |

---

## Tipografía

### Design System base

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

### Sistema Táctico / Landing

```css
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Share+Tech+Mono&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --font-head: 'Barlow Condensed', sans-serif;  /* Títulos impactantes */
  --font-mono: 'Share Tech Mono', monospace;     /* Código, etiquetas */
  --font-body: 'Inter', sans-serif;             /* Cuerpo */

  /* Aliases en tactical.css */
  --sw-font-h: 'Barlow Condensed', sans-serif;
  --sw-font-m: 'Share Tech Mono', monospace;
  --sw-font-b: 'Inter', sans-serif;
}
```

**Reglas de uso:**
- `--font-head` / `--sw-font-h`: Titulares, CTAs. `font-weight: 900`, `text-transform: uppercase`.
- `--font-mono` / `--sw-font-m`: Labels, etiquetas, código, navegación. Siempre `letter-spacing: 0.1em+`.
- `--font-body` / `--sw-font-b`: Párrafos, descripciones.

---

## Paleta de colores — Design System base

```css
:root {
  /* Fondos */
  --bg-primary:    #000000;
  --bg-secondary:  #050505;
  --bg-card:       rgba(18, 18, 30, 0.7);
  --bg-card-hover: rgba(24, 24, 40, 0.85);
  --bg-glass:      rgba(255, 255, 255, 0.03);
  --bg-input:      rgba(255, 255, 255, 0.05);

  /* Texto */
  --text-primary:   #e8e8f0;
  --text-secondary: #8888a0;
  --text-muted:     #555570;

  /* Acentos */
  --accent-cyan:   #00d4ff;
  --accent-violet: #8b5cf6;
  --accent-pink:   #ec4899;
  --accent-green:  #10b981;
  --accent-red:    #ef4444;
  --accent-orange: #f59e0b;

  /* Bordes */
  --border-color: rgba(255, 255, 255, 0.06);
  --border-glow:  rgba(0, 212, 255, 0.15);
}
```

---

## Paleta de colores — Sistema Táctico

```css
:root {
  --red:       #A30000;   /* Rojo principal — acción, peligro, marca */
  --red-dark:  #6B0000;
  --red-glow:  rgba(163, 0, 0, 0.35);
  --black:     #000000;
  --off-white: #F5F5F5;
  --gray-dark: #121212;
  --steel:     #2A2A2A;
  --steel-mid: #1A1A1A;
  --border:    rgba(163, 0, 0, 0.2);

  /* Aliases en tactical.css */
  --sw-red:      #A30000;
  --sw-red-dark: #6B0000;
  --sw-red-glow: rgba(163, 0, 0, 0.3);
  --sw-black:    #000000;
  --sw-white:    #F5F5F5;
  --sw-dark:     #121212;
  --sw-steel:    #2A2A2A;
  --sw-border:   rgba(163, 0, 0, 0.2);
}
```

**Colores de estado (ambos sistemas):**

| Propósito | Valor |
|---|---|
| Éxito / Online | `#22c55e` |
| Error / Peligro | `#ef4444` / `#A30000` |
| Advertencia | `#f59e0b` |
| Info | `#38bdf8` |

---

## Espaciado y bordes redondeados

```css
/* Design System base */
:root {
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
}
```

> **Nota:** El Sistema Táctico usa `clip-path` con esquinas cortadas en vez de `border-radius`:
> ```css
> clip-path: polygon(0 0, calc(100% - Npx) 0, 100% Npx, 100% 100%, Npx 100%, 0 calc(100% - Npx));
> /* N = 5..20 según tamaño del elemento */
> ```

---

## Sombras y efectos glow

```css
/* Design System base */
:root {
  --shadow-sm:   0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md:   0 4px 20px rgba(0, 0, 0, 0.4);
  --shadow-lg:   0 8px 40px rgba(0, 0, 0, 0.5);
  --shadow-glow: 0 0 30px rgba(0, 212, 255, 0.1);
}

/* Sistema Táctico — glow rojo en hover */
box-shadow: 0 0 20px var(--red-glow);     /* botón primario */
box-shadow: 0 0 0 2px var(--sw-red-glow); /* focus en inputs */
```

---

## Gradientes

```css
/* Design System base */
:root {
  --gradient-primary: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet));
  --gradient-danger:  linear-gradient(135deg, var(--accent-red), var(--accent-pink));
  --gradient-success: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
}

/* Fondo animado del body */
body::before {
  content: '';
  position: fixed; inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0, 212, 255, 0.04) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(139, 92, 246, 0.04) 0%, transparent 60%),
    radial-gradient(ellipse at 50% 80%, rgba(236, 72, 153, 0.03) 0%, transparent 60%);
  pointer-events: none; z-index: 0;
}

/* Texto con gradiente */
.gradient-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

## Componentes base (Design System)

### Reset global

```css
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font-sans);
  background: var(--bg-primary);
  color: var(--text-primary);
  min-height: 100vh;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
```

### Layout

```css
.container { max-width: 95%; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }
.page-wrapper { min-height: 100vh; display: flex; flex-direction: column; }
.main-content { flex: 1; padding: 40px 0; }
```

### Navbar

```css
.navbar {
  background: rgba(10, 10, 15, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  padding: 16px 0;
  position: sticky; top: 0; z-index: 100;
}
.navbar-brand span {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.navbar-links a {
  color: var(--text-secondary);
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  font-size: 0.9rem; font-weight: 500;
  transition: all 0.2s ease;
}
.navbar-links a:hover { color: var(--text-primary); background: var(--bg-glass); }
```

### Botones

```css
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px;
  border-radius: var(--radius-sm);
  font-family: var(--font-sans);
  font-size: 0.9rem; font-weight: 600;
  border: none; cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none; line-height: 1.4;
}

.btn-primary {
  background: var(--gradient-primary); color: #fff;
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.25);
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(0, 212, 255, 0.35); }

.btn-secondary {
  background: var(--bg-input); color: var(--text-primary);
  border: 1px solid var(--border-color);
}
.btn-secondary:hover { background: var(--bg-card-hover); border-color: var(--border-glow); }

.btn-danger {
  background: var(--gradient-danger); color: #fff;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
}
.btn-danger:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(239, 68, 68, 0.3); }

.btn-sm { padding: 6px 14px; font-size: 0.8rem; }
.btn-lg { padding: 14px 32px; font-size: 1rem; }
```

### Cards / Tarjetas

```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 28px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}
.card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-glow);
  box-shadow: var(--shadow-glow);
}
.card-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px; padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}
.card-title { font-size: 1.1rem; font-weight: 600; display: flex; align-items: center; gap: 10px; }
```

### Formularios

```css
.form-group { margin-bottom: 20px; }

.form-label {
  display: block; font-size: 0.85rem; font-weight: 500;
  color: var(--text-secondary); margin-bottom: 8px;
  text-transform: uppercase; letter-spacing: 0.5px;
}

.form-input {
  width: 100%; padding: 12px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-family: var(--font-sans); font-size: 0.95rem;
  transition: all 0.3s ease; outline: none;
}

/* Autofill fix */
.form-input:-webkit-autofill,
.form-input:-webkit-autofill:hover,
.form-input:-webkit-autofill:focus,
.form-input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px var(--bg-secondary) inset !important;
  -webkit-text-fill-color: var(--text-primary) !important;
  transition: background-color 5000s ease-in-out 0s;
}

.form-input:focus {
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
}
.form-input::placeholder { color: var(--text-muted); }
.form-inline { display: flex; gap: 10px; align-items: flex-end; }
.form-inline .form-group { flex: 1; margin-bottom: 0; }
```

### Alertas

```css
.alert {
  padding: 14px 20px; border-radius: var(--radius-sm);
  font-size: 0.9rem; margin-bottom: 20px;
  display: flex; align-items: center; gap: 10px;
  animation: slideIn 0.3s ease;
}
.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: var(--accent-green);
}
.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: var(--accent-red);
}
```

### Tablas

```css
.table-wrapper { overflow-x: auto; border-radius: var(--radius-md); }
.table { width: 100%; border-collapse: collapse; }

.table th {
  text-align: left; padding: 12px 16px;
  font-size: 0.8rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-color);
  border-right: 1px solid var(--border-color);
  resize: horizontal; overflow: auto; max-width: 400px;
}
.table th:first-child { border-left: 1px solid var(--border-color); }

.table td {
  padding: 14px 16px; font-size: 0.9rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  border-right: 1px solid var(--border-color);
  vertical-align: middle;
}
.table td:first-child { border-left: 1px solid var(--border-color); }
.table tr:hover td { background: rgba(255, 255, 255, 0.02); }

/* Celda redimensionable */
.table td .td-content {
  overflow: auto; min-width: 60px; max-width: 800px;
  min-height: 24px; max-height: 250px;
  white-space: pre-wrap; word-break: break-word;
}
```

### Badges

```css
.badge {
  display: inline-flex; align-items: center;
  padding: 8px 18px; border-radius: 20px;
  font-size: 0.75rem; font-weight: 600; letter-spacing: 0.3px;
}
.badge-active { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
.badge-inactive { background: rgba(239, 68, 68, 0.15); color: var(--accent-red); }
```

### Bloques de código

```css
.code-block {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 16px; font-family: var(--font-mono);
  font-size: 0.85rem; color: var(--accent-cyan);
  overflow-x: auto; position: relative;
}
.code-block .copy-btn {
  position: absolute; top: 8px; right: 8px;
  background: var(--bg-input); border: 1px solid var(--border-color);
  color: var(--text-secondary); padding: 4px 10px;
  border-radius: var(--radius-sm); font-size: 0.75rem;
  cursor: pointer; transition: all 0.2s ease;
}
```

### Toast / Notificación

```css
.copy-toast {
  position: fixed; bottom: 28px; right: 28px;
  background: #0d0d0d;
  border: 1px solid rgba(163, 0, 0, 0.45);
  border-left: 3px solid #A30000;
  color: #F5F5F5; padding: 0.9rem 1.6rem;
  clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 8px 100%, 0 calc(100% - 8px));
  box-shadow: 0 0 24px rgba(163, 0, 0, 0.18), 0 4px 20px rgba(0, 0, 0, 0.5);
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase;
  z-index: 99999;
  opacity: 0; transform: translateY(16px) translateX(8px);
  transition: opacity 0.25s ease, transform 0.25s ease;
  pointer-events: none;
}
.copy-toast.show { opacity: 1; transform: translateY(0) translateX(0); }
```

### Hero Section

```css
.hero { text-align: center; padding: 100px 0 80px; }
.hero h1 { font-size: 3.5rem; font-weight: 800; line-height: 1.1; letter-spacing: -1px; }
.hero p { font-size: 1.2rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto 40px; line-height: 1.7; }
.hero-actions { display: flex; justify-content: center; gap: 16px; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 16px; background: var(--bg-glass);
  border: 1px solid var(--border-color); border-radius: 30px;
  font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 24px;
}
```

### Footer

```css
.footer {
  border-top: 1px solid var(--border-color);
  padding: 24px 0; text-align: center;
  color: var(--text-muted); font-size: 0.85rem;
}
.footer a { color: var(--text-secondary); text-decoration: none; }
.footer a:hover { color: var(--accent-cyan); }
```

### Página 404

```css
.error-page { text-align: center; padding: 120px 0; }
.error-page h1 {
  font-size: 6rem; font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Modal

```css
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(4px);
  z-index: 1000; display: flex; align-items: center; justify-content: center;
  animation: fadeIn 0.2s ease;
}
.modal-card { width: 100%; max-width: 520px; max-height: 85vh; overflow-y: auto; animation: slideIn 0.3s ease; }
```

### Animaciones

```css
@keyframes slideIn {
  from { opacity: 0; transform: translateY(-10px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.6; }
}

.animate-fade  { animation: fadeIn 0.5s ease; }
.animate-slide { animation: slideIn 0.4s ease; }
```

---

## Componentes tácticos (Tactical System)

> Se activan añadiendo `.tac-page` al `<body>`. Aplica a: login, register, 404, admin-login.

### Navbar táctica

```css
.sw-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  border-bottom: 1px solid transparent;
  transition: background 0.3s, border-color 0.3s;
}
.sw-nav.scrolled {
  background: rgba(var(--bg-primary-rgb, 0,0,0), 0.95);
  border-color: var(--sw-border);
  backdrop-filter: blur(14px);
}
.sw-nav__inner {
  max-width: 1280px; margin: 0 auto;
  padding: 0 clamp(1rem, 4vw, 2.5rem);
  display: flex; align-items: center; justify-content: space-between; height: 64px;
}
.sw-nav__link {
  font-family: var(--sw-font-m);
  font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: rgba(var(--text-primary-rgb, 245,245,245), 0.55);
  padding: 0.4rem 0.7rem; transition: color 0.2s;
}
.sw-nav__link:hover { color: var(--sw-red); }
.sw-nav__sep { width: 1px; height: 18px; background: var(--sw-border); margin: 0 0.4rem; }

/* Hamburger mobile */
.sw-nav__toggle { display: none; flex-direction: column; gap: 5px; }
.sw-nav__toggle span { width: 22px; height: 2px; background: var(--sw-white); }
.sw-nav__toggle.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.sw-nav__toggle.open span:nth-child(2) { opacity: 0; }
.sw-nav__toggle.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
```

### Botones tácticos

```css
.sw-btn {
  display: inline-flex; align-items: center; gap: 0.45rem;
  font-family: var(--sw-font-m);
  font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase;
  border: none; cursor: pointer; padding: 0.65rem 1.6rem;
  clip-path: polygon(0 0, calc(100% - 7px) 0, 100% 7px, 100% 100%, 7px 100%, 0 calc(100% - 7px));
  transition: all 0.2s ease; line-height: 1;
}
.sw-btn--primary { background: var(--sw-red); color: var(--sw-white); }
.sw-btn--primary:hover { background: #c40000; box-shadow: 0 0 18px var(--sw-red-glow); }
.sw-btn--ghost { background: transparent; color: var(--sw-white); border: 1px solid var(--sw-border); }
.sw-btn--ghost:hover { border-color: var(--sw-red); color: var(--sw-red); }
.sw-btn--sm { padding: 0.45rem 1.1rem; font-size: 0.68rem; }
.sw-btn--lg { padding: 0.9rem 2.2rem; font-size: 0.85rem; }
.sw-btn--full { width: 100%; justify-content: center; }
```

### Formulario de autenticación

```css
.sw-auth-wrap { display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 5rem 1rem 2rem; }

.sw-auth-panel {
  width: 100%; max-width: 440px;
  border: 1px solid var(--sw-border);
  background: var(--bg-secondary);
  clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 16px 100%, 0 calc(100% - 16px));
  overflow: hidden;
}

/* Header tipo terminal con dots macOS */
.sw-auth-header {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: rgba(163, 0, 0, 0.06);
  border-bottom: 1px solid var(--sw-border);
}
.sw-auth-dot { width: 9px; height: 9px; border-radius: 50%; }
.sw-auth-dot.r { background: #ff5f57; }
.sw-auth-dot.y { background: #febc2e; }
.sw-auth-dot.g { background: #28c840; }

/* Inputs */
.sw-input {
  width: 100%;
  background: var(--sw-dark);
  border: 1px solid rgba(163, 0, 0, 0.2);
  color: var(--sw-white); font-family: var(--sw-font-m);
  font-size: 0.82rem; padding: 0.65rem 0.9rem; outline: none;
  clip-path: polygon(0 0, calc(100% - 5px) 0, 100% 5px, 100% 100%, 5px 100%, 0 calc(100% - 5px));
  transition: border-color 0.2s, box-shadow 0.2s;
}
.sw-input:-webkit-autofill,
.sw-input:-webkit-autofill:hover,
.sw-input:-webkit-autofill:focus,
.sw-input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px var(--sw-dark) inset !important;
  -webkit-text-fill-color: var(--sw-white) !important;
  transition: background-color 5000s ease-in-out 0s;
}
.sw-input:focus { border-color: var(--sw-red); box-shadow: 0 0 0 2px var(--sw-red-glow); }
.sw-input::placeholder { color: rgba(var(--text-primary-rgb, 245,245,245), 0.18); }

.sw-label {
  font-family: var(--sw-font-m);
  font-size: 0.6rem; letter-spacing: 0.16em;
  color: rgba(163, 0, 0, 0.85); text-transform: uppercase;
}
```

### Alertas tácticas

```css
.sw-alert {
  font-family: var(--sw-font-m); font-size: 0.78rem; letter-spacing: 0.06em;
  padding: 0.75rem 1rem; border: 1px solid rgba(239,68,68,0.3);
  background: rgba(239,68,68,0.07); color: #f87171; margin-bottom: 1.25rem;
  clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 6px 100%, 0 calc(100% - 6px));
}
.sw-alert--success { border-color: rgba(34,197,94,0.3); background: rgba(34,197,94,0.07); color: #4ade80; }
```

### Página 404 táctica

```css
.sw-404-wrap {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  min-height: 100vh; text-align: center; padding: 5rem 1rem 2rem;
}
.sw-404-code {
  font-family: var(--sw-font-h);
  font-size: clamp(8rem, 20vw, 14rem); font-weight: 900; line-height: 0.9;
  color: var(--sw-red); text-shadow: 0 0 80px rgba(163, 0, 0, 0.4); position: relative;
}
.sw-404-code::after {
  content: 'ERROR';
  position: absolute; bottom: -1.2rem; left: 50%; transform: translateX(-50%);
  font-size: 0.9rem; letter-spacing: 0.4em; color: rgba(163, 0, 0, 0.5);
}
```

### Footer táctico

```css
.sw-footer { border-top: 1px solid var(--sw-border); padding: 1.2rem 0; background: var(--bg-primary); }
.sw-footer__inner {
  max-width: 1280px; margin: 0 auto;
  padding: 0 clamp(1rem, 4vw, 2.5rem);
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem;
}
.sw-footer__copy { font-family: var(--sw-font-m); font-size: 0.62rem; letter-spacing: 0.08em; color: rgba(var(--text-primary-rgb, 245,245,245), 0.2); }
.sw-footer__status { display: flex; align-items: center; gap: 0.4rem; font-family: var(--sw-font-m); font-size: 0.62rem; color: #22c55e; }
```

### Efectos especiales

**Scanlines** — overlay de líneas horizontales (efecto CRT):
```css
.sw-scanlines {
  position: fixed; inset: 0; z-index: 9990; pointer-events: none;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(var(--bg-primary-rgb, 0,0,0), 0.04) 2px,
    rgba(var(--bg-primary-rgb, 0,0,0), 0.04) 4px
  );
}
```

**Noise overlay** — textura de ruido fractal:
```css
.noise-overlay {
  position: fixed; inset: 0; z-index: 9997; pointer-events: none;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}
```

**Pulse dot** — indicador de estado online:
```css
.sw-pulse { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #22c55e; animation: swPulse 2s infinite; }
@keyframes swPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.7); }
}
```

**HUD corners** — esquinas decorativas tipo HUD militar:
```css
.hud-corner { position: absolute; width: 40px; height: 40px; pointer-events: none; }
.hud-tl { top: 80px; left: 20px; }
.hud-tr { top: 80px; right: 20px; }
.hud-bl { bottom: 60px; left: 20px; }
.hud-br { bottom: 60px; right: 20px; }
.hud-line { position: absolute; background: var(--red); }
.hud-line.h { width: 100%; height: 1px; top: 0; }
.hud-line.v { width: 1px; height: 100%; left: 0; }
```

---

## Componentes de Landing (index.css)

> Activo en `body.tactical-body`. Estética MGS / Centro de Comando Militar.

### Hero táctica

```css
.hero-tac { position: relative; min-height: 100vh; display: flex; align-items: center; overflow: hidden; background: var(--black); }

/* Tipografía del hero */
.hero-headline { font-family: var(--font-head); font-weight: 900; text-transform: uppercase; line-height: 0.9; letter-spacing: -0.02em; }
.headline-line1, .headline-line2 { font-size: clamp(3.5rem, 8vw, 7rem); }
.headline-line3 { font-size: clamp(3rem, 7vw, 6rem); }

/* Tag eyebrow */
.eyebrow-tag {
  font-family: var(--font-mono); font-size: 0.7rem; letter-spacing: 0.2em; color: var(--red);
  background: rgba(163, 0, 0, 0.08); border: 1px solid var(--border);
  padding: 0.3rem 0.75rem;
  clip-path: polygon(0 0, calc(100% - 5px) 0, 100% 5px, 100% 100%, 5px 100%, 0 calc(100% - 5px));
}

/* Métricas */
.hero-metrics {
  display: flex; align-items: center; gap: 2rem; padding: 1.2rem 1.5rem;
  background: rgba(var(--text-primary-rgb, 255,255,255), 0.03); border: 1px solid var(--border);
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px));
}
.metric-val { font-family: var(--font-mono); font-size: 1.3rem; color: var(--red); font-weight: 700; }
.metric-label { font-family: var(--font-mono); font-size: 0.6rem; letter-spacing: 0.15em; color: rgba(var(--text-primary-rgb, 245,245,245), 0.35); text-transform: uppercase; }
.metric-divider { width: 1px; height: 36px; background: var(--border); }
```

### Features grid

```css
.features-grid-tac {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 1.5px; background: var(--border);
}
.feature-dossier {
  background: var(--bg-secondary); padding: 2rem;
  position: relative; overflow: hidden;
  opacity: 0; transform: translateY(20px);
  transition: opacity 0.5s, transform 0.5s, background 0.3s;
}
.feature-dossier.in-view { opacity: 1; transform: translateY(0); }
.feature-dossier:hover { background: #0e0606; }
/* Borde top rojo en hover */
.feature-dossier::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: transparent; transition: background 0.3s; }
.feature-dossier:hover::before { background: var(--red); }

.dossier-icon {
  width: 44px; height: 44px; background: rgba(163, 0, 0, 0.1); border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center; font-size: 1.2rem; color: var(--red);
  clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 6px 100%, 0 calc(100% - 6px));
}
```

### Terminal (Sección API)

```css
.api-tac__terminal {
  border: 1px solid var(--border); background: var(--bg-secondary);
  clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 16px 100%, 0 calc(100% - 16px));
  overflow: hidden;
}
.terminal-header { display: flex; align-items: center; gap: 0.75rem; padding: 0.7rem 1rem; background: rgba(163, 0, 0, 0.06); border-bottom: 1px solid var(--border); }
.terminal-dots { display: flex; gap: 5px; }
.t-dot { width: 10px; height: 10px; border-radius: 50%; }
.t-dot.red    { background: #ff5f57; }
.t-dot.yellow { background: #febc2e; }
.t-dot.green  { background: #28c840; }
.terminal-code { font-family: var(--font-mono); font-size: 0.82rem; line-height: 1.7; color: var(--off-white); white-space: pre; }

/* Sintaxis */
.t-comment { color: rgba(var(--text-primary-rgb), 0.28); font-style: italic; }
.t-keyword  { color: #c084fc; }
.t-var      { color: #60a5fa; }
.t-string   { color: #86efac; }
.t-number   { color: #fbbf24; }
.t-key      { color: #f87171; }
.t-cursor   { color: var(--red); }
```

### Sección Red (network stats)

```css
.network-stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5px; background: var(--border); }
.net-stat-card { background: var(--bg-secondary); padding: 2rem 1.5rem; opacity: 0; transform: translateY(16px); transition: opacity 0.5s, transform 0.5s; }
.net-stat-card.in-view { opacity: 1; transform: translateY(0); }
.net-stat-val { font-family: var(--font-head); font-size: clamp(1.8rem, 3vw, 2.8rem); font-weight: 900; color: var(--off-white); }
.net-stat-fill { height: 2px; background: var(--red); transition: width 1.5s ease; }
```

### Footer landing

```css
.footer-tac { background: var(--bg-primary); border-top: 2px solid var(--red); padding: 4rem 0 0; }
.footer-tac__grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 3rem; padding-bottom: 3rem; border-bottom: 1px solid var(--border); }
.footer-col-tac h4 { font-family: var(--font-mono); font-size: 0.65rem; letter-spacing: 0.16em; color: var(--red); text-transform: uppercase; margin-bottom: 1.25rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
.footer-col-tac a { color: rgba(var(--text-primary-rgb, 245,245,245), 0.45); text-decoration: none; transition: color 0.2s; }
.footer-col-tac a:hover { color: var(--red); }
```

### Modal de Términos

```css
.terms-modal-overlay {
  display: none; position: fixed; inset: 0; z-index: 9999;
  background: rgba(0, 0, 0, 0.88); align-items: center; justify-content: center;
  backdrop-filter: blur(6px);
}
.terms-modal-box {
  max-width: 700px; width: 100%; max-height: 88vh;
  display: flex; flex-direction: column; background: #0d0d0d;
  border: 1px solid rgba(163, 0, 0, 0.3);
  clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
}
```

---

## Modo oscuro / claro

### Implementación JS (`theme.js`)

Se carga **antes del DOM** en el `<head>` para evitar el FOUC (flash of unstyled content).

```html
<head>
  <!-- Cargar PRIMERO para evitar FOUC -->
  <script src="/theme.js"></script>
</head>
```

```javascript
(function () {
  // 1. Detectar preferencia guardada o del sistema
  const storedTheme = localStorage.getItem("theme");
  const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
  let currentTheme = storedTheme || (prefersLight ? "light" : "dark");

  // 2. Aplicar inmediatamente (antes del paint)
  if (currentTheme === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }

  // 3. Agregar botón toggle al navbar cuando el DOM esté listo
  window.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.createElement("button");
    toggleBtn.id = "theme-toggle-btn";
    toggleBtn.className = "theme-toggle-btn";
    toggleBtn.setAttribute("aria-label", "Cambiar tema");

    const updateIcon = (theme) => {
      toggleBtn.innerHTML =
        theme === "light"
          ? `<i class="fa-solid fa-moon"></i>`
          : `<i class="fa-solid fa-sun"></i>`;
    };
    updateIcon(currentTheme);

    toggleBtn.addEventListener("click", () => {
      const isLight = document.documentElement.getAttribute("data-theme") === "light";
      const newTheme = isLight ? "dark" : "light";
      if (newTheme === "light") {
        document.documentElement.setAttribute("data-theme", "light");
      } else {
        document.documentElement.removeAttribute("data-theme");
      }
      localStorage.setItem("theme", newTheme);
      updateIcon(newTheme);
    });

    // Insertar en el navbar (busca por id o clase)
    const navLinks = document.getElementById("navMenu") || document.querySelector(".sw-nav__links");
    if (navLinks) {
      const li = document.createElement("li");
      li.appendChild(toggleBtn);
      navLinks.appendChild(li);
    } else {
      document.body.appendChild(toggleBtn);
    }
  });
})();
```

**Lógica:**
- Tema por defecto: `dark`.
- Preferencia en `localStorage` tiene prioridad sobre todo.
- Si no hay preferencia, se respeta `prefers-color-scheme`.
- `data-theme="light"` en `<html>` activa todos los overrides de modo claro.
- Modo oscuro = sin atributo `data-theme`.

**Estilo del botón toggle:**
```css
/* Botón flotante (fallback sin navbar) */
.theme-toggle-btn {
  position: fixed; bottom: 24px; left: 24px;
  width: 50px; height: 50px; border-radius: 50%;
  background: var(--bg-card); border: 1px solid var(--border-color);
  color: var(--text-primary); display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem; cursor: pointer; z-index: 9999;
  box-shadow: var(--shadow-md); transition: all 0.3s ease; backdrop-filter: blur(10px);
}
.theme-toggle-btn:hover { transform: translateY(-3px); background: var(--bg-card-hover); border-color: var(--border-glow); box-shadow: var(--shadow-glow); color: var(--accent-cyan); }

/* Versión embebida en .sw-nav__links */
.sw-nav__links .theme-toggle-btn {
  position: relative !important; bottom: auto !important; left: auto !important;
  width: 30px !important; height: 30px !important;
  background: transparent !important; border: none !important; box-shadow: none !important;
  color: var(--text-secondary) !important; font-size: 1.15rem !important;
  margin-left: 10px; backdrop-filter: none !important;
}
.sw-nav__links .theme-toggle-btn:hover { transform: none !important; background: transparent !important; box-shadow: none !important; color: #A30000 !important; }
```

---

### Overrides del Design System base

```css
[data-theme="light"] {
  /* Fondos */
  --bg-primary:    #f8f9fa;
  --bg-secondary:  #ffffff;
  --bg-card:       rgba(255, 255, 255, 0.9);
  --bg-card-hover: #ffffff;
  --bg-glass:      rgba(0, 0, 0, 0.04);
  --bg-input:      rgba(0, 0, 0, 0.05);

  /* Texto */
  --text-primary:   #121212;
  --text-secondary: #121212;
  --text-muted:     #121212;

  /* Acentos más oscuros para contraste sobre fondo blanco */
  --accent-cyan:   #0369a1;
  --accent-violet: #581c87;
  --accent-pink:   #be185d;
  --accent-green:  #166534;
  --accent-red:    #b91c1c;
  --accent-orange: #b45309;

  /* Bordes */
  --border-color: rgba(0, 0, 0, 0.1);
  --border-glow:  rgba(0, 212, 255, 0.2);

  /* Sombras suaves */
  --shadow-sm:   0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-md:   0 4px 20px rgba(0, 0, 0, 0.08);
  --shadow-lg:   0 8px 40px rgba(0, 0, 0, 0.12);
  --shadow-glow: 0 0 20px rgba(0, 212, 255, 0.1);
}

/* Fondo animado más intenso en claro */
[data-theme="light"] body::before {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0, 212, 255, 0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 50% 80%, rgba(236, 72, 153, 0.06) 0%, transparent 60%);
}

/* Logo blanco → invertir en modo claro */
[data-theme="light"] img[src*="logo blanco.png"] { filter: invert(1); }

/* Forzar blanco en botones primarios */
[data-theme="light"] .btn-primary,
[data-theme="light"] .sw-btn--primary,
[data-theme="light"] .tac-btn--primary { color: #ffffff !important; }
```

---

### Overrides del Sistema Táctico

```css
[data-theme="light"] {
  --sw-black: #f8f9fa;
  --sw-white: #121212;
  --sw-dark:  #ffffff;
  --sw-steel: #e0e0e0;
}

[data-theme="light"] body.tac-page { background: var(--sw-black) !important; color: var(--sw-white) !important; }
[data-theme="light"] .sw-nav.scrolled { background: rgba(255, 255, 255, 0.95); }
[data-theme="light"] .sw-auth-panel { background: #ffffff; }
[data-theme="light"] .sw-footer { background: #f8f9fa; }

/* Autofill en modo claro */
[data-theme="light"] .sw-input:-webkit-autofill,
[data-theme="light"] .sw-input:-webkit-autofill:hover,
[data-theme="light"] .sw-input:-webkit-autofill:focus,
[data-theme="light"] .sw-input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px var(--sw-dark) inset !important;
  -webkit-text-fill-color: var(--sw-white) !important;
}

[data-theme="light"] .sw-nav__links { background: rgba(255, 255, 255, 0.97); }
```

---

### Overrides de Landing

```css
[data-theme="light"] {
  --black:      #f8f9fa;
  --off-white:  #121212;
  --gray-dark:  #ffffff;
  --steel:      #e0e0e0;
  --steel-mid:  #e5e5e5;
}

[data-theme="light"] body.tactical-body { background-color: var(--black) !important; }
[data-theme="light"] .tac-nav.scrolled .tac-nav__inner { background: rgba(255, 255, 255, 0.94); }
[data-theme="light"] .features-tac { background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%); }
[data-theme="light"] .feature-dossier { background: #ffffff; }
[data-theme="light"] .feature-dossier:hover { background: #fdfdfd; }
[data-theme="light"] .api-tac { background: #ffffff; }
[data-theme="light"] .api-tac__terminal { background: #f1f3f5; }
[data-theme="light"] .terminal-code { color: #121212; }
[data-theme="light"] .network-tac { background: #f8f9fa; }
[data-theme="light"] .net-stat-card { background: #ffffff; }
[data-theme="light"] .devex-tac { background: #ffffff; }
[data-theme="light"] .devex-code-panel { background: #f1f3f5; }
[data-theme="light"] .devex-feat-icon { color: #ffffff !important; }
[data-theme="light"] .terms-confirm-btn { color: #ffffff; }

/* Copy Toast en modo claro */
[data-theme="light"] .copy-toast {
  background: #f8f9fa; border-color: rgba(163, 0, 0, 0.3); border-left-color: #A30000;
  color: #12121A; box-shadow: 0 0 16px rgba(163, 0, 0, 0.1), 0 4px 16px rgba(0, 0, 0, 0.12);
}
```

---

## Variables RGB auxiliares

Necesarias para `rgba()` con opacidad dinámica según el tema activo:

```css
/* Modo oscuro (default) */
:root {
  --bg-primary-rgb:   0, 0, 0;
  --bg-secondary-rgb: 5, 5, 5;
  --text-primary-rgb: 245, 245, 245;
}

/* Modo claro */
[data-theme="light"] {
  --bg-primary-rgb:   248, 249, 250;
  --bg-secondary-rgb: 255, 255, 255;
  --text-primary-rgb: 18, 18, 26;
}
```

**Uso en cualquier componente:**
```css
background: rgba(var(--bg-primary-rgb), 0.94);
color: rgba(var(--text-primary-rgb), 0.55);
border: 1px solid rgba(var(--text-primary-rgb), 0.06);
```

---

## Responsive / Breakpoints

| Breakpoint | Cambios clave |
|---|---|
| `≤ 1024px` | Grids de 3 cols → 2/1 col, footer 4 cols → 2 cols |
| `≤ 768px` | Nav hamburger, grids 1 col, inputs full width, clip-path desactivado en formularios |
| `≤ 480px` | Network grid 1 col, hero métricas apiladas verticalmente |

```css
/* Tablet */
@media (max-width: 1024px) {
  .features-grid-tac { grid-template-columns: repeat(2, 1fr); }
  .api-tac__grid     { grid-template-columns: 1fr; gap: 2.5rem; }
  .network-stats-grid { grid-template-columns: repeat(2, 1fr); }
  .footer-tac__grid  { grid-template-columns: 1fr 1fr; gap: 2rem; }
}

/* Mobile */
@media (max-width: 768px) {
  .sw-nav__toggle { display: flex; }
  .sw-nav__links {
    position: fixed; top: 64px; right: 0;
    width: min(300px, 100vw); height: calc(100vh - 64px);
    flex-direction: column; transform: translateX(100%);
    transition: transform 0.35s ease; backdrop-filter: blur(16px);
  }
  .sw-nav__links.open { transform: translateX(0); }
  .features-grid-tac { grid-template-columns: 1fr; }
  /* Desactivar clip-path en mobile */
  .api-stat-panel, .api-tac__terminal { clip-path: none; }
  .contact-form-panel { clip-path: none; }
  .sw-auth-panel { clip-path: none; }
}

/* Small mobile */
@media (max-width: 480px) {
  .network-stats-grid { grid-template-columns: 1fr; }
  .hero-metrics { flex-direction: column; gap: 0.75rem; }
  .metric-divider { display: none; }
}
```

---

## Uso en futuros proyectos

### Checklist de adopción

- [ ] Copiar `public/css/styles.css` (Design System base)
- [ ] Copiar `public/css/tactical.css` (si se usa estética táctica)
- [ ] Copiar `public/css/index.css` (si se necesita landing táctica)
- [ ] Copiar `public/theme.js` y cargarlo en `<head>` **antes** de otros scripts
- [ ] Importar Google Fonts:
  - Design System base: Inter + JetBrains Mono
  - Táctica: Barlow Condensed + Share Tech Mono + Inter
- [ ] Importar Font Awesome para íconos del toggle y componentes
- [ ] Añadir clase correcta al `<body>` según contexto (ver tabla abajo)

### Clases de `<body>` según contexto

| Clase en `<body>` | Activa |
|---|---|
| _(sin clase)_ | Design System base (`styles.css`) |
| `tac-page` | Sistema Táctico global (`tactical.css`) |
| `tactical-body` | Landing táctica (`index.css`) |

### Estructura HTML mínima

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Google Fonts (Design System base) -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <!-- Google Fonts (Sistema Táctico / Landing) -->
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Share+Tech+Mono&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

  <!-- Tema: cargar PRIMERO para evitar FOUC -->
  <script src="/theme.js"></script>

  <!-- CSS -->
  <link rel="stylesheet" href="/css/styles.css">
  <!-- Opcional: -->
  <!-- <link rel="stylesheet" href="/css/tactical.css"> -->
  <!-- <link rel="stylesheet" href="/css/index.css"> -->
</head>
<body>
  <!-- Sin clase     → Design System base        -->
  <!-- class="tac-page"       → Sistema Táctico  -->
  <!-- class="tactical-body"  → Landing táctica  -->

  <!-- El navbar debe tener id="navMenu" o class="sw-nav__links"
       para que theme.js inyecte el botón toggle automáticamente -->
  <nav>
    <ul id="navMenu" class="sw-nav__links">
      <li><a href="/" class="sw-nav__link">Inicio</a></li>
      <!-- theme.js agrega aquí el botón sun/moon -->
    </ul>
  </nav>

  <main><!-- contenido --></main>
</body>
</html>
```

> **Tip:** Para nuevas páginas dentro del mismo proyecto, basta con incluir los CSS ya linkados en el layout/template principal. Solo `theme.js` necesita cargarse de forma individual y siempre primero.
