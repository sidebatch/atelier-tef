import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = await fs.readFile(path.join(root, "index.html"), "utf8");
const match = html.match(/const CARDS = (\[.*?\]);\s*const STORAGE_KEY/s);
if (!match) throw new Error("Could not find embedded card data");

const cards = JSON.parse(match[1]);
if (cards.length !== 500) throw new Error(`Expected 500 cards, found ${cards.length}`);
const force = process.argv.includes("--force");

const outputDir = path.join(root, "audio");
await fs.mkdir(outputDir, { recursive: true });

function cleanSegForSpeech(s) {
  s = String(s || "");
  s = s.replace(/\s+\+\s*\S+/g, "");            // " + inf", " + infinitif", " + qn/qc"
  s = s.replace(/\+[^\s]+/g, "");               // attached: "de+qc" -> "de", "que+ind" -> "que"
  s = s.replace(/\s*\+\s*$/, "").replace(/(^|\s)\+(\s|$)/g, "$1"); // leftover lone "+"
  s = s.replace(/\b(?:qc|qn)\s*\/\s*(?:inf|ind|sub|cond|qc|qn)\b/gi, ""); // "qc/inf"
  s = s.replace(/\s*\/\s*(?:inf|ind|sub|cond|qc|qn)\s*$/i, "");           // trailing "/ ind"
  return s.replace(/\s{2,}/g, " ").trim();
}
const NOTATION_ONLY = new Set(["inf", "ind", "sub", "cond", "qc", "qn", "infinitif", "indicatif", "subjonctif", "conditionnel"]);
const FRAGMENT_ONLY = new Set(["que", "qu'", "de", "à", "au", "aux", "en"]);
function spokenText(text) {
  let t = String(text || "");
  t = t.replace(/\s*\([fm]\.\)/gi, "");                       // (f.) (m.)
  // embedded parens (letters follow): "(re)copier" -> "recopier"
  t = t.replace(/([a-zà-ÿ]*)\(([^)]*)\)([a-zà-ÿ]+)/gi, (m, pre, g, post) => {
    const c = cleanSegForSpeech(g);
    return NOTATION_ONLY.has(c.toLowerCase()) ? pre + post : pre + c + post;
  });
  // spaced parens: "(de)" -> " de", "(que + qc / ind)" -> " que", "(ou maladroit)" -> " ou maladroit"
  t = t.replace(/\(([^)]*)\)/g, (m, g, offset, str) => {
    const c = cleanSegForSpeech(g);
    if (!c) return " ";
    const prev = str[offset - 1] || "";
    const next = str[offset + m.length] || "";
    if (/[a-zà-ÿ]/i.test(prev) && !/[a-zà-ÿ]/i.test(next)) return "";  // suffix parens: "assuré(e)" -> "assuré", "(ve)"/"(le)"/"(euse)"도 기본형만
    return " " + c + " ";
  });
  t = t.replace(/\b(?:qc|qn)\s*\/\s*(?:inf|ind|sub|cond|qc|qn)\b/gi, ""); // "qc/inf" 같은 쌍 표기 통째로 제거
  const segs = t.split("/").map(cleanSegForSpeech).filter(Boolean);
  const parts = segs.filter(x => !NOTATION_ONLY.has(x.toLowerCase()) && !FRAGMENT_ONLY.has(x.toLowerCase()));
  return (parts.length ? parts : segs).join(", ").replace(/\bqn\b/gi, "quelqu'un").replace(/\bqc\b/gi, "quelque chose");
}


async function download(card, attempt = 1) {
  const output = path.join(outputDir, `${card.id}.mp3`);
  try {
    const existing = await fs.stat(output).catch(() => null);
    if (!force && existing?.size > 500) return;

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
