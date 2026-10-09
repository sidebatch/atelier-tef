#!/usr/bin/env python3
"""cycle.html 생성기: index.html의 CARDS 데이터를 그대로 읽어 사이클 학습 페이지에 내장한다.
기존 파일은 일절 수정하지 않고 cycle.html 하나만 새로 쓴다."""
import re, json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
index = (root / "index.html").read_text(encoding="utf-8")
m = re.search(r"const CARDS = (\[.*?\]);\s*const STORAGE_KEY", index, re.S)
if not m:
    raise SystemExit("CARDS not found in index.html")
cards = json.loads(m.group(1))
print(f"cards: {len(cards)}")

template = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>사이클 학습 · TEF Atelier</title>
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
  input[type=number]{font:inherit;width:110px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:#fff}
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
  .fr .sub{font-size:.55em;color:var(--muted);font-weight:600}
  .ko{font-size:clamp(21px,5.5vw,28px);font-weight:700;line-height:1.4;margin-top:12px;text-align:center}
  .en{text-align:center}
  .en{color:var(--muted);font-size:15px;margin-top:6px}
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
</style>
</head>
<body>
<div class="app">
  <header>
    <div class="brand"><div class="mark">A</div>
      <div><h1>사이클 학습</h1><div class="subtitle">20개씩 · 다시 · 틀린 것만 · TEF Atelier</div></div>
    </div>
    <a class="link-btn" href="index.html">← 단어장</a>
  </header>

  <!-- 설정 -->
  <section id="view-setup">
    <div id="resume-box"></div>
    <div class="card">
      <div style="font-weight:800;font-size:17px">어떤 덱으로 할까요?</div>
      <label class="flabel">덱</label>
      <div class="chips" id="deck-chips"></div>
      <label class="flabel">블록 크기 (한 번에 돌릴 개수)</label>
      <div class="chips" id="size-chips"></div>
      <label class="flabel">시작 위치 (덱의 몇 번째 단어부터?)</label>
      <input type="number" id="start-input" min="1" value="1"> <span class="note" id="deck-total"></span>
      <div class="note" style="margin-top:8px">예: 앞에서 100개를 이미 봤으면 101을 넣으세요. 덱 순서 그대로 진행합니다.</div>
      <button class="big-btn" id="start-btn">사이클 시작하기</button>
      <div class="note" style="margin-top:12px">흐름: 블록 1회차 → 같은 블록 섞어서 2회차 → 2회차에서 틀린 것만 → 다음 블록. 3블록마다 틀린 단어를 섞어서 누적 복습하고, 마지막에는 끝까지 남은 단어만 한 번 더 봅니다. 진도는 이 기기에 따로 저장돼서 기존 단어장 진도와 섞이지 않습니다.</div>
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
      <div class="fr-row">
        <div class="fr" id="card-fr"></div>
        <button class="audio-btn" id="audio-btn" title="발음 듣기">🔊</button>
      </div>
      <div id="answer-box" class="hidden">
        <div class="ko" id="card-ko"></div>
        <div class="en" id="card-en"></div>
      </div>
      <button class="reveal-btn" id="reveal-btn">뜻 보기 (먼저 머릿속으로 떠올려보세요)</button>
      <div class="row hidden" id="grade-row">
        <button class="btn-wrong" id="wrong-btn">✕ 틀렸어요</button>
        <button class="btn-right" id="right-btn">○ 맞혔어요</button>
      </div>
    </div>
    <button class="ghost-btn" id="study-setup">잠깐 멈추기 (진도 저장됨)</button>
  </section>

  <!-- 완료 -->
  <section id="view-done" class="hidden">
    <div class="card">
      <div class="intro-title">🎉 끝까지 다 돌렸어요</div>
      <div class="intro-body" id="done-body"></div>
      <div class="statgrid">
        <div class="stat"><b id="done-answered">0</b><span>총 인출 횟수</span></div>
        <div class="stat"><b id="done-rate">0%</b><span>맞힌 비율</span></div>
        <div class="stat"><b id="done-stubborn">0</b><span>끝까지 틀린 단어</span></div>
      </div>
      <div id="done-stubborn-list" class="note" style="margin-top:12px"></div>
      <button class="big-btn" id="done-again">새 사이클 시작하기</button>
      <a href="index.html" style="text-decoration:none"><button class="ghost-btn">단어장으로 돌아가기</button></a>
    </div>
  </section>
</div>

<script>
const CARDS = __CARDS_JSON__;
const BY_ID = {}; CARDS.forEach(c=>BY_ID[c.id]=c);
const DECKS = [
  { id:"b1b2-verb", label:"B1·B2 동사", test:c=>c.lexique===6 && (c.number<=399 || c.number>=1399) },
  { id:"base", label:"A2·B1 단어", test:c=>c.lexique>=1 && c.lexique<=5 },
  { id:"a1a2", label:"A1·A2 단어", test:c=>c.lexique===0 },
  { id:"b1b2", label:"B1·B2 전체", test:c=>c.lexique===6 },
  { id:"b1b2-adj", label:"B1·B2 형용사", test:c=>c.lexique===6 && c.number>=400 && c.number<=547 },
  { id:"b1b2-conn", label:"B1·B2 연결어", test:c=>c.lexique===6 && c.number>=548 && c.number<=581 },
  { id:"b1b2-noun", label:"B1·B2 명사", test:c=>c.lexique===6 && c.number>=582 && c.number<=1398 },
  { id:"b2", label:"B2 단어", test:c=>c.lexique===8 },
  { id:"expr", label:"관용 표현", test:c=>c.lexique===7 },
  { id:"all", label:"전체", test:()=>true },
];
const KEY = "tef-cycle-v1";
const $ = id => document.getElementById(id);
const shuffle = a => { a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
const uniq = a => [...new Set(a)];
const deckOf = id => DECKS.find(d=>d.id===id) || DECKS[0];
const poolOf = id => CARDS.filter(deckOf(id).test);
function lexShort(c){ return (c.lexique===0?"A0":c.lexique===7?"E7":"L"+c.lexique)+"-"+String(c.number).padStart(3,"0"); }
function totalBlocks(S){ const pool=poolOf(S.deck); return Math.max(1, Math.ceil((pool.length - S.start)/S.size)); }

let S = null;
function save(){ try{ localStorage.setItem(KEY, JSON.stringify(S)); }catch(e){} }
function load(){ try{ const o=JSON.parse(localStorage.getItem(KEY)||"null"); return (o && o.v===1 && BY_ID[o.queue?.[0]]!==undefined || (o && o.v===1)) ? o : null; }catch(e){ return null; } }

let selDeck = "b1b2-verb", selSize = 20;
function renderSetup(){
  const saved = load();
  const rb = $("resume-box");
  if(saved && saved.view!=="done"){
    const tb = totalBlocks(saved);
    rb.innerHTML = '<div class="resume"><b>이어서 할 사이클이 있어요</b><div style="margin-top:6px;font-size:14px">'
      + deckOf(saved.deck).label + ' · 블록 ' + Math.min(saved.blockIdx+1,tb) + '/' + tb + ' · ' + phaseLabel(saved.phase)
      + ' · 지금까지 ' + saved.stats.answered + '번 인출</div>'
      + '<button class="big-btn" id="resume-btn" style="margin-top:12px">이어서 계속하기</button>'
      + '<button class="ghost-btn danger" id="discard-btn">이 사이클 버리기</button></div>';
    $("resume-btn").onclick = ()=>{ S=saved; show(S.view==="intro"?"intro":"study"); if(S.view==="intro") renderIntro(); else renderCard(); };
    $("discard-btn").onclick = ()=>{ if(confirm("진행 중인 사이클을 버릴까요? (기존 단어장 진도는 그대로입니다)")){ localStorage.removeItem(KEY); renderSetup(); } };
  } else rb.innerHTML = "";
  $("deck-chips").innerHTML = DECKS.map(d=>'<button class="chip'+(d.id===selDeck?" on":"")+'" data-deck="'+d.id+'">'+d.label+' <small>'+poolOf(d.id).length+'개</small></button>').join("");
  document.querySelectorAll("[data-deck]").forEach(b=>b.onclick=()=>{ selDeck=b.dataset.deck; renderSetup(); });
  $("size-chips").innerHTML = [10,20,30].map(n=>'<button class="chip'+(n===selSize?" on":"")+'" data-size="'+n+'">'+n+'개씩</button>').join("");
  document.querySelectorAll("[data-size]").forEach(b=>b.onclick=()=>{ selSize=+b.dataset.size; renderSetup(); });
  $("deck-total").textContent = "이 덱은 총 " + poolOf(selDeck).length + "개입니다";
  show("setup");
}
function phaseLabel(p){ return {r1:"1회차", r2:"2회차 · 섞어서", r3:"틀린 것만", cum:"누적 복습", final:"마지막 복습"}[p] || p; }

function startCycle(){
  const pool = poolOf(selDeck);
  let start = parseInt($("start-input").value||"1",10);
  if(isNaN(start)||start<1) start=1;
  if(start>pool.length) start=pool.length;
  S = { v:1, deck:selDeck, size:selSize, start:start-1, blockIdx:0, blocksSinceCum:0,
        phase:"r1", view:"intro", queue:[], idx:0, blockIds:[], wrongR1n:0, wrongR2:[], pendingCum:[], stubborn:[],
        stats:{answered:0, correct:0}, intro:null };
  beginBlock("사이클 시작");
  save(); renderIntro(); show("intro");
}
function beginBlock(kicker){
  const pool = poolOf(S.deck);
  const from = S.start + S.blockIdx*S.size;
  S.blockIds = pool.slice(from, from+S.size).map(c=>c.id);
  S.phase="r1"; S.queue=S.blockIds.slice(); S.idx=0; S.wrongR1n=0; S.wrongR2=[];
  S.intro = { kicker:(kicker||"새 블록")+" · "+deckOf(S.deck).label,
    title:"블록 "+(S.blockIdx+1)+" / "+totalBlocks(S)+" — "+S.blockIds.length+"개",
    body:"먼저 순서대로 한 번 봅니다. 바로 안 떠오르면 틀린 걸로 넘기세요. 같은 블록을 섞어서 한 번 더 하고, 그때도 틀린 것만 마지막으로 봅니다.",
    btn:"1회차 시작" };
  S.view="intro";
}
function setIntro(kicker,title,body,btn){ S.intro={kicker,title,body,btn}; S.view="intro"; }
function nextBlockOrFinish(lastMsg){
  S.blockIdx++;
  const pool = poolOf(S.deck);
  if(S.start + S.blockIdx*S.size >= pool.length){
    if(S.stubborn.length){
      S.phase="final"; S.queue=shuffle(S.stubborn); S.idx=0;
      setIntro("범위 끝", "마지막 복습 — 끝까지 틀린 단어 "+S.stubborn.length+"개",
        "블록 3회차와 누적 복습에서도 틀렸던 단어들만 모았습니다. 이걸 끝내면 사이클이 완료됩니다.", "마지막 복습 시작");
    } else {
      S.view="done";
    }
  } else {
    beginBlock(lastMsg||"다음 블록");
  }
}
function finishBlock(){
  S.blocksSinceCum++;
  if(S.blocksSinceCum>=3){
    S.blocksSinceCum=0;
    if(S.pendingCum.length){
      S.phase="cum"; S.queue=shuffle(S.pendingCum); S.idx=0;
      const n=S.queue.length; S.pendingCum=[];
      setIntro("3블록 누적 복습", "틀렸던 단어 "+n+"개, 섞어서 한 번 더",
        "방금 지난 3개 블록에서 2회차에 틀렸던 단어들입니다. 여기서 또 틀리면 마지막 복습 목록으로 넘어갑니다.", "누적 복습 시작");
      return;
    }
  }
  nextBlockOrFinish("블록 완료");
}
function endPhase(){
  if(S.phase==="r1"){
    S.phase="r2"; S.queue=shuffle(S.blockIds); S.idx=0;
    setIntro("블록 "+(S.blockIdx+1)+" · 1회차 끝", "같은 "+S.blockIds.length+"개, 순서를 섞어서 다시",
      "1회차에서 틀린 단어는 "+S.wrongR1n+"개였어요. 이번에 맞히는지가 진짜입니다.", "2회차 시작");
  } else if(S.phase==="r2"){
    if(S.wrongR2.length){
      S.phase="r3"; S.queue=shuffle(S.wrongR2); S.idx=0;
      setIntro("블록 "+(S.blockIdx+1)+" · 2회차 끝", "틀린 "+S.wrongR2.length+"개만 한 번 더",
        "여기서 맞히면 이 블록은 졸업입니다. 또 틀리면 누적·마지막 복습에서 다시 만납니다.", "틀린 것만 시작");
    } else {
      setIntro("블록 "+(S.blockIdx+1)+" 완료", "2회차에서 전부 맞혔어요 🎉", "다음 블록으로 넘어갑니다.", "다음으로");
      S.phase="__blockdone";
    }
  } else if(S.phase==="r3"){
    finishBlock(); if(S.view!=="done" && S.phase!=="cum" && !S.intro) return;
    if(S.phase!=="cum" && S.view!=="done" && S.phase!=="final" && S.phase!=="r1"){ /* beginBlock set intro */ }
    if(S.phase==="r3") finishBlockGuard();
    return;
  } else if(S.phase==="cum"){
    nextBlockOrFinish("누적 복습 완료");
  } else if(S.phase==="final"){
    S.view="done";
  }
  if(S.phase==="__blockdone"){ /* intro shown; continue handled in intro button */ }
}
let blockDonePending=false;
function finishBlockGuard(){}

function renderIntro(){
  $("intro-kicker").textContent = S.intro?.kicker||"";
  $("intro-title").textContent = S.intro?.title||"";
  $("intro-body").textContent = S.intro?.body||"";
  $("intro-btn").textContent = S.intro?.btn||"시작";
}
$("intro-btn").onclick = ()=>{
  if(S.phase==="__blockdone"){ S.phase="r1"; finishBlock(); save(); if(S.view==="done"){ renderDone(); show("done"); } else { renderIntro(); show("intro"); } return; }
  S.view="study"; save(); show("study"); renderCard();
};
$("intro-setup").onclick = ()=>{ save(); renderSetup(); };
$("study-setup").onclick = ()=>{ save(); renderSetup(); };

function currentCard(){ return BY_ID[S.queue[S.idx]]; }
function renderCard(){
  const c = currentCard(); if(!c){ endPhase(); afterTransition(); return; }
  $("meta-left").textContent = S.phase==="cum" ? "누적 복습" : S.phase==="final" ? "마지막 복습" : ("블록 "+(S.blockIdx+1)+"/"+totalBlocks(S));
  $("meta-phase").textContent = phaseLabel(S.phase);
  $("meta-right").textContent = "누적 틀림 " + S.stubborn.length + "개";
  $("bar-fill").style.width = Math.round(S.idx/S.queue.length*100)+"%";
  $("card-id").textContent = lexShort(c);
  $("card-count").textContent = (S.idx+1)+" / "+S.queue.length;
  $("card-fr").textContent = c.fr;
  $("answer-box").classList.add("hidden");
  $("grade-row").classList.add("hidden");
  $("reveal-btn").classList.remove("hidden");
  window._revealed=false;
}
function afterTransition(){
  save();
  if(S.view==="done"){ renderDone(); show("done"); }
  else { renderIntro(); show("intro"); }
}
$("reveal-btn").onclick = ()=>{
  const c=currentCard(); if(!c) return;
  $("card-ko").textContent = c.ko||"";
  $("card-en").textContent = c.en||"";
  $("answer-box").classList.remove("hidden");
  $("grade-row").classList.remove("hidden");
  $("reveal-btn").classList.add("hidden");
  window._revealed=true;
};
function answer(ok){
  const c=currentCard(); if(!c || !window._revealed) return;
  S.stats.answered++; if(ok) S.stats.correct++;
  if(S.phase==="r1" && !ok) S.wrongR1n++;
  if(S.phase==="r2" && !ok){ S.wrongR2.push(c.id); if(!S.pendingCum.includes(c.id)) S.pendingCum.push(c.id); }
  if(S.phase==="r3" && !ok){ if(!S.stubborn.includes(c.id)) S.stubborn.push(c.id); }
  if(S.phase==="cum" && !ok){ if(!S.stubborn.includes(c.id)) S.stubborn.push(c.id); }
  S.idx++;
  if(S.idx < S.queue.length){ save(); renderCard(); }
  else { endPhase(); afterTransition(); }
}
$("wrong-btn").onclick = ()=>answer(false);
$("right-btn").onclick = ()=>answer(true);
document.addEventListener("keydown", e=>{
  if($("view-study").classList.contains("hidden")) return;
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
function cleanFr(t){ return cleanFrenchForSpeech(t); }
$("audio-btn").onclick = ()=>{
  const c=currentCard(); if(!c) return;
  const text=cleanFr(c.fr);
  const a=new Audio("audio/"+encodeURIComponent(c.id)+".mp3");
  let fell=false;
  const fallback=()=>{ if(fell) return; fell=true; try{ const u=new SpeechSynthesisUtterance(text); u.lang="fr-FR"; u.rate=.92; speechSynthesis.cancel(); speechSynthesis.speak(u);}catch(e){} };
  a.addEventListener("error", fallback, {once:true});
  const p=a.play(); if(p&&p.catch) p.catch(fallback);
};

function renderDone(){
  $("done-answered").textContent = S.stats.answered;
  $("done-rate").textContent = S.stats.answered? Math.round(S.stats.correct/S.stats.answered*100)+"%":"-";
  $("done-stubborn").textContent = S.stubborn.length;
  $("done-body").textContent = deckOf(S.deck).label+" 범위를 끝까지 돌렸습니다.";
  $("done-stubborn-list").innerHTML = S.stubborn.length
    ? "끝까지 틀린 단어: " + S.stubborn.map(id=>{ const c=BY_ID[id]; return c? (c.fr+" = "+c.ko):id; }).join(" · ")
    : "끝까지 남은 틀린 단어가 없습니다.";
}
$("done-again").onclick = ()=>{ localStorage.removeItem(KEY); S=null; renderSetup(); };
$("start-btn").onclick = startCycle;

function show(name){
  ["setup","intro","study","done"].forEach(v=>$("view-"+v).classList.toggle("hidden", v!==name));
  window.scrollTo(0,0);
}
renderSetup();
</script>
</body>
</html>
"""

out = template.replace("__CARDS_JSON__", json.dumps(cards, ensure_ascii=False))
(root / "cycle.html").write_text(out, encoding="utf-8")
print(f"cycle.html written: {len(out)} bytes")
