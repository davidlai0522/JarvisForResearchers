---
title: Thinking Methods for Researchers
date: '2026-06-13'
---

# Thinking Methods for Researchers

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Researcher's Toolkit: Thinking & Learning Methods for the PhD</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=STIX+Two+Text:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#F7F7F2;
  --ink:#1B2430;
  --ink-soft:#46505E;
  --rule:#D8D9D0;
  --teal:#0E6E63;
  --teal-soft:#E2EFEC;
  --amber:#B07514;
  --amber-soft:#F6EEDC;
  --card:#FFFFFF;
  --mono:'JetBrains Mono',ui-monospace,monospace;
  --display:'Space Grotesk',system-ui,sans-serif;
  --body:'STIX Two Text',Georgia,serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{
  background:var(--paper);
  color:var(--ink);
  font-family:var(--body);
  font-size:1.075rem;
  line-height:1.72;
}
.page{max-width:1060px;margin:0 auto;padding:0 24px}

/* ---------- Header ---------- */
header.hero{
  border-bottom:3px solid var(--ink);
  padding:64px 0 40px;
}
.hero .eyebrow{
  font-family:var(--mono);font-size:.78rem;letter-spacing:.18em;
  text-transform:uppercase;color:var(--teal);margin-bottom:18px;
}
.hero h1{
  font-family:var(--display);font-weight:700;
  font-size:clamp(2.1rem,5vw,3.4rem);line-height:1.08;
  letter-spacing:-.015em;max-width:18ch;
}
.hero h1 em{font-style:normal;color:var(--teal)}
.hero .standfirst{
  margin-top:22px;max-width:62ch;font-size:1.12rem;color:var(--ink-soft);
}
.hero .meta{
  margin-top:26px;font-family:var(--mono);font-size:.8rem;color:var(--ink-soft);
  display:flex;gap:28px;flex-wrap:wrap;
}

/* ---------- TOC ---------- */
nav.toc{padding:34px 0 8px;border-bottom:1px solid var(--rule)}
nav.toc h2{font-family:var(--display);font-size:.95rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:16px}
.toc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:6px 32px;padding-bottom:24px}
.toc-grid a{
  display:block;text-decoration:none;color:var(--ink);
  font-family:var(--display);font-size:.95rem;padding:6px 0;
  border-bottom:1px dotted var(--rule);
}
.toc-grid a:hover{color:var(--teal)}
.toc-grid a .pt{font-family:var(--mono);font-size:.72rem;color:var(--teal);margin-right:8px}

/* ---------- Part dividers ---------- */
.part{
  margin:72px 0 8px;padding-top:18px;border-top:3px solid var(--ink);
}
.part .label{font-family:var(--mono);font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--teal)}
.part h2{font-family:var(--display);font-weight:700;font-size:clamp(1.6rem,3.4vw,2.2rem);letter-spacing:-.01em;margin-top:8px}
.part .part-intro{max-width:64ch;color:var(--ink-soft);margin-top:12px;font-size:1.05rem}

/* ---------- Method sections with margin column ---------- */
section.method{
  display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:0 44px;
  padding:44px 0 12px;border-bottom:1px solid var(--rule);
}
section.method > .main{min-width:0}
section.method > .margin{font-size:.88rem;line-height:1.55;color:var(--ink-soft);padding-top:64px}
.margin .note{margin-bottom:22px;border-left:2px solid var(--teal);padding-left:12px}
.margin .note b{font-family:var(--display);font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:3px}
@media (max-width:880px){
  section.method{grid-template-columns:1fr}
  section.method > .margin{padding-top:8px}
}

.method h3{
  font-family:var(--display);font-weight:600;font-size:1.45rem;letter-spacing:-.01em;
}
.method .kicker{font-family:var(--mono);font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin-bottom:6px}
.specline{
  margin:14px 0 18px;display:flex;flex-wrap:wrap;gap:8px;
}
.specline span{
  font-family:var(--mono);font-size:.72rem;letter-spacing:.02em;
  background:var(--teal-soft);color:var(--teal);
  padding:4px 10px;border-radius:3px;
}
.method p{margin:0 0 16px;max-width:66ch}
.method ul,.method ol{margin:0 0 18px 1.3em;max-width:62ch}
.method li{margin-bottom:8px}
.method li::marker{color:var(--teal);font-family:var(--mono);font-size:.85em}
.method strong{font-weight:600}

