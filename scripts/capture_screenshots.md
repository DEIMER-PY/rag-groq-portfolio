# Regenerar las capturas del README

Las capturas de `docs/screenshots/` se generan con Playwright contra la demo (en vivo o
local), no se editan a mano.

```bash
npm install --no-save playwright
npx playwright install chromium
node scripts/capture-screenshots.js
```

Para capturar contra un entorno local en vez de la demo en producción:

```bash
CAPTURE_BASE_URL=http://localhost:5173 node scripts/capture-screenshots.js
```

El script no es parte del build de `frontend/` ni de `backend/` — es una herramienta de
mantenimiento de documentación, por eso vive en `scripts/` (raíz del repo) y Playwright no es
una dependencia declarada en ningún `package.json`.
