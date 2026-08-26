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

  await browser.close();
  console.log("Capturas guardadas en", OUT_DIR);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
