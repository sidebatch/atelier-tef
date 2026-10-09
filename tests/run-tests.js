#!/usr/bin/env node
/* TEF Atelier 상설 자동 점검.
   실행: node tests/run-tests.js   (tests/에서 npm install 한 번 필요)
   배포 전에 돌려서 전부 PASS일 때만 푸시하는 게 규칙.
   검사 범위: 카드 데이터 정합성 / 페이지 간 데이터 일치 / 버전·링크 /
              전 페이지 무오류 로딩 / 핵심 학습 흐름(단어장·사이클·실전) 클릭 시뮬레이션. */
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.join(__dirname, "..");
const read = f => fs.readFileSync(path.join(ROOT, f), "utf8");

let pass = 0, fail = 0;
const failures = [];
function ok(cond, name, extra = "") {
  if (cond) { pass++; console.log(`  ✓ ${name}`); }
  else { fail++; failures.push(name); console.log(`  ✗ ${name} ${extra}`); }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* ================= 데이터 검사 ================= */
console.log("\n[데이터]");
const idxHtml = read("index.html");
const idxCards = JSON.parse(idxHtml.match(/const CARDS = (\[.*?\]);\s*const STORAGE_KEY/s)[1]);
ok(idxCards.length === 4008, `index 카드 수 = 4008 (실제 ${idxCards.length})`);
ok(new Set(idxCards.map(c => c.id)).size === idxCards.length, "카드 id 중복 없음");
ok(idxCards.every(c => c.fr && c.fr.trim()), "프랑스어 빈 카드 없음");
const KNOWN_KO_GAPS = new Set(["L1-096"]); // 뜻 보강 대상인 알려진 1장. 새 빈 칸이 생기면 여기서 걸린다.
const koGaps = idxCards.filter(c => !c.ko || !c.ko.trim()).map(c => c.id);
ok(koGaps.every(id => KNOWN_KO_GAPS.has(id)), `한국어 뜻 빈 칸은 알려진 것만 (${koGaps.join(",") || "없음"})`);
ok(idxCards.every(c => c.en && c.en.trim()), "영어 뜻 빈 카드 없음");

const cycCards = JSON.parse(read("cycle.html").match(/const CARDS = (\[.*?\]);/s)[1]);
ok(JSON.stringify(cycCards) === JSON.stringify(idxCards), "cycle 데이터 = index 데이터 (완전 일치)");

const quizHtml = read("quiz81.html");
const quizCards = JSON.parse(quizHtml.match(/const CARDS = (\[.*?\]);/s)[1]);
const quizEntries = JSON.parse(quizHtml.match(/const ENTRIES = (\[.*?\]);/s)[1]);
ok(quizEntries.length === 81, `quiz81 항목 수 = 81 (실제 ${quizEntries.length})`);
ok(quizEntries.every((e, i) => e.n === i + 1), "quiz81 항목 번호가 1~81 순서대로");
ok(quizEntries.every(e => idxCards.some(c => c.id === e.pid)), "quiz81 항목의 카드가 전부 index에 실재");
ok(new Set(quizEntries.map(e => e.pid)).size === 80, "quiz81 고유 카드 = 80장 (bénéficier 중복 1쌍)");
ok(quizCards.length === 80 && quizCards.every(c => {
  const src = idxCards.find(x => x.id === c.id);
  return src && src.fr === c.fr && src.ko === c.ko && src.en === c.en;
}), "quiz81 내장 카드가 index와 어긋나지 않음");

const examRaw = JSON.parse(read("exam.html").match(/const RAW_CARDS = (\[.*?\]);/s)[1]);
const byId = Object.fromEntries(idxCards.map(c => [c.id, c]));
ok(examRaw.every(e => byId[e.i] && byId[e.i].fr === e.f && (byId[e.i].ko || "") === e.k),
   "exam 데이터가 index와 어긋나지 않음");
ok(examRaw.length === idxCards.filter(c => c.ko && c.ko.trim()).length,
   `exam 카드 수 = 뜻 있는 카드 수 (${examRaw.length})`);

/* ================= 버전·링크·파일 검사 ================= */
console.log("\n[버전·링크]");
const appVer = idxHtml.match(/const APP_VERSION = "(\d+)"/)[1];
ok(read("version.txt").trim() === appVer, `버전 일치 (APP_VERSION=${appVer}, version.txt=${read("version.txt").trim()})`);

const PAGES = ["index.html", "exam.html", "ce.html", "topics.html", "cognates.html", "cycle.html", "quiz81.html"];
for (const f of PAGES) {
  const hrefs = [...read(f).matchAll(/href="([^"#]+)"/g)].map(m => m[1]);
  const bad = hrefs.filter(h => h.endsWith(".html") || h.includes(".html?"))
                   .map(h => h.split("?")[0])
                   .filter(t => !fs.existsSync(path.join(ROOT, t)));
  ok(bad.length === 0, `${f}의 내부 링크 대상 실재`, bad.join(","));
}
{ // html에 리터럴로 적힌 audio 파일이 실제로 있는지
  const missing = [];
  for (const f of PAGES) {
    for (const m of read(f).matchAll(/audio\/([\w\-]+\.mp3)/g)) {
      if (!fs.existsSync(path.join(ROOT, "audio", m[1]))) missing.push(`${f}:${m[1]}`);
    }
  }
  ok(missing.length === 0, "리터럴 오디오 파일 실재", missing.slice(0, 5).join(","));
}

/* ================= 페이지 로딩·흐름 검사 ================= */
function loadPage(file) {
  const errors = [];
  const { VirtualConsole } = require("jsdom");
  const vc = new VirtualConsole();
  vc.on("jsdomError", e => { if (!/Could not load|Could not parse css|Not implemented/i.test(e.message)) errors.push(e.message); });
  const dom = new JSDOM(read(file), {
    url: "https://localhost/" + file, runScripts: "dangerously", pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(window) {
      window.fetch = () => Promise.reject(new Error("offline in tests"));
      window.Audio = class { constructor() {} play() { return Promise.resolve(); } pause() {} addEventListener() {} };
      window.confirm = () => true;
      window.scrollTo = () => {};
      if (!window.speechSynthesis) {
        window.speechSynthesis = { cancel() {}, speak() {}, getVoices: () => [] };
      }
    },
  });
  dom.window.addEventListener("error", e => errors.push(e.message));
  return { dom, errors };
}

(async () => {
  console.log("\n[페이지 로딩]");
  for (const f of PAGES) {
    const { dom, errors } = loadPage(f);
    await sleep(350);
    ok(errors.length === 0, `${f} 자바스크립트 오류 없이 열림`, errors[0] || "");
    dom.window.close();
  }

  console.log("\n[흐름: 단어장 index]");
  {
    const { dom, errors } = loadPage("index.html");
    const d = dom.window.document;
    await sleep(400);
    const sel = d.getElementById("deckSelect");
    ok(!!sel, "덱 선택 요소 있음");
    sel.value = "b1b2-verb";
    sel.dispatchEvent(new dom.window.Event("change", { bubbles: true }));
    await sleep(150);
    ok((d.getElementById("totalCount")?.textContent || "").includes("402"),
       `동사 덱 총계 402 표시 (실제: ${d.getElementById("totalCount")?.textContent})`);
    const cycBtn = [...d.querySelectorAll('a[href="cycle.html"]')];
    ok(cycBtn.length >= 1, "헤더에 사이클 버튼 있음");
    const quizBtn = [...d.querySelectorAll('a[href="quiz81.html"]')];
    ok(quizBtn.length >= 1, "헤더에 퀴즈81 버튼 있음");
    const before = d.getElementById("doneCount")?.textContent;
    d.getElementById("revealBtn")?.click();
    await sleep(100);
    d.getElementById("rightBtn")?.click();
    await sleep(150);
    const saved = dom.window.localStorage.getItem("tef-5hour-vocab-v1");
    ok(!!saved, "채점 후 진도가 localStorage에 저장됨");
    ok(errors.length === 0, "단어장 흐름 중 오류 없음", errors[0] || "");
    dom.window.close();
  }

  console.log("\n[흐름: 사이클 cycle]");
  {
    const { dom, errors } = loadPage("cycle.html");
    const d = dom.window.document;
    await sleep(300);
    dom.window.localStorage.setItem("tef-5hour-vocab-v1", '{"SENTINEL":1}');
    [...d.querySelectorAll("[data-deck]")].find(c => c.dataset.deck === "b1b2-conn")?.click();
    [...d.querySelectorAll("[data-size]")].find(c => c.dataset.size === "10")?.click();
    d.getElementById("start-input").value = "1";
    d.getElementById("start-btn").click();
    await sleep(50);
    const vis = id => !d.getElementById(id).classList.contains("hidden");
    let steps = 0, n = 0;
    while (!vis("view-done") && steps < 3000) {
      steps++;
      if (vis("view-intro")) { d.getElementById("intro-btn").click(); await sleep(1); continue; }
      if (vis("view-study")) {
        d.getElementById("reveal-btn").click();
        n++;
        d.getElementById(n % 3 === 0 ? "wrong-btn" : "right-btn").click();
        await sleep(1); continue;
      }
      await sleep(3);
    }
    ok(vis("view-done"), `사이클 끝까지 완주 (steps=${steps})`);
    ok(+d.getElementById("done-answered").textContent > 34, "사이클 총 인출 횟수 > 덱 크기 (반복 발생)");
    ok(dom.window.localStorage.getItem("tef-5hour-vocab-v1") === '{"SENTINEL":1}',
       "사이클이 기존 단어장 진도를 건드리지 않음");
    ok(errors.length === 0, "사이클 흐름 중 오류 없음", errors[0] || "");
    dom.window.close();
  }

  console.log("\n[흐름: 퀴즈81 quiz81]");
  {
    const { dom, errors } = loadPage("quiz81.html");
    const d = dom.window.document;
    await sleep(300);
    dom.window.localStorage.setItem("tef-5hour-vocab-v1", '{"SENTINEL":1}');
    dom.window.localStorage.setItem("tef-cycle-v1", '{"SENTINEL":2}');
    [...d.querySelectorAll("[data-size]")].find(c => c.dataset.size === "27")?.click();
    d.getElementById("start-btn").click();
    await sleep(50);
    const vis = id => !d.getElementById(id).classList.contains("hidden");
    let steps = 0, n = 0;
    while (!vis("view-done") && steps < 4000) {
      steps++;
      if (vis("view-intro")) { d.getElementById("intro-btn").click(); await sleep(1); continue; }
      if (vis("view-study")) {
        d.getElementById("reveal-btn").click();
        n++;
        d.getElementById(n % 3 === 0 ? "wrong-btn" : "right-btn").click();
        await sleep(1); continue;
      }
      await sleep(3);
    }
    ok(vis("view-done"), `퀴즈81 끝까지 완주 (steps=${steps})`);
    ok(+d.getElementById("done-answered").textContent > 81, "퀴즈81 총 인출 횟수 > 81 (반복 발생)");
    ok(!!dom.window.localStorage.getItem("tef-quiz81-v1"), "퀴즈81 진도가 별도 키에 저장됨");
    ok(dom.window.localStorage.getItem("tef-5hour-vocab-v1") === '{"SENTINEL":1}',
       "퀴즈81이 기존 단어장 진도를 건드리지 않음");
    ok(dom.window.localStorage.getItem("tef-cycle-v1") === '{"SENTINEL":2}',
       "퀴즈81이 사이클 진도를 건드리지 않음");
    ok(errors.length === 0, "퀴즈81 흐름 중 오류 없음", errors[0] || "");
    dom.window.close();
  }

  console.log("\n[흐름: 실전 exam]");
  {
    const { dom, errors } = loadPage("exam.html");
    const d = dom.window.document;
    await sleep(300);
    d.getElementById("startBtn")?.click();
    await sleep(200);
    const quizVisible = !d.getElementById("quiz")?.classList.contains("hidden") && d.getElementById("quiz")?.style.display !== "none";
    ok(quizVisible || (d.getElementById("qPrompt")?.textContent || "").length > 0, "실전 시작하면 문제 화면이 뜸");
    ok((d.getElementById("qPrompt")?.textContent || "").trim().length > 0, "문제 제시어가 비어 있지 않음");
    const choices = d.getElementById("choices")?.querySelectorAll("button");
    ok(choices && choices.length === 4, `선택지 4개 생성 (실제 ${choices?.length})`);
    if (choices?.length) { choices[0].click(); await sleep(150); }
    ok(errors.length === 0, "실전 흐름 중 오류 없음", errors[0] || "");
    dom.window.close();
  }

  console.log("\n[콘텐츠: topics·cognates]");
  {
    const { dom } = loadPage("topics.html");
    await sleep(250);
    const topicLinks = dom.window.document.querySelectorAll('a[href^="exam.html?topic="]');
    ok(topicLinks.length >= 20, `topics 주제별 실전 링크 ≥20 (실제 ${topicLinks.length})`);
    dom.window.close();
  }
  {
    const { dom } = loadPage("cognates.html");
    await sleep(250);
    const rows = dom.window.document.querySelectorAll("li");
    ok(rows.length > 50, `cognates 항목 >50 (실제 ${rows.length})`);
    dom.window.close();
  }

  console.log(`\n===== 결과: ${pass} PASS / ${fail} FAIL =====`);
  if (failures.length) { console.log("실패 항목:\n - " + failures.join("\n - ")); process.exit(1); }
  process.exit(0);
})();
