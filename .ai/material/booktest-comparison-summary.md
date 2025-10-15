
# Booktest: Review‑Driven QA for AI & Data Science — with Minimal Git Noise

> **TL;DR**: Booktest is a review‑first testing tool for AI/DS teams. It produces human‑readable Markdown reports, supports interactive approval, snapshots & fast replay for LLM/HTTP calls, and parallelizes long pipelines with a dependency graph. With the new **CAS/DVC-backed manifest**, Booktest keeps PRs tiny (no bulky snapshots in Git) while staying deterministic in CI.

---

## Why Booktest

- **Review‑driven development**: Tests render to Markdown—tables, headers, snippets—that humans can actually read and approve.
- **Subjective QA**: Perfect for “good vs. bad” outputs (LLM responses, topic models, ranking lists) where strict true/false assertions aren’t enough.
- **Guided CLI**: A workflow‑oriented CLI that walks reviewers through diffs and approvals—fast iteration by design.
- **Deterministic & fast**: Snapshot/replay of slow calls (e.g., OpenAI, local model servers) + parallel execution with an **internal dependency graph**.
- **Minimal Git footprint** (new): Store heavy snapshots/cassettes off‑Git in a **content‑addressable store (CAS)**. Git keeps a tiny **manifest** of hashes. PRs remain clean and easy to merge.

---

## What’s New: Minimal‑Git Storage (Manifest + CAS/DVC)

Traditional snapshot/testing tools commit lots of files to Git—noisy PRs and merge conflicts. Booktest introduces a first‑class **manifest + CAS** backend:

- **Result vs Gazette** split:
  - **Result** = tiny, optional Markdown with human notes (can be omitted if nothing to review).
  - **Gazette** = machine snapshot (env dumps, HTTP/httpx cassettes, function outputs), stored in CAS by **sha256**.
- **Manifest in Git**: `booktest.manifest.yaml` maps `(test_id, type) → sha256`. Only this file changes when snapshots update.
- **Remote store**: S3/GCS/Azure via **DVC** or any CAS. Deterministic replay in CI without committing blobs.
- **GC**: Mark‑and‑sweep—keep digests referenced by `main`/tags (and open PRs), clean everything else.

**Typical PR diff**

```diff
--- a/booktest.manifest.yaml
+++ b/booktest.manifest.yaml
@@
 testsuite/test_dir::test_topic_model:
-  httpx: "sha256:4c0f9b...21a"
+  httpx: "sha256:9b7d26...db"
```

**Folder shape (after)**

```
books/.../_snapshots/          # local, gitignored (for dev ergonomics)
books/.../_reports/            # CI artifact (HTML/MD), not in Git
booktest.manifest.yaml         # tiny & stable (committed)
```

---

## Core Concepts

- **Snapshot Types**: `env`, `http`, `httpx`, `func` (one per type).  
- **Dependency Graph**: Booktest tracks inter‑test deps and elapsed‑time heuristics to optimize parallel runs and partial re‑runs.
- **Replay Modes**: CI replays from the approved manifest—no live network—making tests fast and deterministic.
- **Human‑First Output**: Rendered Markdown/HTML reports, ideal for PR review.

---

## Quickstart (Manifest + DVC)

**Config (`booktest.toml`)**
```toml
[storage]
mode = "dvc-manifest"
manifest = "booktest.manifest.yaml"
remote = "booktest-remote"
remote_prefix = "booktest/blobs"
compress = true

[paths]
snapshots_dir = "books/book/testsuite/test_dir/_snapshots"

[review]
report_dir = "books/book/testsuite/test_dir/_reports"
commit_on_approve = true
```

**DVC Setup**
```bash
dvc init
dvc remote add -d booktest-remote s3://my-bucket/booktest
```

**Developer Flow**
```bash
booktest run       # generate/replay, produce local MD report
booktest review    # guided diffs
booktest approve   # updates manifest, promotes blobs in remote
git commit -m "Approve updated baselines"
```

**CI Flow (sketch)**
```yaml
- run: pip install booktest dvc[s3] pytest pytest-vcr
- run: dvc pull                        # fetch approved baselines from manifest
- run: pytest -q                       # replay mode; fast & deterministic
- uses: actions/upload-artifact@v4     # upload one consolidated HTML/MD review report
```

---

## Evaluations & Metrics (pytest‑friendly)

Booktest focuses on review & replay; pair it with DS evaluation tools to **see metrics and failing cases**:

- **Deepchecks (OSS)** — model/data checks; export HTML report; fail pytest on conditions.
- **Great Expectations** — data assertions with `unexpected_index_list` (row‑level offenders).
- **Pandera** — DataFrame schema/constraint tests; show violating rows.
- **pytest‑subtests** — create a **subtest per misclassification** so failures list exact sample IDs.
- **pytest‑html / Allure** — attach CSV/HTML tables (confusion matrix, failing rows) to test reports.

