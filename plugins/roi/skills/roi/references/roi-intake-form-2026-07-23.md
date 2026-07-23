html<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Use Case ROI Calculator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
--bg:#F2ECDC; --surface:#FBF8F0; --surface-2:#EDE5CE; --surface-3:#E5DBBF;
--border:#DFD3B4; --border-strong:#C7B990;
--text:#2A2519; --text-dim:#6E6650; --text-faint:#9C9377;
--accent:#2E4159; --accent-dim:#E1E6E7; --accent-text:#233245;
--warn:#A8631A; --warn-dim:#F3E3C4;
--danger:#A6362A; --danger-dim:#F2DED7;
--mono:'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
--display:'Bricolage Grotesque', sans-serif;
--body:'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--radius:10px;
}
\*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
background:var(--bg); color:var(--text); font-family:var(--body);
line-height:1.6; -webkit-font-smoothing:antialiased;
}
::selection{background:var(--accent-dim); color:var(--accent-text);}
a{color:var(--accent-text);}
h1,h2,h3{font-family:var(--display); font-weight:600; margin:0;}
.num{font-family:var(--mono); font-variant-numeric:tabular-nums;}
/\* ---- header ---- \*/
header{
border-bottom:1px solid var(--border); padding:26px 36px; background:var(--surface);
display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px;
}
.brand{display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;}
.brand h1{font-size:20px; letter-spacing:-0.01em;}
.brand .tag{font-size:12.5px; color:var(--text-faint); font-family:var(--mono);}
.assumptions-link{
font-size:13px; color:var(--text-dim); background:none; border:1px solid var(--border);
border-radius:var(--radius); padding:16px; cursor:pointer; font-family:var(--body);
}
.assumptions-link:hover{border-color:var(--border-strong); color:var(--text);}
/\* ---- layout ---- \*/
.app{max-width:840px; margin:0 auto; padding:48px 36px 110px;}
.wizard{display:grid; grid-template-columns:200px 1fr; gap:48px;}
@media (max-width:760px){ .wizard{grid-template-columns:1fr;} .rail{display:none;} }
.rail{position:sticky; top:36px; align-self:start;}
.rail-item{
display:flex; align-items:center; gap:10px; padding:11px 0 11px 16px;
border-left:2px solid var(--border); font-size:13.5px; color:var(--text-faint);
transition:color .15s, border-color .15s;
}
.rail-item.active{border-left-color:var(--accent); color:var(--text); font-weight:500;}
.rail-item.done{border-left-color:var(--border-strong); color:var(--text-dim);}
.rail-check{width:14px; height:14px; flex:none;}
.card{background:var(--surface); border:1px solid var(--border); border-radius:18px; padding:24px;
box-shadow:0 1px 2px rgba(42,37,25,0.04), 0 6px 20px rgba(42,37,25,0.05);}
.eyebrow{font-family:var(--mono); font-size:12px; color:var(--accent-text); letter-spacing:.06em; text-transform:uppercase; margin-bottom:14px;}
.question{font-size:23px; font-family:var(--display); font-weight:600; margin-bottom:10px; letter-spacing:-0.01em; line-height:1.3;}
.helper{font-size:14.5px; color:var(--text-dim); margin-bottom:30px; max-width:52ch; line-height:1.65;}
label.field-label{display:block; font-size:13px; color:var(--text-dim); margin-bottom:8px; font-weight:500;}
input[type=text], input[type=number], textarea, select{
width:100%; background:var(--surface-2); border:1px solid var(--border); color:var(--text);
border-radius:8px; padding:16px; font-size:14.5px; font-family:var(--body);
}
input[type=number]{font-family:var(--mono);}
input:focus, textarea:focus, select:focus{outline:none; border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-dim);}
textarea{resize:vertical; min-height:68px;}
.field{margin-bottom:22px;}
.field-hint{font-size:12px; color:var(--text-faint); margin-top:6px; line-height:1.5;}
.field-row{display:grid; grid-template-columns:1fr 1fr; gap:20px;}
@media (max-width:520px){ .field-row{grid-template-columns:1fr;} }
.choice-grid{display:grid; gap:12px; margin-bottom:12px;}
.choice{
border:1px solid var(--border); border-radius:12px; padding:24px; cursor:pointer;
display:flex; flex-direction:column; gap:4px; transition:border-color .12s, background .12s, box-shadow .12s;
background:var(--surface);
}
.choice:hover{border-color:var(--border-strong); box-shadow:0 1px 4px rgba(42,37,25,0.06);}
.choice.selected{border-color:var(--accent); background:var(--accent-dim);}
.choice-title{font-size:14.5px; font-weight:500;}
.choice-desc{font-size:13px; color:var(--text-dim); line-height:1.5;}
.reason-box{
margin-top:10px; border-left:2px solid var(--warn); padding:24px; background:var(--warn-dim);
border-radius:0 8px 8px 0;
}
.reason-box .field-label{color:var(--warn);}
.required-tag{color:var(--danger); font-size:12px; font-family:var(--mono); margin-left:6px;}
.toggle-row{display:flex; align-items:center; gap:10px; font-size:14px; color:var(--text-dim); margin-bottom:16px;}
.toggle-row input{width:auto;}
.nav-row{display:flex; justify-content:space-between; align-items:center; margin-top:34px;}
button.btn{
font-family:var(--body); font-size:14px; font-weight:500; border-radius:8px; padding:16px;
cursor:pointer; border:1px solid var(--border-strong); background:var(--surface-2); color:var(--text);
}
button.btn:hover{border-color:var(--text-faint);}
button.btn.primary{background:var(--accent); border-color:var(--accent); color:#FFFFFF;}
button.btn.primary:hover{background:var(--accent-text);}
button.btn.ghost{background:none; border-color:transparent; color:var(--text-dim);}
button.btn.ghost:hover{color:var(--text);}
button.btn:disabled{opacity:.4; cursor:not-allowed;}
/\* ---- results ---- \*/
.verdict-banner{
border-radius:14px; padding:24px; margin-bottom:32px; display:flex; gap:16px; align-items:flex-start;
}
.verdict-banner.ok{background:var(--accent-dim); border:1px solid rgba(46,65,89,0.25);}
.verdict-banner.warn{background:var(--warn-dim); border:1px solid rgba(168,99,26,0.3);}
.verdict-banner .vtitle{font-family:var(--display); font-weight:600; font-size:16px; margin-bottom:6px;}
.verdict-banner.ok .vtitle{color:var(--accent-text);}
.verdict-banner.warn .vtitle{color:var(--warn);}
.verdict-banner p{margin:0; font-size:13.5px; color:var(--text-dim); line-height:1.65;}
.ledger{
display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:var(--border);
border:1px solid var(--border); border-radius:14px; overflow:hidden; margin-bottom:32px;
}
@media (max-width:640px){ .ledger{grid-template-columns:1fr; overflow-x:visible;} }
.ledger-col{background:var(--surface); padding:24px;}
.ledger-col.expected{background:var(--surface-3);}
.ledger-label{font-family:var(--mono); font-size:11.5px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.06em; margin-bottom:16px;}
.ledger-row{display:flex; justify-content:space-between; font-size:13px; padding:7px 0; border-bottom:1px solid var(--border);}
.ledger-row:last-child{border-bottom:none;}
.ledger-row .k{color:var(--text-dim);}
.ledger-row .v{font-family:var(--mono); font-variant-numeric:tabular-nums;}
.ledger-headline{font-family:var(--mono); font-size:27px; margin:2px 0 18px; letter-spacing:-0.01em;}
.ledger-headline.neg{color:var(--danger);}
.ledger-headline.pos{color:var(--accent-text);}
.caret{color:var(--text-faint); margin-right:6px;}
.stat-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:32px;}
@media (max-width:640px){ .stat-grid{grid-template-columns:repeat(2,1fr);} }
.stat-card{background:var(--surface-2); border-radius:12px; padding:16px 18px;}
.stat-card .slabel{font-size:12px; color:var(--text-faint); margin-bottom:8px;}
.stat-card .sval{font-family:var(--mono); font-size:19px;}
.badge{display:inline-block; font-size:11.5px; font-family:var(--mono); padding:4px 10px; border-radius:5px; text-transform:uppercase; letter-spacing:.03em;}
.badge.high{background:var(--accent-dim); color:var(--accent-text);}
.badge.medium{background:var(--warn-dim); color:var(--warn);}
.badge.low{background:var(--danger-dim); color:var(--danger);}
.section-title{font-family:var(--display); font-size:15.5px; font-weight:600; margin:40px 0 16px;}
table.report-table{width:100%; border-collapse:collapse; font-size:13.5px;}
table.report-table th{text-align:left; color:var(--text-faint); font-weight:500; font-size:12px; text-transform:uppercase; letter-spacing:.03em; padding:10px 12px; border-bottom:1px solid var(--border);}
table.report-table td{padding:11px 12px; border-bottom:1px solid var(--border); color:var(--text-dim);}
table.report-table td.num{color:var(--text); font-family:var(--mono);}
table.report-table tr:last-child td{border-bottom:none;}
.flag-row{display:flex; gap:10px; align-items:flex-start; padding:12px 14px; background:var(--danger-dim); border-radius:8px; font-size:13px; color:var(--danger); margin-bottom:10px;}
.gate-banner{border:1px solid var(--border-strong); border-radius:12px; padding:24px; margin-top:34px; display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap;}
.gate-status{font-family:var(--mono); font-size:13px; padding:5px 12px; border-radius:6px;}
.gate-status.draft{background:var(--warn-dim); color:var(--warn);}
.gate-status.projected{background:var(--accent-dim); color:var(--accent-text);}
.action-row{display:flex; gap:12px; margin-top:34px; flex-wrap:wrap;}
.assumptions-modal{
position:fixed; inset:0; background:rgba(42,37,25,.45); display:none; align-items:flex-start;
justify-content:center; z-index:50; padding:60px 20px; overflow-y:auto;
}
.assumptions-modal.open{display:flex;}
.assumptions-panel{background:var(--surface); border:1px solid var(--border); border-radius:18px; padding:24px; max-width:720px; width:100%; max-height:82vh; overflow-y:auto;
box-shadow:0 8px 32px rgba(42,37,25,0.15);}
.assumptions-panel h2{font-size:18px; margin-bottom:6px;}
.assumptions-panel .meta{font-size:12.5px; color:var(--text-faint); font-family:var(--mono); margin-bottom:22px;}
.a-section{margin-bottom:28px;}
.a-section:last-child{margin-bottom:0;}
.a-section-title{font-family:var(--display); font-size:14px; font-weight:600; margin-bottom:4px;}
.a-section-note{font-size:12.5px; color:var(--text-dim); margin-bottom:12px; line-height:1.6;}
table.a-table{width:100%; border-collapse:collapse; font-size:13px;}
table.a-table th{text-align:left; color:var(--text-faint); font-weight:500; font-size:11.5px; text-transform:uppercase; letter-spacing:.03em; padding:6px 10px; border-bottom:1px solid var(--border);}
table.a-table td{padding:8px 10px; border-bottom:1px solid var(--border); color:var(--text-dim);}
table.a-table td.num{color:var(--text); font-family:var(--mono); text-align:right;}
table.a-table tr:last-child td{border-bottom:none;}
.a-callout{border-left:2px solid var(--warn); padding:12px 16px; background:var(--warn-dim); border-radius:0 8px 8px 0; font-size:12.5px; color:var(--text-dim); line-height:1.6; margin-bottom:8px;}
.a-callout b{color:var(--warn);}
.a-changelog{list-style:none; padding:0; margin:0; font-size:12.5px; color:var(--text-dim); line-height:1.8;}
.a-changelog li{padding-left:14px; position:relative;}
.a-changelog li::before{content:"—"; position:absolute; left:0; color:var(--text-faint);}
.a-stat-row{display:flex; justify-content:space-between; font-size:13px; padding:8px 10px; border-bottom:1px solid var(--border);}
.a-stat-row:last-child{border-bottom:none;}
.a-stat-row .k{color:var(--text-dim);}
.a-stat-row .v{font-family:var(--mono); color:var(--text);}
.assumptions-panel pre{background:var(--surface-2); border-radius:10px; padding:24px; font-size:12px; color:var(--text-dim); overflow-x:auto; font-family:var(--mono); line-height:1.7;}
.close-x{float:right; background:none; border:none; color:var(--text-dim); font-size:20px; cursor:pointer; line-height:1;}
.flag-note{font-size:12px; color:var(--text-faint); margin-top:8px; line-height:1.5;}
.card.intro-hero{max-width:760px; padding:48px;}
.intro-hero{padding:24px 0 8px;}
.intro-hero h2{font-size:30px; letter-spacing:-0.02em; margin-bottom:18px; max-width:22ch; line-height:1.25;}
.intro-hero p{font-size:15.5px; color:var(--text-dim); margin-bottom:30px; line-height:1.75;}
.intro-list{list-style:none; padding:0; margin:0 0 32px; display:grid; gap:14px;}
.intro-list li{font-size:13.5px; color:var(--text-dim); display:flex; gap:12px; line-height:1.6;}
.intro-list .n{font-family:var(--mono); color:var(--accent-text); flex:none; width:20px;}
</style>
</head>
<body>
<header>
<div class="brand">
<h1>AI Use Case ROI Calculator</h1>
<span class="tag">assumptions v<span id="ver-tag"></span> · input collector, not a calculator</span>
</div>
<button class="assumptions-link" onclick="openAssumptions()">View house assumptions</button>
</header>
<div class="app">
<div id="wizard-root"></div>
</div>
<div class="assumptions-modal" id="assumptions-modal">
<div class="assumptions-panel">
<button class="close-x" onclick="closeAssumptions()">&times;</button>
<h2>House assumptions</h2>
<div class="meta" id="assumptions-meta"></div>
<div id="assumptions-body"></div>
</div>
</div>
<script>
/\* =========================================================================
HOUSE ASSUMPTIONS (v1.1.0) — the single source of truth for every case.
Mirrors references/assumptions.json exactly. Edit only here, and bump the
version + changelog if this file is ever updated.
========================================================================= \*/
const ASSUMPTIONS = {
\_meta: {
version: "1.1.0",
owner: "RevOps — <assign a named owner>",
last\_updated: "2026-07-23",
changelog: [
"1.0.0 (2026-06-29): initial house assumptions extracted from methodology v1",
"1.1.0 (2026-07-23): conservatism revision — lowered automation\_share, adoption\_steadystate, adoption\_year1\_ramp, and conversion\_to\_productive; churn\_reduction lowered to 0.08 and reclassified as require\_justification; build\_tshirt\_weeks widened pending real build-history validation; role\_costs\_loaded\_annual flagged pending Finance/HR reconciliation."
],
flagged\_for\_validation: {
build\_tshirt\_weeks: "Widened by judgment (~1.5x). Not yet checked against real build-time history. Treat as placeholder.",
role\_costs\_loaded\_annual: "Not yet reconciled against real comp bands. No system available to verify inside this calculator."
}
},
role\_costs\_loaded\_annual: {
SDR: 95000, AE: 143000, CSM: 150000, RevOps\_analyst: 120000,
support\_rep: 85000, renewals\_specialist: 100000, PMM\_PM: 165000,
engineer: 190000, manager: 210000
},
hours\_per\_year: 2080,
working\_days\_per\_year: 260,
builder\_role: "engineer",
scenario\_levers: {
automation\_share: { conservative: 0.40, expected: 0.55, optimistic: 0.80 },
adoption\_steadystate: { conservative: 0.30, expected: 0.50, optimistic: 0.75 },
coverage: { conservative: 0.70, expected: 0.85, optimistic: 0.95 },
attribution: { conservative: 0.50, expected: 0.50, optimistic: 0.80 }
},
adoption\_year1\_ramp: 0.60,
coverage\_year1\_ramp: 0.80,
revenue\_chain\_defaults: {
conversion\_to\_productive: 0.40,
hours\_per\_downstream\_unit: 3,
at\_risk\_rate: 0.10,
churn\_reduction: 0.08
},
require\_justification: { fields: ["churn\_reduction"] },
run\_cost\_per\_instance: { light: 0.06, medium: 0.30, heavy: 1.00 },
run\_cost\_platform\_annual\_default: 1000,
build\_tshirt\_weeks: { S: 3, M: 9, L: 18 },
confidence\_multiplier: { High: 1.0, Medium: 0.7, Low: 0.4 },
near\_zero\_floor\_usd: 15000
};
const ROLE\_LABELS = {
SDR: "SDR", AE: "Account Executive", CSM: "Customer Success Manager",
RevOps\_analyst: "RevOps Analyst", support\_rep: "Support Rep",
renewals\_specialist: "Renewals Specialist", PMM\_PM: "PMM / PM",
engineer: "Engineer", manager: "Manager"
};
/\* NOTE: this file intentionally does NOT compute anything. It collects a case's facts into the
same inputs JSON the /roi skill's schema expects, then hands that JSON to Claude to run through
the real deterministic engine (references/roi\_engine.py) and the real house assumptions
(references/assumptions.json). Do not re-add math here — that would let this sandbox drift from
the one true engine, which is exactly what the versioned assumptions file exists to prevent. \*/
/\* =========================================================================
WIZARD STATE + STEPS
========================================================================= \*/
let inputs = {
use\_case: {name:"", owner:"", requestor:"", one\_liner:"", value\_type:"", delivery\_model:"augmentation"},
labor: {role:"AE", people:1, eligible\_volume\_year:0, hours\_per\_instance:0, net\_hours\_reported:false,
net\_hours\_per\_period:0, periods\_per\_year:52, gate:"", headcount\_reduction\_fte:0},
revenue\_chain: {value\_per\_account:0, at\_risk\_rate:null, churn\_reduction:null, conversion\_to\_productive:null,
hours\_per\_downstream\_unit:null, holdout\_exists:false, \_reasons:{}},
build: {weeks:null, tshirt:"M"},
run: {tier:"medium", platform\_annual:null},
data\_grounding: {},
overrides: [],
confidence\_override: null,
shared\_capacity\_pool: ""
};
let step = 0;
function needsRevenueChain(){
return inputs.use\_case.value\_type === "revenue" || inputs.labor.gate === "redeploy";
}
const STEP\_DEFS = [
{id:"intro", label:"Start"},
{id:"idea", label:"The idea"},
{id:"who", label:"Who & volume"},
{id:"gate", label:"The gate"},
{id:"revenue", label:"Revenue chain", conditional:true},
{id:"build", label:"Build & run"},
{id:"ground", label:"Data check"},
{id:"review", label:"Review"},
{id:"handoff", label:"Send to Claude"}
];
function activeSteps(){
return STEP\_DEFS.filter(s => !s.conditional || needsRevenueChain());
}
function renderRail(){
const steps = activeSteps();
const curIdx = steps.findIndex(s => s.id === STEP\_DEFS[step].id);
let html = '<div class="rail">';
steps.forEach((s, i) => {
const cls = i===curIdx ? "active" : (i<curIdx ? "done" : "");
html += `<div class="rail-item ${cls}">${i<curIdx ? checkIcon() : ""} ${s.label}</div>`;
});
html += '</div>';
return html;
}
function checkIcon(){
return '<svg class="rail-check" viewBox="0 0 16 16" fill="none"><path d="M3 8.5L6.2 11.5L13 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}
function goTo(id){
const idx = STEP\_DEFS.findIndex(s=>s.id===id);
step = idx;
render();
}
function next(){
const steps = activeSteps();
const curIdx = steps.findIndex(s => s.id === STEP\_DEFS[step].id);
if(curIdx < steps.length-1) goTo(steps[curIdx+1].id);
}
function prev(){
const steps = activeSteps();
const curIdx = steps.findIndex(s => s.id === STEP\_DEFS[step].id);
if(curIdx > 0) goTo(steps[curIdx-1].id);
}
function render(){
const root = document.getElementById("wizard-root");
const id = STEP\_DEFS[step].id;
if(id === "intro"){ root.innerHTML = renderIntro(); return; }
if(id === "handoff"){ root.innerHTML = `<div class="card">${renderHandoff()}</div>`; return; }
root.innerHTML = `<div class="wizard">${renderRail()}<div class="card">${renderStep(id)}</div></div>`;
attachHandlers(id);
}
function renderIntro(){
return `
<div class="card intro-hero">
<div class="eyebrow">Quickbase · AI Use Case ROI</div>
<h2>Package an AI idea for Claude to price out.</h2>
<p>This collects exactly what the internal <code>/roi</code> skill needs — nothing is
calculated on this page. Fill it out, then hand the result to Claude to run through the real
deterministic engine, ground it against real data where possible, and get the actual numbers
in your conversation.</p>
<ul class="intro-list">
<li><span class="n">01</span> Describe the idea in plain language — no jargon required.</li>
<li><span class="n">02</span> Answer a short interview about who it touches and how much time it saves.</li>
<li><span class="n">03</span> Any number that departs from house assumptions gets flagged and needs a reason.</li>
<li><span class="n">04</span> Copy the packaged case and paste it to Claude — that's where the real math happens.</li>
</ul>
<button class="btn primary" onclick="goTo('idea')">Start the estimate →</button>
</div>`;
}
function renderStep(id){
if(id==="idea") return stepIdea();
if(id==="who") return stepWho();
if(id==="gate") return stepGate();
if(id==="revenue") return stepRevenue();
if(id==="build") return stepBuild();
if(id==="ground") return stepGround();
if(id==="review") return stepReview();
return "";
}
/\* ---- Step: the idea ---- \*/
function stepIdea(){
const uc = inputs.use\_case;
return `
<div class="eyebrow">Step 1 of ${activeSteps().length-1}</div>
<div class="question">What's this idea, in one sentence?</div>
<div class="helper">What does the AI actually do? Write it like you'd explain it to a colleague, not a spec.</div>
<div class="field">
<textarea id="f-oneliner" placeholder="e.g. AI drafts QBR decks from account data; CSMs review before sending.">${uc.one\_liner}</textarea>
<div class="field-hint">One or two sentences. This becomes the case name Claude uses when writing it up later.</div>
</div>
<div class="field-row">
<div class="field"><label class="field-label">Use case name (optional)</label><input id="f-name" type="text" value="${uc.name}">
<div class="field-hint">A short title for the register — leave blank and Claude will suggest one.</div></div>
<div class="field"><label class="field-label">Requestor (optional)</label><input id="f-requestor" type="text" value="${uc.requestor}">
<div class="field-hint">Who's asking for this to get built — for tracking, doesn't affect the numbers.</div></div>
</div>
<div class="question" style="font-size:17px; margin-top:8px;">What kind of value is this?</div>
<div class="choice-grid">
${choiceCard("value\_type","labor","Time saved","Saves time for a role — no direct headcount or revenue claim yet.")}
${choiceCard("value\_type","revenue","Revenue or retention","Directly moves a number like churn, win rate, or conversion.")}
${choiceCard("value\_type","risk","Risk reduction","Reduces compliance, security, or error exposure rather than saving time or making money.")}
${choiceCard("value\_type","capability","Strategic capability","A bet on a new capability — not meant to pencil out in hard dollars.")}
</div>
<div class="question" style="font-size:17px; margin-top:20px;">How does it get done?</div>
<div class="choice-grid">
${choiceCard("delivery\_model","augmentation","A person is still in the loop","AI makes the task faster; a human still does it. Uses the adoption rate.")}
${choiceCard("delivery\_model","autonomous","AI does it end-to-end","No person in the loop day-to-day. Uses the coverage rate instead.")}
</div>
<div class="nav-row"><span></span><button class="btn primary" id="btn-next" onclick="saveIdea()">Continue →</button></div>
`;
}
function choiceCard(field, value, title, desc){
const cur = field==="value\_type" ? inputs.use\_case.value\_type : inputs.use\_case.delivery\_model;
const sel = cur===value ? "selected" : "";
return `<div class="choice ${sel}" data-field="${field}" data-value="${value}" onclick="pickChoice(this)">
<div class="choice-title">${title}</div><div class="choice-desc">${desc}</div>
</div>`;
}
function pickChoice(el){
const field = el.dataset.field, value = el.dataset.value;
el.parentElement.querySelectorAll(".choice").forEach(c=>c.classList.remove("selected"));
el.classList.add("selected");
if(field==="value\_type") inputs.use\_case.value\_type = value;
if(field==="delivery\_model") inputs.use\_case.delivery\_model = value;
}
function saveIdea(){
inputs.use\_case.one\_liner = document.getElementById("f-oneliner").value;
inputs.use\_case.name = document.getElementById("f-name").value;
inputs.use\_case.requestor = document.getElementById("f-requestor").value;
if(!inputs.use\_case.value\_type){ alert("Pick what kind of value this creates before continuing."); return; }
next();
}
/\* ---- Step: who & volume ---- \*/
function stepWho(){
const lab = inputs.labor;
const roleOptions = Object.keys(ASSUMPTIONS.role\_costs\_loaded\_annual)
.map(r=>`<option value="${r}" ${lab.role===r?"selected":""}>${ROLE\_LABELS[r]}</option>`).join("");
return `
<div class="eyebrow">Step 2 of ${activeSteps().length-1}</div>
<div class="question">Whose job does this touch?</div>
<div class="helper">Pick the role that spends the time today, and roughly how many of them there are.</div>
<div class="field-row">
<div class="field"><label class="field-label">Role</label><select id="f-role">${roleOptions}</select>
<div class="field-hint">Sets the hourly cost used to value the time this saves.</div></div>
<div class="field"><label class="field-label">How many people</label><input id="f-people" type="number" min="0" value="${lab.people}">
<div class="field-hint">Total headcount in this role who'd actually use it.</div></div>
</div>
<div class="question" style="font-size:17px;">How often does this happen?</div>
<div class="field">
<label class="field-label">Times per year (e.g. 200 QBRs/year, 5,000 tickets/year)</label>
<input id="f-volume" type="number" min="0" value="${lab.eligible\_volume\_year}">
<div class="field-hint">Across everyone in the role combined, not per person.</div>
</div>
<div class="toggle-row">
<input type="checkbox" id="f-nethours" ${lab.net\_hours\_reported?"checked":""} onchange="toggleNetHours(this)">
<label for="f-nethours">I already know the net hours saved per person — skip the automation estimate</label>
</div>
<div id="raw-hours-block" style="${lab.net\_hours\_reported?"display:none;":""}">
<div class="field">
<label class="field-label">Today, without AI, how long does one of these take start to finish? (hours)</label>
<input id="f-hours" type="number" step="0.1" min="0" value="${lab.hours\_per\_instance}">
<div class="field-hint">Your honest current-state estimate — this drives most of what follows, so don't round up.</div>
</div>
</div>
<div id="net-hours-block" style="${lab.net\_hours\_reported?"":"display:none;"}">
<div class="field-row">
<div class="field"><label class="field-label">Net hours saved per period, per person</label><input id="f-nethrs" type="number" step="0.1" min="0" value="${lab.net\_hours\_per\_period}">
<div class="field-hint">Use this only if you've already measured the after-AI time directly.</div></div>
<div class="field"><label class="field-label">Periods per year (e.g. 52 for weekly)</label><input id="f-periods" type="number" min="1" value="${lab.periods\_per\_year}">
<div class="field-hint">How many of those measurement periods happen in a year.</div></div>
</div>
</div>
<div class="nav-row"><button class="btn ghost" onclick="prev()">← Back</button><button class="btn primary" onclick="saveWho()">Continue →</button></div>
`;
}
function toggleNetHours(el){
document.getElementById("raw-hours-block").style.display = el.checked ? "none" : "";
document.getElementById("net-hours-block").style.display = el.checked ? "" : "none";
}
function saveWho(){
const lab = inputs.labor;
lab.role = document.getElementById("f-role").value;
lab.people = Number(document.getElementById("f-people").value)||0;
lab.eligible\_volume\_year = Number(document.getElementById("f-volume").value)||0;
lab.net\_hours\_reported = document.getElementById("f-nethours").checked;
if(lab.net\_hours\_reported){
lab.net\_hours\_per\_period = Number(document.getElementById("f-nethrs").value)||0;
lab.periods\_per\_year = Number(document.getElementById("f-periods").value)||52;
} else {
lab.hours\_per\_instance = Number(document.getElementById("f-hours").value)||0;
}
next();
}
/\* ---- Step: the gate ---- \*/
function stepGate(){
const lab = inputs.labor;
return `
<div class="eyebrow">Step 3 of ${activeSteps().length-1}</div>
<div class="question">If this works, what happens to the freed-up time?</div>
<div class="helper">This is the single biggest driver of whether there's real cash value here — be honest about it.</div>
<div class="choice-grid">
${gateCard("diffuse","Gets absorbed into other work","Nice to have, but nobody can point to a dollar saved. No hard cash claim.")}
${gateCard("redeploy","Gets redirected to something valuable","e.g. CSMs spend it on at-risk accounts, AEs spend it on more pipeline.")}
${gateCard("headcount","Lets you actually reduce headcount or avoid a hire","A real, countable FTE reduction.")}
</div>
<div id="headcount-block" style="${lab.gate==="headcount"?"":"display:none;"} margin-top:14px;">
<div class="field"><label class="field-label">How many FTEs does this remove or avoid hiring?</label>
<input id="f-fte" type="number" step="0.1" min="0" value="${lab.headcount\_reduction\_fte}">
<div class="field-hint">Only count roles actually cut or a hire actually skipped — not hours freed up in general.</div></div>
</div>
<div class="nav-row"><button class="btn ghost" onclick="prev()">← Back</button><button class="btn primary" onclick="saveGate()">Continue →</button></div>
`;
}
function gateCard(value, title, desc){
const sel = inputs.labor.gate===value ? "selected" : "";
return `<div class="choice ${sel}" data-value="${value}" onclick="pickGate(this)">
<div class="choice-title">${title}</div><div class="choice-desc">${desc}</div>
</div>`;
}
function pickGate(el){
el.parentElement.querySelectorAll(".choice").forEach(c=>c.classList.remove("selected"));
el.classList.add("selected");
inputs.labor.gate = el.dataset.value;
document.getElementById("headcount-block").style.display = el.dataset.value==="headcount" ? "" : "none";
}
function saveGate(){
if(!inputs.labor.gate){ alert("Pick what happens to the freed-up time before continuing."); return; }
if(inputs.labor.gate==="headcount"){
inputs.labor.headcount\_reduction\_fte = Number(document.getElementById("f-fte").value)||0;
}
next();
}
/\* ---- Step: revenue chain ---- \*/
function stepRevenue(){
const rc = inputs.revenue\_chain, D = ASSUMPTIONS.revenue\_chain\_defaults;
if(rc.at\_risk\_rate===null) rc.at\_risk\_rate = D.at\_risk\_rate;
if(rc.conversion\_to\_productive===null) rc.conversion\_to\_productive = D.conversion\_to\_productive;
if(rc.hours\_per\_downstream\_unit===null) rc.hours\_per\_downstream\_unit = D.hours\_per\_downstream\_unit;
if(rc.churn\_reduction===null) rc.churn\_reduction = D.churn\_reduction;
return `
<div class="eyebrow">Step 4 of ${activeSteps().length-1}</div>
<div class="question">The revenue math</div>
<div class="helper">This case claims real dollars, so a couple of numbers need to be real too. House defaults are pre-filled — change them only if you have a better number, and say why.</div>
<div class="field">
<label class="field-label">Typical account value per year (ARR or margin, $)</label>
<input id="f-arr" type="number" min="0" value="${rc.value\_per\_account}">
<div class="field-hint">Average across the accounts this touches — not your biggest logo.</div>
</div>
${overrideField("at\_risk\_rate","At-risk rate (fraction of accounts this touches that are genuinely at risk)", rc.at\_risk\_rate, D.at\_risk\_rate, false)}
${overrideField("conversion\_to\_productive","Conversion to productive output (fraction of freed hours that become real, usable work)", rc.conversion\_to\_productive, D.conversion\_to\_productive, false)}
${overrideField("hours\_per\_downstream\_unit","Hours needed per downstream unit of work", rc.hours\_per\_downstream\_unit, D.hours\_per\_downstream\_unit, false)}
${overrideField("churn\_reduction","Churn reduction this drives (fraction)", rc.churn\_reduction, D.churn\_reduction, true)}
<div class="toggle-row">
<input type="checkbox" id="f-holdout" ${rc.holdout\_exists?"checked":""}>
<label for="f-holdout">There's a holdout/control group backing this up</label>
</div>
<div class="nav-row"><button class="btn ghost" onclick="prev()">← Back</button><button class="btn primary" onclick="saveRevenue()">Continue →</button></div>
`;
}
function overrideField(key, label, value, houseDefault, alwaysRequireReason){
const reason = (inputs.revenue\_chain.\_reasons||{})[key] || "";
return `
<div class="field">
<label class="field-label">${label} ${alwaysRequireReason?'<span class="required-tag">reason required</span>':''}</label>
<input class="rc-input" data-key="${key}" type="number" step="0.01" min="0" value="${value}"
oninput="onRcInput('${key}', ${houseDefault}, ${alwaysRequireReason})">
<div class="flag-note">House default: ${houseDefault}</div>
<div class="reason-box" id="reason-${key}" style="display:${(alwaysRequireReason || value!=houseDefault)?'':'none'};">
<label class="field-label">Why this number for this case?</label>
<textarea id="reason-text-${key}" oninput="storeReason('${key}')">${reason}</textarea>
</div>
</div>`;
}
function onRcInput(key, houseDefault, alwaysRequire){
const box = document.getElementById("reason-"+key);
const val = Number(document.querySelector(`.rc-input[data-key="${key}"]`).value);
box.style.display = (alwaysRequire || val!==houseDefault) ? "" : "none";
}
function storeReason(key){
if(!inputs.revenue\_chain.\_reasons) inputs.revenue\_chain.\_reasons = {};
inputs.revenue\_chain.\_reasons[key] = document.getElementById("reason-text-"+key).value;
}
function saveRevenue(){
const rc = inputs.revenue\_chain;
rc.value\_per\_account = Number(document.getElementById("f-arr").value)||0;
["at\_risk\_rate","conversion\_to\_productive","hours\_per\_downstream\_unit","churn\_reduction"].forEach(k=>{
rc[k] = Number(document.querySelector(`.rc-input[data-key="${k}"]`).value);
});
rc.holdout\_exists = document.getElementById("f-holdout").checked;
// churn\_reduction is required-justification: block continue without a reason
if(!rc.\_reasons || !rc.\_reasons.churn\_reduction || !rc.\_reasons.churn\_reduction.trim()){
if(!confirm("No reason given for the churn\_reduction assumption. This will cap confidence at Low and flag the case. Continue anyway?")) return;
}
next();
}
/\* ---- Step: build & run ---- \*/
function stepBuild(){
const b = inputs.build, r = inputs.run;
return `
<div class="eyebrow">Step ${needsRevenueChain()?5:4} of ${activeSteps().length-1}</div>
<div class="question">How big a build is this?</div>
<div class="helper">Rough t-shirt size is fine. These week estimates are flagged as placeholders pending real build-history data — adjust if you know better.</div>
<div class="choice-grid" style="grid-template-columns:repeat(3,1fr); display:grid;">
${tshirtCard("S")}${tshirtCard("M")}${tshirtCard("L")}
</div>
<div class="field" style="margin-top:14px;">
<label class="field-label">Or enter exact weeks (overrides t-shirt size)</label>
<input id="f-weeks" type="number" min="0" value="${b.weeks||""}" placeholder="leave blank to use t-shirt size">
<div class="field-hint">Only fill this in if you have a firmer estimate than the S/M/L buckets above.</div>
</div>
<div class="question" style="font-size:17px; margin-top:10px;">Run cost</div>
<div class="field-row">
<div class="field">
<label class="field-label">Per-instance compute tier</label>
<select id="f-tier">
<option value="light" ${r.tier==="light"?"selected":""}>Light ($${ASSUMPTIONS.run\_cost\_per\_instance.light}/instance)</option>
<option value="medium" ${r.tier==="medium"?"selected":""}>Medium ($${ASSUMPTIONS.run\_cost\_per\_instance.medium}/instance)</option>
<option value="heavy" ${r.tier==="heavy"?"selected":""}>Heavy ($${ASSUMPTIONS.run\_cost\_per\_instance.heavy}/instance)</option>
</select>
<div class="field-hint">How much AI/compute each individual run costs — most cases are Light or Medium.</div>
</div>
<div class="field">
<label class="field-label">Platform cost per year ($)</label>
<input id="f-platform" type="number" min="0" value="${r.platform\_annual!=null?r.platform\_annual:ASSUMPTIONS.run\_cost\_platform\_annual\_default}">
<div class="field-hint">Recurring platform/vendor cost, separate from build cost — house default is $1,000/yr.</div>
</div>
</div>
<div class="nav-row"><button class="btn ghost" onclick="prev()">← Back</button><button class="btn primary" onclick="saveBuild()">Continue →</button></div>
`;
}
function tshirtCard(size){
const sel = inputs.build.tshirt===size ? "selected" : "";
const weeks = ASSUMPTIONS.build\_tshirt\_weeks[size];
const names = {S:"Small",M:"Medium",L:"Large"};
return `<div class="choice ${sel}" data-value="${size}" onclick="pickTshirt(this)">
<div class="choice-title">${names[size]}</div><div class="choice-desc">~${weeks} weeks</div>
</div>`;
}
function pickTshirt(el){
el.parentElement.querySelectorAll(".choice").forEach(c=>c.classList.remove("selected"));
el.classList.add("selected");
inputs.build.tshirt = el.dataset.value;
}
function saveBuild(){
const weeksVal = document.getElementById("f-weeks").value;
inputs.build.weeks = weeksVal ? Number(weeksVal) : null;
inputs.run.tier = document.getElementById("f-tier").value;
inputs.run.platform\_annual = Number(document.getElementById("f-platform").value)||0;
next();
}
/\* ---- Step: data grounding ---- \*/
function stepGround(){
const fields = [
{key:"eligible\_volume\_year", label:"Volume/year ("+inputs.labor.eligible\_volume\_year+")"},
{key:"people", label:"Headcount ("+inputs.labor.people+" people)"},
];
if(needsRevenueChain()){
fields.push({key:"value\_per\_account", label:"Account value ($"+inputs.revenue\_chain.value\_per\_account+")"});
fields.push({key:"at\_risk\_rate", label:"At-risk rate ("+inputs.revenue\_chain.at\_risk\_rate+")"});
}
const rows = fields.map(f=>{
const g = inputs.data\_grounding[f.key] || {source:"user", system:""};
return `
<div class="field" style="border:1px solid var(--border); border-radius:10px; padding:24px;">
<label class="field-label">${f.label}</label>
<div class="toggle-row" style="margin-bottom:8px;">
<input type="radio" name="src-${f.key}" id="src-user-${f.key}" ${g.source==="user"?"checked":""} onchange="setGround('${f.key}','user')">
<label for="src-user-${f.key}" style="margin-right:16px;">This is my estimate</label>
<input type="radio" name="src-${f.key}" id="src-sys-${f.key}" ${g.source==="system"?"checked":""} onchange="setGround('${f.key}','system')">
<label for="src-sys-${f.key}">I verified this against a real record/system</label>
</div>
<div id="sysname-${f.key}" style="display:${g.source==="system"?"":"none"};">
<input type="text" placeholder="Where from? (e.g. Salesforce export, Gainsight report)" value="${g.system||""}" oninput="setGroundSystem('${f.key}', this.value)">
</div>
</div>`;
}).join("");
return `
<div class="eyebrow">Step ${needsRevenueChain()?6:5} of ${activeSteps().length-1}</div>
<div class="question">How solid are these numbers?</div>
<div class="helper">Be honest — this directly drives the confidence score, and an unverified number isn't a bad thing, it's just an unverified number.</div>
<div style="display:grid; gap:12px;">${rows}</div>
<div class="nav-row"><button class="btn ghost" onclick="prev()">← Back</button><button class="btn primary" onclick="next()">Continue →</button></div>
`;
}
function setGround(key, source){
if(!inputs.data\_grounding[key]) inputs.data\_grounding[key] = {};
inputs.data\_grounding[key].source = source;
document.getElementById("sysname-"+key).style.display = source==="system" ? "" : "none";
}
function setGroundSystem(key, val){
if(!inputs.data\_grounding[key]) inputs.data\_grounding[key] = {};
inputs.data\_grounding[key].system = val;
}
/\* ---- Step: review ---- \*/
function stepReview(){
const uc = inputs.use\_case, lab = inputs.labor;
return `
<div class="eyebrow">Step ${activeSteps().length-1} of ${activeSteps().length-1}</div>
<div class="question">Ready to send</div>
<div class="helper">Quick check before you hand this to Claude — nothing is calculated here, this just packages what you've entered.</div>
<table class="report-table">
<tr><td>Idea</td><td class="num">${uc.one\_liner||"(none)"}</td></tr>
<tr><td>Value type</td><td class="num">${uc.value\_type}</td></tr>
<tr><td>Delivery model</td><td class="num">${uc.delivery\_model}</td></tr>
<tr><td>Role / people</td><td class="num">${ROLE\_LABELS[lab.role]} × ${lab.people}</td></tr>
<tr><td>Volume/year</td><td class="num">${lab.eligible\_volume\_year}</td></tr>
<tr><td>Gate</td><td class="num">${lab.gate}</td></tr>
<tr><td>Build</td><td class="num">${inputs.build.weeks ? inputs.build.weeks+" weeks (custom)" : inputs.build.tshirt+" ("+ASSUMPTIONS.build\_tshirt\_weeks[inputs.build.tshirt]+" wks)"}</td></tr>
<tr><td>Run tier</td><td class="num">${inputs.run.tier}</td></tr>
</table>
<div class="nav-row"><button class="btn ghost" onclick="prev()">← Back</button><button class="btn primary" onclick="goTo('handoff')">Review and send →</button></div>
`;
}
/\* ---- Handoff: package inputs for Claude, nothing computed here ---- \*/
function renderHandoff(){
const payload = JSON.stringify(inputs, null, 2);
return `
<div class="verdict-banner ok">
<div>
<div class="vtitle">This part is done — Claude takes it from here</div>
<p>Nothing on this page has been calculated. The block below is everything Claude needs to
run it through the real deterministic engine, ground anything it can against real data,
and give you the actual numbers in your conversation.</p>
</div>
</div>
<div class="section-title">Your case, packaged</div>
<div class="flag-note" style="margin-bottom:10px;">Copy this and paste it into your Claude
conversation — starting with <code>/roi</code> if you're opening a new one.</div>
<pre style="background:var(--surface-2); border-radius:10px; padding:24px; font-size:12px; color:var(--text-dim); overflow-x:auto; font-family:var(--mono); line-height:1.7; max-height:340px;">${payload.replace(/</g,"&lt;")}</pre>
<div class="action-row">
<button class="btn primary" onclick="copyInputs(event)">Copy for Claude</button>
<button class="btn" onclick="openInDesktop()">Open in Claude Desktop</button>
<button class="btn ghost" onclick="restart()">Start a new estimate</button>
</div>
<div class="flag-note" style="margin-top:14px;">"Open in Claude Desktop" only works if you have
the Claude Desktop app installed and set as the handler for <code>claude://</code> links — it
opens a new chat there with this case pre-filled, so you just review and hit send. Nothing
happens if you don't have Desktop installed; use "Copy for Claude" instead. Either way, Claude
will walk through the real numbers with you, then ask before doing anything further — including
publishing this to the Confluence ROI register or filing it as a Jira ticket. Nothing gets
submitted anywhere without that confirmation.</div>
`;
}
function copyInputs(e){ copyText(JSON.stringify(inputs, null, 2), e); }
function openInDesktop(){
// claude://claude.ai/new?q=... prefills a new Claude Desktop chat's message box.
// Anthropic's docs note q is truncated around ~14,000 characters — compact JSON (no
// indentation) instead of the pretty-printed version keeps this well under that limit.
const text = "/roi
" + JSON.stringify(inputs);
if(text.length > 13000){
alert("This case is too large for the Desktop link (Claude truncates long pre-filled text). Use \"Copy for Claude\" instead and paste it in manually.");
return;
}
window.location.href = "claude://claude.ai/new?q=" + encodeURIComponent(text);
}
function copyText(text, e){
function done(){ toast(e); }
function fallback(){
const ta = document.createElement("textarea");
ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
document.body.appendChild(ta); ta.focus(); ta.select();
try{ document.execCommand("copy"); }catch(err){}
document.body.removeChild(ta);
done();
}
if(navigator.clipboard && window.isSecureContext){
navigator.clipboard.writeText(text).then(done).catch(fallback);
} else {
fallback();
}
}
function toast(e){
const b = e.target; const orig = b.textContent;
b.textContent = "Copied"; setTimeout(()=>{b.textContent=orig;}, 1200);
}
function restart(){
location.reload();
}
function attachHandlers(id){ /\* handlers are inline via onclick/oninput; nothing extra needed \*/ }
/\* ---- assumptions modal: formatted for reading, not a JSON dump ---- \*/
function aPct(n){ return Math.round(n\*1000)/10 + "%"; }
function aUSD(n){ return "$" + Math.round(n).toLocaleString("en-US"); }
function renderAssumptionsBody(){
const A = ASSUMPTIONS;
const roleRows = Object.keys(A.role\_costs\_loaded\_annual).map(r =>
`<tr><td>${ROLE\_LABELS[r] || r}</td><td class="num">${aUSD(A.role\_costs\_loaded\_annual[r])}/yr</td></tr>`
).join("");
const leverRows = Object.keys(A.scenario\_levers).map(k => {
const v = A.scenario\_levers[k];
const label = k.replace(/\_/g," ").replace(/\b\w/g, c => c.toUpperCase());
return `<tr><td>${label}</td><td class="num">${aPct(v.conservative)}</td><td class="num">${aPct(v.expected)}</td><td class="num">${aPct(v.optimistic)}</td></tr>`;
}).join("");
const rc = A.revenue\_chain\_defaults;
const requiresJustification = new Set((A.require\_justification||{}).fields||[]);
const rcLabels = {
conversion\_to\_productive: "Conversion to productive output",
hours\_per\_downstream\_unit: "Hours per downstream unit",
at\_risk\_rate: "At-risk rate",
churn\_reduction: "Churn reduction"
};
const rcRows = Object.keys(rc).map(k => {
const isPct = k !== "hours\_per\_downstream\_unit";
const val = isPct ? aPct(rc[k]) : rc[k];
const flag = requiresJustification.has(k) ? ` <span style="color:var(--warn); font-family:var(--mono); font-size:11px;">requires justification</span>` : "";
return `<tr><td>${rcLabels[k] || k}${flag}</td><td class="num">${val}</td></tr>`;
}).join("");
const runRows = Object.keys(A.run\_cost\_per\_instance).map(tier =>
`<tr><td style="text-transform:capitalize;">${tier}</td><td class="num">$${A.run\_cost\_per\_instance[tier].toFixed(2)}/instance</td></tr>`
).join("");
const buildRows = Object.keys(A.build\_tshirt\_weeks).map(size =>
`<tr><td>${{S:"Small",M:"Medium",L:"Large"}[size] || size}</td><td class="num">${A.build\_tshirt\_weeks[size]} weeks</td></tr>`
).join("");
const confRows = Object.keys(A.confidence\_multiplier).map(level =>
`<tr><td>${level}</td><td class="num">${A.confidence\_multiplier[level]}×</td></tr>`
).join("");
const flagged = A.\_meta.flagged\_for\_validation || {};
const flaggedHtml = Object.keys(flagged).map(k =>
`<div class="a-callout"><b>${k}</b> — ${flagged[k]}</div>`
).join("");
const changelogHtml = (A.\_meta.changelog||[]).slice().reverse().map(c => `<li>${c}</li>`).join("");
return `
<div class="a-section">
<div class="a-section-title">Role costs (fully loaded annual)</div>
<div class="a-section-note">Salary + benefits + overhead. Used to value an hour of someone's time — never their OTE.</div>
<table class="a-table">${roleRows}</table>
</div>
<div class="a-section">
<div class="a-section-title">Delivery scenario levers</div>
<div class="a-section-note">How much of the task is automatable, and how much it's actually used, at three confidence levels.</div>
<table class="a-table">
<tr><th></th><th>Conservative</th><th>Expected</th><th>Optimistic</th></tr>
${leverRows}
</table>
<div class="a-stat-row"><span class="k">Year-1 adoption ramp</span><span class="v">${aPct(A.adoption\_year1\_ramp)}</span></div>
<div class="a-stat-row"><span class="k">Year-1 coverage ramp</span><span class="v">${aPct(A.coverage\_year1\_ramp)}</span></div>
</div>
<div class="a-section">
<div class="a-section-title">Revenue chain defaults</div>
<div class="a-section-note">Used only for revenue or redeploy cases. Fields marked "requires justification" can never be used silently, even at the default.</div>
<table class="a-table">${rcRows}</table>
</div>
<div class="a-section">
<div class="a-section-title">Run cost &amp; build time</div>
<table class="a-table">${runRows}
<tr><td>Platform (annual default)</td><td class="num">${aUSD(A.run\_cost\_platform\_annual\_default)}/yr</td></tr>
</table>
<table class="a-table" style="margin-top:10px;">${buildRows}</table>
</div>
<div class="a-section">
<div class="a-section-title">Confidence &amp; thresholds</div>
<table class="a-table">${confRows}</table>
<div class="a-stat-row"><span class="k">Near-zero floor</span><span class="v">${aUSD(A.near\_zero\_floor\_usd)}/yr</span></div>
</div>
${flaggedHtml ? `<div class="a-section"><div class="a-section-title">Flagged for validation</div>${flaggedHtml}</div>` : ""}
<div class="a-section">
<div class="a-section-title">Changelog</div>
<ul class="a-changelog">${changelogHtml}</ul>
</div>
`;
}
function openAssumptions(){
document.getElementById("assumptions-meta").textContent =
`v${ASSUMPTIONS.\_meta.version} · last updated ${ASSUMPTIONS.\_meta.last\_updated} · owner: ${ASSUMPTIONS.\_meta.owner}`;
document.getElementById("assumptions-body").innerHTML = renderAssumptionsBody();
document.getElementById("assumptions-modal").classList.add("open");
}
function closeAssumptions(){ document.getElementById("assumptions-modal").classList.remove("open"); }
document.getElementById("ver-tag").textContent = ASSUMPTIONS.\_meta.version;
render();
</script>
</body>
</html>
