"""Modern browser interface for the CPU Scheduling Simulator.

Uses only the Python standard library. The scheduling is computed by
cpu_scheduler.py (Python); the browser only draws the results.
"""
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from cpu_scheduler import (Process, validate, fcfs, sjf, srtf, round_robin)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CPU Scheduling Simulator</title>
<style>
:root{
  --bg:#f4f5fb; --card:#ffffff; --ink:#1d2140; --muted:#6b7090; --line:#e6e8f2;
  --brand:#c8102e; --brand2:#ff5a3c; --accent:#4f46e5; --good:#12a56b; --shadow:0 8px 30px rgba(40,44,90,.08);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 "Segoe UI",system-ui,-apple-system,Roboto,sans-serif}
header{background:linear-gradient(120deg,var(--brand),var(--brand2));color:#fff;padding:26px 24px 70px}
.wrap{max-width:1100px;margin:0 auto}
header h1{margin:0;font-size:26px;letter-spacing:.2px}
header p{margin:4px 0 0;opacity:.9}
.badge{display:inline-block;background:rgba(255,255,255,.2);padding:3px 10px;border-radius:99px;font-size:12px;margin-bottom:8px}
main{margin-top:-48px;padding:0 16px 40px}
.card{background:var(--card);border-radius:18px;box-shadow:var(--shadow);padding:20px;margin-bottom:18px}
.card h2{margin:0 0 12px;font-size:15px;text-transform:uppercase;letter-spacing:.8px;color:var(--muted)}
.grid{display:grid;grid-template-columns:1fr 1.5fr;gap:18px}
@media(max-width:820px){.grid{grid-template-columns:1fr}}
.seg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.seg button{border:2px solid var(--line);background:#fff;border-radius:12px;padding:11px 8px;font-weight:600;color:var(--ink);cursor:pointer;transition:.15s}
.seg button small{display:block;font-weight:400;color:var(--muted);font-size:11px}
.seg button:hover{border-color:#c9cdf5}
.seg button.on{border-color:var(--accent);background:#eef0ff;color:var(--accent)}
.seg button.on small{color:var(--accent)}
.seg .wide{grid-column:span 2}
label{font-size:13px;color:var(--muted);font-weight:600}
input[type=number],input[type=text]{width:100%;padding:9px 10px;border:2px solid var(--line);border-radius:10px;font:inherit;color:var(--ink);background:#fff;transition:.15s}
input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 4px #e3e5ff}
.q{margin-top:14px;display:none}
.q.show{display:block}
table{width:100%;border-collapse:collapse}
th{font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);text-align:center;padding:8px 6px;border-bottom:2px solid var(--line)}
td{padding:6px;text-align:center;border-bottom:1px solid var(--line)}
td input{text-align:center;padding:7px}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block}
.btn{border:0;border-radius:12px;padding:11px 18px;font:inherit;font-weight:700;cursor:pointer;transition:.15s}
.btn.primary{background:linear-gradient(120deg,var(--accent),#7c6cf0);color:#fff;box-shadow:0 6px 16px rgba(79,70,229,.35)}
.btn.primary:hover{transform:translateY(-1px)}
.btn.ghost{background:#f0f1fa;color:var(--ink)}
.btn.ghost:hover{background:#e5e7f6}
.btn.x{background:none;color:#c0344b;padding:4px 10px;font-size:18px}
.bar{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
.bar .grow{flex:1}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px}
.stat{background:linear-gradient(160deg,#fff,#f5f6ff);border:1px solid var(--line);border-radius:14px;padding:14px;text-align:center}
.stat b{display:block;font-size:26px;color:var(--accent)}
.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px}
.gscroll{overflow-x:auto;padding-bottom:8px}
.gantt{display:flex;position:relative;height:56px}
.blk{height:56px;display:flex;align-items:center;justify-content:center;color:#1d2140;font-weight:700;border-right:2px solid #fff;position:relative;overflow:hidden;
  animation:grow .5s ease both;transform-origin:left}
.blk.idle{background:repeating-linear-gradient(45deg,#eceef6,#eceef6 6px,#dfe2f0 6px,#dfe2f0 12px);color:var(--muted);font-weight:500;font-size:12px}
.blk:first-child{border-radius:10px 0 0 10px}.blk:last-child{border-radius:0 10px 10px 0;border-right:0}
@keyframes grow{from{transform:scaleX(0);opacity:0}to{transform:scaleX(1);opacity:1}}
.ticks{position:relative;height:22px;margin-top:4px}
.tick{position:absolute;transform:translateX(-50%);font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.res td,.res th{padding:9px 8px}
.res tbody tr:hover{background:#f7f8ff}
.pid{font-weight:700}
.sect-title{display:flex;align-items:center;gap:10px;margin:0 0 14px}
.sect-title h3{margin:0;font-size:19px}
.pill{background:#eef0ff;color:var(--accent);padding:3px 10px;border-radius:99px;font-size:12px;font-weight:700}
.cmp-row{display:grid;grid-template-columns:170px 1fr 60px;gap:10px;align-items:center;margin:6px 0}
.cmp-bar{height:14px;border-radius:99px;background:#eceef8;overflow:hidden}
.cmp-bar i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),#8f84f5);transition:width .6s}
.cmp-bar i.best{background:linear-gradient(90deg,var(--good),#53d6a0)}
.cmp-row span:last-child{text-align:right;font-weight:700;font-variant-numeric:tabular-nums}
.note{background:#fff8e6;border:1px solid #ffe3a3;border-radius:12px;padding:12px 14px;color:#6a5313;font-size:14px}
.empty{text-align:center;color:var(--muted);padding:30px}
#toast{position:fixed;left:50%;bottom:26px;transform:translate(-50%,80px);background:#2b2f55;color:#fff;padding:12px 20px;border-radius:12px;box-shadow:var(--shadow);opacity:0;transition:.3s;max-width:90vw;z-index:9}
#toast.show{transform:translate(-50%,0);opacity:1}
#toast.err{background:#c0344b}
#toast.ok{background:var(--good)}
h4{margin:20px 0 8px;color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.7px}
</style>
</head>
<body>
<header><div class="wrap">
  <span class="badge">PT 101 · Platform Technologies</span>
  <h1>CPU Scheduling Simulator</h1>
  <p>FCFS · SJF · SRTF · Round Robin — type your processes, press Run, and see the Gantt chart.</p>
</div></header>

<main><div class="wrap">
  <div class="grid">
    <section class="card">
      <h2>1 · Choose algorithm</h2>
      <div class="seg" id="algos">
        <button data-a="fcfs" class="on">FCFS<small>First Come First Served</small></button>
        <button data-a="sjf">SJF<small>Non-preemptive</small></button>
        <button data-a="srtf">SRTF<small>Preemptive</small></button>
        <button data-a="rr">Round Robin<small>Time quantum</small></button>
        <button data-a="all" class="wide">⚖ Compare All Algorithms</button>
      </div>
      <div class="q" id="qbox">
        <label for="quantum">Time quantum</label>
        <input type="number" id="quantum" min="1" value="3">
      </div>
    </section>

    <section class="card">
      <h2>2 · Process information</h2>
      <table id="ptable">
        <thead><tr><th></th><th>Process ID</th><th>Arrival Time</th><th>Burst Time</th><th></th></tr></thead>
        <tbody></tbody>
      </table>
      <div class="bar">
        <button class="btn ghost" id="add">＋ Add process</button>
        <button class="btn ghost" id="sample">Load sample</button>
        <button class="btn ghost" id="random">🎲 Random</button>
        <button class="btn ghost" id="clear">Clear</button>
        <span class="grow"></span>
        <button class="btn primary" id="run">▶ Run Simulation</button>
      </div>
    </section>
  </div>

  <div id="output"><div class="card empty">Results will appear here. Press <b>Run Simulation</b> (or hit <b>Enter</b>).</div></div>
</div></main>
<div id="toast"></div>

<script>
const COLORS=["#a5d8ff","#b2f2bb","#ffd8a8","#ffc9c9","#d0bfff","#fff3bf","#99e9f2","#fcc2d7","#c0eb75","#e5dbff"];
let algo="fcfs", rows=[];
const $=s=>document.querySelector(s);

function toast(msg,kind){const t=$("#toast");t.textContent=msg;t.className="show "+(kind||"");clearTimeout(t._h);t._h=setTimeout(()=>t.className="",3200)}
function color(pid){const i=rows.findIndex(r=>r.pid===pid);return COLORS[(i<0?0:i)%COLORS.length]}

function renderRows(){
  const tb=$("#ptable tbody");tb.innerHTML="";
  rows.forEach((r,i)=>{
    const tr=document.createElement("tr");
    tr.innerHTML=`<td><span class="dot" style="background:${COLORS[i%COLORS.length]}"></span></td>
      <td><input type="text" value="${r.pid}" data-i="${i}" data-k="pid"></td>
      <td><input type="number" min="0" value="${r.at}" data-i="${i}" data-k="at"></td>
      <td><input type="number" min="1" value="${r.bt}" data-i="${i}" data-k="bt"></td>
      <td><button class="btn x" title="Remove" data-del="${i}">×</button></td>`;
    tb.appendChild(tr);
  });
}
$("#ptable").addEventListener("input",e=>{const i=e.target.dataset.i;if(i!==undefined)rows[i][e.target.dataset.k]=e.target.value});
$("#ptable").addEventListener("click",e=>{const d=e.target.dataset.del;if(d!==undefined){rows.splice(+d,1);renderRows()}});
$("#add").onclick=()=>{rows.push({pid:"P"+(rows.length+1),at:"0",bt:"1"});renderRows()};
$("#clear").onclick=()=>{rows=[];renderRows()};
$("#sample").onclick=()=>{rows=[["P1",0,7],["P2",1,4],["P3",2,3],["P4",3,5]].map(a=>({pid:a[0],at:String(a[1]),bt:String(a[2])}));$("#quantum").value=3;renderRows()};
$("#random").onclick=()=>{const n=3+Math.floor(Math.random()*4);rows=[];for(let i=1;i<=n;i++)rows.push({pid:"P"+i,at:String(Math.floor(Math.random()*8)),bt:String(1+Math.floor(Math.random()*9))});renderRows()};
$("#algos").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;
  document.querySelectorAll("#algos button").forEach(x=>x.classList.remove("on"));b.classList.add("on");algo=b.dataset.a;
  $("#qbox").classList.toggle("show",algo==="rr"||algo==="all")});
document.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.tagName==="INPUT")run()});
$("#run").onclick=run;

async function run(){
  try{
    const res=await fetch("/api/run",{method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({algorithm:algo,quantum:$("#quantum").value,processes:rows})});
    const data=await res.json();
    if(!res.ok){toast(data.error||"Something went wrong","err");return}
    draw(data);toast("Simulation completed!","ok");
    $("#output").scrollIntoView({behavior:"smooth"});
  }catch(err){toast("Cannot reach the simulator. Is the program still running?","err")}
}

function gantt(r){
  const total=r.timeline[r.timeline.length-1][2];
  const px=Math.max(30,Math.min(60,900/total));
  const w=total*px;
  let blocks="",ticks="";
  r.timeline.forEach(([pid,s,e])=>{
    const idle=pid==="Idle";
    blocks+=`<div class="blk ${idle?"idle":""}" style="width:${(e-s)*px}px;${idle?"":"background:"+color(pid)}">${pid}</div>`;
    ticks+=`<span class="tick" style="left:${s*px}px">${s}</span>`;
  });
  ticks+=`<span class="tick" style="left:${w}px">${total}</span>`;
  return `<div class="gscroll"><div style="width:${w+32}px;padding:0 20px 0 12px"><div class="gantt">${blocks}</div><div class="ticks">${ticks}</div></div></div>`;
}
const f=x=>Number(x).toFixed(2);

function section(r){
  let h=`<div class="card"><div class="sect-title"><h3>${r.name}</h3><span class="pill">${r.timeline[r.timeline.length-1][2]} time units</span></div>
  <div class="stats">
    <div class="stat"><b>${f(r.avg.tat)}</b><span>Avg Turnaround</span></div>
    <div class="stat"><b>${f(r.avg.wt)}</b><span>Avg Waiting</span></div>
    <div class="stat"><b>${f(r.avg.rt)}</b><span>Avg Response</span></div></div>
  <h4>Gantt chart</h4>${gantt(r)}
  <h4>Per-process results</h4>
  <table class="res"><thead><tr><th>Process</th><th>AT</th><th>BT</th><th>CT</th><th>TAT</th><th>WT</th><th>RT</th></tr></thead><tbody>`;
  r.processes.forEach(p=>{h+=`<tr><td class="pid"><span class="dot" style="background:${color(p.pid)}"></span> ${p.pid}</td><td>${p.at}</td><td>${p.bt}</td><td>${p.ct}</td><td>${p.tat}</td><td>${p.wt}</td><td>${p.rt}</td></tr>`});
  h+=`</tbody></table>`;
  if(r.trace&&r.trace.length){
    h+=`<h4>Round Robin trace · quantum = ${r.quantum}</h4><table class="res"><thead><tr><th>Slice</th><th>Process</th><th>Start</th><th>End</th><th>Burst before</th><th>Remaining</th></tr></thead><tbody>`;
    r.trace.forEach((t,i)=>{h+=`<tr><td>${i+1}</td><td class="pid"><span class="dot" style="background:${color(t[0])}"></span> ${t[0]}</td><td>${t[1]}</td><td>${t[2]}</td><td>${t[3]}</td><td>${t[4]===0?"✔ done":t[4]}</td></tr>`});
    h+=`</tbody></table>`;
  }
  return h+`</div>`;
}

function compare(list,note){
  const metrics=[["tat","Average Turnaround Time"],["wt","Average Waiting Time"],["rt","Average Response Time"]];
  let h=`<div class="card"><div class="sect-title"><h3>Comparison</h3><span class="pill">lower is better</span></div>`;
  metrics.forEach(([k,label])=>{
    const max=Math.max(...list.map(r=>r.avg[k]),0.0001), min=Math.min(...list.map(r=>r.avg[k]));
    h+=`<h4>${label}</h4>`;
    list.forEach(r=>{h+=`<div class="cmp-row"><span>${r.name}</span><div class="cmp-bar"><i class="${r.avg[k]===min?"best":""}" style="width:${Math.max(4,r.avg[k]/max*100)}%"></i></div><span>${f(r.avg[k])}</span></div>`});
  });
  return h+`<h4>Summary</h4><div class="note">${note}</div></div>`;
}

function draw(data){
  let h="";
  if(data.comparison)h+=compare(data.results,data.comparison);
  data.results.forEach(r=>h+=section(r));
  $("#output").innerHTML=h;
}
$("#sample").click();
</script>

</body>
</html>
"""

def _result_dict(r):
    return {
        "name": r.name,
        "quantum": r.quantum,
        "timeline": [list(t) for t in r.timeline],
        "trace": [list(t) for t in r.rr_trace],
        "processes": [dict(pid=p.pid, at=p.at, bt=p.bt, ct=p.ct, tat=p.tat, wt=p.wt, rt=p.rt)
                      for p in r.processes],
        "avg": {"tat": r.avg_tat, "wt": r.avg_wt, "rt": r.avg_rt},
    }


def _to_int(value, label):
    try:
        text = str(value).strip()
        if text == "":
            raise ValueError
        return int(text)
    except ValueError:
        raise ValueError(f"{label} must be a whole number.")


def simulate(payload):
    """Run the chosen algorithm(s). Returns a JSON-ready dict or raises ValueError."""
    procs = []
    for k, row in enumerate(payload.get("processes", []), start=1):
        pid = str(row.get("pid", "")).strip()
        label = pid or f"row {k}"
        procs.append(Process(pid, _to_int(row.get("at"), f"{label}: arrival time"),
                             _to_int(row.get("bt"), f"{label}: burst time")))
    algo = payload.get("algorithm", "fcfs")
    quantum = None
    if algo in ("rr", "all"):
        quantum = _to_int(payload.get("quantum"), "Time quantum")
    validate(procs, quantum)

    if algo == "fcfs":
        results = [fcfs(procs)]
    elif algo == "sjf":
        results = [sjf(procs)]
    elif algo == "srtf":
        results = [srtf(procs)]
    elif algo == "rr":
        results = [round_robin(procs, quantum)]
    elif algo == "all":
        results = [fcfs(procs), sjf(procs), srtf(procs), round_robin(procs, quantum)]
    else:
        raise ValueError("Unknown algorithm.")

    out = {"results": [_result_dict(r) for r in results], "comparison": None}
    if algo == "all":
        bw = min(results, key=lambda r: r.avg_wt)
        bt = min(results, key=lambda r: r.avg_tat)
        br = min(results, key=lambda r: r.avg_rt)
        out["comparison"] = (
            f"Lowest waiting time: <b>{bw.name}</b> ({bw.avg_wt:.2f}). "
            f"Lowest turnaround time: <b>{bt.name}</b> ({bt.avg_tat:.2f}). "
            f"Lowest response time: <b>{br.name}</b> ({br.avg_rt:.2f}). "
            "SJF/SRTF favor short jobs, FCFS is simple but can cause the convoy effect, "
            "and Round Robin shares the CPU fairly and improves response time at the cost "
            "of more context switches.")
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, HTML, "text/html; charset=utf-8")
        else:
            self._send(404, "Not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/run":
            return self._send(404, "Not found", "text/plain")
        try:
            size = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(size) or b"{}")
            self._send(200, json.dumps(simulate(payload)), "application/json")
        except ValueError as e:
            self._send(400, json.dumps({"error": str(e)}), "application/json")
        except Exception as e:  # never crash the server on bad input
            self._send(500, json.dumps({"error": f"Unexpected error: {e}"}), "application/json")


def serve(port=8765, open_browser=True):
    server = None
    for p in range(port, port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            break
        except OSError:
            continue
    if server is None:
        raise OSError("No free port found.")
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"CPU Scheduling Simulator running at {url}\nPress Ctrl+C to stop.")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
