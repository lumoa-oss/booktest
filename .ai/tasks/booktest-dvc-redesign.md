
# Booktest → Minimal‑Git Redesign with DVC/CAS (Design Doc)

**Owner:** Netigate
**Scope:** Replace bulky Git snapshots & cassettes with a manifest + remote content‑addressable storage (CAS), while keeping Booktest’s review‑driven UX.  
**Status:** Draft ready for implementation

---

## 1) Context & Sanity Check

- Booktest stores reviewable snapshots under `_snapshots/` (e.g., `books/test/examples/snapshots/httpx/_snapshots/httpx.json`).  
- There are 4 snapshot “types”: **env**, **http**, **httpx**, **func** (one per type).  
- Today, result files often embed **gazette hashes** inside the human‑readable snapshot to force re‑creation on invalidation.

**Problem:** Storing these in Git creates noisy PRs and merge conflicts. We want a **static or minimalistic Git footprint** while preserving Booktest’s **review‑driven CLI** and rich Markdown output.

---

## 2) Goals

1. **Minimal Git noise** — keep only tiny pointers in Git; no bulky blobs or cassettes.
2. **Preserve reviewer ergonomics** — rich MD/HTML report with headers, tables, plots; same guided CLI.
3. **Deterministic CI** — replay from approved baselines (no live GPT/HTTP) for speed and stability.
4. **Parallelization & deps** — keep Booktest’s existing dependency graph, resource monitoring, and parallel optimization intact.
5. **Simple GC** — safe, root‑based garbage collection of unreferenced blobs.

---

## 3) Key Design: Split Result vs Gazette

- **Result (human)**: a tiny, stable **Markdown** document per test *only if there’s something to review*. No embedded hashes.
- **Gazette (machine)**: the replay payload (env dump, HTTP/httpx cassette, function snapshot). Stored off‑Git in **content‑addressable storage** (CAS) keyed by **sha256** of the content.

### Minimal Result Example (optional file)

```markdown
# description
One‑liner of what this test checks.

# qa
- assert XYZ is correct … ok
- assert 0 errors … ok
- review correct language … ok
- review response quality … 3/3 ⭐
```

If there’s no reviewable content, **omit** the result file entirely.

---

## 4) Where Things Live

### 4.1 In Remote (CAS via DVC)

```
<remote>/booktest/blobs/
  env/sha256/ab/<sha256>
  http/sha256/cd/<sha256>
  httpx/sha256/ef/<sha256>
  func/sha256/01/<sha256>
```
- Exact blob content is your current JSON/YAML/MD (optionally gzipped).  
- Type appears in the path for readability; content is addressed by hash.

### 4.2 In Git (two modes)

**A) Manifest (recommended, smallest PRs)**  
Single file mapping `(test_id, type) → sha256`:
```yaml
# booktest.manifest.yaml
testsuite/test_dir::test_topic_model:
  env:   "sha256:7b1a4f...e39"
  http:  "sha256:4c0f9b...21a"
  httpx: "sha256:a3d011...9fd"
  func:  "sha256:92b8ce...b55"
```

**B) DVC pointer files (.dvc) per snapshot (zero custom storage code)**  
Git contains tiny `.dvc` files under `_snapshots/` that reference CAS blobs.

---

## 5) Booktest CLI Flow (Ergonomics Preserved)

1. **Run** (`booktest run`):  
   - Pull approved digests from manifest; fetch gazettes from CAS; run tests.  
   - On change, compute new digest, push blob to **staging**, render human‑readable MD locally (not committed).

2. **Review** (`booktest review`):  
   - Show diffs of result MD & structured JSON/plots while tests run or after.  
   - Reviewer decides what to approve.

3. **Approve** (`booktest approve`):  
   - Update manifest (or `.dvc` pointers) with new sha256(s).  
   - Promote CAS objects from `staging/` → `keep/`.  
   - Optionally write/update a minimal `result.md` if you keep one in Git.

4. **CI Replay**:  
   - `dvc pull` (or CAS fetch) → run tests in **replay** (no live GPT/HTTP).  
   - Upload a single **HTML/MD report artifact** for PRs.

---

