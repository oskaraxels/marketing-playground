import json, random, sys
sys.path.insert(0,'.')
from c_common import S, P
from c_upworthy import NOTES
from c_real import REAL, LONG
from c_lessons import LESSONS
from c_teach import TEACH
from c_mixed import MIXED, FINAL_TEACH
from c_drills import DRILLS
TRACKS=[("1","Foundations: the principles"),("2","Meta ad headlines & primary text"),("3","Meta creative, images & hooks"),("4","Offers & big ideas"),("5","Cold email"),("6","Mixed mastery & final exam")]
MODULES=[("1.1","Hopkins & Ogilvy"),("1.2","Caples, Schwartz & Lauder"),("1.3","Modern direct response, Meta & cold email basics"),
("2.1","Headline instinct I (real Upworthy tests)"),("2.2","Headline instinct II (real Upworthy tests)"),("2.3","Headline instinct III (real Upworthy tests)"),("2.4","Primary text for clinics"),
("3.1","Proven creative tests"),("3.2","Image judgment with mockups"),("3.3","Hooks & video"),
("4.1","Proven offer, CTA & headline tests"),("4.2","Building offers (Synlig Media)"),("4.3","Classic big ideas & teardowns"),
("5.1","Subject lines"),("5.2","Openers & body"),("5.3","CTAs & follow-ups"),("5.4","Write & teardown"),
("6.1","Field work (Ad Library) & mixed"),("6.2","Final exam")]
FLAGS={"no_number":"No specific number / fact","no_offer":"No clear offer","weak_hook":"Weak hook / first line","no_proof":"No proof","no_cta":"No clear CTA","wrong_audience":"Wrong or missing audience callout","too_clever":"Too clever / unclear","too_long":"Too long / cluttered","policy_risk":"Meta policy risk","no_personalization":"No personalization / relevance","low_contrast":"Low contrast / no focal point","too_much_text":"Too much text on image","hype":"Hype / unbelievable claim","big_ask":"Asks too much (effort or time)"}
ups=json.load(open('upworthy_selected.json'))
tasks=[]
def mod_of_up(i):
    if i<15: return "2.1"
    if i<30: return "2.2"
    if i<40 or 46<=i<=50: return "2.3"
    return "6.2"
for i,x in enumerate(ups):
    note,pr=NOTES[i]
    wctr=x['wc']/x['wi']*100; lctr=x['lc']/x['li']*100
    tasks.append(dict(type="pick",module=mod_of_up(i),prompt="Upworthy headline test — same story, same image. Which headline got the higher click-through rate?",
      options=[{"text":x['win']},{"text":x['lose']}],answer=0,evidence_type="proven_test",
      metric=f"CTR {wctr:.2f}% vs {lctr:.2f}% ({x['wc']:,}/{x['wi']:,} vs {x['lc']:,}/{x['li']:,} clicks/impressions; z≈{x['z']}). Test {x['test']}, {x['date']}. Our own two-proportion z-test on the archive data.",
      source="upworthy",explanation=note+" (The data shows which won; the 'why' is our interpretation.)",principles=pr,upworthy_test=x['test']))
for d in REAL+LONG+LESSONS+DRILLS+TEACH+MIXED+FINAL_TEACH: tasks.append(dict(d))
order=[m for m,_ in MODULES]
tasks.sort(key=lambda t: order.index(t['module']))  # stable
rng=random.Random(42); cnt={}
for t in tasks:
    m=t['module']; cnt[m]=cnt.get(m,0)+1
    t['id']=f"t{m.replace('.','-')}-{cnt[m]:02d}"; t['track']=m.split('.')[0]
    src=t.pop('source'); assert src in S, src
    t['source_name'],t['source_url']=S[src]
    for p in t['principles']: assert p in P,(p,t['id'])
    if t['type']=="pick":
        if rng.random()<0.5: t['options']=t['options'][::-1]; t['answer']=1-t['answer']
    if t['type']=="missing":
        for f in t['answer']: assert f in FLAGS,(f,t['id'])
    for k in ("id","track","module","type","prompt","evidence_type","source_url","explanation","principles"): assert k in t,(k,t)
    if 'upworthy_test' in t: t['title']=f"Upworthy headline test ({t['upworthy_test'][-6:]})"
    else:
        pr=t['prompt']; t['title']=(pr[:64]+'…') if len(pr)>66 else pr
    t.setdefault('options',[]); t.setdefault('answer',None); t.setdefault('metric','')
data=dict(tracks=[dict(id=a,title=b) for a,b in TRACKS],modules=[dict(id=a,title=b,track=a.split('.')[0]) for a,b in MODULES],
  tasks=tasks,principles={k:dict(label=v[0],source_url=S[v[1]][1],source_name=S[v[1]][0]) for k,v in P.items()},flags=FLAGS,
  evidence_labels={"proven_test":"PROVEN TEST (real A/B test, known winner)","long_running":"LONG-RUNNING SIGNAL (ran for years / Ad Library proxy)","case_study":"PUBLISHED CASE STUDY / BENCHMARK (reported results, not independently verified)","teaching":"Teaching example (written for practice, not real performance data)","principle":"PRINCIPLE LESSON (cited source)"})
open('../data/tasks.js','w').write("window.MTP_DATA="+json.dumps(data,ensure_ascii=False,indent=0)+";\n")
json.dump(data,open('../data/tasks.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print("total",len(tasks)); print(Counter(t['type'] for t in tasks)); print(Counter(t['evidence_type'] for t in tasks))
print(sorted(Counter(t['module'] for t in tasks).items()))
print("real picks", sum(1 for t in tasks if t['type']=='pick' and t['evidence_type'] in ('proven_test','long_running','case_study')))
print("answer A share", sum(1 for t in tasks if t['type']=='pick' and t['answer']==0)/sum(1 for t in tasks if t['type']=='pick'))
