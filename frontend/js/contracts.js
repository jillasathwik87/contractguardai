window.Contracts={
file:null, available:[], result:null,
render(){
 return `<div class="heading"><div class="eyebrow">Contract Management</div><h1 class="title">Upload Contract</h1></div>
 <div class="grid">
 <section class="card page-card"><div class="card-title"><span class="icon">↥</span>Upload Contract</div><p style="margin:7px 0 14px 29px">Select a PDF and analyze it against the active compliance rules.</p>
 <div id="drop" class="dropzone" style="min-height:220px"><div><div class="cloud">☁</div><strong>Drop your PDF here or click to browse</strong><small>PDF files only • maximum 10MB</small><button id="choose" class="btn primary" style="margin-top:11px">Choose PDF</button><input id="file" type="file" accept=".pdf,application/pdf" hidden></div></div>
 <div id="fileRow"></div><div id="selectorBox" style="display:none;margin-top:12px"><label class="form-label">Contract to analyze</label><select id="contractSelector" class="select" style="width:100%"></select></div>
 <button id="analyze" class="btn primary full" disabled>▷ &nbsp; Analyze Contract</button><p id="status" class="micro">Choose a PDF to begin.</p>
 <div style="margin-top:16px;border:1px solid var(--line);border-radius:9px;padding:12px"><div class="card-title">What is checked?</div><p style="font-size:10px;color:var(--muted);line-height:1.6;margin:7px 0">Data protection, liability limitation, termination, governing law, payment terms and other rules defined by the compliance engine.</p></div>
 </section>
 <section class="card analysis" id="results"><div class="card-head"><div class="card-title"><span class="icon">▥</span>Analysis Results</div></div><div id="resultBody"><div class="empty"><div><div class="big">✦</div><b>Ready to analyze</b><p>Upload a PDF and click Analyze Contract. Results, score, checklist and AI summary will appear here.</p></div></div></div></section>
 </div>`;
},
bind(){
 const f=ContractGuard.$("#file"), choose=ContractGuard.$("#choose"), drop=ContractGuard.$("#drop"), analyze=ContractGuard.$("#analyze");
 choose.onclick=()=>f.click();
 f.onchange=()=>{if(f.files[0])this.select(f.files[0])};
 ["dragover"].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add("over")}));
 ["dragleave"].forEach(ev=>drop.addEventListener(ev,()=>drop.classList.remove("over")));
 drop.addEventListener("drop",e=>{e.preventDefault();drop.classList.remove("over");if(e.dataTransfer.files[0])this.select(e.dataTransfer.files[0])});
 analyze.onclick=()=>this.analyze();
},
select(file){
 if((file.type!=="application/pdf"&&!file.name.toLowerCase().endsWith(".pdf"))){ContractGuard.toast("Please choose a PDF file.");return}
 if(file.size>10*1024*1024){ContractGuard.toast("PDF must be 10MB or smaller.");return}
 this.file=file; ContractGuard.$("#fileRow").innerHTML=`<div class="file-row"><span class="pdf">PDF</span><div class="file-copy"><b>${ContractGuard.escape(file.name)}</b><small>${(file.size/1024/1024).toFixed(2)} MB</small></div><button class="x" id="removeFile">×</button></div>`;
 ContractGuard.$("#removeFile").onclick=()=>{this.file=null;this.available=[];ContractGuard.$("#fileRow").innerHTML="";ContractGuard.$("#selectorBox").style.display="none";ContractGuard.$("#analyze").disabled=true;ContractGuard.$("#status").textContent="Choose a PDF to begin."};
 ContractGuard.$("#status").textContent="Reading available contracts…";ContractGuard.$("#analyze").disabled=true;
 const fd=new FormData();fd.append("file",file);
 fetch(`${getApiBaseUrl()}/api/analyze`,{method:"POST",body:fd}).then(async r=>{const d=await r.json();if(!r.ok||!d.success)throw new Error(d.error||d.detail||"Could not read PDF.");this.available=d.available_contracts||[];this.showSelector()}).catch(e=>{ContractGuard.$("#status").textContent="Could not load contracts.";ContractGuard.toast(e.message)});
},
showSelector(){
 const box=ContractGuard.$("#selectorBox"), sel=ContractGuard.$("#contractSelector"), btn=ContractGuard.$("#analyze");
 sel.innerHTML=`<option value="">Select a contract</option>`+this.available.map(x=>`<option value="${ContractGuard.escape(x)}">${ContractGuard.escape(x)}</option>`).join("");
 box.style.display="block";sel.onchange=()=>{btn.disabled=!sel.value;ContractGuard.$("#status").textContent=sel.value?"Contract selected. Ready to analyze.":"Please select a contract.";};ContractGuard.$("#status").textContent="Select the contract you want to analyze.";
},
async analyze(){
 const sel=ContractGuard.$("#contractSelector");if(!this.file||!sel.value)return;
 const btn=ContractGuard.$("#analyze");btn.disabled=true;btn.textContent="Analyzing…";ContractGuard.$("#status").textContent="Analyzing clauses and compliance rules…";
 try{const fd=new FormData();fd.append("file",this.file);const r=await fetch(`${getApiBaseUrl()}/api/analyze?contract_name=${encodeURIComponent(sel.value)}`,{method:"POST",body:fd});const d=await r.json();if(!r.ok||!d.success)throw new Error(d.error||d.detail||"Analysis failed.");this.result=d;ContractGuard.saveHistory(d);this.renderResult(d);ContractGuard.toast("Contract analysis completed.");}catch(e){ContractGuard.$("#status").textContent="Analysis failed.";ContractGuard.toast(e.message)}finally{btn.disabled=false;btn.textContent="▷  Analyze Contract"}},
