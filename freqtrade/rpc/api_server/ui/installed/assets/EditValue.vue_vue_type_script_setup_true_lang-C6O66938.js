import{o as n,c,a as p,g as E,r as V,v as D,N as M,h as d,at as S,y as f,z as H,F as g,b as l,w as u,A as m,M as q,a3 as F,Z as U,aa as j,m as I,j as R,ac as Z,aU as G}from"./index-BQYgRwvm.js";import{_ as J}from"./plus-box-outline-CsqaIVst.js";const K={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"},L=p("path",{fill:"currentColor",d:"M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12z"},null,-1),O=[L];function P(e,v){return n(),c("svg",K,[...O])}const Q={name:"mdi-content-copy",render:P},T={class:"flex-grow-1"},Y=E({__name:"EditValue",props:{modelValue:{type:String,required:!0},allowEdit:{type:Boolean,default:!1},allowAdd:{type:Boolean,default:!1},allowDuplicate:{type:Boolean,default:!1},editableName:{type:String,required:!0},alignVertical:{type:Boolean,default:!1}},emits:["delete","new","duplicate","rename"],setup(e,{emit:v}){const o=e,r=v,t=V(""),a=V(0);D(()=>{t.value=o.modelValue});function k(){a.value=0,t.value=o.modelValue}function h(){t.value=t.value+" (copy)",a.value=3}function b(){t.value="",a.value=2}M(()=>o.modelValue,()=>{t.value=o.modelValue});function w(){a.value===2?r("new",t.value):a.value===3?r("duplicate",o.modelValue,t.value):r("rename",o.modelValue,t.value),a.value=0}return(y,i)=>{const N=U,C=j,s=I,x=Q,$=R,z=J,B=Z,A=G;return n(),c("form",{class:"d-flex flex-row",onSubmit:F(w,["prevent"])},[p("div",T,[d(a)===0?S(y.$slots,"default",{key:0}):(n(),f(N,{key:1,modelValue:d(t),"onUpdate:modelValue":i[0]||(i[0]=_=>H(t)?t.value=_:null),size:"sm"},null,8,["modelValue"]))]),p("div",{class:q(["flex-grow-2 mt-auto d-flex gap-1 ms-1",e.alignVertical?"flex-column":"flex-row"])},[e.allowEdit&&d(a)===0?(n(),c(g,{key:0},[l(s,{size:"sm",variant:"secondary",title:`Edit this ${e.editableName}.`,onClick:i[1]||(i[1]=_=>a.value=1)},{default:u(()=>[l(C)]),_:1},8,["title"]),e.allowDuplicate?(n(),f(s,{key:0,size:"sm",variant:"secondary",title:`Duplicate ${e.editableName}.`,onClick:h},{default:u(()=>[l(x)]),_:1},8,["title"])):m("",!0),l(s,{size:"sm",variant:"secondary",title:`Delete this ${e.editableName}.`,onClick:i[2]||(i[2]=_=>y.$emit("delete",e.modelValue))},{default:u(()=>[l($)]),_:1},8,["title"])],64)):m("",!0),e.allowAdd&&d(a)===0?(n(),f(s,{key:1,size:"sm",title:`Add new ${e.editableName}.`,variant:"primary",onClick:b},{default:u(()=>[l(z)]),_:1},8,["title"])):m("",!0),d(a)!==0?(n(),c(g,{key:2},[l(s,{size:"sm",title:`Add new ${e.editableName}`,variant:"primary",onClick:w},{default:u(()=>[l(B)]),_:1},8,["title"]),l(s,{size:"sm",title:"Abort",variant:"secondary",onClick:k},{default:u(()=>[l(A)]),_:1})],64)):m("",!0)],2)],32)}}});export{Y as _,Q as a};
//# sourceMappingURL=EditValue.vue_vue_type_script_setup_true_lang-C6O66938.js.map
