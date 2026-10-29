(function(){
"use strict";
const D=window.MTP_DATA, TASKS=D.tasks, BYID={}, KEY="mtp-progress-v1";
TASKS.forEach((t,i)=>{t._i=i;BYID[t.id]=t;});
const MODS={};D.modules.forEach(m=>MODS[m.id]=m);
const TRK={};D.tracks.forEach(t=>TRK[t.id]=t);
const GRADED=new Set(["pick","goodbad","missing","lesson"]);
function blank(){return{v:1,done:{},res:{},writes:{},checks:{},why:{},misses:{},last:null,sidebar:true};}
let S=load();
function load(){try{const s=JSON.parse(localStorage.getItem(KEY)||"null");if(s&&s.v===1)return Object.assign(blank(),s);}catch(e){}return blank();}
function save(){try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}}
let ui={sel:{},flags:{},revealed:{},review:false};
function resetUI(){ui={sel:{},flags:{},revealed:{},review:false};}
const $=s=>document.querySelector(s);
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function toast(m){const t=$("#toast");t.textContent=m;t.classList.add("show");clearTimeout(toast._t);toast._t=setTimeout(()=>t.classList.remove("show"),1600);}
function doneCount(list){return list.filter(t=>S.done[t.id]).length;}
function modTasks(mid){return TASKS.filter(t=>t.module===mid);}
function evLabel(e){return D.evidence_labels[e]||e;}
function isRevealed(t){return !!(ui.revealed[t.id]||S.res[t.id]&&S.res[t.id].revealed);}

/* ---------- mock ad renderer (SVG) ---------- */
function wrapText(txt,maxChars){const w=String(txt).split(/\s+/);const lines=[];let cur="";w.forEach(x=>{if((cur+" "+x).trim().length>maxChars){if(cur)lines.push(cur);cur=x;}else cur=(cur+" "+x).trim();});if(cur)lines.push(cur);return lines;}
function face(x,y,r,look){const skin="#e9b98f";const ex=look==="away"?r*0.28:0;
 return `<g><circle cx="${x}" cy="${y+r*1.9}" r="${r*1.5}" fill="#3d5a80"/><circle cx="${x}" cy="${y}" r="${r}" fill="${skin}"/><path d="M${x-r} ${y-r*0.2} Q${x} ${y-r*1.6} ${x+r} ${y-r*0.2} Q${x+r*0.6} ${y-r*0.8} ${x} ${y-r*0.75} Q${x-r*0.6} ${y-r*0.8} ${x-r} ${y-r*0.2}Z" fill="#4a2f1b"/><circle cx="${x-r*0.35+ex}" cy="${y}" r="${r*0.09}" fill="#222"/><circle cx="${x+r*0.35+ex}" cy="${y}" r="${r*0.09}" fill="#222"/><path d="M${x-r*0.3+ex} ${y+r*0.4} Q${x+ex} ${y+r*0.6} ${x+r*0.3+ex} ${y+r*0.4}" stroke="#7a3b2e" stroke-width="${r*0.07}" fill="none"/></g>`;}
function mockSvg(m){const W=360,H=360;let g=`<rect width="${W}" height="${H}" fill="${m.bg}"/>`;
 const f=m.focal||"one";
 if(f==="map"){for(let i=0;i<8;i++){g+=`<line x1="0" y1="${i*48}" x2="${W}" y2="${i*48+30}" stroke="#ffffff" stroke-width="10" opacity=".8"/>`;}
   g+=`<rect x="40" y="200" width="70" height="50" fill="#cfe3cf"/><rect x="230" y="60" width="90" height="60" fill="#cfe3cf"/>`;
   [[90,120,"1"],[180,170,"2"],[270,230,"3"]].forEach(p=>{g+=`<path d="M${p[0]} ${p[1]} l-14 -24 a16 16 0 1 1 28 0z" fill="#d93025"/><text x="${p[0]}" y="${p[1]-26}" font-size="13" fill="#fff" text-anchor="middle" font-weight="700">${p[2]}</text>`;});
   g+=`<circle cx="300" cy="300" r="34" fill="none" stroke="#1f5fbf" stroke-width="5"/><path d="M300 300 l-12 -20 a14 14 0 1 1 24 0z" fill="#7d7d7d"/><text x="300" y="276" font-size="15" text-anchor="middle" font-weight="700" fill="#1f5fbf">#7</text>`;}
 else if(f==="collage"){const cols=["#c9ada7","#9a8c98","#4a4e69","#f2cc8f","#81b29a","#e07a5f","#3d405b","#a8dadc","#e9c46a"];for(let i=0;i<9;i++){g+=`<rect x="${12+(i%3)*116}" y="${12+Math.floor(i/3)*116}" width="104" height="104" fill="${cols[i]}"/>`;}}
 else if(f==="split"){g+=`<rect x="0" y="0" width="180" height="${H}" fill="#f4a3a3"/><rect x="180" y="0" width="180" height="${H}" fill="#ffd0d0"/><ellipse cx="90" cy="230" rx="70" ry="90" fill="#e8a07a"/><ellipse cx="270" cy="230" rx="50" ry="90" fill="#e8a07a"/><text x="90" y="40" font-size="18" text-anchor="middle" fill="#7a0000" font-weight="700">BEFORE</text><text x="270" y="40" font-size="18" text-anchor="middle" fill="#7a0000" font-weight="700">AFTER</text>`;}
 else if(f==="logo"){g+=`<circle cx="180" cy="160" r="70" fill="none" stroke="${m.fg}" stroke-width="8"/>`;}
 else if(f==="gradient"){g=`<defs><linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6c5ce7"/><stop offset="1" stop-color="#00cec9"/></linearGradient></defs><rect width="${W}" height="${H}" fill="url(#gr)"/>`;}
 else if(f==="beach"){g+=`<rect y="200" width="${W}" height="160" fill="#f6d58e"/><rect width="${W}" height="200" fill="#8ecae6"/><circle cx="300" cy="60" r="30" fill="#ffd166"/>`;}
 else if(f==="arm"){g+=`<path d="M0 250 Q180 200 360 230 L360 300 Q180 280 0 320Z" fill="#e9b98f"/><circle cx="170" cy="250" r="16" fill="none" stroke="#1f5fbf" stroke-width="4"/>`;}
 if(m.face){g+=face(m.overlay?250:180,m.overlay?150:150,m.overlay?52:70,m.face);}
 const n=m.clutter||0;if(n&&f!=="collage"){const toks=(m.badge||"★ NEW % SALE TOP HOT").split(/\s+/);for(let i=0;i<n;i++){const x=40+((i*97)%280),y=40+((i*61)%260);g+=`<circle cx="${x}" cy="${y}" r="30" fill="${["#ffbe0b","#fb5607","#ff006e","#8338ec","#3a86ff","#06d6a0"][i%6]}"/><text x="${x}" y="${y+5}" font-size="13" text-anchor="middle" fill="#fff" font-weight="700">${esc(toks[i%toks.length])}</text>`;}}
 if(m.overlay){const sz={xs:13,s:20,m:28,l:38}[m.size||"m"]||28;const mc=Math.floor((m.face?200:320)/(sz*0.55));const lines=wrapText(m.overlay,mc);const lh=sz*1.2;const y0=m.size==="xs"?24:Math.max(40,H-40-lines.length*lh);
   const x=m.face?24:W/2,anchor=m.face?"start":"middle";
   if(m.contrast!=="low"&&m.size!=="xs"){g+=`<rect x="${m.face?12:16}" y="${y0-sz}" width="${m.face?210:W-32}" height="${lines.length*lh+sz*0.5}" rx="8" fill="${m.bg}" opacity=".55"/>`;}
   lines.forEach((l,i)=>{g+=`<text x="${x}" y="${y0+i*lh}" font-size="${sz}" font-weight="700" fill="${m.fg}" text-anchor="${anchor}" font-family="Arial,sans-serif">${esc(l)}</text>`;});}
 return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Mockup ad image">${g}</svg>`;}
function mockAd(m,primary){return `<div class="mock"><div class="mh"><div class="av"></div><div><div class="pn">${esc(m.page)}</div><div class="sp">Sponsored · mockup</div></div></div>${primary?`<div class="pt">${esc(primary)}</div>`:""}${mockSvg(m)}<div class="mf"><div class="hl">${esc(m.headline||"")}</div><div class="cta">${esc(m.cta||"Learn more")}</div></div></div><div class="mocklabel">MOCKUP — made for practice, not a real ad</div>`;}

/* ---------- layout / outline ---------- */
function renderOutline(curId){let h="";D.tracks.forEach(tr=>{h+=`<div class="ol-track">Track ${tr.id} · ${esc(tr.title)}</div>`;
  D.modules.filter(m=>m.track===tr.id).forEach(m=>{const ts=modTasks(m.id),dc=doneCount(ts);const open=curId&&BYID[curId]&&BYID[curId].module===m.id;
   h+=`<details class="ol-mod${dc===ts.length?" complete":""}" data-mod="${m.id}"${open?" open":""}><summary><span class="mt">${m.id} ${esc(m.title)}</span><span class="cnt">${dc}/${ts.length}</span></summary><ul class="ol-tasks">`;
   ts.forEach((t,k)=>{h+=`<li><a href="#/t/${t.id}" data-id="${t.id}" class="${S.done[t.id]?"done ":""}${t.id===curId?"cur":""}"><span class="ck">${S.done[t.id]?"✓":""}</span><span class="tt">${k+1}. ${esc(t.title)}</span></a></li>`;});
   h+=`</ul></details>`;});});
 $("#outline").innerHTML=h;const cur=$("#outline a.cur");if(cur)cur.scrollIntoView({block:"nearest"});}
function updateTop(){const d=doneCount(TASKS);$("#topbarFill").style.width=(100*d/TASKS.length)+"%";$("#topbarText").textContent=`${d}/${TASKS.length}`;$("#missCount").textContent=Object.keys(S.misses).length;}
function applySidebar(){document.body.classList.toggle("nosidebar",!S.sidebar);}

/* ---------- stats ---------- */
function stats(){const out={all:[0,0]};TASKS.forEach(t=>{if(t.type!=="pick")return;const r=S.res[t.id];if(!r||r.correct==null)return;const e=t.evidence_type;out[e]=out[e]||[0,0];out[e][1]++;out.all[1]++;if(r.correct){out[e][0]++;out.all[0]++;}});return out;}
function pct(a){return a[1]?Math.round(100*a[0]/a[1])+"%":"–";}
function nextUndone(from){for(let i=from;i<TASKS.length;i++)if(!S.done[TASKS[i].id])return TASKS[i];for(let i=0;i<from;i++)if(!S.done[TASKS[i].id])return TASKS[i];return null;}

/* ---------- views ---------- */
function viewHome(){const d=doneCount(TASKS),st=stats();const cont=S.last&&BYID[S.last]&&!S.done[S.last]?BYID[S.last]:nextUndone(S.last&&BYID[S.last]?BYID[S.last]._i:0);
 let h=`<div class="wrap"><h1>Marketing Taste Playground</h1><p class="sub">Train your eye like a scientist: pick the winner, see what's missing, then write it yourself. Mostly Meta ads, then cold email. Every real example links to its source and says what kind of evidence it is.</p>
 <div class="card" style="margin:16px 0"><div style="display:flex;justify-content:space-between;align-items:baseline"><strong>Overall progress</strong><span id="homeProgText">${d} of ${TASKS.length} tasks done (${Math.round(100*d/TASKS.length)}%)</span></div><div class="bar big" style="margin:10px 0 14px"><div style="width:${100*d/TASKS.length}%"></div></div>
 ${cont?`<a class="btn big" id="btnContinue" href="#/t/${cont.id}">▶ ${d?"Continue where I left off":"Start Track 1"}</a> <span class="sub" style="margin-left:10px">${esc(cont.module)} · ${esc(cont.title)}</span>`:`<strong>All tasks done! 🎉</strong>`}</div>
 <div class="cards"><div class="card"><div class="sub">Pick-the-winner accuracy</div><div class="stat" id="accAll">${pct(st.all)}</div><div class="sub">${st.all[0]} of ${st.all[1]} correct</div></div>
 <div class="card"><div class="sub">By evidence type</div><table class="stats"><tr><td>Proven tests</td><td>${pct(st.proven_test||[0,0])}</td></tr><tr><td>Case studies / benchmarks</td><td>${pct(st.case_study||[0,0])}</td></tr><tr><td>Long-running</td><td>${pct(st.long_running||[0,0])}</td></tr><tr><td>Teaching pairs</td><td>${pct(st.teaching||[0,0])}</td></tr></table></div>
 <div class="card"><div class="sub">Review queue</div><div class="stat">${Object.keys(S.misses).length}</div><a href="#/review">Review my misses →</a></div></div>
 <h2>Learning path</h2>`;
 D.tracks.forEach(tr=>{const tts=TASKS.filter(t=>t.track===tr.id);h+=`<div class="trk"><h3>Track ${tr.id}: ${esc(tr.title)} <span class="sub" style="font-weight:400">· ${doneCount(tts)}/${tts.length}</span></h3>`;
  D.modules.filter(m=>m.track===tr.id).forEach(m=>{const ts=modTasks(m.id),dc=doneCount(ts),first=ts.find(t=>!S.done[t.id])||ts[0];
   h+=`<div class="modrow" data-mod="${m.id}"><span class="ck">${dc===ts.length?"✓":""}</span><a href="#/t/${first.id}">${m.id} ${esc(m.title)}</a><div class="bar mbar"><div style="width:${100*dc/ts.length}%"></div></div><span class="cnt">${dc}/${ts.length}</span></div>`;});h+=`</div>`;});
 h+=`<h2>Evidence labels</h2><ul class="legend">${Object.keys(D.evidence_labels).map(k=>`<li><span class="ev ${k}">${esc(D.evidence_labels[k])}</span></li>`).join("")}</ul>
 <p class="sub">Honesty notes: Meta's Ad Library shows no performance data for non-political ads, so "long-running" is only a proxy. Vendor benchmarks (Gong, Boomerang, Belkins, Woodpecker) are correlational. Upworthy "why it won" notes are our interpretation; the data only shows which headline won.</p>
 <h2>Keyboard</h2><p><span class="kbd">1</span>/<span class="kbd">2</span> pick · <span class="kbd">Enter</span> reveal / next · <span class="kbd">←</span>/<span class="kbd">→</span> back / next · <span class="kbd">M</span> mark done · <span class="kbd">F</span> focus mode · <span class="kbd">Esc</span> exit focus · <span class="kbd">S</span> toggle outline · <span class="kbd">Ctrl</span>+<span class="kbd">Enter</span> reveal while typing</p>
 <h2>Your data</h2><p class="sub">Progress and written answers are saved in this browser (localStorage).</p>
 <button class="btn ghost" id="btnExport">⬇ Export progress JSON</button> <label class="btn ghost" style="display:inline-block">⬆ Import JSON<input type="file" id="fileImport" accept="application/json,.json" hidden></label> <button class="btn ghost" id="btnReset" style="border-color:var(--bad);color:var(--bad)">Reset all progress</button>
 <p class="sub" style="margin-top:30px">Sources for every example: see each task's source link, or <a href="https://github.com/oskaraxels/marketing-playground/blob/main/SOURCES.md">SOURCES.md</a>.</p></div>`;
 $("#main").innerHTML=h;renderOutline(null);
 $("#btnExport").onclick=exportJSON;$("#fileImport").onchange=importJSON;$("#btnReset").onclick=()=>{if(confirm("Reset ALL progress and written answers? This cannot be undone.")){S=blank();resetUI();save();toast("Progress reset");route();}};}
function viewReview(){const ids=Object.keys(S.misses).filter(id=>BYID[id]);let h=`<div class="wrap"><h1>Review my misses</h1>`;
 if(!ids.length)h+=`<p>No misses in the queue. Tasks you get wrong are added here automatically; answer them right to clear them.</p><a class="btn" href="#/">Back home</a>`;
 else{h+=`<p class="sub">${ids.length} task(s) you got wrong. Each opens fresh so you can answer again. A correct answer removes it from the queue.</p><a class="btn big" id="btnStartReview" href="#/t/${ids[0]}?review">▶ Start review</a><ol class="reviewlist">${ids.map(id=>`<li><a href="#/t/${id}?review">${esc(BYID[id].module)} · ${esc(BYID[id].title)}</a></li>`).join("")}</ol>`;}
 $("#main").innerHTML=h+`</div>`;renderOutline(null);}

function principlesHTML(t){return `<div class="chips">${t.principles.map(p=>{const P=D.principles[p];return P?`<a class="chip" href="${esc(P.source_url)}" target="_blank" rel="noopener" title="${esc(P.source_name)}">${esc(P.label)}</a>`:"";}).join("")}</div>`;}
function sourceHTML(t){return `<div class="src">Source: <a class="srclink" href="${esc(t.source_url)}" target="_blank" rel="noopener">${esc(t.source_name)}</a>${t.field_url?` · <a class="srclink" href="${esc(t.field_url)}" target="_blank" rel="noopener">Open this Ad Library search</a>`:""}</div>`;}
function evHTML(t){return `<span class="ev ${t.evidence_type}">${esc(evLabel(t.evidence_type))}</span>`;}
function optInner(o){return `<span class="txt">${esc(o.text)}</span>${o.mock?mockAd(o.mock,""):""}`;}

function viewTask(id,review){const t=BYID[id];if(!t){location.hash="#/";return;}
 if(review&&!ui.reviewOpened){ui.reviewOpened={};}
 if(review&&ui.reviewOpened&&!ui.reviewOpened[id]){ui.reviewOpened[id]=1;delete ui.revealed[id];delete ui.sel[id];delete ui.flags[id];if(S.res[id])S.res[id].revealed=false;}
 ui.review=!!review;S.last=id;save();
 const ms=modTasks(t.module),k=ms.indexOf(t)+1,rev=isRevealed(t),res=S.res[id]||{};
 let h=`<div class="wrap" data-task="${t.id}" data-type="${t.type}"><div class="crumbs">Track ${t.track} · ${esc(MODS[t.module].id)} ${esc(MODS[t.module].title)} · task ${k} of ${ms.length}${review?" · <strong>Review mode</strong>":""}</div>${evHTML(t)}`;
 const sel=ui.sel[id]!=null?ui.sel[id]:(res.choice!=null?res.choice:null);
 if(t.type==="pick"){h+=`<div class="prompt">${esc(t.prompt)}</div>${t.context?`<div class="context">${esc(t.context)}</div>`:""}<div class="opts">${t.options.map((o,i)=>{let c="opt";if(sel===i)c+=" sel";if(rev)c+=i===t.answer?" win":" lose";return `<button class="${c}" data-opt="${i}"><span class="key">${i+1}</span>${optInner(o)}${rev?`<span class="tag">${i===t.answer?(t.evidence_type==="teaching"?"✓ Stronger (teaching answer)":"✓ WINNER"):"Lost"}</span>`:""}</button>`;}).join("")}</div>
   <label class="why" for="why">Why do you think so? (optional — saved)</label><textarea id="why" placeholder="Type your reasoning before revealing…">${esc(S.why[id]||"")}</textarea>`;}
 else if(t.type==="goodbad"){h+=`<div class="prompt">${esc(t.prompt)}</div><div class="artifact">${esc(t.artifact)}</div>${t.mock?mockAd(t.mock,""):""}<div class="gbrow">${["good","bad"].map((v,i)=>{let c="opt";if(sel===i)c+=" sel";if(rev)c+=v===t.answer?" win":" lose";return `<button class="${c}" data-opt="${i}"><span class="key">${i+1}</span><span class="txt">${v==="good"?"👍 Good":"👎 Bad"}</span>${rev&&v===t.answer?`<span class="tag">✓ Expert rating</span>`:""}</button>`;}).join("")}</div>
   <label class="why" for="why">Why? (optional)</label><textarea id="why">${esc(S.why[id]||"")}</textarea>`;}
 else if(t.type==="missing"){const fl=ui.flags[id]||res.flags||[];h+=`<div class="prompt">${esc(t.prompt)}</div><div class="artifact">${esc(t.artifact)}</div>${t.mock?mockAd(t.mock,""):""}<div class="flags">${Object.keys(D.flags).map(f=>{let c="";if(rev){const exp=t.answer.includes(f),ch=fl.includes(f);c=exp&&ch?"hit":exp?"miss":ch?"extra":"";}return `<label class="${c}"><input type="checkbox" data-flag="${f}" ${fl.includes(f)?"checked":""} ${rev?"disabled":""}> <span>${esc(D.flags[f])}${rev&&t.answer.includes(f)?" <strong>✓ expert</strong>":""}</span></label>`;}).join("")}</div>`;}
 else if(t.type==="write"){h+=`<div class="prompt">${esc(t.prompt)}</div><label class="why" for="wtext">Your answer (auto-saved)</label><textarea id="wtext" class="big" placeholder="Write your version here first. Then reveal the model answers.">${esc(S.writes[id]||"")}</textarea>`;}
 else if(t.type==="teardown"){h+=`<div class="prompt">${esc(t.prompt)}</div>${t.intro?`<div class="context">${esc(t.intro)}</div>`:""}${t.metric?`<div class="metric"><strong>Reported result:</strong> ${esc(t.metric)}</div>`:""}<ol class="parts">${t.parts.map(p=>`<li><strong>${esc(p.label)}:</strong> ${esc(p.text)}${rev?`<span class="note">→ ${esc(p.note)}</span>`:""}</li>`).join("")}</ol><label class="why" for="why">Before revealing: which part does the heavy lifting, and why? (optional)</label><textarea id="why">${esc(S.why[id]||"")}</textarea>`;}
 else if(t.type==="lesson"){h+=`<div class="prompt">${esc(t.prompt)}</div><div class="lessonbody">${esc(t.body)}</div><div class="example"><strong>Real example:</strong> ${esc(t.example)}</div><h2 style="font-size:1.05em">Mini drill</h2><div class="prompt" style="font-size:1em">${esc(t.drill.q)}</div><div class="opts">${t.drill.options.map((o,i)=>{let c="opt";if(sel===i)c+=" sel";if(rev)c+=i===t.drill.answer?" win":" lose";return `<button class="${c}" data-opt="${i}"><span class="key">${i+1}</span><span class="txt">${esc(o)}</span>${rev&&i===t.drill.answer?`<span class="tag">✓ Better</span>`:""}</button>`;}).join("")}</div>`;}
 h+=`<div id="revealArea">${rev?revealHTML(t):`<button class="btn big" id="btnReveal">Reveal <span class="kbd" style="color:#16181d">Enter</span></button>`}</div>`;
 const pos=t._i;h+=`<div class="navrow"><button class="btn ghost" id="btnBack" ${pos===0&&!review?"disabled":""}>← Back</button><button class="donebtn${S.done[id]?" on":""}" id="btnDone">${S.done[id]?"☑ Done":"☐ Mark done"}</button><span class="spacer"></span><button class="btn" id="btnNext">Next →</button></div><div class="hint">1/2 pick · Enter reveal/next · ←/→ navigate · M mark done · F focus · Esc exit focus · S outline</div></div>`;
 $("#main").innerHTML=h;renderOutline(id);
 $("#focusInfo").textContent=`${t.module} · task ${k}/${ms.length} · ${doneCount(TASKS)}/${TASKS.length} done`;
 document.querySelectorAll("[data-opt]").forEach(b=>b.onclick=()=>choose(t,+b.dataset.opt));
 document.querySelectorAll("[data-flag]").forEach(c=>c.onchange=()=>{const a=new Set(ui.flags[id]||[]);c.checked?a.add(c.dataset.flag):a.delete(c.dataset.flag);ui.flags[id]=[...a];});
 const why=$("#why");if(why)why.oninput=()=>{S.why[id]=why.value;save();};
 const wt=$("#wtext");if(wt)wt.oninput=()=>{S.writes[id]=wt.value;save();};
 const rb=$("#btnReveal");if(rb)rb.onclick=()=>reveal(t);
 bindReveal(t);
 $("#btnBack").onclick=()=>go(-1);$("#btnNext").onclick=()=>go(1);$("#btnDone").onclick=()=>toggleDone(id);
 $("#main").focus({preventScroll:true});window.scrollTo(0,0);}
function bindReveal(t){document.querySelectorAll("[data-check]").forEach(c=>c.onchange=()=>{const arr=S.checks[t.id]||[];arr[+c.dataset.check]=c.checked;S.checks[t.id]=arr;save();const sc=$("#selfScore");if(sc)sc.textContent=arr.filter(Boolean).length;});
 const tr=$("#btnRetry");if(tr)tr.onclick=()=>{delete ui.revealed[t.id];delete ui.sel[t.id];delete ui.flags[t.id];if(S.res[t.id])S.res[t.id]={};save();viewTask(t.id,ui.review);};}
function revealHTML(t){const r=S.res[t.id]||{};let h=`<div class="reveal" id="revealBox">`;
 if(GRADED.has(t.type)&&r.correct!=null)h+=`<div class="result ${r.correct?"ok":"no"}">${r.correct?"✓ Correct — nice eye.":"✗ Not this time — added to your review queue."}${t.type==="missing"&&r.score?` (${esc(r.score)})`:""}</div>`;
 if(t.type==="lesson")h+=`<p>${esc(t.drill.why)}</p>`;
 if(t.metric&&t.type!=="teardown")h+=`<div class="metric"><strong>${t.evidence_type==="teaching"?"Note":"Result / metric"}:</strong> ${esc(t.metric)}</div>`;
 if(t.evidence_type==="teaching")h+=`<div class="metric"><strong>Teaching example</strong> (written for practice, not real performance data). The "answer" is the expert call based on the cited principle.</div>`;
 if(t.type!=="lesson")h+=`<p><strong>Why:</strong> ${esc(t.explanation)}</p>`;
 if(t.type==="missing"&&t.answer)h+=`<p><strong>Expert diagnosis:</strong> ${t.answer.map(f=>esc(D.flags[f])).join(" · ")}</p>`;
 if(t.type==="write"){h+=`<h3>Model answers</h3>${t.model_answers.map((m,i)=>`<div class="model"><strong>Model ${i+1}${t.evidence_type==="teaching"?" (teaching example)":""}:</strong>\n${esc(m)}</div>`).join("")}<h3>Thought process, step by step</h3><ol class="steps">${t.steps.map(s=>`<li>${esc(s)}</li>`).join("")}</ol><h3>Self-score checklist (<span id="selfScore">${(S.checks[t.id]||[]).filter(Boolean).length}</span>/${t.checklist.length})</h3><div class="checklist">${t.checklist.map((c,i)=>`<label><input type="checkbox" data-check="${i}" ${(S.checks[t.id]||[])[i]?"checked":""}> ${esc(c)}</label>`).join("")}</div>`;}
 h+=`<div><strong>Principles:</strong></div>${principlesHTML(t)}${sourceHTML(t)}`;
 if(GRADED.has(t.type))h+=`<p style="margin-top:12px"><button class="btn ghost small" id="btnRetry">↺ Try again</button></p>`;
 return h+`</div>`;}
function choose(t,i){if(isRevealed(t))return;ui.sel[t.id]=i;document.querySelectorAll("[data-opt]").forEach(b=>b.classList.toggle("sel",+b.dataset.opt===i));}
function reveal(t){const id=t.id;if(isRevealed(t))return;
 let correct=null,extra={};
 if(t.type==="pick"||t.type==="goodbad"||t.type==="lesson"){const s=ui.sel[id];if(s==null){toast("Pick an option first (1 or 2)");return;}
   const ans=t.type==="goodbad"?(t.answer==="good"?0:1):t.type==="lesson"?t.drill.answer:t.answer;correct=s===ans;extra.choice=s;}
 if(t.type==="missing"){const fl=ui.flags[id]||[];const exp=t.answer;const hit=fl.filter(f=>exp.includes(f)).length,wrong=fl.filter(f=>!exp.includes(f)).length;correct=hit>=Math.ceil(exp.length/2)&&wrong<=1;extra.flags=fl;extra.score=`${hit}/${exp.length} found, ${wrong} extra`;}
 S.res[id]=Object.assign({revealed:true,at:Date.now()},extra,correct!=null?{correct}:{});
 if(correct===false)S.misses[id]=true;else if(correct===true)delete S.misses[id];
 ui.revealed[id]=true;S.done[id]=true;save();updateTop();viewTask(id,ui.review);
 const rb=$("#revealBox");if(rb)rb.scrollIntoView({block:"nearest"});}
function toggleDone(id){if(S.done[id])delete S.done[id];else S.done[id]=true;save();updateTop();const b=$("#btnDone");if(b){b.classList.toggle("on",!!S.done[id]);b.textContent=S.done[id]?"☑ Done":"☐ Mark done";}renderOutline(id);toast(S.done[id]?"Marked done ✓":"Unmarked");}
function curTask(){const m=location.hash.match(/^#\/t\/([^?]+)/);return m?BYID[m[1]]:null;}
function go(dir){const t=curTask();if(!t)return;
 if(ui.review){const ids=Object.keys(S.misses).filter(x=>BYID[x]&&x!==t.id);if(dir>0){if(ids.length)location.hash=`#/t/${ids[0]}?review`;else{toast("Review queue empty 🎉");location.hash="#/review";}}else history.back();return;}
 const j=t._i+dir;if(j>=0&&j<TASKS.length)location.hash=`#/t/${TASKS[j].id}`;else if(j>=TASKS.length){toast("That was the last task!");location.hash="#/";}}
/* focus */
function setFocus(on){document.body.classList.toggle("focus",on);if(on){const el=document.documentElement;if(el.requestFullscreen&&!document.fullscreenElement){el.requestFullscreen().catch(()=>{});}}else if(document.fullscreenElement&&document.exitFullscreen){document.exitFullscreen().catch(()=>{});}}
document.addEventListener("fullscreenchange",()=>{if(!document.fullscreenElement&&document.body.classList.contains("focus"))document.body.classList.remove("focus");});
/* export/import */
function exportJSON(){const blob=new Blob([JSON.stringify({app:"marketing-taste-playground",exported:new Date().toISOString(),state:S},null,1)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="marketing-playground-progress.json";document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);toast("Exported");}
function importJSON(e){const f=e.target.files[0];if(!f)return;const rd=new FileReader();rd.onload=()=>{try{const j=JSON.parse(rd.result);const st=j.state||j;if(st.v!==1||typeof st.done!=="object")throw new Error("bad");S=Object.assign(blank(),st);resetUI();save();toast("Progress imported");route();}catch(err){toast("Could not import: not a valid progress file");}};rd.readAsText(f);}
/* keyboard */
document.addEventListener("keydown",e=>{const tag=(e.target.tagName||"").toLowerCase();const typing=tag==="textarea"||tag==="input";
 if(e.key==="Escape"){if(document.body.classList.contains("focus")){setFocus(false);e.preventDefault();}return;}
 const t=curTask();
 if(typing){if(e.key==="Enter"&&(e.ctrlKey||e.metaKey)&&t){e.preventDefault();isRevealed(t)?go(1):reveal(t);}return;}
 if(e.ctrlKey||e.metaKey||e.altKey)return;
 if(e.key==="s"||e.key==="S"){S.sidebar=!S.sidebar;save();applySidebar();return;}
 if(e.key==="f"||e.key==="F"){setFocus(!document.body.classList.contains("focus"));return;}
 if(!t)return;
 if(/^[1-9]$/.test(e.key)){choose(t,+e.key-1);e.preventDefault();return;}
 if(e.key==="Enter"){if(tag==="button"||tag==="a"){if(e.target.id!=="btnReveal"&&!e.target.dataset.opt)return;}e.preventDefault();isRevealed(t)?go(1):reveal(t);return;}
 if(e.key==="ArrowRight"){go(1);return;} if(e.key==="ArrowLeft"){go(-1);return;}
 if(e.key==="m"||e.key==="M"){toggleDone(t.id);return;}});
/* router */
function route(){updateTop();applySidebar();const h=location.hash||"#/";const m=h.match(/^#\/t\/([^?]+)(\?review)?/);
 if(m)viewTask(m[1],!!m[2]);else if(h.startsWith("#/review"))viewReview();else viewHome();}
window.addEventListener("hashchange",route);
$("#btnSidebar").onclick=()=>{S.sidebar=!S.sidebar;save();applySidebar();};
$("#btnFocus").onclick=()=>setFocus(true);$("#btnExitFocus").onclick=()=>setFocus(false);
window.MTP={state:()=>S,tasks:TASKS};
route();
})();
