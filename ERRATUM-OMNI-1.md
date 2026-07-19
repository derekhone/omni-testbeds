# ERRATUM — OMNI-1 "The Threefold Witness"

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**

- **Corrects:** OMNI-1 v1.0 (Zenodo version DOI [10.5281/zenodo.21436016](https://doi.org/10.5281/zenodo.21436016)), GitHub `derekhone/omni-testbeds`
- **Published in:** OMNI-1 v1.1 — Zenodo version DOI [10.5281/zenodo.21436092](https://doi.org/10.5281/zenodo.21436092); concept DOI (always-latest) [10.5281/zenodo.21436015](https://doi.org/10.5281/zenodo.21436015)
- **Issued:** 2026-07-18 (local time; hardware execution timestamp in the ProofRecord is 2026-07-19 UTC)
- **Scope of this document:** transparent, clearly-labeled correction of six inconsistencies between the human-written narrative files and the machine-generated execution record. **No scientific result changes.** All witness values, verdicts, and the aggregate ALLOW are unchanged.
- **Governing principle:** *Proof Before Power* — the record must survive inspection, not merely sound legendary. Where the narrative and the machine record disagreed, the machine record governs, and the disagreement is disclosed here rather than quietly overwritten.

---

## What is and is not being corrected

**Not changed (and not in question):**
- The hardware execution itself (IBM Quantum `ibm_kingston`, Heron r2, job `d9e3064jeosc73fi98e0`).
- The as-locked preregistration and harness bytes. `MANIFEST.sha256` still verifies OK against `OMNI-1-preregistration.md` and `omni1_harness.py`. **The executed code was not altered post-hoc.**
- The as-executed `results/OMNI-1-proofrecord.json`. Its `record_hash` and `omni_nonce` still hash the exact bytes that were produced at execution time. **This file is not edited by the erratum** — including one defective field (see §6), which is disclosed rather than retro-edited so the hash chain stays intact.
- The machine-generated `results/OMNI-1-report.md`, which already carried the correct canonical values (this erratum appends a labeled note but does not change its figures).

**Changed:** the human-written narrative files — `OMNI-1-COMPLETION-SUMMARY.md` and `README.md` — which contained transcription errors, one fabricated set of per-state significances, and two overclaims. Those files are corrected in this revision, and every correction is enumerated below against the canonical machine record.

**Canonical source of truth:** `results/OMNI-1-proofrecord.json` (`record_hash = fcc409ddcee8774586c3437c52ca3925cde25b4afa2562f3836a922644dd7def`).

---

## Correction 1 — Executed shot configuration (52,000, not 70,000 or "~43,000")

**As released (narrative):**
- The preregistration prose specified Arm A 8,000 / Arm B 8,000 / **Arm C 54,000** (3,000 shots × 6 contexts × 3 states), **total 70,000**, with a preregistered budget fallback reducing Arm C to 2 states at 1,500 shots/context.
- The completion summary reported total shots as **"~43,000."**

**As executed (canonical, `shots` in the ProofRecord):**

| Arm | Circuits | Shots/circuit | Arm total |
|---|---|---|---|
| A — Bell-CHSH | 4 | 2,000 | 8,000 |
| B — Leggett-Garg | 4 | 2,000 | 8,000 |
| C — Peres-Mermin | 18 (3 states × 6 contexts) | 2,000 | 36,000 |
| **Total** | **26** | — | **52,000** |

**What actually happened, honestly stated:**
- The locked harness (`omni1_harness.py`, `--shots` default = 2000) applies **2,000 shots uniformly to every circuit**, giving Arm C = 2,000 × 18 = 36,000 and a grand total of **52,000**. This is exactly what the ProofRecord records.
- The preregistration **prose** said Arm C should run at **3,000 shots/context** (54,000). That prose figure was **internally inconsistent with the locked harness it was committed beside**, and the inconsistency was not reconciled before the lock. The locked code — not the prose — governed execution.
- The **budget fallback was not invoked**: all **three** states (|000⟩, |+++⟩, GHZ) were executed, not the two-state fallback.
- The completion summary's **"~43,000" was an arithmetic error** on our part and is withdrawn.

**Correct statement going forward:** OMNI-1 executed **52,000 shots** (A 8,000 / B 8,000 / C 36,000), matching the locked harness exactly. There was **no post-hoc alteration of the executed code**; the preregistration prose contained a shot-count figure (3,000/context) that disagreed with the locked harness (2,000/circuit) and was never reconciled prior to locking. We are not claiming the executed 52,000 was the preregistered target — it was the harness default, and the prose target of 70,000 was never met.

---

## Correction 2 — Canonical OMNI nonce

**As released (completion summary):** `omni_nonce = 72e982f6f7a8f53d36605b569c0b44b7dbd8a9fd12019630c1d1450c2426e58b`

**Canonical (ProofRecord + machine report):**
```
omni_nonce = f6fa824cca3fb05b2ef64684dac2c46ae8c5f41176820a80fa574a4492417042
```

The value printed in the completion summary was the **simulator-validation run's nonce**, mistakenly carried into the hardware summary. The canonical hardware nonce is `f6fa824c…`. The `record_hash` (`fcc409dd…`) was reported correctly and is unchanged.

---

## Correction 3 — One canonical contextuality significance (20.5579σ)

**As released (completion summary):** headline table listed the Peres-Mermin significance as **22.90σ**, and the detail section gave per-state significances of χ(|000⟩) @ 20.90σ, χ(|+++⟩) @ 23.40σ, χ(GHZ) @ 22.90σ.

**Canonical (ProofRecord `witness_contextual`):**
- `n_sigma_min = 20.5579` — this is the single canonical significance for the contextuality arm (it corresponds to χ_min).
- Per-state χ values are recorded: **χ(|000⟩) = 5.144, χ(|+++⟩) = 5.282, χ(GHZ) = 5.126**, with `chi_min = 5.126`.
- **Per-state σ values were not computed in the released record.** The 20.90 / 23.40 / 22.90 figures in the completion summary were **fabricated** and are withdrawn.

**Correct statement:** the contextuality arm reports **χ_min = 5.126 at n_σ = 20.5579** (binomial shot noise only). Report per-state χ values without attaching per-state σ figures that the record does not contain.

---

## Correction 4 — K3 = 1.502 vs. the ideal quantum maximum 1.5

**Canonical:** `K3 = 1.502`, quantum maximum = **1.5**, `n_sigma = 12.9616` above the macrorealist bound of 1.0.

**Clarification:** the measured value 1.502 slightly exceeds the ideal Lüders-bound quantum maximum of 1.5. This is **not** a claim of exceeding the quantum limit. The excess (0.002) is **statistically consistent with the ideal maximum within measurement uncertainty** (finite-shot binomial fluctuation plus calibration/readout systematics). The scientifically correct reading is: *K3 is consistent with the ideal quantum maximum of 1.5 to within measurement uncertainty, and is decisively above the macrorealist bound of 1.0 (12.96σ).* Any phrasing implying OMNI-1 was "more quantum than the quantum maximum" is incorrect and is withdrawn.

---

## Correction 5 — Removal of unsupported historical and rhetorical claims

Two claims are withdrawn as unsupported:

1. **"World's first single quantum computing job that simultaneously witnesses all three…"** — we have not conducted a systematic prior-art search sufficient to support a first-in-the-world priority claim, and combined witness demonstrations exist in the literature.
   - **Replacement language:** *"To our knowledge, OMNI-1 is an unusual preregistered demonstration that evaluates spatial, temporal, and contextual nonclassicality witnesses within a single hardware job and binds them into one independently reconstructable ExecutionProof record."*

2. **"The provenance is bulletproof."** — an absolute security claim we do not stand behind.
   - **Replacement language:** *"The provenance is tamper-evident, independently reconstructable, and cryptographically bound within the released implementation."*

These corrections apply everywhere the original phrasings appeared (completion summary and README).

---

## Correction 6 — Physical qubit-mapping record (known defect, disclosed not edited)

**Defect:** in `results/OMNI-1-proofrecord.json`, `backend_info.qubit_mapping` lists **all 156 physical qubits (0–155) for every one of the 26 circuits**, including the 1-qubit Leggett-Garg circuits and the 2-qubit Bell-CHSH circuits. This is the **full backend qubit layout**, not the actual per-circuit transpiled physical qubits. It is a logging defect in the v1.0 harness: it recorded `backend.num_qubits` rather than each circuit's transpiled `final_index_layout`.

**What remains reliable in the released record:** the per-circuit **logical width** is correct via `circuits.<name>.n_qubits`:
- Arm A (Bell-CHSH): **2 qubits** per circuit
- Arm B (Leggett-Garg): **1 qubit** per circuit
- Arm C (Peres-Mermin): **5 qubits** per circuit (3-qubit magic-square register plus ancillas as constructed by the harness)

**What is not recoverable from the released record:** the specific physical qubits each circuit was transpiled onto. Because the transpiled layout was not captured at execution time, **the actual physical qubit indices used per circuit cannot be reconstructed from the released v1.0 artifacts.** We state this plainly rather than infer or fabricate a mapping.

**Why the JSON is not edited:** `qubit_mapping` is part of the byte range covered by `record_hash`. Editing it would break the hash and the tamper-evidence guarantee. The defect is therefore disclosed here and left in place; the fix lands in a forward harness revision (v1.1), not a retro-edit of the hashed v1.0 record.

**v1.1 fix (forward-looking, applied in a new harness — the locked v1.0 is preserved):** capture the transpiled layout per circuit instead of the backend width. Illustrative change:

```python
# v1.0 (defective): recorded the full backend width for every circuit
# backend_info["qubit_mapping"][name] = list(range(backend.num_qubits))

# v1.1 (correct): record each circuit's actual transpiled physical qubits
transpiled = pm.run(circuit)                      # pm = generate_preset_pass_manager(...)
layout = transpiled.layout
physical_qubits = layout.final_index_layout()      # actual physical indices used
backend_info["qubit_mapping"][name] = list(physical_qubits)
```

Until an OMNI experiment is re-run under v1.1, the honest position is: **logical circuit widths are 2 / 1 / 5 (A / B / C); the exact physical placement on `ibm_kingston` for this specific job is not available in the released record.**

---

## Summary of canonical values (authoritative)

| Field | Canonical value |
|---|---|
| Backend / job | `ibm_kingston` (Heron r2) · job `d9e3064jeosc73fi98e0` |
| Total shots | **52,000** (A 8,000 / B 8,000 / C 36,000) |
| Spatial — Bell-CHSH | S = **2.797**, n_σ = **17.8215** (bound 2.0, Tsirelson 2.8284) |
| Temporal — Leggett-Garg | K3 = **1.502**, n_σ = **12.9616** (bound 1.0, qmax 1.5 — consistent within uncertainty) |
| Contextual — Peres-Mermin | χ_min = **5.126**, n_σ = **20.5579** (bound 4.0, qbound 6.0) |
| Per-state χ | 000 = 5.144 · +++ = 5.282 · GHZ = 5.126 (no per-state σ in record) |
| Aggregate verdict | **ALLOW** · `omni_certified = True` |
| OMNI nonce | `f6fa824cca3fb05b2ef64684dac2c46ae8c5f41176820a80fa574a4492417042` |
| record_hash | `fcc409ddcee8774586c3437c52ca3925cde25b4afa2562f3836a922644dd7def` |
| Logical circuit widths | A = 2q · B = 1q · C = 5q (physical placement not recoverable from v1.0 record) |

---

## Provenance of this erratum

This correction was prompted by the founder's post-publication review, which flagged six inconsistencies between the narrative files and the machine record. Each was checked against `results/OMNI-1-proofrecord.json` and confirmed. The corrections here are transcription and framing fixes plus one disclosed logging defect; **no measured value, verdict, or the aggregate ALLOW changes.** The as-locked preregistration, the as-executed ProofRecord, and the MANIFEST hash chain are preserved exactly.

**Coherent Inheritance Framework (CIF) · Remnant Fieldworks Inc.**
