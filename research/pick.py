import pandas as pd, math, json, random
df=pd.read_csv('exploratory.csv')
df=df.dropna(subset=['headline'])
out=[]
for tid,g in df.groupby('clickability_test_id'):
    g=g.drop_duplicates('headline')
    if len(g)<2: continue
    # same image
    for eid,h in g.groupby('eyecatcher_id'):
        if len(h)<2: continue
        h=h.assign(ctr=h.clicks/h.impressions).sort_values('ctr')
        lo,hi=h.iloc[0],h.iloc[-1]
        if lo.impressions<2000 or hi.impressions<2000: continue
        p=(lo.clicks+hi.clicks)/(lo.impressions+hi.impressions)
        se=math.sqrt(p*(1-p)*(1/lo.impressions+1/hi.impressions))
        if se==0: continue
        z=(hi.ctr-lo.ctr)/se
        lift=hi.ctr/lo.ctr-1 if lo.ctr>0 else 9
        if z>3.5 and lift>0.5 and len(hi.headline)<140 and len(lo.headline)<140:
            out.append(dict(test=tid,date=str(hi.created_at)[:10],win=hi.headline,lose=lo.headline,wi=int(hi.impressions),wc=int(hi.clicks),li=int(lo.impressions),lc=int(lo.clicks),z=round(z,1),lift=round(lift,2)))
print(len(out))
json.dump(out,open('cands.json','w'),indent=0)