renderResult(d){
 const checks=d.checklist||[];const cls=s=>s==="PASS"?"ok":s==="FAIL"?"fail":"miss";const symbol=s=>s==="PASS"?"✓":s==="FAIL"?"!":"?";
 ContractGuard.$("#resultBody").innerHTML=`<div class="banner"><span class="pdf">PDF</span><div class="copy"><b>${ContractGuard.escape(d.contract_name)}</b><small>PDF • Analyzed just now</small></div><span class="badge ${d.score>=80?"ok":d.score>=60?"miss":"fail"}">${d.score>=80?"✓ Compliant":"Review Required"}</span></div>
 <div class="stats"><div class="stat type"><small>Contract Type</small><b><span class="mini">▣</span>${ContractGuard.escape(d.contract_type)}</b></div><div class="stat green"><small>Passed</small><b>${d.pass||0}</b></div><div class="stat red"><small>Failed</small><b>${d.fail||0}</b></div><div class="stat amber"><small>Missing</small><b>${d.missing||0}</b></div></div>
 <div class="scorebox"><small style="color:var(--muted);font-size:9px">Compliance Score</small><div class="scoreline"><span class="big-score">${d.score||0}%</span><div class="bar"><i style="width:${Math.max(0,Math.min(100,Number(d.score||0)))}%"></i></div></div></div>
 <div class="checklist"><div class="check-head"><div class="card-title"><span class="icon">▤</span>Compliance Checklist</div><a class="link" href="#/compliance">View all rules →</a></div>${checks.map(c=>`<div class="check-row"><span class="circle ${cls(c.status)}">${symbol(c.status)}</span><strong>${ContractGuard.escape(c.name)}</strong><span class="req">${c.status==="PASS"?"Required":"Check"}: ${ContractGuard.escape(c.description||"")}</span><span class="pill ${cls(c.status)}">${c.status}</span></div>`).join("")}</div>
 <div class="summary"><div class="card-title">✦ &nbsp;AI Summary</div><p>${ContractGuard.escape(d.summary||"No summary returned.")}</p></div>
 <div class="source"><div class="card-title">◉ &nbsp;Source Information</div><p>File: ${ContractGuard.escape(d.contract_name)}<br>Source: Upload<br>Analyzed: ${new Date().toLocaleString()}</p></div>`;
 ContractGuard.$("#status").textContent="Analysis complete. Results are shown on this page.";
}
};