**Example (per‑row failures via subtests)**
```python
def test_classifier(subtests, y_true, y_pred, ids):
    from sklearn.metrics import accuracy_score, f1_score
    assert accuracy_score(y_true, y_pred) >= 0.92
    assert f1_score(y_true, y_pred) >= 0.90
    for i,(t,p,sid) in enumerate(zip(y_true, y_pred, ids)):
        if t != p:
            with subtests.test(sample_id=sid, idx=i, true=int(t), pred=int(p)):
                assert t == p
```

---

## How Booktest Compares

| Capability | **Booktest** | Prompt/LLM tools (PromptFoo, LangSmith, UpTrain) | Snapshot libs (Syrupy/pytest‑snapshot, ApprovalTests) | HTTP replay (VCR.py/pytest‑vcr) | Data/ML QA (GE, Deepchecks, Pandera) | DVC |
|---|---|---|---|---|---|---|
| Review‑driven Markdown | **Built‑in, guided** | Web UIs/reports | Basic diffs (no guided CLI) | N/A | HTML/Docs reports | N/A |
| Subjective QA (human judgement) | **First‑class** | Strong for LLMs | Good for small outputs | N/A | Indirect (metrics) | N/A |
| Minimal Git footprint | **Yes (manifest+CAS)** | Yes (platform DB) | No (snapshots in Git) | No (cassettes usually in Git) | Yes (reports as artifacts) | **Yes** |
| Deterministic replay | **Yes** | Yes | No (needs VCR) | **Yes** | N/A | N/A |
| Pipeline & deps | **Internal graph & parallelism** | Limited | None | None | None | Pipelines & caching |
| Per‑row visibility | Via Markdown + pytest helpers | Often (trace viewers) | Limited | N/A | **Yes** (row indices, slices) | N/A |
| CI integration | **Native reports/artifacts** | Strong | Standard pytest | Standard pytest | Strong | Strong |

**Bottom line**: Booktest remains the **review/UX hub**. Pair it with:
- **DVC** for storage/caching,
- **pytest‑vcr** for cassette replay,
- **Deepchecks/GE/Pandera** for metrics + failing rows,
- **PromptFoo/LangSmith/UpTrain** if you need LLM‑specific eval dashboards.

---

## Minimal‑Git Patterns (Best Practices)

- **Manifest in Git, blobs in CAS** (S3/GCS/Azure via DVC); PRs change only the manifest.
- **Single PR artifact**: upload one consolidated HTML/MD report; reviewers don’t dig through dozens of files.
- **Approve‑only writes**: only the Booktest approve step updates the manifest; CI never updates baselines.
- **Normalization**: canonicalize JSON (sort keys, remove timestamps/IDs, round floats) to reduce churn.
- **Two‑tier store**: `staging/` for new blobs, `keep/` for approved; nightly GC deletes unreferenced and old staging.

---

## Migration (from `_snapshots` in Git)

1. **Ingest** current `_snapshots/*` → compute `sha256` → push to CAS.  
2. **Strip** embedded hashes from result files (or delete result files with no review content).  
3. **Write** `booktest.manifest.yaml` for `(test_id, type) → sha256`.  
4. **.gitignore** `_snapshots/**` and `_reports/**`.  
5. Swap CI to `dvc pull` → replay → upload consolidated report.

---

## Example Result File (optional, static)

```markdown
# description
Topic model sanity check on small corpus

# qa
- no empty topics … ok
- top‑10 tokens look coherent … ok
- drift vs previous snapshot … low
- human rating … 3/3 ⭐
```

*(If there’s nothing to review, omit the file entirely and rely on the CI report.)*

---

## Roadmap Ideas

- Native **VCR cassette** integration in storage layer (keyed by content hash).  
- Inline **side‑by‑side rich diffs** (tables/charts) inside the review CLI.  
- Optional **pairwise preference review** for LLM outputs.  
- Built‑in **metrics blocks** (confusion matrix, ROUGE/BLEU/faithfulness) alongside snapshots.

---

## Who Is Booktest For?

- Teams shipping **AI features** (LLM assistance, topic models, ranking/scoring) who need **human‑in‑the‑loop QA**.
- Data science groups that want **fast feedback** and **clean PRs**, not a wall of snapshot files.
- Orgs that value **deterministic CI** and reproducible baselines across branches and releases.

---

**Get Started**  
- Add `booktest.toml` and `booktest.manifest.yaml`  
- Configure a DVC remote (`dvc remote add -d booktest-remote s3://…`)  
- Run: `booktest run → booktest review → booktest approve`  
- Wire CI to `dvc pull` and publish the one‑page review report.
