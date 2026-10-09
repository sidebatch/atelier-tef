#!/usr/bin/env python3
"""quiz81.html 생성기: Quiz 'Les verbes (1-1500)' PDF 81개 항목만 따로 공부하는 페이지.
index.html의 CARDS에서 해당 카드만 읽어 내장한다. 기존 앱 파일은 수정하지 않는다.
방식 2가지: ✍️ 타이핑(뜻 보고 프랑스어 직접 쓰기, 자동 채점 — 기본) / 🃏 카드(뜻 보고 O·X).
진도는 별도 키 tef-quiz81-v1 에 저장한다 (기존 단어장·사이클 진도와 무접촉).
bénéficier는 PDF에서 (à)/(de) 두 항목이라 항목은 81개, 카드는 80장이다."""
import re, json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
index = (root / "index.html").read_text(encoding="utf-8")
m = re.search(r"const CARDS = (\[.*?\]);\s*const STORAGE_KEY", index, re.S)
if not m:
    raise SystemExit("CARDS not found in index.html")
all_cards = {c["id"]: c for c in json.loads(m.group(1))}

# PDF 순서: (번호, 카드 id, PDF 표기, PDF 영어 답)
ENTRIES = [
 [
  1,
  "L3-051",
  "supplémentaire",
  "additional"
 ],
 [
  2,
  "L3-099",
  "vulnérable",
  "vulnerable"
 ],
 [
  3,
  "L6-1048",
  "fermier",
  "farmer"
 ],
 [
  4,
  "L6-1060",
  "stagiaire",
  "intern"
 ],
 [
  5,
  "E7-046",
  "au milieu de",
  "in the middle of"
 ],
 [
  6,
  "L6-492",
  "au contraire",
  "on the contrary"
 ],
 [
  7,
  "L6-498",
  "d'ailleurs",
  "besides / moreover"
 ],
 [
  8,
  "L6-507",
  "du fait de",
  "due to"
 ],
 [
  9,
  "E7-019",
  "à la suite de",
  "following"
 ],
 [
  10,
  "L6-525",
  "à travers",
  "through"
 ],
 [
  11,
  "L6-530",
  "à part",
  "apart"
 ],
 [
  12,
  "E7-281",
  "tandis que",
  "while"
 ],
 [
  13,
  "L6-549",
  "en matière de",
  "regarding / in terms of"
 ],
 [
  14,
  "L6-571",
  "au fond",
  "basically / fundamentally"
 ],
 [
  15,
  "L6-1107",
  "maladroite (ou maladroit)",
  "clumsy (feminine)"
 ],
 [
  16,
  "L6-1197",
  "piller",
  "loot"
 ],
 [
  17,
  "L6-1263",
  "œuvre",
  "work (artistic or intellectual)"
 ],
 [
  18,
  "L6-1307",
  "litigieux",
  "contentious"
 ],
 [
  19,
  "L6-1308",
  "arbitrer",
  "arbitrate"
 ],
 [
  20,
  "L6-1332",
  "le taux de chômage",
  "unemployment rate"
 ],
 [
  21,
  "L6-1344",
  "décalage",
  "gap / discrepancy"
 ],
 [
  22,
  "L6-003",
  "accomplir",
  "accomplish"
 ],
 [
  23,
  "L6-008",
  "affliger / s'affliger",
  "afflict / be afflicted"
 ],
 [
  24,
  "L6-014",
  "appuyer",
  "support"
 ],
 [
  25,
  "L6-015",
  "atteindre",
  "reach"
 ],
 [
  26,
  "L6-023",
  "appartenir (à)",
  "belong (to)"
 ],
 [
  27,
  "L6-024",
  "s'apercevoir (de)",
  "notice / realize"
 ],
 [
  28,
  "L6-037",
  "bénéficier (à)",
  "benefit (someone)"
 ],
 [
  29,
  "L6-037",
  "bénéficier (de)",
  "benefit (from)"
 ],
 [
  30,
  "L6-044",
  "cesser (de)",
  "stop (doing something)"
 ],
 [
  31,
  "L6-048",
  "conseiller",
  "advise"
 ],
 [
  32,
  "L6-058",
  "craindre",
  "fear"
 ],
 [
  33,
  "L6-059",
  "consulter",
  "consult"
 ],
 [
  34,
  "L6-061",
  "dérouler",
  "unfold"
 ],
 [
  35,
  "L6-062",
  "dépêcher / se dépêcher",
  "dispatch / hurry"
 ],
 [
  36,
  "L6-073",
  "diffuser",
  "broadcast"
 ],
 [
  37,
  "L6-075",
  "demeurer",
  "remain / reside"
 ],
 [
  38,
  "L6-076",
  "diriger",
  "direct"
 ],
 [
  39,
  "L6-077",
  "disparaître",
  "disappear"
 ],
 [
  40,
  "L6-086",
  "entraîner",
  "lead to / train"
 ],
 [
  41,
  "L6-089",
  "enlever / s'enlever",
  "remove / come off"
 ],
 [
  42,
  "L6-098",
  "élire",
  "elect"
 ],
 [
  43,
  "L6-099",
  "engager",
  "hire / engage"
 ],
 [
  44,
  "L6-105",
  "se fier",
  "trust"
 ],
 [
  45,
  "L6-106",
  "faillir",
  "almost (do something) / fail"
 ],
 [
  46,
  "L6-119",
  "gratter",
  "scratch"
 ],
 [
  47,
  "L6-121",
  "gêner",
  "bother / hinder"
 ],
 [
  48,
  "L6-122",
  "grimper",
  "climb"
 ],
 [
  49,
  "L6-129",
  "gaspiller",
  "waste"
 ],
 [
  50,
  "L6-132",
  "habituer (à) / s'habituer (à)",
  "get used to"
 ],
 [
  51,
  "L6-150",
  "induire",
  "induce"
 ],
 [
  52,
  "L6-151",
  "influencer",
  "influence"
 ],
 [
  53,
  "L6-156",
  "intervenir",
  "intervene"
 ],
 [
  54,
  "L6-157",
  "interrompre",
  "interrupt"
 ],
 [
  55,
  "L6-158",
  "interférer",
  "interfere"
 ],
 [
  56,
  "L6-161",
  "irriter",
  "irritate"
 ],
 [
  57,
  "L6-172",
  "lâcher",
  "let go"
 ],
 [
  58,
  "L6-178",
  "se méfier (de)",
  "distrust / beware (of)"
 ],
 [
  59,
  "L6-180",
  "mériter",
  "deserve"
 ],
 [
  60,
  "L6-181",
  "modérer",
  "moderate"
 ],
 [
  61,
  "L6-188",
  "minorer",
  "downplay"
 ],
 [
  62,
  "L6-195",
  "négliger",
  "neglect"
 ],
 [
  63,
  "L6-198",
  "nuire (à)",
  "harm"
 ],
 [
  64,
  "L6-201",
  "obliger / s'obliger",
  "oblige / make oneself"
 ],
 [
  65,
  "L6-202",
  "omettre",
  "omit"
 ],
 [
  66,
  "L6-210",
  "parvenir (à)",
  "reach / achieve"
 ],
 [
  67,
  "L6-215",
  "percevoir",
  "perceive"
 ],
 [
  68,
  "L6-216",
  "persuader",
  "persuade"
 ],
 [
  69,
  "L6-228",
  "paraître",
  "appear"
 ],
 [
  70,
  "L6-234",
  "prévoir",
  "foresee / plan"
 ],
 [
  71,
  "L6-235",
  "prévenir",
  "prevent / warn"
 ],
 [
  72,
  "L6-236",
  "prédire",
  "predict"
 ],
 [
  73,
  "L6-264",
  "rédiger",
  "write / draft"
 ],
 [
  74,
  "L6-269",
  "ressembler (à)",
  "resemble"
 ],
 [
  75,
  "L6-295",
  "soigner",
  "care for / treat"
 ],
 [
  76,
  "L6-328",
  "tricher",
  "cheat"
 ],
 [
  77,
  "L6-379",
  "faire la connaissance de",
  "meet / get to know"
 ],
 [
  78,
  "L6-395",
  "s'en faire",
  "worry"
 ],
 [
  79,
  "L6-396",
  "s'en aller",
  "go away / leave"
 ],
 [
  80,
  "L6-397",
  "se rendre compte de",
  "realize"
 ],
 [
  81,
  "L6-399",
  "tomber en panne",
  "break down"
 ]
]

