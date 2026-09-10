# Loblaw Bio

Analysis of immune cell counts from Bob Loblaw’s clinical trial.

## How to run (GitHub Codespaces)

1. Open this repository in GitHub Codespaces.
2. Install dependencies:

```bash
make setup
```

3. Build the database and all Part 2–4 outputs:

```bash
make pipeline
```

4. Start the dashboard:

```bash
make dashboard
```

Then open **http://localhost:8501**. In Codespaces, use the forwarded port for 8501 if the browser does not open on its own.

`make pipeline` is enough to reproduce `cell_count.db` and `response_boxplots.png` from `cell-count.csv`. No extra arguments are required.

## Dashboard

[http://localhost:8501](http://localhost:8501)

The dashboard reads the SQLite database created by the pipeline and shows:

- Part 2: relative frequencies (`population_frequencies`), with an optional sample-id filter
- Part 3: responder vs non-responder boxplots and Mann-Whitney p-values
- Part 4: baseline melanoma / PBMC / miraclib / day-0 counts and sample list

## Database schema

Two tables store the study:

**`subjects`** — one row per patient (`subject` primary key). Project, condition, age, sex, treatment, response, and sample type belong here because they do not change from visit to visit.

**`samples`** — one row per blood draw (`sample` primary key). Time from treatment start and the five cell counts belong here. `subject` is a foreign key to `subjects`.

The CSV repeats patient facts on every sample row. Splitting them avoids that duplication and matches the real relationship: one patient, many samples.

The pipeline then writes analysis tables into the same file:

- `population_frequencies` — Part 2 (one row per sample × cell type)
- `response_comparison` — Part 3 p-values
- `subset_samples` / `subset_counts` — Part 4 baseline slice

### Why this scales

If there were hundreds of projects and thousands of samples, this same split still works. You would add indexes on the columns you filter (`condition`, `treatment`, `sample_type`, `time_from_treatment_start`, `subject`) so those queries stay fast. A `projects` table could hold project-level metadata instead of a bare project name on each subject. Cell counts could move to a long `cell_counts(sample, population, count)` table if new populations are added, without changing `samples`. Analytics (frequencies, response tests, subsets) stay as queries or derived tables on top of `subjects` and `samples`; they do not need a second copy of the raw study.

## Code structure

| File | Role |
|---|---|
| `load_data.py` | Create `cell_count.db` and load `cell-count.csv` |
| `analyze.py` | Part 2 relative frequencies |
| `compare_response.py` | Part 3 boxplots and tests |
| `subset.py` | Part 4 baseline subset counts |
| `dashboard.py` | Interactive Streamlit app for Parts 2–4 |
| `Makefile` | `setup`, `pipeline`, `dashboard` |
| `requirements.txt` | Python dependencies |
| `cell-count.csv` | Input |
| `cell_count.db`, `response_boxplots.png` | Pipeline outputs |

Scripts are separate so each part does one job and `make pipeline` can run them in order. The dashboard does not recompute results; it only reads the database the pipeline already built.
