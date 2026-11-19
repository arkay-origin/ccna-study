// ----- subnetting drill -----
(function(){
const DK='ccna-drill-v1';
let D={mode:'mixed',scope:'any',ok:0,n:0,streak:0,best:0,by:{}};
try{Object.assign(D,JSON.parse(localStorage.getItem(DK)||'{}'))}catch(e){}
const dsave=()=>{try{localStorage.setItem(DK,JSON.stringify(D))}catch(e){}};
const R=(a,b)=>a+Math.floor(Math.random()*(b-a+1));
const pick=a=>a[Math.floor(Math.random()*a.length)];
const toIp=n=>[n>>>24,(n>>>16)&255,(n>>>8)&255,n&255].join('.');
const maskN=p=>p===0?0:(0xFFFFFFFF<<(32-p))>>>0;
const bin8=v=>v.toString(2).padStart(8,'0');
const norm=s=>String(s||'').trim().replace(/^\//,'').replace(/\s+/g,'').toLowerCase();
const MODES=[['mixed','Mixed'],['facts','Subnet facts'],['size','Size it'],['mask','Masks'],['binary','Binary']];
let cur=null,done=false;

function randIp(){const f=pick([10,172,192,R(1,223)]);let a=f,b=R(0,255);if(f===172)b=R(16,31);if(f===192)b=168;if(a===127)a=126;return((a<<24)>>>0)+(b<<16)+(R(0,255)<<8)+R(0,255)}
function genFacts(){const p=D.scope==='last'?R(24,30):pick([R(8,15),R(16,23),R(16,23),R(24,30),R(24,30)]);const ip=randIp(),m=maskN(p),net=(ip&m)>>>0,bc=(net|(~m>>>0))>>>0;
  const oct=Math.floor((p-1)/8),mo=(m>>>(24-8*oct))&255,bs=256-mo,iv=(ip>>>(24-8*oct))&255,nv=Math.floor(iv/bs)*bs,octName=['1st','2nd','3rd','4th'][oct];
  return{kind:'facts',q:`What are the network, broadcast, first and last usable addresses and the number of usable hosts for ${toIp(ip)}/${p}?`,
    f:[['Network',toIp(net)],['Broadcast',toIp(bc)],['First host',toIp(net+1)],['Last host',toIp(bc-1)],['Usable hosts',String(2**(32-p)-2)]],
    w:[`/${p} = ${toIp(m)}. The interesting octet is the ${octName} (mask value ${mo}).`,`Block size = 256 − ${mo} = ${bs}.`,
       `Count in ${bs}s in the ${octName} octet: ${nv} ≤ ${iv} < ${nv+bs}. Network = ${toIp(net)}.`,`Broadcast = one less than the next block (${nv+bs}) = ${toIp(bc)}.`,
       `First host = network + 1 = ${toIp(net+1)}. Last host = broadcast − 1 = ${toIp(bc-1)}.`,`Hosts = 2^(32 − ${p}) − 2 = 2^${32-p} − 2 = ${(2**(32-p)-2).toLocaleString()}.`]}}
function genSize(){if(Math.random()<.6){const h=D.scope==='last'?R(2,250):pick([R(2,250),R(2,250),R(251,4000),R(4001,60000)]);let b=2;while(2**b-2<h)b++;const p=32-b;
    return{kind:'size',q:`A subnet must hold ${h.toLocaleString()} hosts. What is the longest prefix length (smallest subnet) that fits, and what is its mask?`,
      f:[['Prefix (/n)',String(p)],['Mask',toIp(maskN(p))]],w:[`Need ${h.toLocaleString()} hosts + network + broadcast = ${(h+2).toLocaleString()} addresses.`,`Smallest power of two that is at least that: 2^${b} = ${(2**b).toLocaleString()} (${b} host bits, ${(2**b-2).toLocaleString()} usable).`,`32 − ${b} = /${p}, mask ${toIp(maskN(p))}.`]}}
  const base=D.scope==='last'?24:pick([16,20,22,24]),need=R(2,base>=24?30:200);let k=0;while(2**k<need)k++;const p=base+k;if(p>30)return genSize();
  return{kind:'size',q:`You have a /${base} and need at least ${need} equal subnets. What prefix length gives the most hosts per subnet, and how many usable hosts does each have?`,
    f:[['Prefix (/n)',String(p)],['Usable hosts',String(2**(32-p)-2)]],w:[`Each borrowed bit doubles the subnets. 2^${k} = ${2**k} ≥ ${need}, so borrow ${k} bit${k===1?'':'s'}.`,`/${base} + ${k} = /${p}.`,`Hosts = 2^(32 − ${p}) − 2 = ${(2**(32-p)-2).toLocaleString()}.`]}}
function genMask(){const p=R(8,30),m=maskN(p),wc=(~m)>>>0;if(Math.random()<.5)return{kind:'mask',q:`What are the dotted-decimal mask and the wildcard mask for /${p}?`,f:[['Mask',toIp(m)],['Wildcard',toIp(wc)]],
    w:[`/${p} = ${p} ones then ${32-p} zeros: ${[0,1,2,3].map(i=>bin8((m>>>(24-8*i))&255)).join('.')}.`,`That is ${toIp(m)}.`,`Wildcard = 255.255.255.255 − mask = ${toIp(wc)}.`]};
  return{kind:'mask',q:`What prefix length is the mask ${toIp(m)}, and how many usable hosts does it give?`,f:[['Prefix (/n)',String(p)],['Usable hosts',String(2**(32-p)-2)]],
    w:[`Count the 1 bits: ${[0,1,2,3].map(i=>bin8((m>>>(24-8*i))&255)).join('.')} has ${p}.`,`Hosts = 2^${32-p} − 2 = ${(2**(32-p)-2).toLocaleString()}.`]}}
function genBin(){const v=R(1,255),w=[];let r=v;[128,64,32,16,8,4,2,1].forEach(x=>{if(r>=x){w.push(x);r-=x}});
  if(Math.random()<.5)return{kind:'binary',q:`Convert ${v} to 8-bit binary.`,f:[['Binary',bin8(v)]],w:[`Columns: 128 64 32 16 8 4 2 1.`,`${v} = ${w.join(' + ')}.`,`Put a 1 under each of those: ${bin8(v)}.`]};
  return{kind:'binary',q:`Convert ${bin8(v)} to decimal.`,f:[['Decimal',String(v)]],w:[`Columns: 128 64 32 16 8 4 2 1.`,`The 1s are under ${w.join(', ')}.`,`${w.join(' + ')} = ${v}.`]}}
function gen(){const m=D.mode==='mixed'?pick(['facts','facts','size','mask','binary']):D.mode;return{facts:genFacts,size:genSize,mask:genMask,binary:genBin}[m]()}

function render(){const v=$('drillView');if(!cur){cur=gen();done=false}
  const pct=D.n?Math.round(D.ok/D.n*100):0;
  v.innerHTML=`<div class="tpanel"><h2 style="margin:0">Subnetting drill</h2>
    <p class="tsub">Endless practice with worked answers, using the block-size method: find the interesting octet, block size = 256 − mask value, then count in blocks.</p>
    <div class="seg" role="group" aria-label="Drill type">${MODES.map(([k,t])=>`<button type="button" data-dm="${k}" aria-pressed="${D.mode===k}">${t}</button>`).join('')}</div>
    <div class="seg" role="group" aria-label="Difficulty"><button type="button" data-ds="last" aria-pressed="${D.scope==='last'}">4th octet only</button><button type="button" data-ds="any" aria-pressed="${D.scope==='any'}">Any octet</button></div>
    <p class="tsub" style="color:var(--ink)">${D.ok} of ${D.n} right${D.n?` (${pct}%)`:''} · streak ${D.streak} · best ${D.best}</p></div>
  <div class="tpanel"><p class="mq" style="font-size:1.05rem;margin:0">${esc(cur.q)}</p>
    <form id="dForm" class="dform" autocomplete="off">${cur.f.map(([lab],i)=>`<label class="dfl"><span class="label">${esc(lab)}</span><input class="search dinp" id="df${i}" inputmode="${/hosts|Prefix|Decimal|Binary/.test(lab)?'numeric':'decimal'}" spellcheck="false" autocapitalize="off"></label>`).join('')}
    <div class="btnrow"><button type="submit" class="go" id="dCheck">${done?'Next question →':'Check'}</button>${done?'':'<button type="button" class="tool" id="dShow">Show answer</button>'}</div></form>
    <div id="dOut"></div></div>`;
  v.querySelectorAll('[data-dm]').forEach(b=>b.onclick=()=>{D.mode=b.dataset.dm;dsave();cur=null;render()});
  v.querySelectorAll('[data-ds]').forEach(b=>b.onclick=()=>{D.scope=b.dataset.ds;dsave();cur=null;render()});
  $('dForm').onsubmit=e=>{e.preventDefault();if(done){cur=null;render();setTimeout(()=>{const i=$('df0');if(i)i.focus()},0);return}check(false)};
  if($('dShow'))$('dShow').onclick=()=>check(true);
}
function check(reveal){const res=cur.f.map(([lab,ans],i)=>{const inp=$('df'+i),val=norm(inp.value),good=val===norm(ans);inp.classList.toggle('ok',good&&!reveal);inp.classList.toggle('bad',!good||reveal);return good});
  const all=!reveal&&res.every(Boolean);D.n++;if(all){D.ok++;D.streak++;D.best=Math.max(D.best,D.streak)}else D.streak=0;
  const k=cur.kind;D.by[k]=D.by[k]||{ok:0,n:0};D.by[k].n++;if(all)D.by[k].ok++;dsave();done=true;
  const out=`<div class="${all?'ok':'bad'}" style="border:1px solid;border-radius:4px;padding:12px;margin-top:4px"><b>${all?'Correct.':reveal?'Answer:':'Not quite. Answer:'}</b>
    <ul class="lu" style="margin:8px 0">${cur.f.map(([l,a],i)=>`<li>${esc(l)}: <b>${esc(a)}</b>${!reveal&&!res[i]?' ✗':''}</li>`).join('')}</ul>
    <p class="label" style="margin:10px 0 4px">Worked answer</p><ol class="lu" style="margin:0">${cur.w.map(x=>`<li>${esc(x)}</li>`).join('')}</ol></div>`;
  const keep=cur.f.map((_,i)=>$('df'+i).value),cls=cur.f.map((_,i)=>$('df'+i).className);render();
  cur.f.forEach((_,i)=>{const e=$('df'+i);e.value=keep[i];e.className=cls[i];e.readOnly=true});$('dOut').innerHTML=out;$('dCheck').focus()}
window.renderDrill=render;
})();
