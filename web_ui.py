









































































































































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
