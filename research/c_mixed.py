from c_teach import tp, gb, ms, wr, M
AL="https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=SE&q={q}&search_type=keyword_unordered&media_type=all"
def field(mod, q, niche):
    return wr(mod, f"FIELD EXERCISE (real ads, Meta Ad Library). Open the Ad Library search for '{q}' in Sweden (link below). Find (1) an ad that has been running 3+ months ('Started running on' date) and (2) one that started in the last 2 weeks. For each, note: hook/first line, offer, creative type, CTA. Then write which you'd bet is more profitable and why.",
      [f"Example of a good field note (structure, not a real ad):\nAd 1 — started 4+ months ago: video, nurse on camera, hook 'What we check before any {niche} treatment', offer 'free consultation', CTA 'Book now'.\nAd 2 — started 6 days ago: stock image, '20% off', no face.\nBet: Ad 1. Long run time suggests it keeps paying (proxy only), it leads with trust and a free first step, and the creative is native/face-led."],
      ["Use the 'Started running on' date as your long-running signal (3+ months).","Remember: the Ad Library shows NO performance data for non-political ads — run time is only a proxy (advertisers may also keep bad ads running).","Compare hook, offer, creative, CTA side by side.","Write your bet BEFORE reading anyone else's opinion."],
      ["Found a 3+ month ad","Found a <2 week ad","Compared 4 elements","Stated a bet + reason","Noted the proxy caveat"],["test_everything","creative_targeting"],"meta_adlib",ev="long_running",
      extra={"field_url":AL.format(q=q.replace(' ','%20'))})

MIXED = [
field("6.1","tandblekning","teeth whitening"),
field("6.1","laserhårborttagning","laser"),
field("6.1","fysioterapi","physio"),
field("6.1","hudvård klinik","skin"),
tp("6.1","Mixed: an aesthetic clinic wants more consultations. Which ad concept is the better FIRST test?","Discount banner: '20% off all treatments'","Nurse-on-camera video: 'What we check before any skin treatment' + free consultation",1,
 "Trust + free first step + face + education is safer under Meta health policy and addresses the real barrier (uncertainty). Test discounts later as a separate concept.",["sampling","face","policy"],"meta_health"),
tp("6.1","Mixed: which ad set structure fits Meta's Andromeda guidance?","1 ad set, broad audience, 4–6 genuinely different creatives","10 ad sets with narrow interests, the same creative in each",0,
 "Meta's guidance: focus shifted from niche targeting to creative diversification. Give the system different concepts.",["creative_targeting"],"meta_andromeda"),
gb("6.1","Meta ad for Synlig Media. Primary text: \"Klinikägare i Stockholm: syns ni på Google-kartan när patienter söker? Vi gör en gratis 'Google-kartan'-rapport för er klinik — ni ser er placering jämfört med 3 grannkliniker. Tryck 'Få rapport'.\" Creative: map with pins, the clinic at #7.","good",
 "Reader callout, problem shown visually, free sample, one CTA. Passes Hopkins + Caples + Hormozi checks.",["reader_callout","sampling","concrete_image","cta"],"hopkins",
 mock=M(page="Synlig Media",bg="#eaf2ff",fg="#14213d",overlay="Er klinik: #7 på kartan",size="m",focal="map",cta="Få rapport")),
ms("6.1","Meta ad: \"Best marketing agency 🚀 We do everything! DM us.\" Creative: agency logo.",["no_offer","no_proof","wrong_audience","weak_hook","hype"],
 "Every principle fails: no reader, no offer, no proof, no hook, hype.",["reader_callout","offer","proof"],"hopkins",
 mock=M(page="Agency X",bg="#111111",fg="#ffffff",overlay="BEST AGENCY 🚀",size="l",focal="logo",cta="Send message")),
wr("6.1","BRIEF: Write a complete Meta ad for Synlig Media (primary text ≤60 words, headline ≤6 words, image description, CTA button) targeting clinic owners in Stockholm with the free 'Google-kartan' report.",
 ["Primary text: 'Klinikägare i Stockholm: när patienter söker \"tandläkare nära mig\" — var hamnar ni? Vi gör en gratis 1-sidig Google-kartan-rapport: er placering vs 3 grannkliniker + de 3 största luckorna i profilen. Klar inom 24h.'\nHeadline: 'Gratis: er plats på kartan'\nImage: Maps-style screenshot, 3 pins, clinic circled at #7, one-line overlay 'Var hamnar ni?'\nCTA: 'Få rapport' (Learn more)"],
 ["Primary text line 1 = reader callout + problem.","Offer = free, specific, fast.","Headline repeats the offer in ≤6 words.","Image shows the problem (their rank), one focal point, ≤8 words overlay.","One CTA."],
 ["Reader callout","Specific free offer","Image = problem visual","≤8 words overlay","One CTA","No fake numbers"],["reader_callout","sampling","concrete_image","cta"],"hopkins"),
]

FINAL_TEACH = [
tp("6.2","Final: which headline would Caples call 'self-interest + news'?","New for 2026: 3 Google profile fields clinics in Stockholm forget","Our agency is celebrating 2 years!",0,"A is news AND useful to the reader. B is your news, not theirs. (Make sure the 'new' claim is true before using it.)",["news","self_interest"],"caples_wiki"),
tp("6.2","Final: which primary text first line is policy-safe for a dental whitening ad?","Yellow teeth ruining your photos?","Teeth whitening at a dentist, with an enamel check first.",1,"A attacks appearance (Meta: no statements of inferiority about appearance).",["policy"],"meta_health"),
tp("6.2","Final: cold email CTA to a stranger?","'Är det här intressant för er?' (Is this interesting for you?)","'Här är min kalender, boka 1 timme.'",0,"Interest CTA (Gong).",["interest_cta"],"gong_cta"),
tp("6.2","Final: which offer has the lower 'effort & sacrifice'?","'Send us your logins, photos, texts and hours, then we'll start.'","'We pull everything from your website and current profile; you approve in one 15-min call.'",1,"Hormozi: shrink effort & sacrifice.",["value_equation"],"hormozi"),
gb("6.2","Final: \"Nervös inför tandläkaren? Första besöket hos oss är bara samtal och röntgen — ingen behandling samma dag. Boka en tid som passar dig.\" (Nervous about the dentist? First visit is just a talk and X-rays — no treatment the same day.)","good","Situation callout without shaming, specific reassuring fact, low-risk first step, one CTA.",["specificity","risk_reversal","cta"],"hopkins"),
ms("6.2","Final: \"Revolutionary paradigm-shifting aesthetics. Unlock your best self now!!! 🔥\"",["too_clever","hype","no_offer","policy_risk"],"Jargon, hype, no offer, and 'best self' implies the reader isn't — risky.",["clarity","policy"],"meta_health"),
]
