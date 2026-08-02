# OMNI-1 — STATUS

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**
**As of 2026-07-19:** hardware execution **COMPLETE**, independently verified (**ALLOW**), published to GitHub and Zenodo.

> **Execution summary:** OMNI-1 executed on IBM Quantum `ibm_kingston` (job `d9e3064jeosc73fi98e0`), **52,000 shots total** (Arm A 8,000 / Arm B 8,000 / Arm C 36,000 — uniform 2,000/circuit). Results: S = 2.797, K3 = 1.502, χmin = 5.126. Aggregate ExecutionProof verdict **ALLOW**. Independent verifier PASS. Published to Zenodo — concept DOI (always-latest): [10.5281/zenodo.21436015](https://doi.org/10.5281/zenodo.21436015); v1.1 (corrected): [10.5281/zenodo.21436092](https://doi.org/10.5281/zenodo.21436092); v1.0 (original): [10.5281/zenodo.21436016](https://doi.org/10.5281/zenodo.21436016). See **[ERRATUM-OMNI-1.md](ERRATUM-OMNI-1.md)** for the six-point correction record (shot count, nonce, contextuality, K3 wording, two withdrawn overclaims, qubit-mapping logging defect). No measured value or verdict changed.

## Completed

- [x] **Preregistration** (`OMNI-1-preregistration.md`) — Threefold Witness design, three arms,
      thresholds, kill condition, ExecutionProof aggregate verdict logic
      (ALLOW / HOLD / DENY / GATE-STOP), full chain-binding schema, publication rule, honesty
      caveats, scope statement.
- [x] **Harness** (`omni1_harness.py`) — builds all 26 circuits (Arm A: 4 CHSH; Arm B: 4
      Leggett-Garg; Arm C: 18 = 6 contexts × 3 states), fetches NIST beacon, assembles the
      unified `omni-proofrecord-1.0` ProofRecord, computes the aggregate governance verdict,
      writes the report.
- [x] **Independent verifier** (`omni1_verify.py`) — reconstructs S, K3, χ, witness hashes,
      OMNI nonce, and record hash directly from released raw counts with no quantum-library or
      harness dependency; emits its own governance verdict.
- [x] **Preregistration lock** (`MANIFEST.sha256`) — SHA-256 of prereg + harness, committed to
      git before any run.
- [x] **Simulator validation** (ideal + depolarizing noise):
  - Ideal: **S = 2.844**, **K3 = 1.504**, **χ = 6.000** on all three states →
    aggregate **ALLOW**; independent verifier reconstructs the record and agrees.
  - Noise (depolarizing): **S ≈ 2.75**, **K3 ≈ 1.50**, **χ ≈ 5.27** (consistent with the
    published BELLWETHER-3 range 5.268–5.376) → aggregate **ALLOW**.
  - Tamper test: corrupting a single raw count triggers `record_hash mismatch` → **DENY**,
    confirming the reconstruction / provenance gate works.

## Hardware execution (completed 2026-07-19)

- [x] **IBM Quantum hardware run** — executed on `ibm_kingston` (job `d9e3064jeosc73fi98e0`), 52,000 shots, Batch mode.
- [x] **Independent verification** — `omni1_verify.py` PASS, reconstructed all witness values and aggregate verdict from raw counts.
- [x] **Zenodo publication** — v1.0 published; v1.1 correction published after erratum.
- [x] **GitHub push** — published to `derekhone/omni-testbeds`.
