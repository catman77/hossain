import{o as n,c,a as t,g as w,u as L,r as b,v as C,F as k,L as B,e as m,x as r,M as y,h as V,b as s,w as p,i as N,m as R,_ as f}from"./index-BQYgRwvm.js";const $={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"},z=t("path",{fill:"currentColor",d:"M10 4h4v9l3.5-3.5l2.42 2.42L12 19.84l-7.92-7.92L6.5 9.5L10 13z"},null,-1),S=[z];function E(_,a){return n(),c("svg",$,[...S])}const M={name:"mdi-arrow-down-thick",render:E},T={class:"d-flex h-100 p-0 align-items-start"},F={class:"text-muted"},I={class:"text-{{ log[1] }}"},A={class:"d-flex flex-column gap-1 ms-1"},D=w({__name:"LogViewer",setup(_){const a=L(),e=b(null);C(async()=>{i()});async function i(){await a.activeBot.getLogs(),l()}function h(d){switch(d){case"WARNING":return"text-warning";case"ERROR":return"text-danger";default:return"text-secondary"}}function l(){e.value&&(e.value.scrollTop=e.value.scrollHeight)}return(d,j)=>{const g=N,u=R,x=M;return n(),c("div",T,[t("div",{ref_key:"scrollContainer",ref:e,class:"border p-1 text-start pb-5 w-100 h-100 overflow-auto"},[(n(!0),c(k,null,B(V(a).activeBot.lastLogs,(o,v)=>(n(),c("pre",{key:v,class:"m-0 overflow-visible",style:{"line-height":"unset"}},[t("span",F,[m(r(o[0])+" ",1),t("span",{class:y(h(o[3]))},r(o[3].padEnd(7," ")),3),m(" "+r(o[2])+" - ",1)]),t("span",I,r(o[4]),1)]))),128))],512),t("div",A,[s(u,{id:"refresh-logs",size:"sm",title:"Reload Logs",onClick:i},{default:p(()=>[s(g)]),_:1}),s(u,{size:"sm",title:"Scroll to bottom",onClick:l},{default:p(()=>[s(x)]),_:1})])])}}}),G=f(D,[["__scopeId","data-v-f7c6fcb3"]]),H={},O={class:"p-1 p-md-4 pe-md-2 h-100"};function W(_,a){const e=G;return n(),c("div",O,[s(e)])}const J=f(H,[["render",W]]);export{J as default};
//# sourceMappingURL=LogView-Q6Hk8KAF.js.map