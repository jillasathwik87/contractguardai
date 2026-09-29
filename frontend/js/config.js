(function(){
  function api(){
    if(window.CONTRACTGUARD_API_URL) return String(window.CONTRACTGUARD_API_URL).replace(/\/+$/,"");
    try{const saved=localStorage.getItem("contractGuardApiUrl"); if(saved) return saved.replace(/\/+$/,"")}catch(e){}
    const meta=document.querySelector('meta[name="api-base"]');
    if(meta && meta.content) return meta.content.replace(/\/+$/,"");
    if(location.protocol==="http:" || location.protocol==="https:") return location.origin;
    return "http://127.0.0.1:8000";
  }
  window.getApiBaseUrl=()=>api();
})();