# PROGRESS (resume file)
## Done
- Upworthy exploratory CSV downloaded (research/exploratory.csv, OSF https://osf.io/download/3vqmp/). 46 curated same-image headline pairs in research/upworthy_selected.json (z>3.5, lift>50%).
- Verified sources (fetched): Obama 2008 splash (medium Siroker), BIT organ donation (PMC6150960, bi.team), Obama 2012 email "I will be outspent" (Wired/Marketingsherpa/Bluestate), Highrise headlines (signalvnoise 1525), Unbounce my vs your (+90%), Gong interest CTA (30% vs 15%/13%), Gong cold email stats, Boomerang sign-offs + length/grade, Belkins subject lines, Woodpecker follow-ups, AdEspresso format + thumbnail experiments, Meta health policy, FB IQ 47% first 3s.
## Next
- write data/tasks.js (build script research/build_tasks.py), index.html app, tests, deploy
- More verified: Meta success Standard Foods (browser only; FB returns 400 to curl -> link-check FB via Chrome), CRUK Reels A/B, FB news updated-features-for-video-ads (47%/3s, captions +12%), FB IQ capturing-attention, Andromeda diversification page, Wikipedia Sherwin Cody (Schwab 10-yr ~3x headline comparison), Martin Conroy WSJ letter (Wikipedia, SOFII), Caples (Hall of Fame, Wikipedia), Rolls-Royce (damngoodads), Hopkins LOC https://www.loc.gov/item/23009362/, Hormozi acquisition.com/training, HBR Bing 12%, Ogilvy quote campaignlive, Schwartz personalmba.
- Plan: research/content_*.py -> build.py -> data/tasks.js ; app index.html/app.js/styles.css
- [x] Content written: research/c_*.py ; build: `cd research && python3 build.py` -> data/tasks.js + tasks.json
- [x] App written: index.html, styles.css, app.js (vanilla JS). Serve: python3 -m http.server 18731
- [x] tests/test_site.py written (python3 tests/test_site.py http://127.0.0.1:18731/ local)
- [x] Local functional tests 40/40 (no links yet). Next: SOURCES.md, link check, README, deploy
- [x] SOURCES.md generated (research/make_sources.py)
- [x] SOFII dropped (404), Lauder source -> elcompanies.com; README, .nojekyll
- [x] Repo created + pushed (commit 6d753c7). Next: enable Pages, live test
- [x] Pages built
- [x] Live tests 41/41 at https://oskaraxels.github.io/marketing-playground/ (tests/results-live.json). Local 41/41 (tests/results-local.json).
## Status: COMPLETE. To change content: edit research/c_*.py -> python3 research/build.py (from research/) -> make_sources.py -> test -> push.
