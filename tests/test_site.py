"""End-to-end tests for Marketing Taste Playground.
Usage: python3 tests/test_site.py <base_url> [label]   e.g. http://127.0.0.1:18731/ local
"""
import sys, json, re, time, ssl, urllib.request, concurrent.futures, os
from playwright.sync_api import sync_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:18731/"
LABEL=sys.argv[2] if len(sys.argv)>2 else "local"
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results=[]; 
def check(name, ok, detail=""):
    results.append({"test":name,"pass":bool(ok),"detail":str(detail)[:300]}); print(("PASS " if ok else "FAIL ")+name+(" — "+str(detail)[:200] if (detail and not ok) else ""))

def run_viewport(p, w, h, shots=False):
    tag=f"{w}x{h}"
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",headless=True)
    ctx=b.new_context(viewport={"width":w,"height":h},accept_downloads=True)
    pg=ctx.new_page(); errs=[]
    pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
    pg.goto(BASE+"#/"); pg.wait_for_selector("#btnContinue")
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_selector("#btnContinue")
    tasks=pg.evaluate("window.MTP.tasks.map(t=>({id:t.id,type:t.type,answer:t.answer,ev:t.evidence_type,url:t.source_url}))")
    check(f"[{tag}] task count >= 200", len(tasks)>=200, len(tasks))
    if shots: pg.wait_for_timeout(300); pg.screenshot(path=f"{ROOT}/shots/home.png")
    # every task renders + reveal works
    bad=[]
    for t in tasks:
        pg.evaluate(f"location.hash='#/t/{t['id']}'")
        try:
            pg.wait_for_selector(f"[data-task='{t['id']}']",timeout=4000)
            if t["type"] in ("pick","goodbad","lesson"):
                pg.click("[data-opt='0']")
                pg.click("#btnReveal")
            elif t["type"]=="missing":
                pg.check(f"[data-flag='{t['answer'][0]}']"); pg.click("#btnReveal")
            elif t["type"]=="write":
                pg.fill("#wtext","My test draft for "+t["id"]); pg.click("#btnReveal")
            else:
                pg.click("#btnReveal")
            pg.wait_for_selector("#revealBox",timeout=3000)
            assert pg.locator("#revealBox .srclink").count()>=1
            assert pg.locator(".ev").first.inner_text().strip()!=""
            if t["type"]=="write": assert pg.locator(".model").count()>=1 and pg.locator("[data-check]").count()>=1
            if t["type"]=="teardown": assert pg.locator(".parts .note").count()>=1
            if t["type"]=="pick": assert pg.locator(".opt.win").count()==1
        except Exception as e:
            bad.append((t["id"],str(e)[:120]))
    check(f"[{tag}] all {len(tasks)} tasks render and reveal (with source link + evidence label)", not bad, bad[:5])
    st=pg.evaluate("window.MTP.state()")
    check(f"[{tag}] revealing auto-marks tasks done", len(st["done"])==len(tasks), len(st["done"]))
    # reset via UI (dialog)
    pg.goto(BASE+"#/"); pg.wait_for_selector("#btnReset")
    pg.once("dialog",lambda d: d.accept()); pg.click("#btnReset"); pg.wait_for_timeout(300)
    check(f"[{tag}] reset clears progress", len(pg.evaluate("window.MTP.state()")["done"])==0)
    # keyboard pick flow
    picks=[t for t in tasks if t["type"]=="pick"]
    t0=picks[0]; pg.evaluate(f"location.hash='#/t/{t0['id']}'"); pg.wait_for_selector(f"[data-task='{t0['id']}']")
    pg.keyboard.press("2"); sel=pg.locator(".opt.sel").get_attribute("data-opt")
    pg.keyboard.press("Enter"); pg.wait_for_selector("#revealBox")
    check(f"[{tag}] keyboard 2 selects option 2 and Enter reveals", sel=="1")
    idx=[t["id"] for t in tasks].index(t0["id"]); nxt=tasks[idx+1]["id"]
    pg.keyboard.press("Enter"); pg.wait_for_selector(f"[data-task='{nxt}']",timeout=3000)
    check(f"[{tag}] Enter after reveal goes to next task", True)
    pg.keyboard.press("ArrowLeft"); pg.wait_for_selector(f"[data-task='{t0['id']}']",timeout=3000)
    check(f"[{tag}] ArrowLeft goes back", True)
    if shots:
        # pick-the-winner reveal screenshot on an Upworthy task
        up=[t for t in picks if t["ev"]=="proven_test"][3]
        pg.evaluate(f"location.hash='#/t/{up['id']}'"); pg.wait_for_selector(f"[data-task='{up['id']}']")
        pg.fill("#why","The winner is more concrete and creates a curiosity gap.")
        pg.click(f"[data-opt='{up['answer']}']"); pg.click("#btnReveal"); pg.wait_for_selector("#revealBox")
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1900); pg.screenshot(path=f"{ROOT}/shots/pick-reveal.png")
        wt=[t for t in tasks if t["type"]=="write"][0]
        pg.evaluate(f"location.hash='#/t/{wt['id']}'"); pg.wait_for_selector("#wtext")
        pg.fill("#wtext","Laser hair removal on Södermalm — free patch test first.\nLicensed nurse, fixed price before you decide.\nBook a time below.")
        pg.click("#btnReveal"); pg.wait_for_selector("#revealBox"); pg.locator("[data-check='0']").check(); pg.locator("[data-check='2']").check()
        pg.evaluate("document.querySelector('#revealBox h3').scrollIntoView()"); pg.evaluate("window.scrollBy(0,-120)"); pg.wait_for_timeout(1900); pg.screenshot(path=f"{ROOT}/shots/write-reveal.png")
    # mark done persists across reload + sidebar check
    t1=tasks[5]["id"]; pg.evaluate(f"location.hash='#/t/{t1}'"); pg.wait_for_selector("#btnDone")
    before=pg.evaluate("Object.keys(window.MTP.state().done).length")
    if pg.locator("#btnDone.on").count(): pg.click("#btnDone")
    pg.click("#btnDone"); pg.reload(); pg.wait_for_selector(f"[data-task='{t1}']")
    ok=pg.locator("#btnDone.on").count()==1 and pg.locator(f"#outline a[data-id='{t1}'].done").count()==1 and "✓" in pg.locator(f"#outline a[data-id='{t1}'] .ck").inner_text()
    check(f"[{tag}] Mark done persists across reload (button + sidebar ✓ + strike class)", ok)
    pg.keyboard.press("m"); pg.reload(); pg.wait_for_selector(f"[data-task='{t1}']")
    check(f"[{tag}] M key toggles done and persists", pg.locator("#btnDone.on").count()==0)
    pg.keyboard.press("m")
    # written answer persists
    wt=[t for t in tasks if t["type"]=="write"][1]["id"]
    pg.evaluate(f"location.hash='#/t/{wt}'"); pg.wait_for_selector("#wtext"); pg.fill("#wtext","persist me 123"); pg.reload(); pg.wait_for_selector("#wtext")
    check(f"[{tag}] written answer persists across reload", pg.input_value("#wtext")=="persist me 123")
    # home progress + continue
    pg.goto(BASE+"#/"); pg.wait_for_selector("#homeProgText")
    check(f"[{tag}] home shows progress and Continue", "of" in pg.inner_text("#homeProgText") and pg.locator("#btnContinue").count()==1 and pg.locator(".modrow").count()>=19)
    # focus mode
    pg.evaluate(f"location.hash='#/t/{tasks[10]['id']}'"); pg.wait_for_selector(f"[data-task='{tasks[10]['id']}']")
    pg.keyboard.press("f"); pg.wait_for_timeout(300)
    f_on=pg.evaluate("document.body.classList.contains('focus')") and not pg.is_visible("#sidebar") and not pg.is_visible("#topbar") and pg.is_visible("#btnExitFocus")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    f_off=not pg.evaluate("document.body.classList.contains('focus')") and pg.is_visible("#topbar")
    check(f"[{tag}] Focus mode via F and Esc exits", f_on and f_off, (f_on,f_off))
    pg.click("#btnFocus"); pg.wait_for_timeout(200); a=pg.evaluate("document.body.classList.contains('focus')"); pg.click("#btnExitFocus"); pg.wait_for_timeout(200)
    check(f"[{tag}] Focus button + Exit button", a and not pg.evaluate("document.body.classList.contains('focus')"))
    # sidebar toggle
    pg.click("#btnSidebar"); hidden=not pg.is_visible("#sidebar"); pg.reload(); pg.wait_for_selector("#main .wrap"); hidden2=not pg.is_visible("#sidebar")
    pg.click("#btnSidebar"); shown=pg.is_visible("#sidebar"); pg.keyboard.press("s"); k1=not pg.is_visible("#sidebar"); pg.keyboard.press("s")
    check(f"[{tag}] Sidebar ☰ toggle (persists) and S key", hidden and hidden2 and shown and k1, (hidden,hidden2,shown,k1))
    # review misses
    tw=picks[7]; pg.evaluate(f"location.hash='#/t/{tw['id']}'"); pg.wait_for_selector(f"[data-task='{tw['id']}']")
    if pg.locator("#btnRetry").count(): pg.click("#btnRetry")
    pg.click(f"[data-opt='{1-tw['answer']}']"); pg.click("#btnReveal"); pg.wait_for_selector(".result.no")
    mc=int(pg.inner_text("#missCount"))
    pg.goto(BASE+"#/review"); pg.wait_for_selector("#btnStartReview")
    listed=pg.locator(f".reviewlist a[href='#/t/{tw['id']}?review']").count()==1
    pg.click(f".reviewlist a[href='#/t/{tw['id']}?review']"); pg.wait_for_selector("#btnReveal")
    pg.click(f"[data-opt='{tw['answer']}']"); pg.click("#btnReveal"); pg.wait_for_selector(".result.ok")
    cleared=tw["id"] not in pg.evaluate("window.MTP.state().misses")
    check(f"[{tag}] Review my misses: wrong answer queued, re-answer clears", mc>=1 and listed and cleared, (mc,listed,cleared))
    # accuracy stats
    pg.goto(BASE+"#/"); pg.wait_for_selector("#accAll")
    check(f"[{tag}] accuracy stat displayed", re.search(r"\d+%",pg.inner_text("#accAll")) is not None, pg.inner_text("#accAll"))
    # export/import
    with pg.expect_download() as dl: pg.click("#btnExport")
    path=dl.value.path(); data=json.load(open(path))
    check(f"[{tag}] export JSON", data.get("app")=="marketing-taste-playground" and "done" in data["state"])
    data["state"]["done"]={tasks[0]["id"]:True,tasks[1]["id"]:True,tasks[2]["id"]:True}
    imp="/tmp/mtp_import.json"; json.dump(data,open(imp,"w"))
    pg.set_input_files("#fileImport",imp); pg.wait_for_timeout(500)
    check(f"[{tag}] import JSON restores progress", len(pg.evaluate("window.MTP.state().done"))==3)
    # layout: no horizontal overflow at this viewport
    ov=pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")
    check(f"[{tag}] no horizontal overflow", ov)
    errs=[e for e in errs if "favicon" not in e]
    check(f"[{tag}] no console errors", not errs, errs[:5])
    b.close()

UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
def http_status(u):
    ctx=ssl.create_default_context()
    for method in ("HEAD","GET"):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,method=method,headers={"User-Agent":UA,"Accept":"text/html,*/*"}),timeout=25,context=ctx)
            return r.status
        except urllib.error.HTTPError as e:
            if method=="HEAD" and e.code in (403,404,405,400,501,429): continue
            return e.code
        except Exception as e:
            if method=="HEAD": continue
            return "timeout/err:"+type(e).__name__
    return "err"
def link_check(p):
    data=json.load(open(f"{ROOT}/data/tasks.json"))
    urls=set(t["source_url"] for t in data["tasks"])|set(t["field_url"] for t in data["tasks"] if t.get("field_url"))|set(v["source_url"] for v in data["principles"].values())
    if os.path.exists(f"{ROOT}/SOURCES.md"): urls|=set(re.findall(r"\((https?://[^)\s]+)\)",open(f"{ROOT}/SOURCES.md").read()))
    fb=[u for u in urls if "facebook.com" in u or "meta.com" in u]; other=[u for u in urls if u not in fb]
    st={}
    with concurrent.futures.ThreadPoolExecutor(12) as ex:
        for u,s in zip(other,ex.map(http_status,other)): st[u]=s
    # Sites that reject non-browser clients (Meta returns 400 to curl) or answer 4xx to scripts: verify in real Chrome.
    recheck=fb+[u for u,s in st.items() if isinstance(s,int) and s in (400,404,410)]
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",headless=True); pg=b.new_page()
    for u in recheck:
        try:
            r=pg.goto(u,timeout=40000,wait_until="domcontentloaded"); pg.wait_for_timeout(1500)
            s=r.status if r else None
            body=pg.inner_text("body")[:4000]
            if s is None: s=200 if len(body)>200 else "no-response"
            if s==200 and ("page that doesn" in body or "Page not found" in body or "404" in pg.title()): s=404
            st[u]=s
        except Exception as e: st[u]="timeout/err"
    b.close()
    bad={u:s for u,s in st.items() if s in (404,410) or (isinstance(s,int) and s>=400 and s not in (403,429,401,999))}
    json.dump(st,open(f"{ROOT}/tests/link-status-{LABEL}.json","w"),indent=1)
    check(f"[links] {len(st)} unique source links non-404 (403/timeouts allowed)", not bad, bad)

with sync_playwright() as p:
    run_viewport(p,1366,768)
    run_viewport(p,1440,900,shots=True)
    if "--nolinks" not in sys.argv: link_check(p)
passed=sum(r["pass"] for r in results)
json.dump({"base":BASE,"label":LABEL,"when":time.strftime("%Y-%m-%d %H:%M:%S %Z"),"passed":passed,"total":len(results),"results":results},open(f"{ROOT}/tests/results-{LABEL}.json","w"),indent=1)
print(f"\n{passed}/{len(results)} passed ({LABEL})"); sys.exit(0 if passed==len(results) else 1)
