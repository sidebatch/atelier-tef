import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = await fs.readFile(path.join(root, "index.html"), "utf8");
const match = html.match(/const CARDS = (\[.*?\]);\s*const STORAGE_KEY/s);
if (!match) throw new Error("Could not find embedded card data");

const cards = JSON.parse(match[1]);
if (cards.length !== 500) throw new Error(`Expected 500 cards, found ${cards.length}`);

const outputDir = path.join(root, "audio");
await fs.mkdir(outputDir, { recursive: true });

function spokenText(text) {
  return text.replace(/\s*\([fm]\.\)/gi, "").replace(/\s{2,}/g, " ").trim();
}

async function download(card, attempt = 1) {
  const output = path.join(outputDir, `${card.id}.mp3`);
  try {
    const existing = await fs.stat(output).catch(() => null);
    if (existing?.size > 500) return;

    const query = encodeURIComponent(spokenText(card.fr));
    const url = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=fr&q=${query}`;
    const response = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0" } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("audio")) throw new Error(`Unexpected content type: ${contentType}`);
    const bytes = Buffer.from(await response.arrayBuffer());
    if (bytes.length < 500) throw new Error(`Audio too small: ${bytes.length} bytes`);
    await fs.writeFile(output, bytes);
  } catch (error) {
    if (attempt >= 4) throw new Error(`${card.id}: ${error.message}`);
    await new Promise(resolve => setTimeout(resolve, attempt * 700));
    return download(card, attempt + 1);
  }
}

const concurrency = 6;
let completed = 0;
for (let start = 0; start < cards.length; start += concurrency) {
  await Promise.all(cards.slice(start, start + concurrency).map(download));
  completed = Math.min(start + concurrency, cards.length);
  if (completed % 50 === 0 || completed === cards.length) console.log(`Generated ${completed}/${cards.length}`);
}

console.log(`Audio files ready in ${outputDir}`);
