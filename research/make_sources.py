import json,sys
sys.path.insert(0,'.')
from c_common import S
d=json.load(open('../data/tasks.json'))
use={}
for t in d['tasks']:
    for k,(n,u) in S.items():
        if t['source_url']==u: use.setdefault(k,[]).append(t['id'])
pr={}
for k,v in d['principles'].items():
    for sk,(n,u) in S.items():
        if v['source_url']==u: pr.setdefault(sk,[]).append(v['label'])
TAKEN={
"upworthy":"Exploratory packages CSV (osf.io/download/3vqmp). We selected 54 tests where two packages shared the same image (eyecatcher_id) and differed in headline, both ≥2,000 impressions, our two-proportion z>3.5 and relative CTR lift >50%; filtered out sensitive/political topics. Headlines quoted verbatim (short); CTRs computed from impressions/clicks.",
"upworthy_site":"Background on the archive; cited for the 'clarity beats cleverness' pattern seen in the data.",
"obama08":"2008 splash-page test: 24 combos, 310,382 visitors, 8.26%→11.6% (+40.6%), all videos lost to all images.",
"obama08wired":"'Learn More' +18.6% vs 'Sign Up'; family photo +13.1%.",
"obama12wired":"'I will be outspent' subject line won among 13 tested; raised ~$2.6M in one day; other tested subject lines.",
"obama12sherpa":"Process: drafts + 3 subject lines each tested on segments (background, not used as a task source).",
"bit_pmc":"Peer-reviewed RCT table of 8 messages; reciprocity 4,256 vs control 3,085 sign-ups (OR 1.38); social-norm+image arm worse than control (OR 0.94).",
"bit":"BIT summary: reciprocity +38% / ~96,000 extra registrations; reciprocity vs loss frame not significantly different.",
"highrise":"5 headline/subhead variants; '30-day Free Trial on All Accounts' +30%, testimonial subhead +7%.",
"unbounce_my":"'Start my free 30 day trial' vs 'your' → +90% CTR.",
"cxl_forms":"Empire Flippers 'Join us!' vs 'Make Money Flipping Websites' +33.1%.",
"hbr_bing":"Bing 2012 ad-title change → +12% revenue (>$100M/yr US).",
"cody_wiki":"Sackheim/Cody ad ran 40+ years; Schwab's 10-year comparison ~3x response vs 'How to Speak and Write Masterly English'.",
"cody_neh":"Ad placed in hundreds of publications; 15 minutes a day; free booklet.",
"adesp_format":"$1,000 test: image vs slideshow video vs carousel CPL; predictions favoured video.",
"adesp_thumb":"Thumbnail test (photo of presenter $25.02 vs cartoon $49.87 CPI) + Wistia $1k/$10k/$100k video CPIs.",
"meta_video":"Up to 47% of video value in first 3 seconds, 74% in first 10 (Meta/Nielsen); captions +12% view time; 41% of videos meaningless without sound.",
"meta_iq":"2016 Facebook IQ study of 850+ video ads (creative elements vs ad recall); used for contrast/brand-early/sound-off guidance.",
"meta_stdfoods":"Meta case study: Reels following creative essentials → 36% lower CPC, 34% lower cost per LPV, 2.9x CTR (reported).",
"meta_cruk":"Meta case study: Reels-first A/B → 10,000 more reach, 2% more conversions, lower CPA (reported).",
"meta_andromeda":"Meta's statement that focus shifted from niche targeting to creative diversification; Advantage+ notes.",
"meta_health":"Health & Wellness ad standard: 18+ targeting; no statements of inferiority about appearance; no pinched-fat close-ups.",
"meta_adlib":"Ad Library entry point; field exercises link to keyword searches (country=SE). No performance data is shown for non-political ads.",
"gong_cta":"304,174 emails; Interest CTA highest-performing for cold; specific-time CTA 15% cold → 37% in-deal.",
"gong_stats":"Longer (30–150 words) emails better; ROI language −15%; 'thoughts' −20% meetings; 'I never heard back' −14% meetings; 'Hope all is well' +24%.",
"boom_signoff":"Sign-off response rates (Thanks in advance 65.7%, Best 51.2%, baseline 47.5%).",
"boom_tips":"50–125 words best; 3rd-grade reading level 53% vs college 39%; 1–3 questions +50%; 3–4 word subjects; no-subject 14%.",
"belkins_subj":"5.5M B2B cold emails: personalised subject 7% vs 3% reply, 46% vs 35% open; 2–4 words 46% vs 10 words 34%; questions 46%; hype <36%.",
"woodpecker_fu":"9% reply without follow-up vs 13% with ≥1; 2–3 follow-ups optimal.",
"hopkins":"Public-domain book (LOC scan). Principles paraphrased: specificity, headlines, samples, test campaigns, service.",
"hopkins_read":"Same text, readable PDF; chapter list used for principle cards.",
"ogilvy_conf":"Short quote: 'five times as many people read the headline…eighty cents out of your dollar'.",
"rolls":"1958 Rolls-Royce headline (short quote) and research background; sales effects reported, not tested.",
"caples_hof":"Piano ad drew a record number of coupons when it first ran; Caples' testing books.",
"caples_wiki":"Caples biography; piano ad 1926; Tested Advertising Methods (principles paraphrased).",
"piano_swipe":"Structure of the 1926 Screenland printing (headline, scene, proof from a skeptic, free lesson coupon).",
"conroy_wiki":"'Two Young Men' letter in continuous use 1975–2003; estimated ~$2B.",
"conroy_sofii":"Letter structure (story → difference → offer), ran 1975–2003, ~$2B estimate. (SOFII's Denny Hatch article was dropped: it returns HTTP 404 to browsers.)",
"schwartz":"Summary of the five awareness levels.",
"sophistication":"Summary of the market sophistication stages.",
"hormozi":"Value equation (paraphrased) — free training page.",
"schlitz":"Hopkins' biography (Schlitz 'process' story, sampling).",
"lauder":"Company founder page: free sample with purchase → 'Gift with Purchase'; personal demonstration.",
"gbp":"Google's own guidance on local ranking (relevance, distance, prominence; complete profile) — used to keep teaching claims honest.",
}
out=["# SOURCES","","Every source used in the playground, what was taken from it, and which tasks cite it. Link status is re-checked by `tests/test_site.py` (see `tests/link-status-*.json`).","",
"Evidence labels: PROVEN TEST (real A/B with known winner) · LONG-RUNNING SIGNAL · PUBLISHED CASE STUDY / BENCHMARK (reported, often correlational) · Teaching example (written for practice, no metrics) · PRINCIPLE LESSON (cited).",""]
for k,(n,u) in S.items():
    ids=use.get(k,[]); p=pr.get(k,[])
    out.append(f"## {n}\n- URL: [{u}]({u})\n- Taken: {TAKEN.get(k,'')}\n- Cited by {len(ids)} task(s){': '+', '.join(ids[:40])+(' …' if len(ids)>40 else '') if ids else ''}"+(f"\n- Principle chips linking here: {', '.join(p)}" if p else "")+"\n")
out.append("## Not used / could not verify\n- Facebook/Instagram 'sweetgreen' success story URL returned 404 (dropped). KiwiCo success story did not load reliably (dropped).\n- Specific Meta Ad Library ads are not cited individually (pages need login/JS and show no performance data); field exercises link to live searches instead.\n- John Caples' individual split-test pairs from *Tested Advertising Methods* were not used because no reliable online copy could be verified.\n- Foreplay/swipe-file posts were not used (performance not verifiable).\n")
open('../SOURCES.md','w').write("\n".join(out))
print(len(S),"sources;", sum(len(v) for v in use.values()),"task citations")
