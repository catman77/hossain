import{g as K,u as J,r as b,ba as _e,l as Y,o as _,y as E,w as s,a as F,a3 as le,h as e,b as l,z as B,A as S,ah as Q,ar as ye,I as xe,$ as ee,Z as te,ai as oe,c as U,x as z,X as Ve,e as I,m as ne,bb as re,j as ge,bc as ke,bd as $e,aN as Te,v as he,n as G,q as Be,N as we,k as Ce,be as Ee,_ as Se}from"./index-BQYgRwvm.js";import{a as Fe,_ as Oe}from"./InfoBox.vue_vue_type_script_setup_true_lang-PSVXsnAa.js";const Ie=K({__name:"ForceEntryForm",props:{modelValue:{required:!0,default:!1,type:Boolean},pair:{type:String,default:""},positionIncrease:{type:Boolean,default:!1}},emits:["update:modelValue"],setup(t,{emit:i}){const o=t,x=i,d=J(),C=b(),p=b(""),u=b(void 0),m=b(void 0),$=b(void 0),n=b(""),y=b(_e.long),T=b("force_entry"),g=[{value:"market",text:"Market"},{value:"limit",text:"Limit"}],f=[{value:"long",text:"Long"},{value:"short",text:"Short"}],h=Y({get(){return o.modelValue},set(V){x("update:modelValue",V)}}),L=()=>{var c;return(c=C.value)==null?void 0:c.checkValidity()},H=async()=>{if(!L())return;const V={pair:p.value};u.value&&(V.price=Number(u.value)),n.value&&(V.ordertype=n.value),m.value&&(V.stakeamount=m.value),d.activeBot.botApiVersion>=2.13&&d.activeBot.shortAllowed&&(V.side=y.value),d.activeBot.botApiVersion>=2.16&&T.value&&(V.entry_tag=T.value),$.value&&(V.leverage=$.value),d.activeBot.forceentry(V),await ye(),x("update:modelValue",!1)},D=()=>{var V,c,M,O,P,q,k,Z;console.log("resetForm"),p.value=o.pair,u.value=void 0,m.value=void 0,n.value=((c=(V=d.activeBot.botState)==null?void 0:V.order_types)==null?void 0:c.forcebuy)||((O=(M=d.activeBot.botState)==null?void 0:M.order_types)==null?void 0:O.force_entry)||((q=(P=d.activeBot.botState)==null?void 0:P.order_types)==null?void 0:q.buy)||((Z=(k=d.activeBot.botState)==null?void 0:k.order_types)==null?void 0:Z.entry)||"limit"},w=()=>{H()},N=V=>{var c;(c=V.srcElement)==null||c.select()};return(V,c)=>{const M=xe,O=ee,P=te,q=oe;return _(),E(q,{id:"forceentry-modal",ref:"modal",modelValue:e(h),"onUpdate:modelValue":c[7]||(c[7]=k=>B(h)?h.value=k:null),title:t.positionIncrease?`Increasing position for ${t.pair}`:"Force entering a trade",onShow:D,onHidden:D,onOk:w},{default:s(()=>[F("form",{ref_key:"form",ref:C,onSubmit:le(H,["stop","prevent"])},[e(d).activeBot.botApiVersion>=2.13&&e(d).activeBot.shortAllowed?(_(),E(O,{key:0,label:"Order direction (Long or Short)","label-for":"order-direction","invalid-feedback":"Order direction must be set",state:e(y)!==void 0},{default:s(()=>[l(M,{id:"order-direction",modelValue:e(y),"onUpdate:modelValue":c[0]||(c[0]=k=>B(y)?y.value=k:null),options:f,name:"radios-btn-default",size:"sm",buttons:"",style:{"min-width":"10em"},"button-variant":"outline-primary"},null,8,["modelValue"])]),_:1},8,["state"])):S("",!0),l(O,{label:"Pair","label-for":"pair-input","invalid-feedback":"Pair is required",state:e(p)!==void 0},{default:s(()=>[l(P,{id:"pair-input",modelValue:e(p),"onUpdate:modelValue":c[1]||(c[1]=k=>B(p)?p.value=k:null),required:"",disabled:t.positionIncrease,onKeydown:Q(w,["enter"]),onFocus:N},null,8,["modelValue","disabled"])]),_:1},8,["state"]),l(O,{label:"*Price [optional]","label-for":"price-input","invalid-feedback":"Price must be empty or a positive number",state:!e(u)||e(u)>0},{default:s(()=>[l(P,{id:"price-input",modelValue:e(u),"onUpdate:modelValue":c[2]||(c[2]=k=>B(u)?u.value=k:null),type:"number",step:"0.00000001",onKeydown:Q(w,["enter"])},null,8,["modelValue"])]),_:1},8,["state"]),l(O,{label:`*Stake-amount in ${e(d).activeBot.stakeCurrency} [optional]`,"label-for":"stake-input","invalid-feedback":"Stake-amount must be empty or a positive number",state:!e(m)||e(m)>0},{default:s(()=>[l(P,{id:"stake-input",modelValue:e(m),"onUpdate:modelValue":c[3]||(c[3]=k=>B(m)?m.value=k:null),type:"number",step:"0.000001",onKeydown:Q(w,["enter"])},null,8,["modelValue"])]),_:1},8,["label","state"]),e(d).activeBot.botApiVersion>2.16&&e(d).activeBot.shortAllowed?(_(),E(O,{key:1,label:"*Leverage to apply [optional]","label-for":"leverage-input","invalid-feedback":"Leverage must be empty or a positive number",state:!e($)||e($)>0},{default:s(()=>[l(P,{id:"leverage-input",modelValue:e($),"onUpdate:modelValue":c[4]||(c[4]=k=>B($)?$.value=k:null),type:"number",step:"0.01",onKeydown:Q(w,["enter"])},null,8,["modelValue"])]),_:1},8,["state"])):S("",!0),l(O,{label:"OrderType","label-for":"ordertype-input","invalid-feedback":"OrderType",state:!0},{default:s(()=>[l(M,{id:"ordertype-input",modelValue:e(n),"onUpdate:modelValue":c[5]||(c[5]=k=>B(n)?n.value=k:null),options:g,name:"radios-btn-orderType",buttons:"","button-variant":"outline-primary",style:{"min-width":"10em"},size:"sm"},null,8,["modelValue"])]),_:1}),e(d).activeBot.botApiVersion>1.16?(_(),E(O,{key:2,label:"*Custom entry tag Optional]","label-for":"enterTag-input"},{default:s(()=>[l(P,{id:"enterTag-input",modelValue:e(T),"onUpdate:modelValue":c[6]||(c[6]=k=>B(T)?T.value=k:null),type:"text",name:"radios-btn-orderType"},null,8,["modelValue"])]),_:1})):S("",!0)],544)]),_:1},8,["modelValue","title"])}}}),Le=F("br",null,null,-1),Ae=K({__name:"ForceExitForm",props:{trade:{type:Object,required:!0},modelValue:{required:!0,default:!1,type:Boolean}},emits:["update:modelValue"],setup(t,{emit:i}){const o=t,x=i,d=J(),C=b(),p=b(void 0),u=b("limit"),m=()=>{var f;return(f=C.value)==null?void 0:f.checkValidity()},$=Y({get(){return o.modelValue},set(g){x("update:modelValue",g)}});function n(){if(!m())return;const g={tradeid:String(o.trade.trade_id)};u.value&&(g.ordertype=u.value),p.value&&(g.amount=p.value),d.activeBot.forceexit(g),$.value=!1}function y(){var g,f,h,L;p.value=o.trade.amount,u.value=((f=(g=d.activeBot.botState)==null?void 0:g.order_types)==null?void 0:f.force_exit)||((L=(h=d.activeBot.botState)==null?void 0:h.order_types)==null?void 0:L.exit)||"limit"}function T(){n()}return(g,f)=>{const h=te,L=ee,H=Ve,D=oe;return _(),U("div",null,[l(D,{id:"forceexit-modal",modelValue:e($),"onUpdate:modelValue":f[3]||(f[3]=w=>B($)?$.value=w:null),title:"Force exiting a trade",onShow:y,onHidden:y,onOk:T},{default:s(()=>[F("form",{ref_key:"form",ref:C,onSubmit:le(n,["stop","prevent"])},[F("p",null,[F("span",null,"Exiting Trade #"+z(t.trade.trade_id)+" "+z(t.trade.pair)+".",1),Le,F("span",null,"Currently owning "+z(t.trade.amount)+" "+z(t.trade.base_currency),1)]),l(L,{label:`*Amount in ${t.trade.base_currency} [optional]`,"label-for":"stake-input","invalid-feedback":"Amount must be empty or a positive number",state:e(p)!==void 0&&e(p)>0},{default:s(()=>[l(h,{id:"stake-input",modelValue:e(p),"onUpdate:modelValue":f[0]||(f[0]=w=>B(p)?p.value=w:null),type:"number",step:"0.000001"},null,8,["modelValue"]),l(h,{id:"stake-input",modelValue:e(p),"onUpdate:modelValue":f[1]||(f[1]=w=>B(p)?p.value=w:null),type:"range",step:"0.000001",min:"0",max:t.trade.amount},null,8,["modelValue","max"])]),_:1},8,["label","state"]),l(L,{label:"*OrderType","label-for":"ordertype-input","invalid-feedback":"OrderType",state:e(u)!==void 0},{default:s(()=>[l(H,{modelValue:e(u),"onUpdate:modelValue":f[2]||(f[2]=w=>B(u)?u.value=w:null),class:"ms-2",options:["market","limit"],style:{"min-width":"7em"},size:"sm"},null,8,["modelValue"])]),_:1},8,["state"])],544)]),_:1},8,["modelValue"])])}}}),Pe={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"},ze=F("path",{fill:"currentColor",d:"M2 12c0 5 4 9 9 9c2.4 0 4.7-.9 6.4-2.6l-1.5-1.5c-1.3 1.4-3 2.1-4.9 2.1c-6.2 0-9.4-7.5-4.9-11.9S18 5.8 18 12h-3l4 4h.1l3.9-4h-3c0-5-4-9-9-9s-9 4-9 9m8 3h2v2h-2zm0-8h2v6h-2z"},null,-1),He=[ze];function Ue(t,i){return _(),U("svg",Pe,[...He])}const Me={name:"mdi-reload-alert",render:Ue},De={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"},qe=F("path",{fill:"currentColor",d:"M18 11h-3v3h-2v-3h-3V9h3V6h2v3h3m2-5v12H8V4zm0-2H8c-1.1 0-2 .9-2 2v12a2 2 0 0 0 2 2h12c1.11 0 2-.89 2-2V4a2 2 0 0 0-2-2M4 6H2v14a2 2 0 0 0 2 2h14v-2H4z"},null,-1),Re=[qe];function Ne(t,i){return _(),U("svg",De,[...Re])}const je={name:"mdi-plus-box-multiple-outline",render:Ne},Ke={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"},Ze=F("path",{fill:"currentColor",d:"M4 20h14v2H4a2 2 0 0 1-2-2V6h2zM20.22 2H7.78C6.8 2 6 2.8 6 3.78v12.44C6 17.2 6.8 18 7.78 18h12.44c.98 0 1.78-.8 1.78-1.78V3.78C22 2.8 21.2 2 20.22 2M19 13.6L17.6 15L14 11.4L10.4 15L9 13.6l3.6-3.6L9 6.4L10.4 5L14 8.6L17.6 5L19 6.4L15.4 10z"},null,-1),Qe=[Ze];function We(t,i){return _(),U("svg",Ke,[...Qe])}const Xe={name:"mdi-close-box-multiple",render:We},Ge={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"},Je=F("path",{fill:"currentColor",d:"M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2m-3.4 14L12 13.4L8.4 17L7 15.6l3.6-3.6L7 8.4L8.4 7l3.6 3.6L15.6 7L17 8.4L13.4 12l3.6 3.6z"},null,-1),Ye=[Je];function et(t,i){return _(),U("svg",Ge,[...Ye])}const tt={name:"mdi-close-box",render:et},ot={class:"d-flex flex-column"},at=K({__name:"TradeActions",props:{botApiVersion:{type:Number,default:1},trade:{type:Object,required:!0},enableForceEntry:{type:Boolean,default:!1}},emits:["forceExit","forceExitPartial","cancelOpenOrder","reloadTrade","deleteTrade","forceEntry"],setup(t){return(i,o)=>{const x=tt,d=ne,C=Xe,p=re,u=je,m=Me,$=ge;return _(),U("div",ot,[t.botApiVersion<=1.1?(_(),E(d,{key:0,class:"btn-xs text-start",size:"sm",title:"Forceexit",onClick:o[0]||(o[0]=n=>i.$emit("forceExit",t.trade))},{default:s(()=>[l(x,{class:"me-1"}),I("Forceexit ")]),_:1})):S("",!0),t.botApiVersion>1.1?(_(),E(d,{key:1,class:"btn-xs text-start",size:"sm",title:"Forceexit limit",onClick:o[1]||(o[1]=n=>i.$emit("forceExit",t.trade,"limit"))},{default:s(()=>[l(x,{class:"me-1"}),I("Forceexit limit ")]),_:1})):S("",!0),t.botApiVersion>1.1?(_(),E(d,{key:2,class:"btn-xs text-start mt-1",size:"sm",title:"Forceexit market",onClick:o[2]||(o[2]=n=>i.$emit("forceExit",t.trade,"market"))},{default:s(()=>[l(x,{class:"me-1"}),I("Forceexit market ")]),_:1})):S("",!0),t.botApiVersion>2.16?(_(),E(d,{key:3,class:"btn-xs text-start mt-1",size:"sm",title:"Forceexit partial",onClick:o[3]||(o[3]=n=>i.$emit("forceExitPartial",t.trade))},{default:s(()=>[l(C,{class:"me-1"}),I("Forceexit partial ")]),_:1})):S("",!0),t.botApiVersion>=2.24&&(t.trade.open_order_id||t.trade.has_open_orders)?(_(),E(d,{key:4,class:"btn-xs text-start mt-1",size:"sm",title:"Cancel open orders",onClick:o[4]||(o[4]=n=>i.$emit("cancelOpenOrder",t.trade))},{default:s(()=>[l(p,{class:"me-1"}),I("Cancel open order ")]),_:1})):S("",!0),t.enableForceEntry?(_(),E(d,{key:5,class:"btn-xs text-start mt-1",size:"sm",title:"Increase position",onClick:o[5]||(o[5]=n=>i.$emit("forceEntry",t.trade))},{default:s(()=>[l(u,{class:"me-1"}),I("Increase position ")]),_:1})):S("",!0),t.botApiVersion>=2.28?(_(),E(d,{key:6,class:"btn-xs text-start mt-1",size:"sm",title:"Reload",onClick:o[6]||(o[6]=n=>i.$emit("reloadTrade",t.trade))},{default:s(()=>[l(m,{class:"me-1"}),I("Reload Trade ")]),_:1})):S("",!0),l(d,{class:"btn-xs text-start mt-1",size:"sm",title:"Delete trade",onClick:o[7]||(o[7]=n=>i.$emit("deleteTrade",t.trade))},{default:s(()=>[l($,{class:"me-1"}),I(" Delete ")]),_:1})])}}}),lt={viewBox:"0 0 24 24",width:"1.2em",height:"1.2em"},nt=F("path",{fill:"currentColor",d:"M10 9a1 1 0 0 1 1-1a1 1 0 0 1 1 1v4.47l1.21.13l4.94 2.19c.53.24.85.77.85 1.35v4.36c-.03.82-.68 1.47-1.5 1.5H11c-.38 0-.74-.15-1-.43l-4.9-4.2l.74-.77c.19-.21.46-.32.74-.32h.22L10 19zm1-4a4 4 0 0 1 4 4c0 1.5-.8 2.77-2 3.46v-1.22c.61-.55 1-1.35 1-2.24a3 3 0 0 0-3-3a3 3 0 0 0-3 3c0 .89.39 1.69 1 2.24v1.22C7.8 11.77 7 10.5 7 9a4 4 0 0 1 4-4"},null,-1),rt=[nt];function it(t,i){return _(),U("svg",lt,[...rt])}const dt={name:"mdi-gesture-tap",render:it},st=K({__name:"TradeActionsPopover",props:{trade:{type:Object,required:!0},id:{type:Number,required:!0},botApiVersion:{type:Number,required:!0},enableForceEntry:{type:Boolean,default:!1}},emits:["forceExit","forceExitPartial","cancelOpenOrder","reloadTrade","deleteTrade","forceEntry"],setup(t,{emit:i}){const o=i,x=b(!1);function d(n,y=void 0){x.value=!1,o("forceExit",n,y)}function C(n){x.value=!1,o("forceExitPartial",n)}function p(n){x.value=!1,o("cancelOpenOrder",n)}function u(n){x.value=!1,o("reloadTrade",n)}function m(n){x.value=!1,o("deleteTrade",n)}function $(n){x.value=!1,o("forceEntry",n)}return(n,y)=>{const T=dt,g=ne,f=at,h=re,L=ke;return _(),U("div",null,[l(g,{id:`btn-actions-${t.id}`,class:"btn-xs",size:"sm",title:"Actions",onClick:y[0]||(y[0]=H=>x.value=!e(x))},{default:s(()=>[l(T)]),_:1},8,["id"]),l(L,{container:"body",target:`btn-actions-${t.id}`,title:`Actions for ${t.trade.pair}`,triggers:"manual",show:e(x),placement:"left"},{default:s(()=>[l(f,{trade:t.trade,"bot-api-version":t.botApiVersion,"enable-force-entry":t.enableForceEntry,onForceExit:d,onForceExitPartial:C,onDeleteTrade:y[1]||(y[1]=H=>m(t.trade)),onCancelOpenOrder:p,onReloadTrade:u,onForceEntry:$},null,8,["trade","bot-api-version","enable-force-entry"]),l(g,{class:"mt-1 w-100 text-start",size:"sm",onClick:y[2]||(y[2]=H=>x.value=!1)},{default:s(()=>[l(h,{class:"me-1"}),I("Close Actions menu ")]),_:1})]),_:1},8,["target","title","show"])])}}}),ut={class:"h-100 overflow-auto w-100"},ct={class:"w-100 d-flex justify-content-between"},mt=K({__name:"TradeList",props:{trades:{required:!0,type:Array},title:{default:"Trades",type:String},stakeCurrency:{required:!1,default:"",type:String},activeTrades:{default:!1,type:Boolean},showFilter:{default:!1,type:Boolean},multiBotView:{default:!1,type:Boolean},emptyText:{default:"No Trades to show.",type:String}},setup(t){const i=t,o=J(),x=$e(),d=Te(),C=b(1),p=b(),u=b(""),m=b({}),$=i.activeTrades?200:15,n=b(),y=b(!1),T=b(!1),g=b(""),f=b(null),h=b({visible:!1,trade:{}}),L=[{key:"actions"}],H=[{key:"close_timestamp",label:"Close date"},{key:"exit_reason",label:"Close Reason"}];function D(a){return G(a,o.activeBot.stakeCurrencyDecimals)}const w=Y(()=>i.trades.length),N=b([]);he(()=>{N.value=[{key:"trade_id",label:"ID"},{key:"pair",label:"Pair"},{key:"amount",label:"Amount"},{key:"stake_amount",label:"Stake amount"},{key:"open_rate",label:"Open rate",formatter:a=>G(a)},{key:i.activeTrades?"current_rate":"close_rate",label:i.activeTrades?"Current rate":"Close rate",formatter:a=>G(a)},{key:"profit",label:i.activeTrades?"Current profit %":"Profit %",formatter:(a,v,A)=>{if(!A)return"";const R=A;return`${Be(R.profit_ratio,2)} ${`(${D(R.profit_abs)})`}`}},{key:"open_timestamp",label:"Open date"},...i.activeTrades?L:H],i.multiBotView&&N.value.unshift({key:"botName",label:"Bot"})});const V=b(void 0);function c(a,v=void 0){m.value=a,f.value=1,g.value=`Really exit trade ${a.trade_id} (Pair ${a.pair}) using ${v} Order?`,V.value=v,d.confirmDialog===!0?T.value=!0:M()}function M(){if(f.value===0){const a={tradeid:String(m.value.trade_id),botId:m.value.botId};o.deleteTradeMulti(a).catch(v=>console.log(v.response))}if(f.value===1){const a={tradeid:String(m.value.trade_id),botId:m.value.botId};V.value&&(a.ordertype=V.value),o.forceSellMulti(a).then(v=>console.log(v)).catch(v=>console.log(v.response))}if(f.value===3){const a={tradeid:String(m.value.trade_id),botId:m.value.botId};o.cancelOpenOrderMulti(a)}V.value=void 0,T.value=!1}function O(a){g.value=`Really delete trade ${a.trade_id} (Pair ${a.pair})?`,f.value=0,m.value=a,T.value=!0}function P(a){m.value=a,y.value=!0}function q(a){g.value=`Cancel open order for trade ${a.trade_id} (Pair ${a.pair})?`,m.value=a,f.value=3,T.value=!0}function k(a){o.reloadTradeMulti({tradeid:String(a.trade_id),botId:a.botId})}function Z(a){h.value.trade=a,h.value.visible=!0}function ie(a,v,A){i.activeTrades&&(A.preventDefault(),console.log(a))}const de=a=>{i.multiBotView&&o.selectedBot!==a.botId&&o.selectBot(a.botId),a&&a.trade_id!==o.activeBot.detailTradeId?(o.activeBot.setDetailTrade(a),i.multiBotView&&x.push({name:"Freqtrade Trading"})):o.activeBot.setDetailTrade(null)},se=()=>{var a;if(o.activeBot.detailTradeId){const v=i.trades.findIndex(A=>A.trade_id===o.activeBot.detailTradeId);v>=0?(a=n.value)==null||a.selectRow(v):(console.log(`Unsetting item for tradeid ${p.value}`),p.value=void 0)}};return we(()=>o.activeBot.detailTradeId,a=>{var A;i.trades.findIndex(R=>R.trade_id===a)<0&&((A=n.value)==null||A.clearSelected())}),(a,v)=>{var ae;const A=st,R=Fe,W=Oe,ue=Ce,ce=Ee,me=te,pe=ee,fe=Ae,ve=Ie,be=oe;return _(),U("div",ut,[l(ue,{ref_key:"tradesTable",ref:n,small:"",hover:"",stacked:"md",items:t.trades.filter(r=>{var j,X;return r.pair.toLowerCase().includes(e(u).toLowerCase())||((j=r.exit_reason)==null?void 0:j.toLowerCase().includes(e(u).toLowerCase()))||((X=r.enter_tag)==null?void 0:X.toLowerCase().includes(e(u).toLowerCase()))}),fields:e(N),"show-empty":"","empty-text":t.emptyText,"per-page":e($),"current-page":e(C),"primary-key":"botTradeId",selectable:"","select-head":!1,"select-mode":"single",onRowContextmenu:ie,onRowClicked:de,onRowSelected:se},{"cell(actions)":s(({index:r,item:j})=>[l(A,{id:r,"enable-force-entry":e(o).activeBot.botState.force_entry_enable,trade:j,"bot-api-version":e(o).activeBot.botApiVersion,onDeleteTrade:X=>O(j),onForceExit:c,onForceExitPartial:P,onCancelOpenOrder:q,onReloadTrade:k,onForceEntry:Z},null,8,["id","enable-force-entry","trade","bot-api-version","onDeleteTrade"])]),"cell(pair)":s(r=>[F("span",null,z(`${r.item.pair}${r.item.open_order_id||r.item.has_open_orders?"*":""}`),1)]),"cell(trade_id)":s(r=>[I(z(r.item.trade_id)+" "+z(e(o).activeBot.botApiVersion>2&&r.item.trading_mode!=="spot"?"| "+(r.item.is_short?"Short":"Long"):""),1)]),"cell(stake_amount)":s(r=>[I(z(D(r.item.stake_amount))+" "+z(r.item.trading_mode!=="spot"?`(${r.item.leverage}x)`:""),1)]),"cell(profit)":s(r=>[l(R,{trade:r.item},null,8,["trade"])]),"cell(open_timestamp)":s(r=>[l(W,{date:r.item.open_timestamp},null,8,["date"])]),"cell(close_timestamp)":s(r=>[l(W,{date:r.item.close_timestamp??0},null,8,["date"])]),_:1},8,["items","fields","empty-text","per-page","current-page"]),F("div",ct,[t.activeTrades?S("",!0):(_(),E(ce,{key:0,modelValue:e(C),"onUpdate:modelValue":v[0]||(v[0]=r=>B(C)?C.value=r:null),"total-rows":e(w),"per-page":e($),"aria-controls":"my-table"},null,8,["modelValue","total-rows","per-page"])),t.showFilter?(_(),E(pe,{key:1,"label-for":"trade-filter"},{default:s(()=>[l(me,{id:"trade-filter",modelValue:e(u),"onUpdate:modelValue":v[1]||(v[1]=r=>B(u)?u.value=r:null),type:"text",placeholder:"Filter"},null,8,["modelValue"])]),_:1})):S("",!0)]),t.activeTrades?(_(),E(fe,{key:0,modelValue:e(y),"onUpdate:modelValue":v[2]||(v[2]=r=>B(y)?y.value=r:null),trade:e(m)},null,8,["modelValue","trade"])):S("",!0),l(ve,{modelValue:e(h).visible,"onUpdate:modelValue":v[3]||(v[3]=r=>e(h).visible=r),pair:(ae=e(h).trade)==null?void 0:ae.pair,"position-increase":""},null,8,["modelValue","pair"]),l(be,{modelValue:e(T),"onUpdate:modelValue":v[4]||(v[4]=r=>B(T)?T.value=r:null),title:"Exit trade",onOk:M},{default:s(()=>[I(z(e(g)),1)]),_:1},8,["modelValue"])])}}}),vt=Se(mt,[["__scopeId","data-v-e7858a8a"]]);export{Ie as _,Xe as a,je as b,vt as c};
//# sourceMappingURL=TradeList-B2l_5J2J.js.map
