# Straw Hat Dashboard — profile README package

A dark navy + gold profile README built from your dashboard design. The
**Skill Inventory** section is copied byte-for-byte from your previous README;
everything else is redesigned.

## What's inside

| Path | What it is |
|---|---|
| `README.md` | The profile page |
| `assets/hero.svg` | Top banner (your design's header, with a light sweep, twinkling stars and a blinking cursor) |
| `assets/head-*.svg` | Section headers (Captain's Log, Bounty Board, Voyage Log) with a turning helm/compass |
| `assets/captains-log.svg` | About-me terminal card + sunset ship panel |
| `assets/footer.svg` | Open Channel banner with your real contact handles |
| `assets/divider.svg` | Animated gold divider |
| `assets/img/*.jpg` | Image crops from your design, embedded into the SVGs |
| `assets/fonts/` | Cinzel and JetBrains Mono (SIL Open Font License, licences included) |
| `scripts/build_static.py` | Rebuilds the static SVGs above — edit your details at the top, then run it |
| `scripts/generate_voyage.py` | Builds the **live** Voyage Log cards from your real GitHub data |
| `.github/workflows/snake.yml` | Runs twice a day: Voyage Log cards + contribution snake → `output` branch |

## Install

1. Copy everything in this zip into your `estkayon/estkayon` repository, keeping the folders.
   `snake.yml` replaces your old workflow of the same name — keep only this one, because
   two workflows publishing to `output` would erase each other's files.
2. Optional cleanup: the old `assets/straw-hat-crew-hero.gif`, `straw-hat-crew-cover.png` and
   `straw-hat-divider.svg` are no longer used and can be deleted.
3. Commit and push. The push itself triggers the workflow (it also has *Run workflow* under
   **Actions → Voyage Log + contribution snake**).
4. Make sure **Settings → Actions → General → Workflow permissions** is set to
   *Read and write permissions*.
5. Once the run finishes, the Voyage Log and snake images appear. Before the first run they show as broken images — that's expected.

## Live stats — how they work

`generate_voyage.py` reads your contribution calendar and the languages of your
own (non-fork) repositories, then draws:

- **My Contributions** — total, active days, best and current streak, heatmap for the last 8 months
- **Tech Stack Usage** — share of code by language (top 8 + Others)
- **Monthly Contributions** — bar chart for the same 8 months
- **Best Day** — your busiest day in that window, on the night-city banner

By default it counts **public** activity. To include private contributions, create a
classic personal access token with the `read:user` and `repo` scopes and save it as a
repository secret named `GH_STATS_TOKEN`.

Jupyter Notebook, HTML, CSS and a few build files are left out of the language chart
because their size would swamp the real code. To change that list, add an
`EXCLUDE_LANGS` env value in the workflow (comma-separated, e.g. `Jupyter Notebook,HTML`).

## Editing your details

Open `scripts/build_static.py`, change `PROFILE`, `FOCUS` or `CONTACT`, then run:

```bash
cd scripts
python build_static.py
```

Preview the live cards locally with sample data (no network):

```bash
python scripts/generate_voyage.py --demo --out dist
```

## Notes

- The images inside the banners are cropped from the design image you supplied.
- The email used everywhere is `estiakayon@gmail.com` (from your previous README). Your
  design image showed `estkayon@gmail.com` — if that's the right one, update `CONTACT` in
  `build_static.py` and the two `mailto:` links in `README.md`.
- GitHub shows README images through `<img>`, which can't run scripts, so all animation is
  SVG/SMIL, and fonts and images are embedded inside each SVG.
