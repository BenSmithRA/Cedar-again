# CEDAR — Fast

A lightweight, instant-search rebuild of the CEDAR browse/query interface
(https://cedar.azurewebsites.net/), now loaded with the **full exported
dataset** (5,852 factors). Everything runs client-side against a single
JSON file, so filtering and searching are immediate — no server
round-trip, no "load the whole dataset before you can filter" wait.

## What's here

- `index.html` — the whole app. Two views: **Factors** (search + filter by
  host, microbe, resistance class, country, study design; sortable; a
  detail popup per factor; "group by reference" toggle) and **References**
  (one row per study, with a factor count — click through to see its
  factors). No build step, no dependencies.
- `data/factors.json` — the full dataset, converted from your export.
- `convert_timber.py` — re-run this any time you have a fresh export.

## Try it locally

The app fetches `data/factors.json`, so you need a local server (opening
`index.html` directly via `file://` will fail on the fetch):

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Refreshing the data later

If CEDAR's dataset changes and you export again:

```bash
pip install pandas openpyxl
python convert_timber.py your_new_export.csv     # .xlsx also works
```

This overwrites `data/factors.json` in place — no code changes needed.
The converter matches the column names your export actually uses
(`ref_bibtex_key`, `host_level_01`, `resistance_class`, etc.). If a future
export renames or adds columns, open `convert_timber.py` and adjust the
`TIMBER_COLUMNS` list.

## Deploy it somewhere free

**Recommended: GitHub Pages.** Free, no server to manage or sleep, and a
great fit since this is a static site with baked-in data:

1. Create a new GitHub repo and push this folder to it.
2. In the repo: **Settings → Pages → Source**, pick the `main` branch and
   `/ (root)`, save.
3. Live at `https://<your-username>.github.io/<repo-name>/` within a
   minute or two.

Netlify or Vercel work just as well (drag-and-drop the folder, or connect
the repo) if you'd rather not use GitHub Pages.

## A note on the data

This dataset comes from the CEDAR database maintained by the iAM-AMR /
GRDI-AMR project (https://cedar.azurewebsites.net). This app is a personal,
faster browsing tool over an export you made yourself — it isn't affiliated
with or endorsed by the CEDAR maintainers. If you plan to share it more
broadly (beyond your own use), it's worth crediting the original project
and checking in with the maintainers, since the underlying data represents
real curation work by CEDAR's research team.