## 6) CI / PR Shape

- PR diff typically shows **1–3 lines** changed in `booktest.manifest.yaml` (plus small `result.md` if you keep it).  
- CI provides **one** artifact link (consolidated HTML/MD review report).  
- No bulky cassette/snapshot files in Git, no merge conflicts on YAML blobs.

---

## 7) Parallelization & Dependencies

- Keep Booktest’s **internal dependency graph**, resource monitoring, and elapsed‑time heuristics for parallel runs — unchanged.
- CAS digests do not affect scheduling; they only define **which baselines** are replayed in CI.

---

## 8) Garbage Collection (GC)

Use two CAS prefixes: `staging/` and `keep/`.

- **Mark**: read digests from `booktest.manifest.yaml` on `main` + release tags (+ open PRs if desired).  
- **Sweep**:  
  - Remove `staging/` older than **N days** (e.g., 7).  
  - Remove any `keep/` blobs **not reachable** from the marked set (optional extra grace, e.g., 14 days).

If using DVC pointers, you can also rely on `dvc gc -w -c --all-branches --all-tags`.

---

## 9) Migration Plan (remove hashes from result files)

1. **Ingest** each existing `_snapshots/*` file: extract current payload (and any embedded hash), compute sha256, **push to CAS**.  
2. **Strip** hash metadata from result files (or delete result files with no human content).  
3. **Write** `booktest.manifest.yaml` for `(test_id, type) → sha256`.  
4. **.gitignore** `_snapshots/` payload files; keep only minimal `result.md` files if needed.  
5. Update CI to `dvc pull` → replay; upload a unified review report.

---

## 10) Example Config Snippets

### 10.1 `booktest.toml`
```toml
[storage]
mode = "dvc-manifest"              # or "dvc-pointers"
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

### 10.2 `dvc.yaml` (optional pipeline caching)
```yaml
stages:
  build_topics:
    cmd: python pipelines/build_topics.py --out artifacts/topics.pkl
    deps:
      - data/raw_corpus.jsonl
      - pipelines/build_topics.py
    outs:
      - artifacts/topics.pkl
  test_topics_snapshot:
    cmd: booktest run --select tests/topics/test_top_words.py
    deps:
      - artifacts/topics.pkl
      - tests/topics/test_top_words.py
    outs:
      - books/book/testsuite/test_dir/_snapshots/topics.json  # local, gitignored
```

### 10.3 Git hygiene
```
# .gitignore
books/**/_snapshots/**
books/**/_reports/**
.booktest_cache/**
```

### 10.4 Folder Diff (before vs after)

**Before**
```
books/.../_snapshots/httpx.json   # committed; big; embeds hashes
```

**After**
```
books/.../_snapshots/httpx.json   # local only (gitignored)
booktest.manifest.yaml            # small (few lines changed per PR)
books/.../_reports/index.html     # CI artifact only (not committed)
```

---

## 11) FAQ & Risks

- **Q: How do we force re‑creation when invalidated if hashes aren’t in result files?**  
  **A:** Use the engine’s dependency graph + timestamps/inputs. When inputs change, the produced content changes → new sha256, surfaced in review. No need to mix hashes into human docs.

- **Q: What about VCR cassettes (http/httpx)?**  
  **A:** Store cassettes in CAS like any other gazette; in CI run strictly in **replay**. Key by content hash. No cassette churn in Git.

- **Q: Can we keep zero result files?**  
  **A:** Yes. If there’s nothing to review, omit them entirely. Rely on the consolidated report artifact in CI and local preview during `booktest review`.

- **Q: How big is the change?**  
  **A:** Storage layer change + a small manifest writer/reader. Everything else (review CLI, parallel graph, UX) remains.

---

## 12) Action Items

- [ ] Implement storage backend: **manifest + DVC/CAS** (push/pull, staging/keep).  
- [ ] Add `booktest approve`: update manifest and promote blobs.  
- [ ] Add consolidated review report artifact in CI.  
- [ ] Write migration script (ingest old `_snapshots/`, strip hashes, build manifest).  
- [ ] Add nightly GC job (mark‑and‑sweep).

---

**End of document.**
