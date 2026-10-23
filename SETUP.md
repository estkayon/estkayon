# Straw Hat Dashboard — profile README for estkayon

Your profile, laid out like the `ahasan-ullah` README template (cover → about card →
skills → project table → live stat cards → snake → footer) and styled after your
Straw Hat dashboard design. The round Luffy avatar is removed from the cover, and the
**Skill Inventory** section is kept exactly as it was in your previous README.

## What's inside

| Path | What it is |
|---|---|
| `README.md` | The profile page |
| `assets/hero.svg` | Animated cover (see below) |
| `assets/captains-log.svg` | About-me terminal card + slowly zooming sunset-ship panel |
| `assets/pipeline.svg` | Animated Mission 01 MLOps pipeline (DVC → Train → MLflow → FastAPI → Streamlit → Docker) |
| `assets/head-*.svg` | Section headers with a turning helm / ship / compass |
| `assets/footer.svg` | Open Channel banner with your handles, slow zoom + light sweep |
| `assets/divider.svg` | Animated gold divider |
| `assets/img/` | Art cropped from your design, with baked-in text and the avatar removed |
| `assets/fonts/` | Cinzel, JetBrains Mono, Kaushan Script (SIL Open Font License, licences included) |
| `scripts/build_static.py` | Rebuilds every SVG in `assets/` — your details are at the top |
| `scripts/generate_voyage.py` | Builds the live Voyage Log cards and frames the snake |
| `scripts/prepare_images.py` | One-time image prep from the design image (needs `opencv-python`) |
| `.github/workflows/snake.yml` | Every 6 h: Voyage Log cards + contribution snake → `output` branch |

## Animations

- **Cover:** the art zooms and drifts very slowly (26 s, eased) behind still, crisp text; sunset glow
  breathes, light rays turn, the sea glints, stars twinkle, seagulls glide, embers drift up.
  "Ayon" draws itself in, a little straw hat drops onto it and rocks, the roles fade in, and four
  taglines type out on a loop. "Dream · Build · Ship · Repeat" glows word by word.
- **Captain's Log:** rows fade in one by one, blinking cursor, ship panel slowly zooms.
- **Pipeline:** each stage lights up in turn and a data packet travels down the pipeline.
- **Voyage Log:** heatmap fills week by week, language bars and monthly bars grow, stars twinkle over the city.
- **Snake:** the contribution snake eats your graph, on a matching dark panel.
- **Headers / divider / footer:** turning helm and compass, travelling gold spark, footer zoom + light sweep.

Without SVG animation support (some previews), every image still shows its finished state.

## Install

1. Copy everything from this zip into your `estkayon/estkayon` repository, keeping the folders.
   `.github/workflows/snake.yml` replaces your current workflow of the same name — keep only
   this one, since two workflows publishing to `output` would erase each other's files.
2. Optional cleanup — no longer used: `assets/straw-hat-crew-hero.gif`,
   `assets/straw-hat-crew-cover.png`, `assets/straw-hat-divider.svg`.
3. **Settings → Actions → General → Workflow permissions** → *Read and write permissions*.
4. Commit and push. The push runs the workflow (or **Actions → Build profile graphics → Run workflow**).
5. After the run the `output` branch holds `voyage-log.svg`, `voyage-bestday.svg` and `snake.svg`.
   Until then those three images show as broken — that's expected.

For private contributions, add a classic PAT (`read:user`, `repo`) as the secret `GH_STATS_TOKEN`.

## Editing

Change `HERO`, `PROFILE`, `FOCUS`, `SHIP_CARD`, `CONTACT` or `PIPELINE` at the top of
`scripts/build_static.py`, then:

```bash
cd scripts
python build_static.py
```

Preview the live cards with sample data: `python scripts/generate_voyage.py --demo --out dist`.

Jupyter Notebook, HTML, CSS and a few build files are left out of the language chart.
Set an `EXCLUDE_LANGS` env value in the workflow to change that (comma-separated).

## Note

The email used is `estiakayon@gmail.com` (from your previous README). Your design image shows
`estkayon@gmail.com` — if that's the right one, change it in `CONTACT` and in the two
`mailto:` links in `README.md`.