cards = []
seen = set()
for n, pid, pfr, pen in ENTRIES:
    if pid not in all_cards:
        raise SystemExit(f"card not found: {pid} (quiz #{n})")
    if pid not in seen:
        seen.add(pid)
        cards.append(all_cards[pid])
print(f"entries: {len(ENTRIES)}, unique cards: {len(cards)}")

template = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>퀴즈 동사 81 · TEF Atelier</title>
<link rel="icon" href="icons/icon-192.png">
<style>
  :root{
    --paper:#f6f3ec; --surface:#fffdf8; --ink:#1f2925; --muted:#66706b; --line:#ddd8cc;
    --green:#19724a; --green-soft:#e2f1e7; --red:#b9483d; --red-soft:#f7e5e2;
    --shadow:0 18px 50px rgba(36,43,39,.10); color-scheme:light;
  }
  *{box-sizing:border-box} html{-webkit-tap-highlight-color:transparent}
  body{margin:0;min-height:100dvh;background:radial-gradient(circle at 18% 0%,rgba(235,221,183,.42),transparent 30rem),var(--paper);
    color:var(--ink);font-family:Inter,Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
  button{font:inherit;color:inherit;touch-action:manipulation;cursor:pointer}
  button:active{transform:scale(.98)}
  .app{width:min(720px,100%);margin:0 auto;padding:max(16px,env(safe-area-inset-top)) 18px max(24px,env(safe-area-inset-bottom));display:flex;flex-direction:column;gap:14px}
  header{display:flex;align-items:center;justify-content:space-between;gap:10px}
  .brand{display:flex;align-items:center;gap:11px}
  .mark{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;background:linear-gradient(145deg,#2a3d34,#141c18);color:#ead9b8;font-family:Georgia,serif;font-size:22px;flex:0 0 auto}
  h1{margin:0;font-size:20px;font-family:Georgia,serif}
  .subtitle{color:var(--muted);font-size:12px;margin-top:2px}
  .link-btn{border:1px solid var(--line);background:rgba(255,253,248,.82);border-radius:12px;padding:9px 11px;font-size:13px;text-decoration:none;color:var(--ink);white-space:nowrap}
  .card{background:var(--surface);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);padding:20px}
  .chips{display:flex;flex-wrap:wrap;gap:8px}
  .chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:9px 13px;font-size:14px}
  .chip.on{background:var(--green);border-color:var(--green);color:#fff;font-weight:700}
  .chip small{opacity:.75;font-size:12px}
  label.flabel{display:block;font-size:13px;color:var(--muted);margin:16px 0 8px}
  .big-btn{width:100%;border:none;border-radius:14px;padding:15px;font-size:16px;font-weight:700;background:var(--green);color:#fff;margin-top:20px}
  .ghost-btn{width:100%;border:1px solid var(--line);border-radius:14px;padding:13px;font-size:15px;background:#fff;margin-top:10px}
  .danger{color:var(--red)}
  .resume{border:1px solid var(--green);background:var(--green-soft);border-radius:16px;padding:16px}
  .resume b{font-size:16px}
  .meta{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:13px;color:var(--muted);flex-wrap:wrap}
  .phase-badge{background:var(--ink);color:#fff;border-radius:999px;padding:4px 10px;font-size:12px;font-weight:700}
  .bar{height:8px;border-radius:99px;background:#e9e4d6;overflow:hidden;margin-top:10px}
  .bar>i{display:block;height:100%;background:var(--green);border-radius:99px;transition:width .25s}
  .word-id{font-size:12px;color:var(--muted);letter-spacing:.04em}
  .fr{font-size:clamp(28px,7vw,40px);font-weight:800;line-height:1.25;margin:14px 0 6px;word-break:keep-all;text-align:center;padding:0 52px}
  .quiz-note{text-align:center;color:var(--muted);font-size:14px;margin-top:2px}
  .ko{font-size:clamp(21px,5.5vw,28px);font-weight:700;line-height:1.4;margin-top:12px;text-align:center}
  .en{text-align:center;color:var(--muted);font-size:15px;margin-top:6px}
  .quiz-answer{text-align:center;color:var(--green);font-size:14px;margin-top:8px;font-weight:600}
  .row{display:flex;gap:10px;margin-top:18px}
  .row>button{flex:1;border-radius:14px;padding:15px;font-size:16px;font-weight:700;border:1px solid var(--line);background:#fff}
  .btn-wrong{background:var(--red-soft)!important;border-color:#e3b7b1!important;color:var(--red)}
  .btn-right{background:var(--green-soft)!important;border-color:#a9d3ba!important;color:var(--green)}
  .reveal-btn{width:100%;border:1px dashed #b9b2a0;border-radius:14px;padding:16px;font-size:16px;background:rgba(255,253,248,.6);margin-top:16px}
  .audio-btn{position:absolute;right:0;top:10px;border:1px solid var(--line);background:#fff;border-radius:999px;width:44px;height:44px;font-size:19px}
  .fr-row{position:relative}
  .intro-title{font-size:22px;font-weight:800;margin:4px 0 8px}
  .intro-body{color:var(--muted);line-height:1.6;font-size:15px}
  .hidden{display:none!important}
  .note{font-size:12px;color:var(--muted);line-height:1.55}
  .statgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:14px}
  .stat{border:1px solid var(--line);border-radius:14px;padding:12px;text-align:center;background:#fff}
  .stat b{display:block;font-size:20px}
  .stat span{font-size:12px;color:var(--muted)}
  details.listbox{margin-top:14px}
  details.listbox summary{cursor:pointer;font-weight:700;font-size:15px;padding:6px 0}
  .qlist{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
  .qlist td,.qlist th{border-bottom:1px solid var(--line);padding:6px 4px;text-align:left;vertical-align:top}
  .qlist th{color:var(--muted);font-weight:600}
  .prompt-ko{font-size:clamp(24px,6vw,34px);font-weight:800;line-height:1.35;margin:16px 0 4px;text-align:center}
  .prompt-en{text-align:center;color:var(--muted);font-size:15px;margin-top:4px}
  #type-input{font:inherit;width:100%;padding:15px;border:2px solid var(--line);border-radius:14px;background:#fff;margin-top:18px;text-align:center;font-size:19px}
  #type-input:focus{outline:none;border-color:var(--green)}
  .type-result{border-radius:14px;padding:16px;margin-top:16px;text-align:center}
  .type-result.correct{background:var(--green-soft)}
  .type-result.wrong{background:var(--red-soft)}
  .type-msg{font-size:19px;font-weight:800}
  .type-flag{font-size:13px;font-weight:700;color:#8a6d1a;background:#f7ecc9;border-radius:999px;padding:2px 9px;margin-left:6px;vertical-align:middle}
  .type-given{color:var(--muted);font-size:14px;margin-top:6px}
  .type-answer{font-size:17px;margin-top:8px}
</style>
</head>
<body>
<div class="app">
  <header>
    <div class="brand"><div class="mark">A</div>
      <div><h1>퀴즈 동사 81</h1><div class="subtitle">Quiz : Les verbes (1-1500) 81개만 · TEF Atelier</div></div>
    </div>
    <a class="link-btn" href="index.html">← 단어장</a>
  </header>

  <!-- 설정 -->
  <section id="view-setup">
    <div id="resume-box"></div>
    <div class="card">
      <div style="font-weight:800;font-size:17px">퀴즈 81개만 공부하기</div>
      <div class="note" style="margin-top:8px">실제 퀴즈처럼 뜻을 보고 프랑스어를 직접 타이핑하는 게 기본입니다. PDF 순서 그대로이고, 22~81번은 앱의 B1·B2 동사 덱, 1~21번은 명사·형용사·연결어·관용 표현·A2·B1에 흩어져 있던 것까지 전부 모아놨습니다. bénéficier는 (à)/(de) 두 항목이라 항목 81개 · 카드 80장입니다.</div>
      <label class="flabel">방식</label>
      <div class="chips" id="mode-chips"></div>
      <label class="flabel">블록 크기 (한 번에 돌릴 개수)</label>
      <div class="chips" id="size-chips"></div>
      <button class="big-btn" id="start-btn">시작하기</button>
      <div class="note" style="margin-top:12px">흐름은 사이클 학습과 같습니다: 블록 1회차 → 같은 블록 섞어서 2회차 → 2회차에서 틀린 것만 → 다음 블록. 3블록마다 틀린 단어를 섞어서 누적 복습하고, 마지막에는 끝까지 남은 것만 한 번 더 봅니다. 타이핑 채점은 기존 단어장과 같은 기준입니다 — 악센트만 틀리거나 관사·재귀대명사·끝 전치사가 빠진 경우는 맞힌 것으로 보되 "정확한 형태 확인" 표시를 띄워줍니다. 단, bénéficier (à)/(de)는 그 전치사가 정답의 핵심이라 꼭 써야 합니다. 진도는 이 기기에 따로 저장돼서 기존 단어장·사이클 진도와 섞이지 않습니다.</div>
      <details class="listbox">
        <summary>81개 목록 먼저 보기</summary>
        <table class="qlist"><thead><tr><th>#</th><th>퀴즈 표기</th><th>앱 카드</th><th>뜻</th></tr></thead><tbody id="list-body"></tbody></table>
      </details>
    </div>
  </section>

  <!-- 단계 안내 -->
  <section id="view-intro" class="hidden">
    <div class="card">
      <div class="word-id" id="intro-kicker"></div>
      <div class="intro-title" id="intro-title"></div>
      <div class="intro-body" id="intro-body"></div>
      <button class="big-btn" id="intro-btn">시작</button>
      <button class="ghost-btn" id="intro-setup">설정으로 (진도는 저장돼 있어요)</button>
    </div>
  </section>

  <!-- 학습 -->
  <section id="view-study" class="hidden">
    <div class="meta"><span id="meta-left"></span><span class="phase-badge" id="meta-phase"></span><span id="meta-right"></span></div>
    <div class="bar"><i id="bar-fill" style="width:0%"></i></div>
    <div class="card" style="margin-top:12px">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span class="word-id" id="card-id"></span>
        <span class="word-id" id="card-count"></span>
      </div>

      <!-- 카드 방식 -->
      <div id="prompt-card">
        <div class="fr-row">
          <div class="fr" id="card-fr"></div>
          <button class="audio-btn" id="audio-btn" title="발음 듣기">🔊</button>
        </div>
        <div class="quiz-note" id="card-note"></div>
        <div id="answer-box" class="hidden">
          <div class="ko" id="card-ko"></div>
          <div class="en" id="card-en"></div>
          <div class="quiz-answer" id="card-quiz-answer"></div>
        </div>
        <button class="reveal-btn" id="reveal-btn">뜻 보기 (먼저 머릿속으로 떠올려보세요)</button>
        <div class="row hidden" id="grade-row">
          <button class="btn-wrong" id="wrong-btn">✕ 틀렸어요</button>
          <button class="btn-right" id="right-btn">○ 맞혔어요</button>
        </div>
      </div>

      <!-- 타이핑 방식 -->
      <div id="prompt-type" class="hidden">
        <div class="prompt-ko" id="type-ko"></div>
        <div class="prompt-en" id="type-en"></div>
        <input id="type-input" type="text" autocomplete="off" autocapitalize="none" autocorrect="off" spellcheck="false" placeholder="프랑스어로 입력">
        <div class="row" id="type-btn-row">
          <button class="btn-wrong" id="giveup-btn">모름</button>
          <button class="btn-right" id="check-btn">확인</button>
        </div>
        <div id="type-result"></div>
      </div>
    </div>
    <button class="ghost-btn" id="study-setup">잠깐 멈추기 (진도 저장됨)</button>
  </section>

  <!-- 완료 -->
  <section id="view-done" class="hidden">
    <div class="card">
      <div class="intro-title">🎉 81개를 끝까지 다 돌렸어요</div>
      <div class="intro-body" id="done-body"></div>
      <div class="statgrid">
        <div class="stat"><b id="done-answered">0</b><span>총 인출 횟수</span></div>
        <div class="stat"><b id="done-rate">0%</b><span>맞힌 비율</span></div>
        <div class="stat"><b id="done-stubborn">0</b><span>끝까지 틀린 단어</span></div>
      </div>
      <div id="done-stubborn-list" class="note" style="margin-top:12px"></div>
      <button class="big-btn" id="done-again">처음부터 다시 시작하기</button>
      <a href="index.html" style="text-decoration:none"><button class="ghost-btn">단어장으로 돌아가기</button></a>
    </div>
  </section>
</div>

<script>
const CARDS = __CARDS_JSON__;
const ENTRIES = __ENTRIES_JS__;
const BY_ID = {}; CARDS.forEach(c=>BY_ID[c.id]=c);
const BY_N = {}; ENTRIES.forEach(e=>BY_N[e.n]=e);
const ALL = ENTRIES.map(e=>e.n);
const KEY = "tef-quiz81-v1";
const $ = id => document.getElementById(id);
const shuffle = a => { a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
function lexShort(c){ return (c.lexique===0?"A0":c.lexique===7?"E7":"L"+c.lexique)+"-"+String(c.number).padStart(3,"0"); }
function chunks(size){ const out=[]; for(let i=0;i<ALL.length;i+=size) out.push(ALL.slice(i,i+size)); return out; }
function phaseLabel(p){ return {r1:"1회차", r2:"2회차 · 섞어서", r3:"틀린 것만", cum:"누적 복습", final:"마지막 복습"}[p] || p; }
function modeLabel(m){ return m==="type" ? "✍️ 타이핑" : "🃏 카드"; }
function promptKo(e){ if(e.pko) return e.pko; const c=BY_ID[e.pid]; return c? (c.ko||c.en||"") : ""; }

/* ===== 프랑스어 타이핑 채점 (기존 단어장과 같은 기준) ===== */
function normFr(s){ return String(s).toLowerCase().replace(/[’‘]/g,"'").replace(/[.!?]+$/g,"").trim().replace(/\s+/g," "); }
function cleanInput(s){ return normFr(s).replace(/\s*\([^)]*\)/g," ").trim().replace(/\s+/g," "); }
function stripAccents(s){ return s.replace(/œ/g,"oe").replace(/æ/g,"ae").normalize("NFD").replace(/[\u0300-\u036f]/g,""); }
function coreForm(a){
  let s = String(a);
  s = s.replace(/\s*\+\s*[\w/]+$/, "");
  s = s.replace(/^l'/, "");
  s = s.replace(/^(le|la|les|un|une|des)\s+/, "");
  s = s.replace(/^s'/, "").replace(/^se\s+/, "");
  s = s.replace(/\s+(de|d'|à|au|aux|en|pour|contre|avec|sur|dans|par|sans|chez)$/, "");
  return s.trim().replace(/\s+/g," ");
}
function acceptableAnswers(fr){
  const out = [];
  String(fr).split("/").forEach(v => {
    const base = v.replace(/\s*\([^)]*\)/g,"").replace(/\s{2,}/g," ").trim();
    if(base) out.push(base);
    const kept = v.replace(/\s*\(([^)]*)\)/g, (m,g) => /^(de|à|au|aux|en|par|pour|avec|sur|dans|chez|contre|d')$/i.test(g.trim()) ? " "+g.trim() : "").replace(/\s{2,}/g," ").trim();
    if(kept && kept !== base) out.push(kept);
  });
  return out;
}
function normKeepParens(s){ return normFr(s).replace(/[()]/g," ").trim().replace(/\s+/g," "); }
/* 채점 결과: correct | accent | partial | wrong  (accent·partial도 맞힌 것으로 침, 표시만 다름) */
function gradeEntry(e, raw, gaveUp){
  if(gaveUp) return "wrong";
  if(!String(raw||"").trim()) return "wrong";
  if(e.strict){
    const n = normKeepParens(raw);
    const target = normKeepParens(e.pfr);
    if(n === target) return "correct";
    if(stripAccents(n) === stripAccents(target)) return "accent";
    return "wrong";
  }
  const card = BY_ID[e.pid];
  const answers = [...new Set([...acceptableAnswers(e.pfr), ...(card? acceptableAnswers(card.fr):[])])];
  const n = cleanInput(raw);
  const parts = n.split("/").map(x=>x.trim()).filter(Boolean);
  const hit = x => answers.some(a => normFr(a) === x || stripAccents(normFr(a)) === stripAccents(x));
  if(parts.length > 1 && parts.every(hit)) return "correct";
  if(answers.some(a => normFr(a) === n)) return "correct";
  if(answers.some(a => stripAccents(normFr(a)) === stripAccents(n))) return "accent";
  if(answers.some(a => { const full = normFr(a), core = coreForm(full); return core && core !== full && stripAccents(core) === stripAccents(n); })) return "partial";
  return "wrong";
}
window.__quizGrade = (n, raw) => gradeEntry(BY_N[n], raw, false);

let S = null;
function save(){ try{ localStorage.setItem(KEY, JSON.stringify(S)); }catch(e){} }
function load(){ try{ const o=JSON.parse(localStorage.getItem(KEY)||"null"); return (o && o.v===1 && Array.isArray(o.queue)) ? o : null; }catch(e){ return null; } }

let selSize = 20, selMode = "type";
function renderSetup(){
  const saved = load();
  const rb = $("resume-box");
  if(saved && saved.view!=="done"){
    const tb = chunks(saved.size).length;
    rb.innerHTML = '<div class="resume"><b>이어서 할 퀴즈 학습이 있어요</b><div style="margin-top:6px;font-size:14px">'
      + modeLabel(saved.mode||"card") + ' · 블록 ' + Math.min(saved.blockIdx+1,tb) + '/' + tb + ' · ' + phaseLabel(saved.stage)
      + ' · 지금까지 ' + saved.stats.answered + '번 인출</div>'
      + '<button class="big-btn" id="resume-btn" style="margin-top:12px">이어서 계속하기</button>'
      + '<button class="ghost-btn danger" id="discard-btn">이 학습 버리기</button></div>';
    $("resume-btn").onclick = ()=>{ S=saved; S.mode=S.mode||"card"; selSize=saved.size; selMode=S.mode; if(S.view==="intro"){ renderIntro(); show("intro"); } else if(S.view==="done"){ renderDone(); show("done"); } else { show("study"); renderCard(); } };
    $("discard-btn").onclick = ()=>{ if(confirm("진행 중인 퀴즈 학습을 버릴까요? (기존 단어장 진도는 그대로입니다)")){ localStorage.removeItem(KEY); renderSetup(); } };
  } else rb.innerHTML = "";
  $("mode-chips").innerHTML = [["type","✍️ 타이핑 <small>뜻 보고 프랑스어 직접 쓰기</small>"],["card","🃏 카드 <small>프랑스어 보고 뜻 떠올리기</small>"]].map(([id,label])=>'<button class="chip'+(id===selMode?" on":"")+'" data-mode="'+id+'">'+label+'</button>').join("");
  document.querySelectorAll("[data-mode]").forEach(b=>b.onclick=()=>{ selMode=b.dataset.mode; renderSetup(); });
  $("size-chips").innerHTML = [10,20,27].map(n=>'<button class="chip'+(n===selSize?" on":"")+'" data-size="'+n+'">'+n+'개씩</button>').join("");
  document.querySelectorAll("[data-size]").forEach(b=>b.onclick=()=>{ selSize=+b.dataset.size; renderSetup(); });
  $("list-body").innerHTML = ENTRIES.map(e=>{ const c=BY_ID[e.pid]; return '<tr><td>'+e.n+'</td><td>'+e.pfr+'</td><td>'+lexShort(c)+'</td><td>'+(c?c.ko:"")+'</td></tr>'; }).join("");
  show("setup");
}
function setIntro(kicker,title,body,btn){ S.intro={kicker:kicker,title:title,body:body,btn:btn}; S.view="intro"; }
function enterBlock(note){
  const bs = chunks(S.size);
  S.block = bs[S.blockIdx].slice();
  S.stage="r1"; S.queue=S.block.slice(); S.idx=0; S.wrongR1=0; S.wrongR2=[];
  setIntro("퀴즈 81 · "+modeLabel(S.mode)+" · 블록 "+(S.blockIdx+1)+"/"+bs.length,
    "블록 "+(S.blockIdx+1)+" / "+bs.length+" — "+S.block.length+"개",
    (note? note+" ":"")+(S.mode==="type"
      ? "뜻을 보고 프랑스어를 직접 써보세요. 바로 안 떠오르면 모름으로 넘기세요. 같은 블록을 섞어서 한 번 더 하고, 그때도 틀린 것만 마지막으로 봅니다."
      : "먼저 순서대로 한 번 봅니다. 바로 안 떠오르면 틀린 걸로 넘기세요. 같은 블록을 섞어서 한 번 더 하고, 그때도 틀린 것만 마지막으로 봅니다."),
    "1회차 시작");
}
function startStudy(){
  S = { v:1, size:selSize, mode:selMode, blockIdx:0, stage:"r1", view:"intro", queue:[], idx:0, block:[],
        wrongR1:0, wrongR2:[], cumPending:[], stubborn:[], blocksSinceCum:0,
        stats:{answered:0, correct:0}, intro:null };
  enterBlock("");
  save(); renderIntro(); show("intro");
}
function finishBlock(note){
  S.blocksSinceCum++;
  if(S.blocksSinceCum>=3){
    S.blocksSinceCum=0;
    if(S.cumPending.length){
      S.stage="cum"; S.queue=shuffle(S.cumPending); S.idx=0; const n=S.queue.length; S.cumPending=[];
      setIntro("3블록 누적 복습", "틀렸던 단어 "+n+"개, 섞어서 한 번 더",
        (note? note+" ":"")+"지난 블록들에서 2회차에 틀렸던 단어들입니다. 여기서 또 틀리면 마지막 복습 목록으로 넘어갑니다.", "누적 복습 시작");
      return;
    }
  }
  advance(note);
}
function advance(note){
  S.blockIdx++;
  if(S.blockIdx < chunks(S.size).length){ enterBlock(note); }
  else if(S.stubborn.length){
    S.stage="final"; S.queue=shuffle(S.stubborn); S.idx=0;
    setIntro("범위 끝", "마지막 복습 — 끝까지 틀린 단어 "+S.stubborn.length+"개",
      (note? note+" ":"")+"블록 3회차와 누적 복습에서도 틀렸던 단어들만 모았습니다. 이걸 끝내면 완료됩니다.", "마지막 복습 시작");
  } else { S.view="done"; }
}
function endStage(){
  if(S.stage==="r1"){
    S.stage="r2"; S.queue=shuffle(S.block); S.idx=0;
    setIntro("블록 "+(S.blockIdx+1)+" · 1회차 끝", "같은 "+S.block.length+"개, 순서를 섞어서 다시",
      "1회차에서 틀린 단어는 "+S.wrongR1+"개였어요. 이번에 맞히는지가 진짜입니다.", "2회차 시작");
  } else if(S.stage==="r2"){
    if(S.wrongR2.length){
      S.stage="r3"; S.queue=shuffle(S.wrongR2); S.idx=0;
      setIntro("블록 "+(S.blockIdx+1)+" · 2회차 끝", "틀린 "+S.wrongR2.length+"개만 한 번 더",
        "여기서 맞히면 이 블록은 졸업입니다. 또 틀리면 누적·마지막 복습에서 다시 만납니다.", "틀린 것만 시작");
    } else finishBlock("2회차에서 전부 맞혔어요 🎉");
  } else if(S.stage==="r3"){
    finishBlock("");
  } else if(S.stage==="cum"){
    advance("누적 복습 완료");
  } else if(S.stage==="final"){
    S.view="done";
  }
}
function afterTransition(){
  save();
  if(S.view==="done"){ renderDone(); show("done"); }
  else { renderIntro(); show("intro"); }
}
function recordGrade(ok){
  const e=currentEntry(); if(!e) return;
  const uid=e.n;
  S.stats.answered++; if(ok) S.stats.correct++;
  if(S.stage==="r1" && !ok) S.wrongR1++;
  if(S.stage==="r2" && !ok){ S.wrongR2.push(uid); if(!S.cumPending.includes(uid)) S.cumPending.push(uid); }
  if((S.stage==="r3" || S.stage==="cum") && !ok){ if(!S.stubborn.includes(uid)) S.stubborn.push(uid); }
}
function progressNext(){
  S._pending=null;
  S.idx++;
  if(S.idx < S.queue.length){ save(); renderCard(); }
  else { endStage(); afterTransition(); }
}
function renderIntro(){
  $("intro-kicker").textContent = S.intro? S.intro.kicker : "";
  $("intro-title").textContent = S.intro? S.intro.title : "";
  $("intro-body").textContent = S.intro? S.intro.body : "";
  $("intro-btn").textContent = S.intro? S.intro.btn : "시작";
}
$("intro-btn").onclick = ()=>{ S.view="study"; save(); show("study"); renderCard(); };
$("intro-setup").onclick = ()=>{ save(); renderSetup(); };
$("study-setup").onclick = ()=>{ save(); renderSetup(); };

function currentEntry(){ return BY_N[S.queue[S.idx]]; }
function renderCard(){
  const e = currentEntry(); if(!e){ endStage(); afterTransition(); return; }
  const c = BY_ID[e.pid];
  const tb = chunks(S.size).length;
  $("meta-left").textContent = S.stage==="cum" ? "누적 복습" : S.stage==="final" ? "마지막 복습" : ("블록 "+(S.blockIdx+1)+"/"+tb);
  $("meta-phase").textContent = phaseLabel(S.stage);
  $("meta-right").textContent = "누적 틀림 " + S.stubborn.length + "개";
  $("bar-fill").style.width = Math.round(S.idx/S.queue.length*100)+"%";
  $("card-id").textContent = "퀴즈 " + e.n + "번 · " + lexShort(c);
  $("card-count").textContent = (S.idx+1)+" / "+S.queue.length;
  const isType = S.mode==="type";
  $("prompt-card").classList.toggle("hidden", isType);
  $("prompt-type").classList.toggle("hidden", !isType);
  window._revealed=false; window._typeChecked=false;
  if(isType){
    $("type-ko").textContent = promptKo(e);
    $("type-en").textContent = "영어: " + e.pen;
    $("type-input").value = "";
    $("type-result").innerHTML = "";
    $("type-btn-row").classList.remove("hidden");
    if(S._pending && S._pending.n===e.n){
      window._typeChecked = true;
      $("type-input").value = S._pending.raw || "";
      renderTypeResult(e, S._pending.result, S._pending.raw || "");
    } else {
      setTimeout(()=>{ try{ $("type-input").focus({preventScroll:true}); }catch(err){} }, 30);
    }
  } else {
    $("card-fr").textContent = c.fr;
    const sameForm = e.pfr.replace(/’/g,"'").toLowerCase() === c.fr.replace(/’/g,"'").toLowerCase();
    $("card-note").textContent = sameForm ? "" : ("퀴즈 표기: " + e.pfr);
    $("answer-box").classList.add("hidden");
    $("grade-row").classList.add("hidden");
    $("reveal-btn").classList.remove("hidden");
  }
}
$("reveal-btn").onclick = ()=>{
  const e=currentEntry(); if(!e) return;
  const c=BY_ID[e.pid];
  $("card-ko").textContent = c.ko||"";
  $("card-en").textContent = c.en||"";
  $("card-quiz-answer").textContent = "퀴즈 답: " + e.pen;
  $("answer-box").classList.remove("hidden");
  $("grade-row").classList.remove("hidden");
  $("reveal-btn").classList.add("hidden");
  window._revealed=true;
};
function answer(ok){
  if(!currentEntry() || !window._revealed) return;
  recordGrade(ok);
  progressNext();
}
$("wrong-btn").onclick = ()=>answer(false);
$("right-btn").onclick = ()=>answer(true);

/* ===== 타이핑 방식 ===== */
function checkTyped(gaveUp){
  const e=currentEntry(); if(!e || window._typeChecked) return;
  const raw = $("type-input").value;
  if(!gaveUp && !raw.trim()){ $("type-input").focus(); return; }
  const result = gradeEntry(e, raw, gaveUp);
  const ok = result !== "wrong";
  window._typeChecked = true;
  recordGrade(ok);
  S._pending = { n:e.n, result:result, raw:raw };
  save();
  renderTypeResult(e, result, raw);
}
function renderTypeResult(e, result, raw){
  const ok = result !== "wrong";
  const c = BY_ID[e.pid];
  const flag = result==="accent" ? '<span class="type-flag">악센트 확인</span>'
    : result==="partial" ? '<span class="type-flag">정확한 형태 확인</span>' : "";
  const sameForm = e.pfr.replace(/’/g,"'").toLowerCase() === c.fr.replace(/’/g,"'").toLowerCase();
  $("type-result").innerHTML =
    '<div class="type-result '+(ok?"correct":"wrong")+'">'
    + '<div class="type-msg">'+(ok? "⭕ 맞았어요!" : "❌ 틀렸어요")+flag+'</div>'
    + (ok? "" : '<div class="type-given">입력: '+(raw.trim()? raw.replace(/</g,"&lt;") : "(비어 있음)")+'</div>')
    + '<div class="type-answer">정답: <b>'+e.pfr.replace(/</g,"&lt;")+'</b>'+(sameForm? "" : ' <span style="color:var(--muted);font-size:14px">(앱 표기: '+c.fr.replace(/</g,"&lt;")+')</span>')+'</div>'
    + '<div class="type-given">'+promptKo(e)+' · '+e.pen+'</div>'
    + '<div class="row" style="margin-top:12px"><button id="type-audio-btn" style="flex:1;border-radius:12px;padding:12px;border:1px solid var(--line);background:#fff;font-weight:700">🔊 발음 듣기</button>'
    + '<button id="type-next-btn" style="flex:1;border-radius:12px;padding:12px;border:none;background:var(--green);color:#fff;font-weight:700">다음 →</button></div>'
    + '</div>';
  $("type-btn-row").classList.add("hidden");
  $("type-audio-btn").onclick = ()=>playAudio(e);
  $("type-next-btn").onclick = ()=>{ progressNext(); };
  setTimeout(()=>{ try{ $("type-next-btn").focus({preventScroll:true}); }catch(err){} }, 30);
}
$("check-btn").onclick = ()=>checkTyped(false);
$("giveup-btn").onclick = ()=>checkTyped(true);
$("type-input").addEventListener("keydown", ev=>{
  if(ev.key==="Enter"){ ev.preventDefault(); if(!window._typeChecked) checkTyped(false); }
});
document.addEventListener("keydown", e=>{
  if($("view-study").classList.contains("hidden")) return;
  if(S && S.mode==="type"){
    if(window._typeChecked && e.code==="Enter"){ e.preventDefault(); const b=$("type-next-btn"); if(b) b.click(); }
    return;
  }
  if(!window._revealed && (e.code==="Space"||e.code==="Enter")){ e.preventDefault(); $("reveal-btn").click(); }
  else if(window._revealed && e.key==="ArrowLeft") answer(false);
  else if(window._revealed && e.key==="ArrowRight") answer(true);
});

/* 발음: 내장 MP3 우선, 없으면 기기 프랑스어 음성 */
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
function cleanFrenchForSpeech(text) {
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
function speechTextForEntry(e){ return cleanFrenchForSpeech(e.pfr); }
window.__quizSpeechText = n => speechTextForEntry(BY_N[n]);
function playAudio(e){
  if(!e) return;
  const c = BY_ID[e.pid]; if(!c) return;
  const text = speechTextForEntry(e) || cleanFrenchForSpeech(c.fr);
  const a=new Audio("audio/"+encodeURIComponent(c.id)+".mp3");
  let fell=false;
  const fallback=()=>{ if(fell) return; fell=true; try{ const u=new SpeechSynthesisUtterance(text); u.lang="fr-FR"; u.rate=.92; speechSynthesis.cancel(); speechSynthesis.speak(u); }catch(err){} };
  a.addEventListener("error", fallback, {once:true});
  const p=a.play(); if(p&&p.catch) p.catch(fallback);
}
$("audio-btn").onclick = ()=>{ const e=currentEntry(); if(e) playAudio(e); };

function renderDone(){
  $("done-answered").textContent = S.stats.answered;
  $("done-rate").textContent = S.stats.answered? Math.round(S.stats.correct/S.stats.answered*100)+"%":"-";
  $("done-stubborn").textContent = S.stubborn.length;
  $("done-body").textContent = "퀴즈 81개를 "+modeLabel(S.mode)+" 방식으로 끝까지 돌렸습니다.";
  $("done-stubborn-list").innerHTML = S.stubborn.length
    ? "끝까지 틀린 단어: " + S.stubborn.map(n=>{ const e=BY_N[n]; const c=BY_ID[e.pid]; return n+"번 "+c.fr+" = "+c.ko; }).join(" · ")
    : "끝까지 남은 틀린 단어가 없습니다.";
}
$("done-again").onclick = ()=>{ localStorage.removeItem(KEY); S=null; renderSetup(); };
$("start-btn").onclick = startStudy;

function show(name){
  ["setup","intro","study","done"].forEach(v=>$("view-"+v).classList.toggle("hidden", v!==name));
  window.scrollTo(0,0);
}
renderSetup();
</script>
</body>
</html>
"""

PROMPT_KO = {28: "-에 도움이 되다 (남에게)", 29: "-에 득을 보다 (본인이)"}
STRICT = {28, 29}  # bénéficier (à)/(de): 전치사가 정답의 핵심이라 괄호를 벗겨내지 않고 채점
entries_js = [{"n": n, "pid": pid, "pfr": pfr, "pen": pen, "pko": PROMPT_KO.get(n, ""), "strict": n in STRICT} for n, pid, pfr, pen in ENTRIES]
out = template.replace("__CARDS_JSON__", json.dumps(cards, ensure_ascii=False))
out = out.replace("__ENTRIES_JS__", json.dumps(entries_js, ensure_ascii=False))
(root / "quiz81.html").write_text(out, encoding="utf-8")
print(f"quiz81.html written: {len(out)} bytes")
