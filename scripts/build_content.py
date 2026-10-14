"""Generate the self-contained, browser-friendly VEOC teaching notebooks."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content"
OUT.mkdir(exist_ok=True)

SETUP = '''import math, json, statistics
from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML, Markdown
plt.rcParams.update({"figure.figsize": (9, 4), "axes.spines.top": False, "axes.spines.right": False})
SECTORS = [
 {"name":"Harbor", "lat":29.93,"lon":-90.07,"population":18000,"calls":34,"flood_m":0.9,"open_beds":12,"road_min":28,"reporting":0.84},
 {"name":"Eastbank","lat":29.96,"lon":-90.00,"population":24000,"calls":22,"flood_m":0.4,"open_beds":24,"road_min":19,"reporting":0.91},
 {"name":"Canal",   "lat":29.98,"lon":-90.10,"population":12000,"calls":31,"flood_m":1.4,"open_beds":4, "road_min":42,"reporting":0.68},
 {"name":"North",   "lat":30.05,"lon":-90.07,"population":30000,"calls":18,"flood_m":0.1,"open_beds":38,"road_min":14,"reporting":0.96},
 {"name":"Bayou",   "lat":29.89,"lon":-90.12,"population":9000, "calls":25,"flood_m":1.1,"open_beds":7, "road_min":51,"reporting":0.72},
 {"name":"Airport", "lat":30.00,"lon":-90.25,"population":16000,"calls":11,"flood_m":0.2,"open_beds":18,"road_min":23,"reporting":0.89},
]
for sector in SECTORS:
    sector["rate_10k"] = sector["calls"] / sector["population"] * 10000
print("EXERCISE DATA â€” fictional sectors, observations and facilities; no real incident implied")'''

SOURCES = '''## Source desk
- [OSIRIS source and MIT license](https://github.com/simplifaisoul/osiris) Â· [OSIRIS live console](https://osirisai.live/)
- [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) Â· [NASA EONET](https://eonet.gsfc.nasa.gov/docs/v3) Â· [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)
- [NOAA National Hurricane Center](https://www.nhc.noaa.gov/) Â· [GDACS](https://www.gdacs.org/) Â· [OpenSky Network](https://opensky-network.org/)

**Use rule:** A source link provides context, not independent confirmation of this fictional exercise. Check timestamps, geography, provider terms, and incident command procedures before any real decision.'''

def md(s): return nbf.v4.new_markdown_cell(s)
def code(s): return nbf.v4.new_code_cell(s)
def make(slug, title, mission, cells, prompts):
    intro = f'''# {title}\n\n**Mission.** {mission}\n\n![Illustrated OSIRIS VEOC mission board](assets/veoc-splash.svg)\n\n> **Exercise only.** All sectors, calls, flood depths, beds, and travel times below are invented. Run each notebook independently with the **Python (Pyodide)** kernel in JupyterLite. First startup downloads the browser runtime. The linked OSIRIS console is a separate application.\n\n[Book home](intro.md) Â· [2D operations map](https://jltobias.github.io/JupyterLite-Osiris/scenes/operations-2d.html) Â· [3D scene](https://jltobias.github.io/JupyterLite-Osiris/scenes/operations-3d.html) Â· [OSIRIS](https://osirisai.live/)'''
    nb = nbf.v4.new_notebook(cells=[md(intro),code(SETUP),*cells,md('## Field exercise and review\n'+prompts),md(SOURCES)],metadata={"kernelspec":{"display_name":"Python (Pyodide)","language":"python","name":"python"},"language_info":{"name":"python"}})
    nbf.write(nb, OUT / f'{slug}.ipynb')

make('00_start_here','00 Â· Enter the virtual EOC','Build a common operating picture and identify what the map cannot yet tell you.',[
 md('## From signal to decision\nOSIRIS brings public flight, maritime, camera, earthquake, fire, weather, space, news and other layers into a live map. This companion turns those layers into a repeatable **observe â†’ verify â†’ prioritize â†’ brief** workflow. A VEOC is a coordination pattern, not a claim that OSIRIS alone is an emergency management system.\n\n![Signal-to-decision workflow](assets/workflow.svg)'),
 code('''names=[s["name"] for s in SECTORS]
calls=[s["calls"] for s in SECTORS]
fig,ax=plt.subplots(); ax.barh(names,calls,color="#12b8b0"); ax.set(xlabel="Synthetic assistance calls",title="First look: workload is uneven"); ax.invert_yaxis(); plt.show()
print(f"Total exercise calls: {sum(calls)} | sectors: {len(SECTORS)}")'''),
 md('## What to do in OSIRIS\nOpen the [live console](https://osirisai.live/). Inspect layer counts and last updates before interpreting a marker. Compare the same place in the 2D and 3D exercise views. Record provider, observation time, retrieval time, confidence, and next action. Do not treat a camera snapshot as continuous coverage.'),
 code('''brief={"incident":"FICTIONAL COASTAL STORM / EXERCISE","as_of":"exercise T+0","observed":"Synthetic assistance calls vary by sector.","unknowns":["Road status","Real-time shelter capacity","Reporting completeness"],"next_action":"Request verified field reports for Canal and Bayou."}
display(Markdown("\\n".join(f"**{k.replace('_',' ').title()}:** {v}" for k,v in brief.items())))''')
], '1. Which three observations would need field verification? 2. State a decision you should defer until road access is confirmed. 3. Write one sentence that separates observed, modeled, and unknown information.')

make('01_osiris_layer_atlas','01 Â· OSIRIS layer atlas','Choose OSIRIS layers by operational question, source, update behavior, and caveat.',[
 md('## A layer is a lead, not a verdict\nOSIRIS documents live or near-live aviation, CCTV, seismic, fire, weather, space, news, and other layers. Some, including conflict zones and maritime reference points, are static context. Backend availability, rate limits, and provider delays differ. Open the [upstream feature and architecture description](https://github.com/simplifaisoul/osiris#key-capabilities) alongside this matrix.'),
 code('''layers=[
 ("Earthquakes","USGS","Magnitude/time/location","Confirm impact separately"),
 ("Severe events","NASA EONET","Event category and geometry","Event geometry is not damage"),
 ("Fire hotspots","NASA FIRMS","Thermal detections","Clouds and resolution affect coverage"),
 ("Aircraft","OpenSky","Tracked aircraft positions","Coverage and identification vary"),
 ("Cameras","Public operators","View or snapshot","Blind spots, time lag, privacy"),
 ("Maritime","OSIRIS/static reference","Ports and chokepoints","Not live vessel positions"),
]
display(HTML('<table><tr><th>Layer</th><th>Provider</th><th>Useful for</th><th>Caution</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a,b,c,d in layers)+'</table>'))'''),
 md('**Analyst habit:** log an observation timestamp and a retrieval timestamp. If either is missing, say so in the situation report. Open the source provider before claiming a layer is current.'),
 code('''questions={"Where might shaking be felt?":"Earthquakes","Is a thermal anomaly near assets?":"Fire hotspots","Can a public camera corroborate road conditions?":"Cameras"}
for q,l in questions.items(): print(f"{q} â†’ {l} â†’ verify with an independent source")''')
], 'Pick an OSIRIS layer for a coastal storm. Name a second source that could contradict it. Explain one reason an empty layer does not prove an event is absent.')

make('02_2d_common_picture','02 Â· 2D common operating picture','Map exposure, demand, and verification needs without hiding missing information.',[
 md('## Read a map as an argument\nThe [interactive 2D map](https://jltobias.github.io/JupyterLite-Osiris/scenes/operations-2d.html) shows the same fictional sectors with switchable demand, flood, and reporting measures. Circle size in this notebook encodes calls; color encodes water depth. Neither measure is a forecast.'),
 code('''fig,ax=plt.subplots(figsize=(9,6))
sc=ax.scatter([s['lon'] for s in SECTORS],[s['lat'] for s in SECTORS],s=[s['calls']*22 for s in SECTORS],c=[s['flood_m'] for s in SECTORS],cmap='YlOrRd',edgecolors='#17324d',linewidths=1.2)
for s in SECTORS: ax.annotate(s['name'],(s['lon'],s['lat']),xytext=(6,5),textcoords='offset points')
fig.colorbar(sc,ax=ax,label='Synthetic flood depth (m)');ax.set(xlabel='Longitude',ylabel='Latitude',title='Fictional coastal sectors Â· size = calls');ax.grid(alpha=.2);plt.show()'''),
 code('''feature_collection={"type":"FeatureCollection","properties":{"scenario":"FICTIONAL","schema":"VEOC exercise points"},"features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[s['lon'],s['lat']]},"properties":{k:v for k,v in s.items() if k not in ('lat','lon')}} for s in SECTORS]}
print(json.dumps(feature_collection,indent=2)[:850]+"\\nâ€¦")'''),
 md('Export the displayed `feature_collection` with `json.dumps` when needed. The browser file system belongs to JupyterLite; saving in a notebook does not update the live OSIRIS application.')
], 'Find the high-call sector with the weakest reporting. What label would you add to avoid false precision? Try switching metrics on the interactive map.')

make('03_3d_terrain_scene','03 Â· 3D scene and vertical scale','Use a 3D view to communicate priorities without letting visual height imply physical height.',[
 md('The [interactive 3D scene](https://jltobias.github.io/JupyterLite-Osiris/scenes/operations-3d.html) extrudes **synthetic calls** over a dark basemap. It is a thematic scene, not terrain, a flood simulation, or satellite reconstruction. Rotate and zoom to see how perspective can obscure short columns. For real terrain context, compare [OSIRIS](https://osirisai.live/) and inspect its layer provenance.'),
 code('''depth=np.array([s['flood_m'] for s in SECTORS]);calls=np.array([s['calls'] for s in SECTORS]);order=np.argsort(calls)[::-1]
fig=plt.figure(figsize=(9,6));ax=fig.add_subplot(projection='3d')
ax.bar3d(np.arange(len(SECTORS)),np.zeros(len(SECTORS)),np.zeros(len(SECTORS)),.65,.65,calls,color=['#f97316' if d>=1 else '#16b8ad' for d in depth],shade=True)
ax.set_xticks(np.arange(len(SECTORS))+.3,[s['name'] for s in SECTORS],rotation=25);ax.set_yticks([]);ax.set_zlabel('Synthetic calls, not meters');ax.set_title('Thematic 3D columns');plt.show()'''),
 code('''for i in order[:3]: print(f"{SECTORS[i]['name']}: {calls[i]} calls; {depth[i]:.1f} m synthetic depth")''')
], 'Explain which variable determines column height and which determines color. Identify a sector hidden from one viewing angle. Recheck the ranking in the printed table.')

make('04_hazards_and_feeds','04 Â· Hazards and public feeds','Separate provider observation, model output, and impact assessment.',[
 md('## Three different clocks\nA feed may have an event time, provider publication time, and analyst retrieval time. OSIRIS aggregates feeds; verify an event at its origin. Useful provider entry points: [USGS latest earthquakes](https://earthquake.usgs.gov/earthquakes/map/), [NASA EONET](https://eonet.gsfc.nasa.gov/), [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/), [NHC advisories](https://www.nhc.noaa.gov/), and [GDACS alerts](https://www.gdacs.org/). These external sites may change or require network access.'),
 code('''exercise_events=[
 {"source":"Exercise weather desk","event":"Heavy rain warning","event_hour":0,"retrieved_hour":1,"confidence":"modeled"},
 {"source":"Exercise camera","event":"Standing water image","event_hour":2,"retrieved_hour":4,"confidence":"unverified"},
 {"source":"Exercise field team","event":"Canal road closure","event_hour":3,"retrieved_hour":3.5,"confidence":"verified report"},
]
for e in exercise_events: e['lag_h']=e['retrieved_hour']-e['event_hour']
display(HTML('<table><tr><th>Source</th><th>Event</th><th>Lag (h)</th><th>Status</th></tr>'+''.join(f"<tr><td>{e['source']}</td><td>{e['event']}</td><td>{e['lag_h']:.1f}</td><td>{e['confidence']}</td></tr>" for e in exercise_events)+'</table>'))'''),
 code('''fig,ax=plt.subplots();ax.barh([e['event'] for e in exercise_events],[e['lag_h'] for e in exercise_events],color='#f59e0b');ax.set(xlabel='Exercise retrieval lag (hours)',title='Freshness is a separate variable');plt.show()''')
], 'Choose one provider and write down event time, retrieval time, coordinates, and license or use terms. For the exercise, decide which item warrants an immediate verification call.')

make('05_aviation_maritime_logistics','05 Â· Aviation, maritime and logistics','Plan a route using explicit assumptions while keeping live movement data separate.',[
 md('OSIRIS describes OpenSky-based aviation and static maritime reference context. A tracked aircraft is **not** evidence of a relief mission, and a port marker is **not** a live vessel location. Cross-check flight status at [OpenSky](https://opensky-network.org/) and port conditions with the relevant authority.'),
 code('''routes=[("Harbor","North",28,0.9),("Canal","North",42,1.4),("Bayou","Eastbank",51,1.1),("Airport","Harbor",23,0.2)]
for a,b,minutes,depth in routes:
    adjusted=minutes*(1+max(0,depth-.5)*.7)
    print(f"{a:8} â†’ {b:8}: baseline {minutes:2} min | scenario sensitivity {adjusted:4.1f} min")'''),
 code('''fig,ax=plt.subplots();ax.bar([f'{a}â†’{b}' for a,b,_,_ in routes],[m for _,_,m,_ in routes],label='baseline',color='#2b799e');ax.bar([f'{a}â†’{b}' for a,b,_,_ in routes],[m*(1+max(0,d-.5)*.7) for a,b,m,d in routes],alpha=.45,label='simple sensitivity',color='#f97316');ax.set(ylabel='Minutes',title='Assumed road delay, not routing guidance');ax.legend();plt.xticks(rotation=20);plt.show()'''),
 md('The multiplier above is invented for teaching sensitivity. Real logistics needs verified closures, dispatch authorization, capacity, and a road network. [OpenStreetMap](https://www.openstreetmap.org/copyright) data may help map roads but is not a live passability guarantee.')
], 'Change the water-depth threshold from 0.5 m to 0.8 m. Which route changes most? Write a dispatch note that explicitly calls the travel times estimates.')

make('06_cameras_and_verification','06 Â· Camera verification desk','Track evidence and privacy constraints for public camera observations.',[
 md('OSIRIS indexes public camera feeds and snapshots from many operators. Availability differs by operator. A camera can corroborate visible conditions in its field of view; it cannot prove conditions off camera or after its last frame. Respect the operator terms and avoid collecting identifiable people or license plates.'),
 code('''claims=[("Canal underpass flooded","Public camera frame",2,0.65),("Bayou road blocked","Field report",1,0.88),("Harbor bridge open","No current view",5,0.25)]
for claim,source,age,quality in claims:
    freshness=math.exp(-age/3)
    score=quality*freshness
    print(f"{claim:25} {source:20} age={age}h  illustrative evidence score={score:.2f}")'''),
 md('The score is a **teaching heuristic**, not an OSIRIS confidence score. Recording the source, frame timestamp, viewpoint, and verification owner matters more than collapsing evidence to a number.'),
 code('''fig,ax=plt.subplots();ax.barh([c[0] for c in claims],[c[3]*math.exp(-c[2]/3) for c in claims],color=['#f59e0b','#16b8ad','#ef4444']);ax.set(xlim=(0,1),xlabel='Illustrative freshness Ã— quality',title='Check stale evidence');plt.show()''')
], 'Draft a verification log row for a camera snapshot: operator, camera URL, frame time, retrieval time, visible finding, blind spots, reviewer, and next check.')

make('07_health_and_access','07 Â· Health access and population','Compare calls, population denominators, beds, and reporting coverage.',[
 md('A raw call count can mislead when sector populations differ. Here all counts and denominators are fictional. The call rate below is a workload indicator, not disease incidence or risk.'),
 code('''for s in SECTORS: s['rate_10k']=s['calls']/s['population']*10000
for s in sorted(SECTORS,key=lambda x:x['rate_10k'],reverse=True): print(f"{s['name']:8} {s['rate_10k']:5.1f} calls/10k | beds {s['open_beds']:2} | reporting {s['reporting']:.0%}")'''),
 code('''fig,axs=plt.subplots(1,2,figsize=(12,4));names=[s['name'] for s in SECTORS]
axs[0].bar(names,[s['calls'] for s in SECTORS],color='#209ab5');axs[0].set_title('Raw calls')
axs[1].bar(names,[s['rate_10k'] for s in SECTORS],color='#ea8b35');axs[1].set_title('Calls per 10,000 residents')
for ax in axs: ax.tick_params(axis='x',rotation=35)
plt.tight_layout();plt.show()'''),
 md('For real population data, inspect each [WorldPop](https://www.worldpop.org/) productâ€™s year, model, license, and uncertainty. The companion [STAC Browser](https://github.com/jltobias/JupyterLite-STAC-Browser) teaches catalog provenance; its metadata footprints are not population values.')
], 'Which sector changes rank when normalized? Why might low reporting lead to a lower observed count? Name two additional health access variables needed for a real EOC.')

make('08_priorities_and_sitrep','08 Â· Priorities and situation report','Make an auditable exercise priority list and concise handover.',[
 md('## Explicit weights\nThis score demonstrates how assumptions change the ranking. It does **not** automate emergency decisions. Terms use normalized synthetic call rate, flood depth, road time, and a reporting gap. Discuss weights and missing data with the incident team.'),
 code('''weights={'calls':.35,'flood':.30,'access':.20,'gap':.15}
for s in SECTORS:
 s['priority']=weights['calls']*min(s['rate_10k']/30,1)+weights['flood']*min(s['flood_m']/1.5,1)+weights['access']*min(s['road_min']/60,1)+weights['gap']*(1-s['reporting'])
ranking=sorted(SECTORS,key=lambda x:x['priority'],reverse=True)
for rank,s in enumerate(ranking,1):print(f"{rank}. {s['name']:8} {s['priority']:.3f} | reporting {s['reporting']:.0%}")'''),
 code('''fig,ax=plt.subplots();ax.barh([s['name'] for s in ranking],[s['priority'] for s in ranking],color='#ec8e3c');ax.invert_yaxis();ax.set(xlabel='Illustrative weighted score',title='Review the ranking with subject matter experts');plt.show()'''),
 code('''sitrep=f"""# EXERCISE SITREP Â· T+4
