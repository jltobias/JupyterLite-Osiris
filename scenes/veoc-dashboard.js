/* Original, dependency-free dashboard. All values and event markers are fictional. */
(() => {
  'use strict';
  const sectors = [
    {name:'Harbor',x:620,y:367,lat:29.93,lon:-90.07,population:18000,calls:34,flood:0.9,beds:12,road:28,reporting:.84},
    {name:'Eastbank',x:780,y:295,lat:29.96,lon:-90.00,population:24000,calls:22,flood:0.4,beds:24,road:19,reporting:.91},
    {name:'Canal',x:525,y:245,lat:29.98,lon:-90.10,population:12000,calls:31,flood:1.4,beds:4,road:42,reporting:.68},
    {name:'North',x:645,y:105,lat:30.05,lon:-90.07,population:30000,calls:18,flood:0.1,beds:38,road:14,reporting:.96},
    {name:'Bayou',x:410,y:442,lat:29.89,lon:-90.12,population:9000,calls:25,flood:1.1,beds:7,road:51,reporting:.72},
    {name:'Airport',x:195,y:200,lat:30.00,lon:-90.25,population:16000,calls:11,flood:0.2,beds:18,road:23,reporting:.89}
  ];
  const signals = [
    {name:'Public camera · underpass',kind:'cameras',x:565,y:290,glyph:'▣',status:'Unverified',detail:'Illustrative frame lead; operator, frame time, and blind spots must be checked.'},
    {name:'Public camera · harbor',kind:'cameras',x:670,y:390,glyph:'▣',status:'Unverified',detail:'Illustrative camera lead near the port; a single frame cannot establish road status.'},
    {name:'Public camera · airport',kind:'cameras',x:250,y:185,glyph:'▣',status:'Unverified',detail:'Illustrative camera lead; verify source and timestamp.'},
    {name:'Aircraft track A',kind:'aircraft',x:175,y:98,glyph:'✈',status:'Context',detail:'Synthetic track. A flight marker says nothing about mission, cargo, or authorization.'},
    {name:'Aircraft track B',kind:'aircraft',x:360,y:130,glyph:'✈',status:'Context',detail:'Synthetic aviation context; confirm any operational flight with the aviation authority.'},
    {name:'Port reference',kind:'maritime',x:785,y:455,glyph:'⚓',status:'Static',detail:'Illustrative port marker, not live vessel movement or port status.'},
    {name:'Chokepoint reference',kind:'maritime',x:905,y:365,glyph:'⚓',status:'Static',detail:'Illustrative maritime reference; no AIS is shown in this exercise.'},
    {name:'Severe weather lead',kind:'hazards',x:330,y:295,glyph:'⚠',status:'Modeled',detail:'Exercise weather warning, not a live NHC product.'},
    {name:'Thermal hotspot lead',kind:'hazards',x:340,y:485,glyph:'△',status:'Unverified',detail:'Exercise thermal lead; a hotspot is not an incident impact assessment.'},
    {name:'Seismic lead',kind:'hazards',x:855,y:155,glyph:'◎',status:'Unverified',detail:'Exercise seismic marker; verify at USGS before use.'},
    {name:'Clinic · North',kind:'clinics',x:685,y:140,glyph:'✚',status:'Modeled',detail:'Fictional facility and bed count.'},
    {name:'Clinic · Eastbank',kind:'clinics',x:815,y:255,glyph:'✚',status:'Modeled',detail:'Fictional facility and bed count.'},
    {name:'Clinic · Harbor',kind:'clinics',x:605,y:410,glyph:'✚',status:'Modeled',detail:'Fictional facility and bed count.'}
  ];
  const leads = [
    {title:'Canal underpass image',time:'T+2 h',status:'Unverified',description:'Camera viewpoint and frame timestamp needed.'},
    {title:'Bayou road closure',time:'T+3 h',status:'Field report',description:'Exercise report; request a second confirmation.'},
    {title:'Heavy rain warning',time:'T+0 h',status:'Modeled',description:'Exercise weather desk; compare with official advisories.'},
    {title:'Harbor bridge status',time:'T+4 h',status:'Unknown',description:'No current field observation in the exercise.'},
    {title:'Clinic bed count',time:'T+4 h',status:'Unverified',description:'Call facility liaison before allocating patients.'}
  ];
  const capabilities = [
    ['◉','Earthquakes','USGS event monitoring','https://earthquake.usgs.gov/earthquakes/map/'],
    ['△','Fire hotspots','NASA FIRMS context','https://firms.modaps.eosdis.nasa.gov/'],
    ['☁','Severe weather','NASA EONET / NOAA','https://eonet.gsfc.nasa.gov/'],
    ['✈','Aviation','OpenSky tracks','https://opensky-network.org/'],
    ['⚓','Maritime','Ports and chokepoints','https://github.com/simplifaisoul/osiris#key-capabilities'],
    ['▣','Public cameras','Operator-origin views','https://osirisai.live/'],
    ['▥','Live broadcasts','News context; verify claims','https://osirisai.live/'],
    ['◌','Satellites & space','NOAA / satellite context','https://www.swpc.noaa.gov/'],
    ['⌁','Cyber & CVEs','Specialist investigation','https://nvd.nist.gov/'],
    ['◇','Sanctions','Verify official records','https://ofac.treasury.gov/sanctions-list-service'],
    ['✧','OI Assist','Map interaction; user key','https://github.com/simplifaisoul/osiris#oi--a-prediction-engine-bring-your-own-key'],
    ['∿','OI Forecast','Exploratory scenarios','https://github.com/simplifaisoul/osiris#oi--a-prediction-engine-bring-your-own-key'],
    ['⚑','Conflict zones','Static OSINT context','https://github.com/simplifaisoul/osiris#conflict-zone-monitoring'],
    ['✉','Telegram OSINT','Public-channel context','https://github.com/simplifaisoul/osiris#telegram-osint-layer'],
    ['◈','Crypto tracing','Specialist investigation','https://github.com/simplifaisoul/osiris#crypto-wallet-intelligence'],
    ['⌘','RECON toolkit','Authorized assets only','https://github.com/simplifaisoul/osiris#recon-toolkit']
  ];
  const $ = id => document.getElementById(id);
  const getHour = () => Number($('hour').value);
  const getState = (s,h=getHour()) => ({...s,calls:Math.round(s.calls*(.68+.08*h)),flood:+(s.flood*(.60+.1*h)).toFixed(2),reporting:Math.min(1,s.reporting*(.85+.0375*h))});
  const svg = (body,viewBox='0 0 440 245') => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox}" preserveAspectRatio="xMidYMid meet">${body}</svg>`;
  const line = (values,x0,y0,w,h,max) => values.map((v,i)=>`${i?'L':'M'}${(x0+i*w/(values.length-1)).toFixed(1)},${(y0+h-v/max*h).toFixed(1)}`).join(' ');
  const download = (name,content,type) => {const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1200)};
  const layerOn = name => document.querySelector(`[data-layer="${name}"]`).checked;
  const makeSvgNode = (tag,attrs={}) => {const el=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));return el};

  function selectSector(s){const v=getState(s);$('selection').innerHTML=`<span class="eyebrow">EXERCISE SECTOR / ${s.name.toUpperCase()}</span><h3>${s.name}</h3><dl><dt>Assistance calls</dt><dd>${v.calls}</dd><dt>Modeled depth</dt><dd>${v.flood.toFixed(1)} m</dd><dt>Open beds</dt><dd>${s.beds}</dd><dt>Road time</dt><dd>${s.road} min</dd><dt>Reporting</dt><dd>${Math.round(v.reporting*100)}%</dd><dt>Calls / 10k</dt><dd>${(v.calls/s.population*10000).toFixed(1)}</dd></dl>`;$('map-caption').textContent=`${s.name}: synthetic metrics at T+${getHour()} h. Confirm any real condition with a source owner.`}
  function selectSignal(s){$('selection').innerHTML=`<span class="eyebrow">${s.kind.toUpperCase()} / ${s.status.toUpperCase()}</span><h3>${s.name}</h3><p>${s.detail}</p>`;$('map-caption').textContent=`${s.name}: ${s.status.toLowerCase()} exercise lead. Open the provider before using an analogous live signal.`}
  function renderMap(){const flood=$('flood-zones'),routes=$('route-lines'),points=$('sector-points'),other=$('signal-points');for(const el of [flood,routes,points,other])el.replaceChildren();const metric=$('metric').value;
    for(const s of sectors){const v=getState(s);if(layerOn('flood')){const e=makeSvgNode('ellipse',{cx:s.x,cy:s.y,rx:32+v.flood*50,ry:23+v.flood*31,fill:v.flood>=1?'#f38452':'#58c9c6',opacity:v.flood>=1?.18:.09});flood.append(e)}if(layerOn('calls')){const g=makeSvgNode('g',{'data-clickable':'',tabindex:0,role:'button','aria-label':`${s.name}, ${v.calls} synthetic calls`});const val=metric==='calls'?v.calls:metric==='flood'?v.flood*25:metric==='reporting'?v.reporting*32:v.calls/s.population*10000;const radius=13+Math.min(val,40)*.42;g.append(makeSvgNode('circle',{cx:s.x,cy:s.y,r:radius,fill:v.flood>=1?'#ef955e':'#33c8be',opacity:.82,stroke:'#dcfaf6','stroke-width':2}));const t=makeSvgNode('text',{x:s.x+radius+5,y:s.y+5,class:'map-label'});t.textContent=s.name;g.append(t);g.addEventListener('click',()=>selectSector(s));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectSector(s)}});points.append(g)}}
    if(layerOn('clinics')){const path=makeSvgNode('path',{d:'M685 140L815 255L605 410',fill:'none',stroke:'#8de0a2','stroke-width':2,'stroke-dasharray':'9 8',opacity:.45});routes.append(path)}
    const colors={clinics:'#8de0a2',cameras:'#73bef3',aircraft:'#bc9aff',maritime:'#80ded7',hazards:'#ff6875'};for(const s of signals){if(!layerOn(s.kind))continue;const g=makeSvgNode('g',{'data-clickable':'',tabindex:0,role:'button','aria-label':s.name});g.append(makeSvgNode('circle',{cx:s.x,cy:s.y,r:15,fill:'#0a2638',stroke:colors[s.kind],'stroke-width':2.5}));const icon=makeSvgNode('text',{x:s.x,y:s.y+6,'text-anchor':'middle',fill:colors[s.kind],'font-size':19,'font-weight':800});icon.textContent=s.glyph;g.append(icon);g.addEventListener('click',()=>selectSignal(s));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectSignal(s)}});other.append(g)}
    $('count-flood').textContent=sectors.filter(s=>getState(s).flood>=1).length;
  }
  function renderKPIs(){const v=sectors.map(s=>getState(s));$('kpi-calls').textContent=v.reduce((a,s)=>a+s.calls,0);$('kpi-flood').textContent=v.filter(s=>s.flood>=1).length+' / 6';$('kpi-beds').textContent=sectors.reduce((a,s)=>a+s.beds,0);$('kpi-reporting').textContent=Math.round(v.reduce((a,s)=>a+s.reporting*s.population,0)/v.reduce((a,s)=>a+s.population,0)*100)+'%';$('kpi-queue').textContent=leads.filter(x=>x.status==='Unverified'||x.status==='Unknown').length;$('hour-label').textContent=`T+${getHour()} h`;
    const series=Array.from({length:13},(_,i)=>sectors.reduce((a,s)=>a+getState(s,i).calls,0));$('calls-spark').innerHTML=svg(`<path d="${line(series,2,4,135,37,Math.max(...series))}" fill="none" stroke="#65e4dc" stroke-width="3"/>`,'0 0 140 45')}
  function renderFeed(){$('feed').innerHTML='';for(const lead of leads){const b=document.createElement('button');b.type='button';b.innerHTML=`<b>${lead.title}</b><span class="status ${lead.status==='Field report'?'verified':lead.status==='Modeled'?'modeled':''}">${lead.status}</span><small>${lead.time} · inspect lead</small>`;b.onclick=()=>{$('selection').innerHTML=`<span class="eyebrow">EVIDENCE LEAD / ${lead.status.toUpperCase()}</span><h3>${lead.title}</h3><p>${lead.description}</p>`};$('feed').append(b)}}
  function renderTrend(){const values=Array.from({length:13},(_,i)=>sectors.reduce((a,s)=>a+getState(s,i).calls,0));const coverage=Array.from({length:13},(_,i)=>sectors.reduce((a,s)=>a+getState(s,i).reporting*s.population,0)/sectors.reduce((a,s)=>a+s.population,0)*100);const selected=getHour();let g='<path d="M35 16V205H422" stroke="#7899a6" stroke-opacity=".55" fill="none"/>';for(let i=0;i<=4;i++){const y=205-i*45;g+=`<path d="M35 ${y}H422" stroke="#6b9caa" stroke-opacity=".14"/><text x="5" y="${y+4}" fill="#91b3bb" font-size="11">${i*60}</text>`}g+=`<path d="${line(values,35,20,385,185,240)}" fill="none" stroke="#4ad9ce" stroke-width="3"/><path d="${line(coverage,35,20,385,185,100)}" fill="none" stroke="#ffb27b" stroke-width="3"/><path d="M${35+selected*385/12} 20V205" stroke="#fff" stroke-dasharray="4 5" opacity=".7"/>`;for(let i=0;i<=12;i+=3)g+=`<text x="${35+i*385/12}" y="230" fill="#9dbac2" font-size="11" text-anchor="middle">T+${i}</text>`;g+='<text x="230" y="18" fill="#4ad9ce" font-size="11">● Calls</text><text x="300" y="18" fill="#ffb27b" font-size="11">● Coverage %</text>';$('trend-chart').innerHTML=svg(g)}
  function renderSectorChart(){const v=sectors.map(s=>getState(s));let g='<text x="170" y="15" fill="#58d9d0" font-size="11">Calls per 10k</text><text x="315" y="15" fill="#ffad73" font-size="11">Road minutes</text>';v.forEach((s,i)=>{const y=35+i*33;g+=`<text x="4" y="${y+11}" fill="#dae9ea" font-size="12">${s.name}</text><rect x="85" y="${y}" width="${Math.min(170,s.calls/s.population*10000*4.6)}" height="11" rx="4" fill="#42d5cb"/><rect x="85" y="${y+14}" width="${s.road*2.5}" height="9" rx="4" fill="#ffad73"/><text x="270" y="${y+11}" fill="#bcd9dd" font-size="10">${(s.calls/s.population*10000).toFixed(1)}</text>`});$('sector-chart').innerHTML=svg(g)}
  function scored(){return sectors.map(s=>{const v=getState(s);const score=.35*Math.min(v.calls/s.population*10000/30,1)+.30*Math.min(v.flood/1.5,1)+.20*Math.min(s.road/60,1)+.15*(1-v.reporting);return {...v,score}}).sort((a,b)=>b.score-a.score)}
  function renderPriority(){const ranked=scored();let g='';ranked.forEach((s,i)=>{const y=19+i*34;g+=`<text x="5" y="${y+14}" fill="#deeeee" font-size="12">${i+1}. ${s.name}</text><rect x="102" y="${y}" width="${Math.max(3,s.score*320)}" height="19" rx="5" fill="${i<2?'#f39b68':'#39beb9'}"/><text x="${Math.min(420,108+s.score*320)}" y="${y+14}" fill="#d7edf0" font-size="11">${s.score.toFixed(2)}</text>`});$('priority-chart').innerHTML=svg(g)}
  function renderSitrep(){const ranked=scored(),h=getHour(),calls=ranked.reduce((a,s)=>a+s.calls,0);$('sitrep').innerHTML=`<span class="eyebrow">EXERCISE SITREP · T+${h} H</span><p><strong>Situation.</strong> ${calls} synthetic assistance calls across six fictional sectors; ${ranked.filter(s=>s.flood>=1).length} sectors meet the modeled 1 m water-depth threshold.</p><p><strong>Priority for verification.</strong> ${ranked[0].name} and ${ranked[1].name} lead the illustrative score. Confirm road status, need, reporting, and bed availability with field teams.</p><p><strong>Evidence boundary.</strong> Verified real-world facts: none in this exercise. Flood depth and travel times are modeled; camera and facility leads are unverified.</p><p><strong>Next briefing.</strong> Record the observation and retrieval time for each live OSIRIS layer used, then link original provider records.</p>`}
  function renderCapabilities(){$('capabilities').innerHTML=capabilities.map(([symbol,title,subtitle,url])=>`<a class="capability" href="${url}" target="_blank" rel="noopener"><span class="symbol">${symbol}</span><b>${title} ↗</b><small>${subtitle}</small></a>`).join('')}
  function exportGeoJSON(){const fc={type:'FeatureCollection',properties:{scenario:'FICTIONAL VEOC EXERCISE',hour:getHour(),caution:'Do not use for operations'},features:sectors.map(s=>{const v=getState(s);return {type:'Feature',geometry:{type:'Point',coordinates:[s.lon,s.lat]},properties:{name:s.name,population:s.population,calls:v.calls,flood_m:v.flood,reporting:v.reporting,open_beds:s.beds,road_min:s.road}}})};download(`osiris-veoc-exercise-t${getHour()}.geojson`,JSON.stringify(fc,null,2),'application/geo+json')}
  function exportSitrep(){const ranked=scored(),h=getHour();const body=`# FICTIONAL VEOC SITREP · T+${h} h\n\nExercise only. No real incident is represented.\n\n## Situation\n${ranked.reduce((a,s)=>a+s.calls,0)} synthetic assistance calls across six sectors.\n\n## Verification priorities\n${ranked.slice(0,2).map(s=>`- ${s.name}: illustrative score ${s.score.toFixed(2)}; confirm field conditions.`).join('\n')}\n\n## Evidence and uncertainty\nAll exercise locations and counts are invented. Flood depths and road times are modeled. Camera and facility leads are unverified. Review official warnings and original providers for any real operation.\n\nSource: https://github.com/jltobias/JupyterLite-Osiris\n`;download(`osiris-veoc-sitrep-t${h}.md`,body,'text/markdown')}
  function render(){renderMap();renderKPIs();renderTrend();renderSectorChart();renderPriority();renderSitrep()}
  $('clock').textContent=new Intl.DateTimeFormat('en-US',{timeZone:'UTC',month:'short',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date())+' UTC';
  $('hour').addEventListener('input',render);$('metric').addEventListener('change',renderMap);document.querySelectorAll('[data-layer]').forEach(el=>el.addEventListener('change',renderMap));$('export-geojson').onclick=exportGeoJSON;$('export-sitrep').onclick=exportSitrep;
  $('view-2d').onclick=()=>{$('map-2d').parentElement.classList.remove('show-3d');$('view-2d').classList.add('active');$('view-3d').classList.remove('active');$('view-2d').setAttribute('aria-pressed','true');$('view-3d').setAttribute('aria-pressed','false')};
  $('view-3d').onclick=()=>{$('map-2d').parentElement.classList.add('show-3d');$('view-3d').classList.add('active');$('view-2d').classList.remove('active');$('view-3d').setAttribute('aria-pressed','true');$('view-2d').setAttribute('aria-pressed','false')};
  renderFeed();renderCapabilities();render();selectSector(sectors[2]);
})();
