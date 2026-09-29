const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("C:/Users/leeks/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
  });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true,
  });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", error => errors.push(String(error)));
  const url = pathToFileURL(path.resolve(__dirname, "..", "index.html")).href;
  await page.goto(url);
  await page.locator("#pronounceBtn").tap();
  await page.waitForTimeout(1200);

  const audio = await page.evaluate(() => ({
    src: onlineFrenchAudio?.src || "",
    error: onlineFrenchAudio?.error?.code || null,
    readyState: onlineFrenchAudio?.readyState ?? -1,
  }));
  if (!audio.src.endsWith("/audio/L1-001.mp3")) throw new Error(`Unexpected audio source: ${audio.src}`);
  if (audio.error) throw new Error(`Audio element error code: ${audio.error}`);
  if (audio.readyState < 2) throw new Error(`Audio did not load; readyState=${audio.readyState}`);
  await page.locator("#directionBtn").tap();
  if (!(await page.locator("#pronounceBtn").isHidden())) throw new Error("Reverse-mode audio should stay hidden before reveal");
  await page.locator("#revealBtn").tap();
  if (!(await page.locator("#pronounceBtn").isVisible())) throw new Error("Reverse-mode audio did not appear after reveal");
  if (errors.length) throw new Error(errors.join(" | "));

  console.log("PASS: mobile touch loaded bundled audio; reverse-mode audio appears only after reveal");
  await browser.close();
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
