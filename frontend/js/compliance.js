window.Compliance={
rules:[
["Data Protection Clause","Required","Privacy/data protection language should be present.","on"],
["Liability Limitation","Required","Defines the parties' liability boundaries.","on"],
["Termination Clause","Required","Sets termination rights and conditions.","on"],
["Governing Law","Required","Identifies the applicable governing law.","on"],
["Payment Terms","Recommended","Defines payment timing and related terms.","on"],
["Confidentiality","Recommended","Protects confidential business information.","on"]
],
render(){
return `<div class="heading"><div class="eyebrow">Governance</div><h1 class="title">Compliance Rules</h1></div><section class="card page-card"><div style="display:flex;justify-content:space-between;align-items:center;gap:10px"><div><h3>Active compliance checklist</h3><p>These rules are presented in the workspace and the backend remains the source of truth for analysis.</p></div><button class="btn primary" onclick="ContractGuard.toast('Rule editor opened')">＋ Add Rule</button></div><div class="searchbar"><input id="ruleSearch" class="input" placeholder="Search rules…"><select id="ruleFilter" class="select"><option value="all">All rules</option><option value="required">Required</option><option value="recommended">Recommended</option></select></div><div id="ruleList" class="rule-list"></div></section>`;
},
bind(){
const draw=()=>{
  const q=(ContractGuard.$("#ruleSearch").value||"").toLowerCase();
  const f=ContractGuard.$("#ruleFilter").value;
  const rows=this.rules.filter(r=>
    (f==="all"||r[1].toLowerCase()===f) &&
    (!q||r.join(" ").toLowerCase().includes(q))
  );
  ContractGuard.$("#ruleList").innerHTML=rows.length
    ? rows.map((r,i)=>`<div class="rule"><span class="circle ok">${i+1}</span><div class="rule-copy"><b>${r[0]}</b><small>${r[2]}</small></div><span class="badge ${r[1]==="Required"?"ok":"miss"}">${r[1]}</span><button class="toggle ${r[3]}" onclick="this.classList.toggle('on')"></button></div>`).join("")
    : `<div class="empty"><div><div class="big">◇</div><b>No matching rules</b></div></div>`;
};
ContractGuard.$("#ruleSearch").oninput=draw;
ContractGuard.$("#ruleFilter").onchange=draw;
draw();
}
};