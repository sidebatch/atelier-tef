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
  const cleaned = await page.evaluate(() => [
    cleanFrenchForSpeech("oser + inf"),
    cleanFrenchForSpeech("avoir de la peine à +inf"),
    cleanFrenchForSpeech("afin de+inf / que+sub"),
    cleanFrenchForSpeech("faute de qc/inf"),
    cleanFrenchForSpeech("l'écologie (f.)"),
  ]);
  const expectedCleaned = ["oser", "avoir de la peine à", "afin de / que", "faute de", "l'écologie"];
  if (JSON.stringify(cleaned) !== JSON.stringify(expectedCleaned)) throw new Error(`Speech cleanup mismatch: ${JSON.stringify(cleaned)}`);
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
  await page.locator("#revealBtn").tap();
  await page.locator("#wrongBtn").tap();
  if ((await page.locator("#wrongCount").innerText()).trim() !== "1") throw new Error("First wrong answer was not counted once");
  for (let i = 0; i < 10; i += 1) {
    await page.locator("#revealBtn").tap();
    await page.locator("#rightBtn").tap();
  }
  if ((await page.locator("#correctCount").innerText()).trim() !== "0") throw new Error("Single O attempts were counted as completed cards");
  if (!(await page.locator(".prompt").innerText()).includes("avoir besoin de")) throw new Error("Wrong card did not return after ten cards");
  await page.locator("#revealBtn").tap();
  await page.locator("#wrongBtn").tap();
  if ((await page.locator("#wrongCount").innerText()).trim() !== "1") throw new Error("Repeated wrong answer was counted twice");
  await page.locator("#directionBtn").tap();
  if (!(await page.locator("#pronounceBtn").isHidden())) throw new Error("Reverse-mode audio should stay hidden before reveal");
  await page.locator("#revealBtn").tap();
  if (!(await page.locator("#pronounceBtn").isVisible())) throw new Error("Reverse-mode audio did not appear after reveal");
  await page.evaluate(() => {
    const id = getQueue()[0];
    progressOf(id).streak = 2;
    revealed = false;
    render();
  });
  await page.locator("#revealBtn").tap();
  await page.locator("#rightBtn").tap();
  if ((await page.locator("#correctCount").innerText()).trim() !== "1") throw new Error("Third consecutive O did not count one completed card");
  if (errors.length) throw new Error(errors.join(" | "));

  console.log("PASS: mobile audio omits grammar labels; X counts unique wrong cards; O counts only mastered cards");
  await browser.close();
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