/* ---------- Boxes ---------- */
.howto{
  background:var(--card);border:1px solid var(--rule);border-top:3px solid var(--teal);
  padding:20px 22px 8px;margin:8px 0 22px;max-width:66ch;
}
.howto h4{font-family:var(--display);font-size:.82rem;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin-bottom:12px}
.trybox{
  background:var(--amber-soft);border-left:3px solid var(--amber);
  padding:14px 18px;margin:6px 0 26px;max-width:66ch;font-size:.98rem;
}
.trybox b{font-family:var(--display);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);display:block;margin-bottom:4px}
.pitfall{
  border:1px dashed var(--rule);padding:14px 18px;margin:6px 0 26px;max-width:66ch;font-size:.98rem;
}
.pitfall b{font-family:var(--display);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:#8A3B2E;display:block;margin-bottom:4px}
blockquote{
  margin:8px 0 22px;padding-left:18px;border-left:3px solid var(--rule);
  font-style:italic;color:var(--ink-soft);max-width:60ch;
}
blockquote .who{display:block;font-style:normal;font-family:var(--mono);font-size:.76rem;margin-top:6px;color:var(--teal)}
code{font-family:var(--mono);font-size:.86em;background:#ECEDE6;padding:1px 5px;border-radius:3px}

/* ---------- Tables ---------- */
table{border-collapse:collapse;width:100%;margin:8px 0 26px;font-size:.95rem;background:var(--card)}
th{font-family:var(--display);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;text-align:left;
   background:var(--ink);color:var(--paper);padding:10px 12px}
td{padding:10px 12px;border-bottom:1px solid var(--rule);vertical-align:top}
tr:nth-child(even) td{background:#FBFBF7}

/* ---------- Footer ---------- */
footer{padding:48px 0 64px;color:var(--ink-soft);font-size:.92rem}
footer .colophon{font-family:var(--mono);font-size:.74rem;letter-spacing:.06em;margin-top:14px}
a{color:var(--teal)}
:focus-visible{outline:2px solid var(--teal);outline-offset:2px}
@media print{
  body{font-size:10.5pt}
  .toc-grid a{border:none}
}
</style>
</head>
<body>
<div class="page">

<header class="hero">
  <div class="eyebrow">A Field Manual · For Doctoral Researchers</div>
  <h1>How to Think, How to Learn: <em>The Researcher's Toolkit</em></h1>
  <p class="standfirst">A PhD is less a test of what you know than of how you come to know. This note collects the thinking methods, learning techniques, knowledge systems, and working practices that compound over a doctorate — each one explained, with concrete steps, pitfalls, and a way to try it this week.</p>
  <div class="meta">
    <span>6 PARTS · 21 METHODS</span>
    <span>READING TIME ≈ 45 MIN</span>
    <span>REVISED JUNE 2026</span>
  </div>
</header>

<nav class="toc" aria-label="Table of contents">
  <h2>Contents</h2>
  <div class="toc-grid">
    <a href="#part1"><span class="pt">I</span>How Learning Actually Works</a>
    <a href="#part2"><span class="pt">II</span>Thinking Methods</a>
    <a href="#part3"><span class="pt">III</span>Learning Techniques</a>
    <a href="#part4"><span class="pt">IV</span>Knowledge Systems</a>
    <a href="#part5"><span class="pt">V</span>Working Practices</a>
    <a href="#part6"><span class="pt">VI</span>Putting It Together</a>
  </div>
</nav>

<!-- ================= PART I ================= -->
<div class="part" id="part1">
  <div class="label">Part I</div>
  <h2>How Learning Actually Works</h2>
  <p class="part-intro">Before the methods, three findings from cognitive science. Every technique in this manual works because of one of these mechanisms — knowing them lets you evaluate any new method you encounter, including ones not in this note.</p>
</div>

<section class="method" id="m-foundations">
  <div class="main">
    <div class="kicker">Foundation 01</div>
    <h3>Retrieval Beats Re-reading</h3>
    <div class="specline"><span>MECHANISM: TESTING EFFECT</span><span>EVIDENCE: VERY STRONG</span></div>
    <p>The single most replicated finding in learning research: <strong>memory is strengthened by pulling information out, not by putting it in again.</strong> Re-reading a paper feels productive because the text becomes fluent and familiar — but fluency is recognition, not recall. When you close the PDF and try to reconstruct the argument from nothing, you discover how little transferred. That uncomfortable act of reconstruction is precisely what builds durable knowledge.</p>
    <p>This is why almost every effective technique below — the Feynman technique, active recall, self-explanation, writing summaries from memory — is some disguised form of retrieval practice. The discomfort is the signal that it's working; researchers call these <strong>desirable difficulties</strong>.</p>
  </div>
  <div class="margin">
    <div class="note"><b>Key term</b>Desirable difficulty: a condition that makes practice feel harder and slower but produces stronger long-term retention (Bjork &amp; Bjork).</div>
    <div class="note"><b>The trap</b>The "fluency illusion": mistaking ease of processing for depth of understanding. Highlighted PDFs are its natural habitat.</div>
  </div>
</section>

<section class="method">
  <div class="main">
    <div class="kicker">Foundation 02</div>
    <h3>Forgetting Is a Feature</h3>
    <div class="specline"><span>MECHANISM: SPACING EFFECT</span><span>EVIDENCE: VERY STRONG</span></div>
    <p>Memory decays on a predictable curve (Ebbinghaus, 1885). Each time you retrieve something <em>just as it's about to slip away</em>, the curve flattens — the memory becomes more durable and the next review can come later. Cramming works for tomorrow's exam; spacing works for the knowledge you'll need at your defence in year four.</p>
    <p>The practical consequence: <strong>distribute exposure over time, and let yourself partially forget between exposures.</strong> Reading a seminal paper once carefully is worth less than reading it three times across three months, each time noticing what you'd lost.</p>
  </div>
  <div class="margin">
    <div class="note"><b>Rule of thumb</b>Review intervals that roughly double — 1 day, 3 days, 1 week, 2 weeks, 1 month — capture most of the benefit without software.</div>
  </div>
</section>

<section class="method">
  <div class="main">
    <div class="kicker">Foundation 03</div>
    <h3>Understanding Is Connection</h3>
    <div class="specline"><span>MECHANISM: ELABORATION & SCHEMA</span><span>EVIDENCE: STRONG</span></div>
    <p>Experts don't merely know more facts; their knowledge is <strong>organized differently</strong> — chunked into rich structures (schemas) where each idea is linked to causes, consequences, examples, and contrasts. A new fact that connects to nothing is almost immediately lost; a fact woven into an existing structure is nearly free to retain.</p>
    <p>This is the deep justification for elaborative questioning ("why is this true? when would it fail?"), for analogy, and for note systems like the Zettelkasten that force you to link every new idea to old ones. <strong>Learning is less like filling a container and more like growing a graph</strong> — and you, not the textbook, have to draw the edges.</p>
  </div>
  <div class="margin">
    <div class="note"><b>For the ML-minded</b>A useful (if loose) analogy: isolated facts are like training samples memorized verbatim; schemas are like learned representations that generalize. Elaboration is your regularizer.</div>
  </div>
</section>

<!-- ================= PART II ================= -->
<div class="part" id="part2">
  <div class="label">Part II</div>
  <h2>Thinking Methods</h2>
  <p class="part-intro">Techniques for generating ideas, interrogating claims, and reasoning under uncertainty — the daily work of research. Each entry: what it is, how to run it, where it fails.</p>
</div>

<section class="method" id="m-first-principles">
  <div class="main">
    <div class="kicker">Method 01</div>
    <h3>First-Principles Thinking</h3>
    <div class="specline"><span>ORIGIN: ARISTOTLE</span><span>BEST FOR: STUCK PROBLEMS, NOVELTY</span><span>COST: HIGH EFFORT</span></div>
    <p>Most reasoning is <strong>reasoning by analogy</strong>: "this is how it's done in the field, so we'll do roughly that, slightly modified." It's efficient, and it's also how entire research communities get stuck in local optima. First-principles thinking instead decomposes a problem into its most basic, independently verifiable truths — physical laws, definitions, hard constraints, measured facts — and rebuilds the solution from those, ignoring convention.</p>
    <div class="howto">
      <h4>How to run it</h4>
      <ol>
        <li><strong>State the conventional assumption.</strong> Write down what "everyone knows" about the problem. ("VLA policies need large teleoperation datasets.")</li>
        <li><strong>Interrogate each component.</strong> For each assumption ask: is this a law of nature, a measured fact, or merely an inherited habit? Demand evidence for each.</li>
        <li><strong>Keep only the bedrock.</strong> List the constraints that survive: physics, information-theoretic limits, hard resource budgets, definitions.</li>
        <li><strong>Rebuild upward.</strong> Ask: given only these constraints, what is the space of possible solutions? Often it's far larger than the field's current corner of it.</li>
      </ol>
    </div>
    <p>In research, first principles is most valuable at two moments: when <strong>choosing a problem</strong> (is this limitation fundamental or incidental?) and when <strong>a method mysteriously fails</strong> (what must be true for this to work at all, and which of those preconditions is violated?).</p>
    <div class="pitfall"><b>Pitfall</b>Reinventing wheels. First principles is expensive; reasoning by analogy exists because it's usually right. Use first principles selectively — on the one or two assumptions whose overthrow would matter most — not as a lifestyle.</div>
    <div class="trybox"><b>Try it this week</b>Take one "obvious" assumption in your current project and write a half-page interrogation: what evidence supports it, and what would the design look like if it were false?</div>
  </div>
  <div class="margin">
    <div class="note"><b>Distinguish</b>First principles ≠ "being contrarian." The output is a constraint set, not an opinion. If your bedrock list is empty of physics and full of vibes, you skipped step 2.</div>
    <div class="note"><b>Pairs well with</b>Fermi estimation (Method 07) — quick numbers tell you whether a rebuilt solution is even in the right order of magnitude.</div>
  </div>
</section>

<section class="method" id="m-socratic">
  <div class="main">
    <div class="kicker">Method 02</div>
    <h3>The Socratic Method</h3>
    <div class="specline"><span>ORIGIN: PLATO'S DIALOGUES</span><span>BEST FOR: TESTING UNDERSTANDING & CLAIMS</span><span>COST: LOW</span></div>
    <p>Socratic questioning is <strong>systematic interrogation by question</strong> — pursuing a claim with a disciplined sequence of probes until its foundations are either exposed as solid or shown to be sand. Used on others, it's a teaching tool; used on yourself, it's the cheapest peer review available. The six classical question families:</p>
    <ul>
      <li><strong>Clarification</strong> — "What exactly do I mean by <em>robust</em> here? Could I define it operationally?"</li>
      <li><strong>Probing assumptions</strong> — "What am I taking for granted? What would have to be true?"</li>
      <li><strong>Probing evidence</strong> — "How do I know this? What's the actual experiment, and what else could explain the result?"</li>
      <li><strong>Alternative viewpoints</strong> — "How would a skeptical reviewer frame this? What would the rival lab say?"</li>
      <li><strong>Implications</strong> — "If this is true, what else must be true? Do I believe <em>those</em> things?"</li>
      <li><strong>Questioning the question</strong> — "Why is this the right question at all? What question is it standing in for?"</li>
    </ul>
    <div class="howto">
      <h4>Three research uses</h4>
      <ol>
        <li><strong>Pre-mortem on claims.</strong> Before a lab meeting, run your central claim through all six families in writing. Most reviewer-2 objections surface here, for free.</li>
        <li><strong>Reading papers adversarially.</strong> Interrogate the paper as if the author were across the table. "You say X improves Y — was the baseline tuned as carefully as the method?"</li>
        <li><strong>Advising and being advised.</strong> When your advisor asks "what do you think is going on?", they're doing this to you. Learn to do it to yourself first.</li>
      </ol>
    </div>
    <div class="pitfall"><b>Pitfall</b>Socratic questioning of <em>other people</em> can slide into interrogation theatre. The goal is shared discovery, not winning. On yourself, the failure mode is the opposite: pulling punches. Write the questions down; you lie less on paper.</div>
    <div class="trybox"><b>Try it this week</b>Take your current working hypothesis and write one question from each of the six families, then answer them honestly. Anything you can't answer becomes an experiment.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Original sense</b>Socrates' elenchus aimed at <em>aporia</em> — productive puzzlement. Reaching "I genuinely don't know" is a successful outcome, not a failure. It tells you where the research is.</div>
  </div>
</section>

<section class="method" id="m-inversion">
  <div class="main">
    <div class="kicker">Method 03</div>
    <h3>Inversion</h3>
    <div class="specline"><span>ORIGIN: JACOBI / STOICS</span><span>BEST FOR: PLANNING, FAILURE ANALYSIS</span><span>COST: LOW</span></div>
    <p>"Invert, always invert" (mathematician Carl Jacobi). Instead of asking "how do I succeed?", ask <strong>"what would guarantee failure?"</strong> — then avoid those things. Forward thinking generates options; inverted thinking exposes constraints and hidden risks, and humans are reliably better at spotting flaws than at imagining successes.</p>
    <div class="howto">
      <h4>Two research formats</h4>
      <ol>
        <li><strong>The pre-mortem.</strong> "It is one year from now and this project has failed completely. Write the story of what went wrong." Common entries: the effect was a confound, the baseline was unfair, the dataset was too small, the hardware ate six months. Each story becomes a checklist item now.</li>
        <li><strong>Negative-space hypotheses.</strong> Instead of "what would prove my method works?", ask "what is the cheapest experiment that could <em>kill</em> this idea?" Run that first. Dead ideas are cheapest when young.</li>
      </ol>
    </div>
    <div class="trybox"><b>Try it this week</b>Run a 20-minute pre-mortem on your main project. List five failure stories, then mark which ones you can test or mitigate this month.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Why it works</b>Loss framing recruits more critical scrutiny than gain framing — the same bias that makes reviewers harsh makes your inverted self a better critic.</div>
  </div>
</section>

<section class="method" id="m-strong-inference">
  <div class="main">
    <div class="kicker">Method 04</div>
    <h3>Strong Inference</h3>
    <div class="specline"><span>ORIGIN: PLATT, 1964</span><span>BEST FOR: EXPERIMENT DESIGN</span><span>COST: MEDIUM</span></div>
    <p>John Platt's classic <em>Science</em> paper asked why some fields advance fast and others crawl, and answered: the fast ones practice <strong>strong inference</strong> — a disciplined loop of competing hypotheses and decisive experiments, rather than affectionate accumulation of evidence for one pet idea.</p>
    <div class="howto">
      <h4>The loop</h4>
      <ol>
        <li><strong>Enumerate alternative hypotheses</strong> — not one, but every plausible explanation. (Your policy hovers without grasping: bad labels? distribution shift? action-space scaling? gripper latency? insufficient demonstrations of the final 5&nbsp;cm?)</li>
        <li><strong>Design a crucial experiment</strong> whose possible outcomes <em>exclude</em> at least one hypothesis, whatever the result.</li>
        <li><strong>Run it cleanly</strong>, get an unambiguous answer.</li>
        <li><strong>Recurse</strong> on the survivors.</li>
      </ol>
    </div>
    <p>The discipline is in step 1. Single-hypothesis research invites confirmation bias: every ambiguous result reads as support. Multiple working hypotheses (Chamberlin, 1890) keep you emotionally diversified — you can't fall in love with all of them.</p>
    <div class="pitfall"><b>Pitfall</b>Some questions don't admit decisive experiments (effects are small, systems are entangled). Then the honest version is Bayesian: design experiments to maximize <em>expected information gain</em>, not certainty.</div>
    <div class="trybox"><b>Try it this week</b>For your current bug or anomaly, list five hypotheses before touching anything, then pick the experiment that splits the list most evenly. (Binary search over explanations.)</div>
  </div>
  <div class="margin">
    <div class="note"><b>Quote</b>"The method consists of devising alternative hypotheses; devising a crucial experiment…; carrying out the experiment to get a clean result; recycling the procedure." — paraphrasing Platt (1964)</div>
    <div class="note"><b>Debugging is science</b>Strong inference is exactly principled debugging. The "five hypotheses first" rule prevents the most expensive failure mode: fixing the wrong thing convincingly.</div>
  </div>
</section>

<section class="method" id="m-bayesian">
  <div class="main">
    <div class="kicker">Method 05</div>
    <h3>Bayesian Thinking</h3>
    <div class="specline"><span>ORIGIN: BAYES / LAPLACE</span><span>BEST FOR: REASONING UNDER UNCERTAINTY</span><span>COST: LOW (INFORMAL)</span></div>
    <p>You don't need the formula to think Bayesianly; you need three habits:</p>
    <ul>
      <li><strong>Hold beliefs as probabilities, not verdicts.</strong> "I'm ~70% sure the schema mismatch caused the failure" invites updating; "the schema caused it" invites defending.</li>
      <li><strong>Weigh evidence by its likelihood ratio.</strong> Ask not "is this consistent with my hypothesis?" but "is this <em>more</em> consistent with my hypothesis than with the alternatives?" A result every hypothesis predicts is worth nothing.</li>
      <li><strong>Respect base rates.</strong> Most surprising results are bugs; most "huge improvements" shrink on the second seed; most projects take 2–3× the estimate. Extraordinary posterior requires extraordinary likelihood.</li>
    </ul>
    <p>For a researcher the deepest use is calibration: track your predictions ("I expect the ablation to drop ≥5 points — 80% confident") and review them. Systematic over-confidence in your own methods is the default human state; written predictions are the antidote.</p>
    <div class="trybox"><b>Try it this week</b>Before your next experiment finishes, write a one-line prediction with a probability. Grade it after. Ten of these will teach you more about your judgment than any course.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Slogan</b>Strong opinions, weakly held — but with the strength stated numerically, so "weakly" is auditable.</div>
  </div>
</section>

<section class="method" id="m-analogical">
  <div class="main">
    <div class="kicker">Method 06</div>
    <h3>Analogical & Lateral Thinking</h3>
    <div class="specline"><span>BEST FOR: IDEA GENERATION, TRANSFER</span><span>COST: LOW</span></div>
    <p>If first principles is for depth, analogy is for breadth. Most genuinely new ideas in a field are old ideas from a neighboring field wearing new notation: attention from machine translation into vision; diffusion from thermodynamics into generative modeling; control-theoretic ideas resurfacing as RL. The skill is <strong>structural mapping</strong> — matching the relations in a problem, not its surface features.</p>
    <div class="howto">
      <h4>Deliberate analogy hunting</h4>
      <ol>
        <li><strong>Abstract your problem one level up.</strong> "Grasping under perception noise" → "acting on uncertain state estimates" → "decision-making with partial observability."</li>
        <li><strong>Ask who else has the abstract problem.</strong> Aviation? Finance? Ecology? Operations research solved versions of many lab problems decades ago.</li>
        <li><strong>Import the structure, re-derive the details.</strong> The analogy gives you a candidate skeleton; first principles checks whether it survives your domain's constraints.</li>
      </ol>
    </div>
    <p>Cultivate this by reading <em>outside</em> your subfield on a schedule — a survey from an adjacent field once a month does more for originality than another reading of your own field's latest preprints.</p>
    <div class="pitfall"><b>Pitfall</b>Surface analogies ("the brain is like a transformer") mislead exactly as confidently as structural ones illuminate. Always identify which relations the analogy is claiming to preserve — and where it must break.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Mental models</b>Charlie Munger's "latticework of mental models" is this practiced as a lifestyle: collect the few big ideas of many disciplines (feedback loops, selection effects, equilibria, compounding) and run every problem past the lattice.</div>
  </div>
</section>

<section class="method" id="m-fermi">
  <div class="main">
    <div class="kicker">Method 07</div>
    <h3>Fermi Estimation & Back-of-the-Envelope</h3>
    <div class="specline"><span>ORIGIN: ENRICO FERMI</span><span>BEST FOR: SANITY CHECKS, SCOPING</span><span>COST: MINUTES</span></div>
    <p>The ability to get within an order of magnitude using decomposition and known anchors. For researchers it is primarily a <strong>filter</strong>: a five-minute estimate kills infeasible plans before they cost five months.</p>
    <ul>
      <li>"How many demonstrations can I realistically collect?" — episodes per hour × hours per week × usable weeks. If the answer is 2,000 and the method needs 50,000, the project is a data-efficiency project now, whatever the original title said.</li>
      <li>"Will this fit?" — parameters × bytes × activation overhead vs. device memory. Estimate before provisioning.</li>
      <li>"Is this effect plausible?" — if a claimed improvement implies your sensor exceeds its physical noise floor, the claim has a bug.</li>
    </ul>
    <div class="trybox"><b>Try it this week</b>Estimate the total wall-clock cost (data + training + evaluation + writing) of your next planned experiment before starting it. Compare with reality afterward; your personal correction factor is reusable forever.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Technique</b>Estimate in logarithms: choose between 1, 3, 10, 30, 100… Errors then tend to cancel across the chain of factors.</div>
  </div>
</section>

<section class="method" id="m-polya">
  <div class="main">
    <div class="kicker">Method 08</div>
    <h3>Pólya's Problem-Solving Heuristics</h3>
    <div class="specline"><span>ORIGIN: HOW TO SOLVE IT, 1945</span><span>BEST FOR: HARD TECHNICAL PROBLEMS</span><span>COST: LOW</span></div>
    <p>George Pólya's four phases — <strong>understand, plan, execute, look back</strong> — sound trivial until you notice that stuck researchers are almost always stuck because they skipped phase one or four. The named heuristics within the phases are the real toolkit:</p>
    <ul>
      <li><strong>Solve a simpler problem first.</strong> Can't get the full pipeline working? Solve the 1-D version, the noiseless version, the two-object version. (In ML: overfit a single batch before training at scale.)</li>
      <li><strong>Work backwards</strong> from the desired result to the data you'd need.</li>
      <li><strong>Exploit symmetry and invariants</strong> — what must stay constant, and does your solution respect it?</li>
      <li><strong>Have you seen a related problem?</strong> — the analogical bridge again.</li>
      <li><strong>Check the extreme cases.</strong> Set the parameter to 0 and to ∞; if the method's behavior there surprises you, you don't understand it yet.</li>
      <li><strong>Look back.</strong> After solving, ask: what was the actual key step? Could it solve anything else? This is where one solved problem becomes a transferable technique.</li>
    </ul>
  </div>
  <div class="margin">
    <div class="note"><b>The neglected phase</b>"Looking back" is where research taste is built. A solved problem without a retrospective is consumed; with one, it's invested.</div>
  </div>
</section>

<section class="method" id="m-steelman">
  <div class="main">
    <div class="kicker">Method 09</div>
    <h3>Steelmanning & Red-Teaming Your Own Work</h3>
    <div class="specline"><span>BEST FOR: WRITING, REBUTTALS, ROBUST CLAIMS</span><span>COST: MEDIUM</span></div>
    <p>The strawman attacks the weakest version of an opposing view; the <strong>steelman constructs the strongest version</strong> — sometimes stronger than its actual proponents manage — and engages with that. For a researcher this has two faces:</p>
    <ol>
      <li><strong>Steelman the rival approach.</strong> Before claiming your method beats the baseline, give the baseline its best hyperparameters, its fairest evaluation, its most charitable interpretation. If you win against the steelman, the claim survives review; if you only beat the strawman, a reviewer will build the steelman for you, publicly.</li>
      <li><strong>Red-team your own paper.</strong> Allocate a real session (not a guilty afterthought) to attacking your own draft as a hostile expert: alternative explanations, missing ablations, overgeneralized claims, statistical sins. Write the imagined review, then fix or pre-empt each point in the text.</li>
    </ol>
    <div class="trybox"><b>Try it this week</b>Write the single harshest fair sentence a reviewer could say about your current project. If you can't answer it yet, you've just found your next experiment.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Social version</b>Ask a labmate to play the adversary for 30 minutes, with explicit permission to be ruthless. Reciprocate. This is among the highest-value trades in any lab.</div>
  </div>
</section>

<!-- ================= PART III ================= -->
<div class="part" id="part3">
  <div class="label">Part III</div>
  <h2>Learning Techniques</h2>
  <p class="part-intro">A PhD demands learning at two speeds: deep mastery of your niche, and rapid functional literacy in whatever the project needs next month. These techniques cover both.</p>
</div>

<section class="method" id="m-feynman">
  <div class="main">
    <div class="kicker">Method 10</div>
    <h3>The Feynman Technique</h3>
    <div class="specline"><span>BEST FOR: DEEP UNDERSTANDING</span><span>MECHANISM: RETRIEVAL + ELABORATION</span><span>COST: 30–60 MIN/TOPIC</span></div>
    <p>Richard Feynman's reputed test of understanding: <strong>if you can't explain it simply, you don't understand it.</strong> The technique operationalizes this as a four-step loop that converts vague familiarity into genuine command — and pinpoints exactly where your understanding is hollow.</p>
    <div class="howto">
      <h4>The loop</h4>
      <ol>
        <li><strong>Choose a concept and write its name at the top of a blank page.</strong> ("Flow-matching action heads." "KKT conditions." "Why batch norm interacts badly with small batches.")</li>
        <li><strong>Explain it in plain language</strong>, from memory, as if to a smart undergraduate — concrete examples, no jargon you can't immediately unpack.</li>
        <li><strong>Find the cracks.</strong> Wherever you stall, reach for jargon as a shield, or wave your hands — that's a precise map of what you don't know. Go back to the source <em>for those points only</em>.</li>
        <li><strong>Simplify and analogize.</strong> Rewrite until the explanation flows; create an analogy for the hardest part. If the analogy breaks, find where and say why — that's understanding too.</li>
      </ol>
    </div>
    <p>The technique works because it stacks three mechanisms from Part I: retrieval (step 2 is closed-book), elaboration (analogies force connection), and metacognitive monitoring (step 3 makes ignorance visible instead of comfortable).</p>
    <div class="pitfall"><b>Pitfall</b>Doing it open-book. With the source visible, you're paraphrasing, not retrieving, and the cracks never show. The blank page is the instrument.</div>
    <div class="trybox"><b>Try it this week</b>Pick the concept from your field you're most likely to be asked about at your next talk's Q&A. One page, closed book, 25 minutes. Whatever you couldn't explain becomes the week's reading list.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Variant for researchers</b>"Feynman a paper": after reading, close it and write the abstract from memory in your own words, including the one experiment that carries the claim. Compare. The diff is your comprehension gap.</div>
  </div>
</section>

<section class="method" id="m-recall-spacing">
  <div class="main">
    <div class="kicker">Method 11</div>
    <h3>Active Recall & Spaced Repetition</h3>
    <div class="specline"><span>BEST FOR: DURABLE FACTUAL FOUNDATION</span><span>EVIDENCE: STRONGEST IN THE LITERATURE</span><span>COST: 10–15 MIN/DAY</span></div>
    <p>The direct application of Foundations 01 and 02. Active recall = self-testing instead of re-reading; spaced repetition = scheduling those tests at expanding intervals, usually via software (Anki, RemNote, Mochi) that implements the scheduling for you.</p>
    <p>For a PhD researcher the question is <em>what deserves a card</em>. Carding everything is a famous way to burn out. Good candidates:</p>
    <ul>
      <li><strong>Load-bearing definitions and theorems</strong> you must produce fluently (your quals/comprehensive material).</li>
      <li><strong>Key numbers of your field</strong> — canonical benchmark scores, dataset sizes, physical constants, typical magnitudes. Fermi estimation (Method 07) runs on these anchors.</li>
      <li><strong>The one-sentence contribution of each important paper</strong> in your literature — so related work flows from memory when writing and reviewing.</li>
      <li><strong>Your own hard-won lessons</strong> — "stale HF cache masks schema fixes; clear it before re-debugging" is exactly the kind of thing you'll need again in eight months and won't recall.</li>
    </ul>
    <div class="howto">
      <h4>Card-writing rules that prevent burnout</h4>
      <ol>
        <li><strong>One atomic fact per card.</strong> Composite cards fail forever and breed resentment.</li>
        <li><strong>Card only after understanding.</strong> Cards maintain knowledge; they don't create it. Feynman first, Anki second.</li>
        <li><strong>Delete ruthlessly.</strong> A card that annoys you twice gets rewritten or removed. The deck serves you.</li>
      </ol>
    </div>
  </div>
  <div class="margin">
    <div class="note"><b>No-software version</b>End each reading session by writing 3 questions on the source's first page. Answer them before your next session with that material. Crude spacing, most of the benefit.</div>
  </div>
</section>

<section class="method" id="m-interleaving">
  <div class="main">
    <div class="kicker">Method 12</div>
    <h3>Interleaving & Varied Practice</h3>
    <div class="specline"><span>BEST FOR: SKILLS & PROBLEM CLASSIFICATION</span><span>MECHANISM: DISCRIMINATION LEARNING</span><span>COST: FREE (REORDERING)</span></div>
    <p>Blocked practice (AAA BBB CCC) feels smooth and produces fast short-term gains; interleaved practice (ABC CAB BCA) feels rough and produces better long-term transfer. The reason: mixing forces you to <strong>identify which kind of problem you're facing</strong> before solving it — and in research, problem identification is most of the difficulty.</p>
    <p>Applications: when learning a mathematical toolkit, mix problem types within a session rather than grinding one chapter; when learning a field, alternate between theory papers, methods papers, and applications rather than reading monothematically; when practicing derivations, shuffle them so the cue "which technique applies?" gets trained too.</p>
    <div class="pitfall"><b>Pitfall</b>Interleaving feels worse while you do it — slower, more errors — which tempts you back to blocking. Judge by next-week performance, not session-end performance.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Caveat</b>Total beginners benefit from a short blocked phase first to acquire the basic procedure; interleave once you can execute each type slowly.</div>
  </div>
</section>

<section class="method" id="m-deliberate">
  <div class="main">
    <div class="kicker">Method 13</div>
    <h3>Deliberate Practice</h3>
    <div class="specline"><span>ORIGIN: ERICSSON</span><span>BEST FOR: RESEARCH CRAFT SKILLS</span><span>COST: SUSTAINED</span></div>
    <p>Experience alone does not produce expertise — ten years of casual practice produces ten years of plateau. Deliberate practice is what does: <strong>focused work on the specific component just beyond your current ability, with immediate feedback and repetition.</strong> A PhD quietly assumes you'll do this for its core crafts, but never schedules it. Schedule it yourself for:</p>
    <ul>
      <li><strong>Writing.</strong> Don't just "write more" — isolate the weak component. Bad abstracts? Write five abstracts of published papers from their introductions, compare to the real ones. Muddy paragraphs? Rewrite one paragraph five ways.</li>
      <li><strong>Talks.</strong> Record yourself; review with the same ruthlessness as a training curve. Practice the 60-second version of your research until it's reflexive.</li>
      <li><strong>Reviewing.</strong> Review papers (journal clubs, OpenReview) and compare your assessment against the eventual official reviews — that's the feedback loop.</li>
      <li><strong>Technical fluency.</strong> Re-derive the key results of your field from scratch on a schedule; implement the canonical algorithm without reference once.</li>
    </ul>
    <p>The defining features to check: is it <em>effortful</em>, is it <em>targeted at a weakness</em>, is there <em>fast feedback</em>, and is there <em>repetition with refinement</em>? If an activity has all four, it builds skill; if not, it merely accumulates hours.</p>
  </div>
  <div class="margin">
    <div class="note"><b>Feedback sources</b>Advisors are slow feedback; build fast loops too — labmates, writing groups, recorded rehearsals, and comparing your work against exemplars you reverse-engineer.</div>
  </div>
</section>

<section class="method" id="m-teaching">
  <div class="main">
    <div class="kicker">Method 14</div>
    <h3>Learning by Teaching (the Protégé Effect)</h3>
    <div class="specline"><span>BEST FOR: CONSOLIDATION</span><span>COST: USUALLY ALREADY REQUIRED OF YOU</span></div>
    <p>Preparing to teach produces deeper encoding than preparing for a test of the same material — you organize, anticipate questions, and generate examples, which is elaboration at industrial intensity. The PhD is full of conscripted teaching (TA-ing, journal club, mentoring undergrads); the method is simply to <strong>stop treating these as taxes and start treating them as your consolidation schedule.</strong></p>
    <ul>
      <li>Volunteer to present the papers you most need to understand, not the ones you already do.</li>
      <li>Mentor a junior student through the exact pipeline you just learned — their naive questions ("why is the cache a problem at all?") are Socratic probes you'd never aim at yourself.</li>
      <li>Maintain a public-facing explanation channel (blog, internal wiki, lab talks). Writing for an audience enforces the Feynman standard with real stakes.</li>
    </ul>
    <div class="trybox"><b>Try it this week</b>Claim the next journal-club slot for the paper that intimidates you most.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Rubber-duck corollary</b>Explaining a bug aloud to an inert listener routinely dissolves it — verbalization forces serial, explicit inspection of assumptions your eyes skip over.</div>
  </div>
</section>

<!-- ================= PART IV ================= -->
<div class="part" id="part4">
  <div class="label">Part IV</div>
  <h2>Knowledge Systems</h2>
  <p class="part-intro">A doctorate produces thousands of papers read, ideas had, and lessons learned. Without a system, this evaporates; with one, it compounds into your thesis, your papers, and your taste. The system matters less than its properties: written, linked, and revisited.</p>
</div>

<section class="method" id="m-zettelkasten">
  <div class="main">
    <div class="kicker">Method 15</div>
    <h3>The Zettelkasten (Linked Note System)</h3>
    <div class="specline"><span>ORIGIN: NIKLAS LUHMANN</span><span>BEST FOR: IDEA DEVELOPMENT OVER YEARS</span><span>COST: 20–30 MIN/DAY</span></div>
    <p>Sociologist Niklas Luhmann published ~70 books and 400 papers, and credited a box of ~90,000 interlinked notes as his collaborator. The modern version (Obsidian, Logseq, plain Markdown + grep) rests on three note types and one discipline:</p>
    <div class="howto">
      <h4>The architecture</h4>
      <ol>
        <li><strong>Fleeting notes</strong> — capture anything, anywhere, fast. Inbox, not archive. Processed within a day or two, then discarded.</li>
        <li><strong>Literature notes</strong> — per source: the claim, the evidence, the limitation, <em>in your own words</em> (retrieval, again), with the citation.</li>
        <li><strong>Permanent notes</strong> — one idea per note, written as a full claim in prose ("Linguistic perturbations degrade VLA success rates non-uniformly: semantic > syntactic"), each <strong>explicitly linked</strong> to the existing notes it supports, contradicts, or refines.</li>
      </ol>
    </div>
    <p>The discipline is the linking. A note with no links is a dead fact; the forced question "what does this connect to?" is where research ideas actually come from — two notes from different months colliding. Over a year, clusters of linked notes literally become paper outlines: Luhmann claimed he never forced himself to write, he just harvested the box.</p>
    <div class="pitfall"><b>Pitfall</b>The collector's fallacy: hoarding PDFs, highlights, and clipped passages feels like knowledge work but stores other people's words, not your understanding. If a "note" contains no sentence you composed, it isn't one yet.</div>
    <div class="trybox"><b>Try it this week</b>Convert the last three papers you read into one literature note each (3–5 sentences, closed book), and write one permanent note connecting two of them.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Reference</b>Sönke Ahrens, <em>How to Take Smart Notes</em> — the standard modern treatment, written specifically for academics.</div>
    <div class="note"><b>Tooling note</b>The tool is irrelevant; plain text files outlive every app. Optimize for friction-free capture and reliable search, nothing else.</div>
  </div>
</section>

<section class="method" id="m-litreview">
  <div class="main">
    <div class="kicker">Method 16</div>
    <h3>Structured Literature Practice</h3>
    <div class="specline"><span>BEST FOR: READING AT PHD VOLUME</span><span>COST: REPLACES UNSTRUCTURED READING</span></div>
    <p>You cannot read everything; you must read <em>strategically and in passes</em>. The widely used three-pass method (Keshav):</p>
    <div class="howto">
      <h4>Three passes</h4>
      <ol>
        <li><strong>Pass 1 (5–10 min):</strong> title, abstract, intro, section headings, conclusion, a glance at figures. Output: category, context, correctness-at-a-glance, and a keep/discard decision. Most papers end here, legitimately.</li>
        <li><strong>Pass 2 (~1 hr):</strong> read carefully, ignore proofs; scrutinize figures and tables (axes, error bars, baselines — this is where claims live and die); mark references to chase.</li>
        <li><strong>Pass 3 (several hrs, rare):</strong> virtual re-implementation — reconstruct the work mentally or in code, making every assumption explicit. Reserve for the papers your own work stands on.</li>
      </ol>
    </div>
    <p>Pair the passes with a <strong>synthesis matrix</strong> for any literature review: a table of papers × dimensions (problem, method, data, evaluation, key limitation). Gaps in the matrix are visible research opportunities — and the matrix later writes your related-work section nearly by itself.</p>
    <ul>
      <li><strong>Read citation graphs, not feeds.</strong> From a seminal paper, walk backward (its references) and forward (papers citing it, via Semantic Scholar / Connected Papers) — structure beats chronology.</li>
      <li><strong>Quarantine the firehose.</strong> Skim new-paper feeds on a schedule (e.g., 30 min, twice a week), pass-1 only, queue the survivors. Continuous skimming destroys deep work (Method 18) for negligible gain.</li>
    </ul>
  </div>
  <div class="margin">
    <div class="note"><b>Adversarial reading</b>On pass 2, run the Socratic families (Method 02) against the paper. The habit of asking "what would make this result an artifact?" is what separates literate readers from trained ones.</div>
  </div>
</section>

<section class="method" id="m-journal">
  <div class="main">
    <div class="kicker">Method 17</div>
    <h3>The Research Journal & Decision Log</h3>
    <div class="specline"><span>BEST FOR: CONTINUITY, HONESTY, THESIS-WRITING</span><span>COST: 10 MIN/DAY</span></div>
    <p>A daily working log: what you tried, what happened, what you concluded, what's next — plus, crucially, <strong>predictions before experiments and decisions with their reasons.</strong> Three compounding payoffs:</p>
    <ul>
      <li><strong>Continuity.</strong> Research is constantly interrupted (hardware delays, reviews, teaching). "What's next" written by yesterday-you eliminates the 40-minute reload tax.</li>
      <li><strong>Epistemic honesty.</strong> Pre-registered predictions (Method 05) and logged negative results inoculate against the gentle self-deception of remembering only the runs that worked.</li>
      <li><strong>Raw material.</strong> Methods sections, thesis chapters, and "lessons learned" talks assemble themselves from a good log. Six months of debugging GR00T-style hover failures is a war story worth a workshop paper — if it was written down.</li>
    </ul>
    <div class="howto">
      <h4>A minimal template (5 lines, end of day)</h4>
      <ol>
        <li><strong>Did:</strong> the one-line summary of today's work.</li>
        <li><strong>Result:</strong> what actually happened, numbers included.</li>
        <li><strong>Surprise:</strong> anything that contradicted expectations (this line is gold).</li>
        <li><strong>Decision:</strong> any choice made, and why — future-you will litigate this.</li>
        <li><strong>Next:</strong> the first concrete action for tomorrow.</li>
      </ol>
    </div>
  </div>
  <div class="margin">
    <div class="note"><b>Pairs with</b>Experiment trackers (W&B, MLflow) log the runs; the journal logs the <em>reasoning between</em> runs — which is the part no tool captures and the part that constitutes research.</div>
  </div>
</section>
<!-- ================= PART V ================= -->
<div class="part" id="part5">
  <div class="label">Part V</div>
  <h2>Working Practices</h2>
  <p class="part-intro">Thinking methods fail without the conditions to run them. These practices protect attention, convert vague intentions into experiments, and keep a multi-year project pointed somewhere.</p>
</div>

<section class="method" id="m-deepwork">
  <div class="main">
    <div class="kicker">Method 18</div>
    <h3>Deep Work & Attention Management</h3>
    <div class="specline"><span>ORIGIN: NEWPORT (TERM); OLD PRACTICE</span><span>BEST FOR: EVERYTHING HARD</span><span>COST: REQUIRES DEFENDING</span></div>
    <p>Deep work: cognitively demanding effort in a state of distraction-free concentration. The research findings underneath it are blunt: <strong>attention residue</strong> means each glance at Slack degrades the next several minutes of thought, and hard problems (proofs, designs, debugging entangled systems) require loading large mental state that interruptions evict entirely. A researcher's output correlates with deep hours, not total hours.</p>
    <div class="howto">
      <h4>Implementation</h4>
      <ol>
        <li><strong>Schedule blocks, don't await mood.</strong> 2–4 protected hours, ideally at your best time of day, on the calendar like a meeting with your most important collaborator (yourself).</li>
        <li><strong>Define done before starting.</strong> "Work on the controller" invites drift; "produce a plot of settling-time vs. gain for three values" is a deep-work target.</li>
        <li><strong>Make distraction physically expensive.</strong> Phone in another room, notifiers quit, one ritual location. Willpower is a budget; spend architecture instead.</li>
        <li><strong>Close with a shutdown note</strong> — current state + next action — so re-entry tomorrow costs minutes, not an hour.</li>
      </ol>
    </div>
    <p>Variants for taste: <strong>Pomodoro</strong> (25 min on / 5 off) suits aversive tasks and trains the focus muscle; long unbroken blocks suit problems with heavy mental state. <strong>Timeboxing</strong> — giving a task a fixed budget — exploits Parkinson's law and, in research, caps the sunk-cost spiral ("two more days on this bug, then I switch strategy and ask for help").</p>
    <div class="pitfall"><b>Pitfall</b>Performing busyness — replying instantly, attending everything — is the path of least resistance in any lab and is rewarded socially while costing you the only hours that produce a thesis. Negotiate availability windows explicitly; most people only need predictability, not immediacy.</div>
  </div>
  <div class="margin">
    <div class="note"><b>Diagnostic</b>Count last week's genuinely deep hours. Most PhD students who do this for the first time find a number under ten — and a thesis is built almost entirely out of those hours.</div>
  </div>
</section>

<section class="method" id="m-hamming">
  <div class="main">
    <div class="kicker">Method 19</div>
    <h3>Hamming Questions (Problem Selection)</h3>
    <div class="specline"><span>ORIGIN: "YOU AND YOUR RESEARCH," 1986</span><span>BEST FOR: CHOOSING WHAT TO WORK ON</span><span>COST: ONE UNCOMFORTABLE HOUR, QUARTERLY</span></div>
    <p>Richard Hamming's famous Bell Labs talk reduces career-scale strategy to questions he literally asked colleagues at lunch, to their annoyance and benefit:</p>
    <ul>
      <li><strong>What are the important problems in your field?</strong></li>
      <li><strong>Why aren't you working on one of them?</strong></li>
      <li>And the qualifier most people miss: an important problem is one that is important <em>and attackable</em> — you need an angle of attack, not just admiration for the problem's size.</li>
    </ul>
    <p>Supporting habits from the same talk: keep <strong>"open doors"</strong> (researchers who stay exposed to colleagues' problems do better long-term than those who isolate for efficiency); cultivate <strong>preparation for luck</strong> ("luck favors the prepared mind" — the prepared mind is built by the methods in Parts II–IV); and tolerate <strong>ambiguity</strong>: believe your theory enough to push it, doubt it enough to notice the anomaly that becomes the next paper.</p>
    <div class="trybox"><b>Try it this week</b>Write your field's three most important attackable problems, and one honest sentence on how your current project relates to any of them. Revisit quarterly; drift is information.</div>
  </div>
  <div class="margin">
    <div class="note"><b>PhD translation</b>You can't always choose the important problem — funding and advisors constrain. But you can usually choose the <em>important version</em> of your assigned problem: the general mechanism behind the specific system.</div>
  </div>
</section>

<section class="method" id="m-metacognition">
  <div class="main">
    <div class="kicker">Method 20</div>
    <h3>Metacognition & the Weekly Review</h3>
    <div class="specline"><span>BEST FOR: STEERING; CATCHING DRIFT EARLY</span><span>COST: 30 MIN/WEEK</span></div>
    <p>Metacognition — monitoring and regulating your own thinking — is the master skill the others hang from: it's what tells you <em>which</em> method the current situation needs. The most reliable way to make it routine is a fixed weekly review:</p>
    <div class="howto">
      <h4>A 30-minute weekly review</h4>
      <ol>
        <li><strong>Reread the week's journal entries</strong> (Method 17). What actually moved? What did I predict vs. observe?</li>
        <li><strong>Classify how you're stuck</strong>, if stuck: missing knowledge (→ learn: Methods 10–12), unclear problem (→ clarify: Methods 02, 08), untested assumptions (→ test: Methods 03, 04), or no protected time (→ Method 18). Different stucknesses, different medicine.</li>
        <li><strong>Check the strategy layer.</strong> Is this week's work still on the path to the quarter's goal? Am I polishing a dead branch because it's comfortable?</li>
        <li><strong>Set the next week's one most-important outcome</strong>, and schedule the deep blocks that produce it.</li>
      </ol>
    </div>
    <p>Calibration belongs here too: review your written predictions (Method 05) and your time estimates (Method 07). The goal isn't self-criticism; it's building an accurate model of your own research process — the instrument you'll use for the rest of your career.</p>
  </div>
  <div class="margin">
    <div class="note"><b>Question bank</b>"What do I believe today that I didn't last month?" "What's the cheapest experiment that would change my plans?" "What am I avoiding, and is the avoidance information?"</div>
  </div>
</section>

<section class="method" id="m-collab">
  <div class="main">
    <div class="kicker">Method 21</div>
    <h3>Thinking With Others (and With Machines)</h3>
    <div class="specline"><span>BEST FOR: ESCAPING YOUR OWN PRIORS</span><span>COST: SOCIAL CAPITAL, WISELY SPENT</span></div>
    <p>Every method so far runs inside one head, and one head has fixed priors. The corrective is structured external thinking:</p>
    <ul>
      <li><strong>Explain-to-understand conversations.</strong> The lab whiteboard session where you present a half-formed idea and field naive questions is the Socratic method with free labor. Offer it back generously; labs with this culture out-produce labs without it.</li>
      <li><strong>Writing as thinking.</strong> "Writing is nature's way of letting you know how sloppy your thinking is" (Guindon). Drafting the introduction <em>before</em> the experiments are done — the claim, the gap, the planned evidence — exposes incoherent projects while they're still cheap to fix. (Some labs formalize this as writing the imagined abstract first.)</li>
      <li><strong>AI as sparring partner.</strong> Modern assistants are strong at the adversarial roles: "steelman the opposite conclusion," "act as Reviewer 2 on this draft," "list ten alternative explanations for this result," "question every assumption in this plan." Use them where independence from your priors matters — and never as a substitute for the closed-book retrieval that builds your own understanding. Generated explanations you merely read are someone else's schema; the fluency illusion applies with full force.</li>
    </ul>
  </div>
  <div class="margin">
    <div class="note"><b>Rule of thumb</b>Use external minds (human or machine) to <em>attack, broaden, and check</em> your thinking; use solitary retrieval and writing to <em>build</em> it.</div>
  </div>
</section>

<!-- ================= PART VI ================= -->
<div class="part" id="part6">
  <div class="label">Part VI</div>
  <h2>Putting It Together</h2>
  <p class="part-intro">Twenty-one methods is a menu, not a regimen. Here is the minimal combination that covers the mechanisms, a map of what to reach for when, and the failure modes of method-collecting itself.</p>
</div>

<section class="method" id="m-system">
  <div class="main">
    <div class="kicker">Synthesis</div>
    <h3>A Minimal Operating System for a PhD</h3>
    <div class="specline"><span>TOTAL OVERHEAD: ≈ 45 MIN/DAY + 30 MIN/WEEK</span></div>
    <table>
      <thead><tr><th>Cadence</th><th>Practice</th><th>Methods it carries</th></tr></thead>
      <tbody>
        <tr><td><strong>Daily</strong></td><td>2–4 hr protected deep block with a defined "done"</td><td>Deep work (18), timeboxing</td></tr>
        <tr><td><strong>Daily</strong></td><td>5-line journal entry: did / result / surprise / decision / next</td><td>Journal (17), Bayesian calibration (05)</td></tr>
        <tr><td><strong>Daily</strong></td><td>10–15 min spaced review of your card deck or question lists</td><td>Recall &amp; spacing (11)</td></tr>
        <tr><td><strong>Per paper read</strong></td><td>Three-pass read → closed-book literature note → link it</td><td>Lit practice (16), Zettelkasten (15), Feynman (10)</td></tr>
        <tr><td><strong>Per experiment</strong></td><td>Five hypotheses + a written prediction before running anything</td><td>Strong inference (04), inversion (03), Bayes (05)</td></tr>
        <tr><td><strong>Weekly</strong></td><td>30-min review: reread journal, classify stuckness, set next outcome</td><td>Metacognition (20)</td></tr>
        <tr><td><strong>Monthly</strong></td><td>One Feynman page on a core concept; one survey from an adjacent field</td><td>Feynman (10), analogy (06)</td></tr>
        <tr><td><strong>Quarterly</strong></td><td>Hamming hour: important problems, angle of attack, project drift check; one pre-mortem on the main project</td><td>Hamming (19), inversion (03), steelman (09)</td></tr>
      </tbody>
    </table>
    <p>Adopt this incrementally — one row at a time, two weeks per row. A habit that survives a deadline crunch is installed; one adopted in a motivated weekend rarely is.</p>
  </div>
  <div class="margin">
    <div class="note"><b>Start here</b>If you adopt only two rows: the daily deep block and the per-experiment predictions. They have the highest yield per minute of overhead.</div>
  </div>
</section>

<section class="method" id="m-lookup">
  <div class="main">
    <div class="kicker">Quick Reference</div>
    <h3>"I Am Currently…" — A Situation Map</h3>
    <table>
      <thead><tr><th>Situation</th><th>Reach for</th></tr></thead>
      <tbody>
        <tr><td>Stuck on a hard technical problem</td><td>Pólya (08): simpler version, extreme cases, work backwards; then rubber-duck it (14)</td></tr>
        <tr><td>An experiment gave a confusing result</td><td>Strong inference (04): five hypotheses, splitting experiment; Bayes (05): which hypothesis does this favor?</td></tr>
        <tr><td>Can't decide if a project idea is good</td><td>Fermi (07) for feasibility, Hamming (19) for importance, pre-mortem (03) for risk</td></tr>
        <tr><td>Need to learn a new field fast</td><td>Citation-graph reading (16), Feynman pages (10) on the 5 core concepts, card the anchors (11)</td></tr>
        <tr><td>The field's standard approach feels wrong</td><td>First principles (01): isolate the bedrock constraints, rebuild</td></tr>
        <tr><td>Writing a paper / rebuttal</td><td>Steelman the baseline and the reviewer (09), Socratic pass on every claim (02)</td></tr>
        <tr><td>Drowning in PDFs, retaining nothing</td><td>Three-pass triage (16), literature notes in your own words (15), accept that most papers end at pass 1</td></tr>
        <tr><td>Busy all week, nothing moved</td><td>Deep-work audit (18), weekly review (20), one most-important outcome</td></tr>
        <tr><td>Suspect I'm fooling myself about my method</td><td>Written predictions (05), kill-experiments (03), red-team session (09)</td></tr>
        <tr><td>Explaining my research and it comes out muddled</td><td>Feynman loop (10) until the one-page version flows; deliberate practice on the 60-second version (13)</td></tr>
      </tbody>
    </table>
  </div>
  <div class="margin">
    <div class="note"><b>Meta-rule</b>When unsure which method applies, that's a metacognition moment (20): first classify the stuckness — knowledge, clarity, assumptions, or time — then choose.</div>
  </div>
</section>

<section class="method" id="m-warnings">
  <div class="main">
    <div class="kicker">Final Warnings</div>
    <h3>How Method-Collecting Goes Wrong</h3>
    <ul>
      <li><strong>Productivity procrastination.</strong> Tweaking your Zettelkasten schema is more pleasant than confronting the experiment that might kill your hypothesis. Systems overhead should stay under ~10% of work time; the rest is the work.</li>
      <li><strong>The fluency illusion, everywhere.</strong> Re-reading, re-watching, highlighting, and reading AI-generated summaries all feel like learning and mostly aren't. If there's no closed-book production step, be suspicious.</li>
      <li><strong>Confusing capture with understanding.</strong> A thousand clipped highlights are a museum of other people's sentences. The unit of knowledge is a claim you wrote, linked to others you wrote.</li>
      <li><strong>Rigor as procrastination's evil twin.</strong> Five hypotheses and a pre-mortem for a 10-minute experiment is theatre. Match the method's weight to the decision's stakes; cheap experiments should just be run.</li>
      <li><strong>Solitary perfectionism.</strong> Every method here improves with other people involved earlier than feels comfortable. Half-formed ideas shown at the whiteboard beat polished ideas shown too late to change.</li>
      <li><strong>Forgetting the point.</strong> These methods exist to produce true, important, well-communicated findings — and a trained mind. Any practice that stops serving that gets deleted, like a bad flashcard.</li>
    </ul>
    <blockquote>
      "The first principle is that you must not fool yourself — and you are the easiest person to fool."
      <span class="who">— RICHARD FEYNMAN, CALTECH COMMENCEMENT, 1974</span>
    </blockquote>
    <p>That sentence is the entire manual in one line. Every method above — retrieval instead of re-reading, predictions before results, hypotheses in plural, steelmen instead of strawmen, logs instead of memory — is a different defense against the same adversary. Build the defenses while the stakes are a PhD; you'll use them for the rest of a career.</p>
  </div>
  <div class="margin">
    <div class="note"><b>Further reading</b>Ahrens, <em>How to Take Smart Notes</em> · Brown et al., <em>Make It Stick</em> · Newport, <em>Deep Work</em> · Pólya, <em>How to Solve It</em> · Platt, "Strong Inference" (1964) · Hamming, "You and Your Research" (1986) · Keshav, "How to Read a Paper".</div>
  </div>
</section>

<footer>
  <p>Compiled as a working field manual for doctoral researchers. The methods are old; the obligation to actually run them is daily.</p>
  <div class="colophon">SET IN SPACE GROTESK · STIX TWO TEXT · JETBRAINS MONO — PRINTS CLEANLY TO PDF</div>
</footer>

</div>
</body>
</html>