## Situation
Fictional heavy rain and assistance calls across six sectors. No real incident is represented.
## Verified / modeled / unknown
Verified: none in this exercise dataset. Modeled: flood depths and road travel times. Unknown: actual closures, shelter demand, medical acuity.
## Priority for verification
{', '.join(s['name'] for s in ranking[:2])} (illustrative score; review with field teams).
## Next update
Obtain timestamped field reports and publish an updated map with source links.
"""
display(Markdown(sitrep))''')
], 'Double the reporting-gap weight and renormalize the weights. Does the first priority change? Add a dated decision log entry describing why the team accepted or rejected the score.')

make('09_cockpit_and_beyond','09 Â· Cockpit and beyond the VEOC','Explore OSIRIS functions that may support broader intelligence work while setting scope boundaries.',[
 md('## OSIRIS capability tour\nThe upstream project documents a 3D map cockpit, aviation and maritime context, satellites and solar weather, 24/7 broadcasts, OI Assist and OI Forecast, OSINT investigation tools, cyber/CVE lookups, crypto tracing, and sanctions search. Some capabilities need user keys or a backend. Read [upstream README](https://github.com/simplifaisoul/osiris), [deployment notes](https://github.com/simplifaisoul/osiris/blob/master/DOCKER.md), and the [live console](https://osirisai.live/) before enabling them.\n\n| VEOC-adjacent | Broader cockpit / specialist use |\n|---|---|\n| Map layers, event time, cameras, verified briefings | Forecast experiments, RECON scans, wallet tracing |\n| Logistics context and public broadcasts | Sanctions and cyber investigations |\n| Explicit operational handover | OI interactions on a personally supplied model key |'),
 code('''capabilities=[('Map cockpit','core VEOC','Check layer freshness'),('OI Forecast','exploratory','Document inputs, baselines and uncertainty'),('RECON scanner','specialist','Use only on authorized assets'),('Sanctions search','specialist','Verify official records'),('Broadcasts','context','Corroborate claims at source')]
display(HTML('<table><tr><th>Capability</th><th>Role</th><th>Review action</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in capabilities)+'</table>'))'''),
 md('## A cockpit checklist\n1. Pick a question and geography. 2. Turn on only relevant layers. 3. Record source and update time. 4. Open original evidence. 5. Separate inference from observation. 6. Export a dated briefing.\n\n**Video and imagery desk:** [OSIRIS live camera and broadcast interface](https://osirisai.live/) Â· [NOAA satellite imagery](https://www.star.nesdis.noaa.gov/GOES/) Â· [NASA Earth Observatory videos](https://earthobservatory.nasa.gov/videos). These are external media links; availability and rights remain with their providers.'),
 code('''decision={"question":"Could a live aviation marker assist response?","observation":"A marker exists (hypothetical)","inference":"Its mission is unknown","verification":"Contact aviation coordination authority","decision":"Do not assign mission from map marker alone"}
display(Markdown('\\n'.join(f'- **{k.title()}:** {v}' for k,v in decision.items())))''')
], 'Choose one specialist capability and explain when it belongs outside an emergency briefing. Describe the authorization and provenance checks needed before using it.')

make('10_veoc_mission_control','10 · VEOC mission control dashboard','Explore a full-screen OSIRIS-inspired coordination workspace and reproduce its evidence-led analysis in Python.',[
 md('## Launch the visual command center\n[**Open the full-screen VEOC dashboard →**](https://jltobias.github.io/JupyterLite-Osiris/scenes/veoc-dashboard.html)\n\nThe dashboard combines a time scrubber, seven switchable exercise overlays, a selectable 2D map and rotatable 3D globe, demand and reporting trends, sector comparison, priority ranking, an evidence desk, sixteen OSIRIS capability cards, GeoJSON export, and a situation-report preview. It runs as a standalone static page with original code and **fictional exercise data**. It does not call OSIRIS or provider APIs. Open [live OSIRIS](https://osirisai.live/) separately to compare how its actual layers behave.\n\nThe embedded dashboard below may be constrained by a notebook viewer. Use the full-screen link for the complete interaction.'),
 code('''from IPython.display import IFrame
dashboard_url = "https://jltobias.github.io/JupyterLite-Osiris/scenes/veoc-dashboard.html"
display(IFrame(src=dashboard_url,width='100%',height=920))'''),
 md('## Reproduce the desk calculations\nThe dashboard uses a transparent four-term exercise priority score: assistance-call rate (35%), modeled flood depth (30%), assumed road time (20%), and reporting gap (15%). Change `hour` below to compare conditions. The score is a conversation aid, not an automated dispatch rule.'),
 code('''hour = 4  # Set an exercise hour from 0 to 12.
assert 0 <= hour <= 12
state=[]
for s in SECTORS:
    row=s.copy()
    row['calls']=round(s['calls']*(.68+.08*hour))
    row['flood_m']=round(s['flood_m']*(.60+.10*hour),2)
    row['reporting']=min(1,s['reporting']*(.85+.0375*hour))
    row['rate_10k']=row['calls']/row['population']*10000
    row['score']=(.35*min(row['rate_10k']/30,1)+.30*min(row['flood_m']/1.5,1)
                  +.20*min(row['road_min']/60,1)+.15*(1-row['reporting']))
    state.append(row)
print(f"EXERCISE T+{hour} h · {sum(s['calls'] for s in state)} fictional assistance calls")
for rank,s in enumerate(sorted(state,key=lambda s:s['score'],reverse=True),1):
    print(f"{rank}. {s['name']:8} score {s['score']:.3f} · {s['calls']:2} calls · {s['flood_m']:.1f} m modeled depth")'''),
 md('## The map, trend, and pressure dashboard\nEach panel answers a different operational question. The map asks **where**; the trend asks **when**; the sector chart asks **relative to what denominator**; the priority chart asks **under which assumptions**. Review all four before writing a headline.'),
 code('''fig,axs=plt.subplots(2,2,figsize=(14,10),layout='constrained')
ax=axs[0,0]
sizes=[75+s['calls']*20 for s in state]
sc=ax.scatter([s['lon'] for s in state],[s['lat'] for s in state],s=sizes,c=[s['flood_m'] for s in state],cmap='YlOrRd',vmin=0,vmax=1.6,edgecolor='#173b51',linewidth=1.4)
for s in state: ax.annotate(s['name'],(s['lon'],s['lat']),xytext=(7,5),textcoords='offset points',fontsize=9)
ax.set(xlabel='Longitude',ylabel='Latitude',title='WHERE · synthetic demand and modeled depth');ax.grid(alpha=.2);fig.colorbar(sc,ax=ax,label='Modeled depth (m)')
hours=np.arange(13)
totals=[sum(round(s['calls']*(.68+.08*h)) for s in SECTORS) for h in hours]
coverage=[sum(min(1,s['reporting']*(.85+.0375*h))*s['population'] for s in SECTORS)/sum(s['population'] for s in SECTORS)*100 for h in hours]
ax=axs[0,1];ax.plot(hours,totals,'o-',color='#12a9a4',label='Assistance calls');ax.axvline(hour,color='#f28c50',ls='--',label=f'T+{hour}');ax.set(xlabel='Exercise hour',ylabel='Synthetic calls',title='WHEN · demand and reporting');ax2=ax.twinx();ax2.plot(hours,coverage,'s-',color='#e8893c',label='Reporting coverage');ax2.set_ylabel('Coverage (%)');ax.legend(loc='upper left')
names=[s['name'] for s in state];ax=axs[1,0];ax.barh(names,[s['rate_10k'] for s in state],color='#14b4aa');ax.invert_yaxis();ax.set(xlabel='Calls per 10,000 residents',title='RELATIVE TO WHAT · population-normalized workload')
ranked=sorted(state,key=lambda s:s['score'],reverse=True);ax=axs[1,1];ax.barh([s['name'] for s in ranked],[s['score'] for s in ranked],color=['#ee8750' if i<2 else '#2da9a4' for i in range(len(ranked))]);ax.invert_yaxis();ax.set(xlabel='Illustrative weighted score',title='UNDER WHICH ASSUMPTIONS · priority ranking')
plt.show()'''),
 md('## Evidence and handover\nThe map and charts contain no verified facts. A live VEOC would need a timestamped source record, alternate corroboration, owner, and review state for each claim. Cameras cannot establish conditions outside their view; an aircraft marker cannot establish a relief mission; a port marker cannot establish a live vessel position. The [upstream OSIRIS README](https://github.com/simplifaisoul/osiris#readme) describes its layers and specialist features. [NOAA GOES imagery](https://www.star.nesdis.noaa.gov/GOES/) and [OSIRIS broadcast/camera views](https://osirisai.live/) are external visual sources with their own provenance and rights.'),
 code('''evidence_packet={
    'scenario':'FICTIONAL COASTAL STORM / EDUCATIONAL EXERCISE',
    'exercise_hour':hour,
    'observed':[],
    'modeled':['Flood depth','Road travel time','Assistance-call trajectory'],
    'unverified':['Camera leads','Clinic bed counts','Road closure lead'],
    'priority_for_verification':[s['name'] for s in ranked[:2]],
    'next_actions':['Call field liaison for road status','Confirm facility capacity','Check original provider timestamps'],
    'source':'https://github.com/jltobias/JupyterLite-Osiris'
}
display(Markdown('### Exercise handover packet\\n```json\\n'+json.dumps(evidence_packet,indent=2)+'\\n```'))'''),
 md('## Continue into the real cockpit\nThe capability wall points to live or authoritative context for earthquakes, fire, weather, aviation, maritime references, public cameras, broadcasts, space weather, cyber/CVE information, sanctions, and OI Assist/Forecast. OSIRIS documents these domains, but some functions depend on credentials, backend services, or source availability. A dashboard card is an invitation to investigate, not proof that a live feed was loaded. For a working VEOC, add authentication, incident logging, data-quality monitoring, operational roles, and official alerting under local incident-command procedures.')
], '1. Scrub the dashboard from T+0 to T+12 and identify when the top two sectors exchange rank. Explain why their scores change. 2. Toggle off flood depth and explain what the map hides. 3. Inspect one camera lead and state what must be checked at the operator. 4. Download the GeoJSON and situation report, then rewrite the report with observed, modeled, and unknown headings. 5. Name one OSIRIS capability that requires special authorization or provider terms.')

print('Generated 11 notebooks in', OUT)
