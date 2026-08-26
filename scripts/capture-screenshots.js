/**
 * Captura las capturas de docs/screenshots/ contra la demo en vivo (o local) usando
 * Playwright. No es parte del build de la app; es una herramienta de mantenimiento del
 * README. Uso: ver scripts/capture_screenshots.md.
 */
const { chromium } = require("playwright");
const path = require("path");

const BASE_URL = process.env.CAPTURE_BASE_URL || "https://rag-groq-portfolio.onrender.com";
const OUT_DIR = path.join(__dirname, "..", "docs", "screenshots");

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

  await page.goto(BASE_URL, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, "01-chat-inicial.png") });

  await page.locator("textarea").fill("¿qué es un closure en JavaScript?");
  await page.locator('button[type="submit"]').click();
  await page.waitForSelector("text=📚", { timeout: 45000 });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(OUT_DIR, "02-chat-respuesta-kb.png"), fullPage: true });

  await page.locator("textarea").fill("¿cuál es la mejor receta de arroz con pollo?");
  await page.locator('button[type="submit"]').click();
  await page.waitForTimeout(4000);
  await page.screenshot({ path: path.join(OUT_DIR, "03-chat-fuera-de-alcance.png"), fullPage: true });

  // Dashboard
  await page.getByRole("tab", { name: /dashboard/i }).click();
  await page.waitForSelector("text=Chunks indexados", { timeout: 15000 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, "04-dashboard.png") });

  // Notebook: subir un documento propio y preguntar solo sobre él
  await page.getByRole("tab", { name: /notebook/i }).click();
  await page.waitForTimeout(300);
  await page.getByPlaceholder(/título de la fuente/i).fill("Receta de pastel");
  await page
    .getByPlaceholder(/pega aquí el contenido/i)
    .fill(
      "Para hacer un pastel de chocolate necesitas 200g de harina, 150g de azucar, 3 huevos y 50g de cacao. Se hornea a 180 grados por 35 minutos."
    );
  await page.getByRole("button", { name: /agregar fuente/i }).click();
  await page.waitForSelector("text=Receta de pastel", { timeout: 15000 });
  await page.getByPlaceholder(/pregunta sobre tu documento/i).fill("¿a qué temperatura se hornea?");
  await page.getByRole("button", { name: /enviar/i }).click();
  await page.waitForSelector("text=180", { timeout: 45000 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, "05-notebook.png"), fullPage: true });

  await browser.close();
  console.log("Capturas guardadas en", OUT_DIR);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
