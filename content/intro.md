# OSIRIS Â· Virtual Emergency Operations Center

![Original illustrated VEOC mission board](assets/veoc-splash.svg)

**A field guide and executable browser lab for turning public signals into accountable emergency briefings.** This is an independent educational companion to [OSIRIS](https://github.com/simplifaisoul/osiris), created by simplifaisoul. It is not an official OSIRIS distribution or an operational emergency response platform.

[Launch JupyterLite](https://jltobias.github.io/JupyterLite-Osiris/lab/index.html) Â· [2D map](https://jltobias.github.io/JupyterLite-Osiris/scenes/operations-2d.html) Â· [3D scene](https://jltobias.github.io/JupyterLite-Osiris/scenes/operations-3d.html) Â· [OSIRIS live console](https://osirisai.live/)

## Choose a route

| Route | Read and run | Outcome |
|---|---|---|
| Incident onboarding | 00 â†’ 01 â†’ 02 | Layer selection and common operating picture |
| Geospatial operations | 02 â†’ 03 â†’ 05 | 2D/3D communication and logistics assumptions |
| Evidence and decision | 04 â†’ 06 â†’ 07 â†’ 08 | Freshness, corroboration, population context, sitrep |
| Full cockpit | 09 | Explore OSIRIS functions beyond VEOC scope |

## Exercise boundary

The coastal sectors, calls, flood depths, beds, routes, and reports in these labs are **fictional**. The linked OSIRIS application and public provider sites can contain real information with varying latency and availability. Never dispatch resources from the exercise maps. For real operations, follow local incident command, official alerts, and verified field reports.

## Working method

![Observe, verify, prioritize, brief](assets/workflow.svg)

1. **Observe:** identify the operational question and inspect relevant layers.
2. **Verify:** record source, observation time, retrieval time, limitations, and corroboration.
3. **Prioritize:** expose assumptions and sensitivity; keep human review in the loop.
4. **Brief:** separate verified facts, modeled estimates, and unknowns.

The notebooks use Python, NumPy, Matplotlib, and IPython display in a Pyodide browser kernel. Each notebook includes its own data and setup so it can run independently. Initial launch requires network access to download the runtime. The Book renders a guide; run code in JupyterLite.

## Attribution and further reading

See the repository [README](https://github.com/jltobias/JupyterLite-Osiris#sources-attribution-and-licensing) for software and data-provider attribution, licensing requirements, and terms. Original illustrations in this book are part of this repository. Start at the [OSIRIS source and license](https://github.com/simplifaisoul/osiris), [USGS](https://earthquake.usgs.gov/fdsnws/event/1/), [NASA EONET](https://eonet.gsfc.nasa.gov/docs/v3), [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/), [OpenSky](https://opensky-network.org/), [NOAA NHC](https://www.nhc.noaa.gov/), and [GDACS](https://www.gdacs.org/).



\n