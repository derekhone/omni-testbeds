# OMNI-1 Preregistration — The Threefold Witness

**REMNANT FIELDWORKS™ · CIF EXPERIMENT SERIES · EXECUTIONPROOF-GOVERNED**

## OMNI-1: The Threefold Witness — Three Independently Evaluated Nonclassicality Witnesses Bound Into One Chain-Linked, Independently Reconstructable Execution Record

- **Experiment ID:** OMNI-1
- **Organization:** Remnant Fieldworks Inc.
- **Principal investigator:** Derek Hone
- **Framework:** Coherent Inheritance Framework (CIF)
- **Governance:** ExecutionProof (RF-100 verification-first execution control)
- **Preregistration status:** LOCKED prior to hardware execution (see `MANIFEST.sha256`)
- **Target hardware (GATED — not yet authorized):** IBM Quantum, `ibm_kingston` (preferred) /
  `ibm_fez` (fallback), Heron r2, 156 qubits
- **Channel:** `ibm_quantum_platform` (open plan) — execution mode: **Batch** (not Session)
- **ProofRecord schema:** `omni-proofrecord-1.0`

> This is a preregistration document. Arms, thresholds, kill conditions, verdict logic, and
> publication rules below are fixed **before** any hardware run. No post-hoc alteration of
> hypotheses, metrics, or acceptance windows is permitted. Whatever comes out — ALLOW, HOLD,
> DENY, or GATE-STOP — is published verbatim.

---

## 0. The honest public claim

The only claim OMNI-1 makes publicly is:

> **"A preregistered demonstration of three independently evaluated nonclassicality witnesses
> bound into one chain-linked, independently reconstructable execution record."**

OMNI-1 is explicitly **not** claimed to be "the greatest quantum experiment," a loophole-free
test, or a device-independent certification. Its contribution is the **governed binding** of
three witness classes into a single ExecutionProof record — connecting the quantum evidence
directly to ExecutionProof rather than standing as an isolated physics stunt.

---

## 1. Purpose and hypothesis

> **Hypothesis (H1):** One governed execution record can bind — and an independent party can
> reconstruct — three distinct quantum evidence classes measured in a single job:
> a **spatial** correlation witness (Bell-CHSH), a **temporal** correlation witness
> (Leggett-Garg K3), and a **contextuality** witness (Peres-Mermin), such that each witness is
> independently evaluated and the aggregate is governed by an ExecutionProof verdict.

- **Null (H0):** At least one witness cannot be validly evaluated above its preregistered
  threshold under the tested conditions, or the three witnesses cannot be bound into a single
  independently reconstructable record.

Prior published Remnant Fieldworks results (context only; not re-run here):

| Prior experiment | Witness | Reported value |
|---|---|---|
| BELLWETHER-1 | CHSH S | 2.514 |
| BELLWETHER-2 | Mermin \|M\| | 3.423 |
| BELLWETHER-3 | Peres-Mermin χ | 5.268–5.376 (state-independent) |
| CHRONO-1 | Leggett-Garg K3 | 1.450 |
| WITNESS-3 "Cosmic Beacon" | CHSH S | 2.545 @ 15.8σ (NIST + LIGO nonce) |

OMNI-1 does not re-derive these; it unifies the three *families* into one governed record and
chain-links to the previous WITNESS record hash.

---

## 2. Experimental arms (witnesses)

### Arm A — Bell-CHSH (spatial correlation witness)

- **State:** 2-qubit Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 (H on q0, CX q0→q1).
- **Settings:** Alice a ∈ {0, π/4}; Bob b ∈ {π/8, 3π/8}. Four correlators E(a,b) across 4
  circuits, each rotating the measurement basis by `Ry(-2θ)` before Z-measurement.
- **Statistic:** S = E(a0,b0) − E(a0,b1) + E(a1,b0) + E(a1,b1).
- **Bounds:** classical LHV |S| ≤ 2; Tsirelson quantum max 2√2 ≈ 2.8284.
- **Witness thresholds (preregistered):**
  - VALID + above threshold → **S ≥ 2.2**
  - INCONCLUSIVE → 2.0 ≤ S < 2.2
  - INVALID → S < 2.0
- **Shots:** 2000 × 4 settings = 8000.

### Arm B — Leggett-Garg K3 (temporal correlation witness)

- **System:** single qubit under repeated `Ry(π/3)` evolution between times t1, t2, t3.
- **Correlators:** C12, C23, C13 measured on 3 separate circuits (plus a baseline circuit),
  each recording the two relevant sequential measurements, avoiding classical feed-forward
  ambiguity.
- **Statistic:** K3 = C12 + C23 − C13.
- **Bounds:** macrorealist (with NIM) K3 ≤ 1; quantum max 1.5.
- **Witness thresholds (preregistered):**
  - VALID + above threshold → **K3 ≥ 1.1**
  - INCONCLUSIVE → 1.0 ≤ K3 < 1.1
  - INVALID → K3 < 1.0
- **Shots:** 2000 × 4 circuits (C12, C23, C13, baseline) = 8000.

### Arm C — Peres-Mermin magic square (contextuality witness)

- **System:** 3-qubit Peres-Mermin 3×3 magic square of Pauli observables. Six contexts (rows
  R1,R2,R3; columns C1,C2,C3).

  |       | col 1 | col 2 | col 3 |
  |-------|-------|-------|-------|
  | row 1 | XI    | IX    | XX    |
  | row 2 | IZ    | ZI    | ZZ    |
  | row 3 | XZ    | ZX    | YY    |

  Rows and first two columns multiply to +I; column 3 multiplies to −I.
- **Statistic:** χ = ⟨R1⟩ + ⟨R2⟩ + ⟨R3⟩ + ⟨C1⟩ + ⟨C2⟩ − ⟨C3⟩.
- **Bounds:** noncontextual HV ≤ 4; quantum value = 6.
- **State-independence:** run on **3 states** — |000⟩, |+++⟩, GHZ.
- **Witness thresholds (preregistered):**
  - VALID + above threshold → **χ ≥ 4.5 on all three states**
  - INCONCLUSIVE → 4.0 ≤ χ_min < 4.5
  - INVALID → χ < 4.0 on any state
- **Shots:** 3000 × 6 contexts × 3 states = 54000.

**Total submitted:** 8000 + 8000 + 54000 = **70,000 shots** across 26 circuits, one Batch job.

> **Budget fallback (preregistered):** if estimated QPU time exceeds remaining budget, reduce
> Arm C to **2 states** (|000⟩, GHZ) and **1500 shots/context**. Declared here so invoking it
> is not a post-hoc change.

---

## 3. Unified ProofRecord — full chain binding (`omni-proofrecord-1.0`)

The ProofRecord MUST bind all of the following so an independent party can reconstruct every
witness and every verdict without the harness runtime:

1. **exact circuits** — QASM3 (or serialized) source + SHA-256 per circuit
2. **backend and calibration** — backend name + calibration snapshot hash
3. **qubit mapping** — physical qubit layout used by the transpiled circuits
4. **shot counts** — per circuit and per arm
5. **raw counts** — the measured bitstring histograms, verbatim
6. **witness calculations** — S, K3, χ (per state) with intermediate correlators
7. **independent verdicts** — per-arm witness verdict (VALID+ABOVE / INCONCLUSIVE / INVALID)
8. **aggregate governance verdict** — ALLOW / HOLD / DENY / GATE-STOP
9. **previous WITNESS record hash** — chain link to the prior record (WITNESS-3)
10. **fresh NIST not-before anchor** — latest NIST beacon pulse fetched before submission
11. **full manifest hashes** — SHA-256 of preregistration + harness (`MANIFEST.sha256`)

```json
{
  "schema": "omni-proofrecord-1.0",
  "experiment": "OMNI-1",
  "framework": "Coherent Inheritance Framework (CIF)",
  "governance": "ExecutionProof",
  "witness_spatial":   {"S": 0.0, "n_sigma": 0.0, "classical_bound": 2.0, "tsirelson": 2.8284, "verdict": "", "certified": false},
  "witness_temporal":  {"K3": 0.0, "n_sigma": 0.0, "macrorealist_bound": 1.0, "quantum_max": 1.5, "verdict": "", "certified": false},
  "witness_contextual":{"chi_000": 0.0, "chi_ppp": 0.0, "chi_ghz": 0.0, "chi_min": 0.0, "n_sigma_min": 0.0, "noncontextual_bound": 4.0, "quantum_bound": 6.0, "state_independent": false, "verdict": "", "certified": false},
  "aggregate_verdict": "ALLOW|HOLD|DENY|GATE-STOP",
  "omni_certified": false,
  "circuits": {"<name>": {"qasm_sha256": "", "n_qubits": 0}},
  "backend_info": {"name": "", "calibration_hash": "", "qubit_mapping": {}},
  "shots": {"per_arm": {}, "per_circuit": {}},
  "raw_counts": {"<circuit_name>": {}},
  "external_entropy": {"nist_beacon_pulse": 0, "nist_value": "", "nist_timestamp": "", "ligo_gw150914_hash": ""},
  "chain": {"previous_witness_record_hash": "", "manifest_prereg_sha256": "", "manifest_harness_sha256": ""},
  "backend": "", "job_id": "", "shots_per_arm": 0,
  "omni_nonce": "SHA-256(spatial_hash|temporal_hash|contextual_hash|nist_beacon|job_id)",
  "record_hash": "SHA-256(full canonical JSON minus record_hash)",
  "verdict": "ALLOW|HOLD|DENY|GATE-STOP"
}
```

---

## 4. Aggregate governance verdict logic (preregistered)

Each arm is first assigned an independent **witness verdict**:
`VALID_ABOVE` (≥ threshold), `INCONCLUSIVE` (classical bound ≤ value < threshold),
or `INVALID` (< classical bound).

The **aggregate ExecutionProof verdict** is then:

- **ALLOW** — all three witnesses `VALID_ABOVE` **AND** the record reconstructs (independent
  verification reproduces every witness and the record/nonce hashes) **AND** provenance is
  valid (NIST anchor present, chain hash present, manifest hashes match).
- **HOLD** — any witness `INCONCLUSIVE` but **none** `INVALID`, and provenance is otherwise
  valid. (Above classical bound, below preregistered ceiling.)
- **DENY** — tampering detected, reconstruction mismatch, or invalid provenance (manifest hash
  mismatch, missing/invalid NIST anchor, broken chain link).
- **GATE-STOP** — hardware or data conditions prevent a valid evaluation (job error, backend
  unavailable, missing counts, insufficient shots, NIST beacon unreachable at submission time).

`omni_certified = True` only when `aggregate_verdict = ALLOW`.

Precedence when multiple conditions hold: **DENY > GATE-STOP > HOLD > ALLOW**
(a tampering/provenance failure always dominates; an execution failure dominates a
merely-inconclusive witness).

---

## 5. Kill condition (preregistered)

> **If ANY arm produces a witness value below its classical/macrorealist bound
> (S < 2.0, K3 < 1.0, or χ < 4.0 on any state), the witness is INVALID, the aggregate cannot be
> ALLOW, and the honest result (HOLD/DENY/GATE-STOP as applicable) is published verbatim.**

There is no retry-until-pass. The first preregistered hardware run is the run of record.

---

## 6. External entropy & chain anchor

- **NIST randomness beacon (not-before anchor):** latest pulse fetched from
  `https://beacon.nist.gov/beacon/2.0/pulse/last` **before** circuit submission. Pulse index,
  `outputValue` hex, and timestamp recorded. If unreachable at submission → **GATE-STOP**.
- **LIGO GW150914 reference hash:** `66c4b196...` fixed cosmological anchor (from WITNESS-3).
- **Previous WITNESS record hash:** chain-links OMNI-1 to the prior record (WITNESS-3).
- **IBM job_id:** assigned at submission (unknowable before run).

**Fusion:**

```
omni_nonce = SHA-256( nist_value_hex | ligo_hash | job_id_bytes
                      | spatial_witness_hash | temporal_witness_hash | contextual_witness_hash )
```

where each `*_witness_hash` = SHA-256 of that arm's canonical witness sub-object.

---

## 7. Publication rule

**Publish whatever comes out.** ALLOW, HOLD, DENY, and GATE-STOP are all published verbatim
with the same rigor. No result is suppressed; no threshold is moved after seeing data. Report,
raw counts, ProofRecord JSON, and verification output are released together.

---

## 8. Execution protocol — simulator validation BEFORE hardware (preregistered)

1. **Preregistration lock** — `MANIFEST.sha256` committed to git before any run.
2. **Simulator validation** — the harness runs first in **simulator mode**
   (`qiskit-aer`, ideal + optional noise model) to confirm all circuits construct, all
   witnesses compute, the ProofRecord assembles, and `omni1_verify.py` independently
   reconstructs the record. This is validation of the *harness and verdict logic*, not a
   physics claim.
3. **Hardware gate (NOT auto-authorized).** The hardware run is **withheld** until:
   (a) exposed secrets (IBM Quantum + Zenodo tokens) are **rotated**, and
   (b) the design passes **scientific and IP-integrity review**.
   The harness refuses to submit to hardware unless explicitly authorized via
   `--authorize-hardware` AND a rotated token is supplied; absent authorization it runs
   simulator-only and records `GATE-STOP` for any hardware-only fields.

---

## 9. Honesty caveats (preregistered, non-negotiable)

- **Device-dependent.** Witnesses are computed from a specific backend, qubit selection,
  calibration snapshot, transpilation, and shot budget — not device-independent certifications.
- **Bell (Arm A):** locality loophole and detection/fair-sampling loophole remain open; not a
  loophole-free Bell test.
- **Leggett-Garg (Arm B):** relies on the non-invasive measurability (NIM) assumption, which
  cannot be enforced here; the clumsiness loophole remains open.
- **Contextuality (Arm C):** the compatibility (finite-precision / disjoint-measurement)
  loophole remains open; commuting observables measured in separate circuits.
- **Hardware noise:** gate, readout, crosstalk, and drift errors on Heron r2 bias witnesses,
  generally downward; reported values are lower bounds on ideal behavior, not exact.
- **SPAM:** readout mitigation (M3/mthree or matrix inversion) may be applied and is reported
  alongside raw (unmitigated) values; raw values are always reported.
- **Statistical σ** reflects binomial shot noise only, not systematic/calibration error.

---

## 10. Scope statement

> **Results apply within the tested circuit model, backend, qubits, calibration, shot counts,
> software harnesses, and stated experimental conditions. This is an experimental evidence
> record, not a universal security proof or production certification.**

CIF is the current framework of record for Remnant Fieldworks. (UIP was the former working
title; it is not referred to as the "former CIF.")

---

## 11. Reproducibility and preregistration lock

- `MANIFEST.sha256` contains SHA-256 digests of this preregistration and `omni1_harness.py`,
  committed to git **before** hardware execution.
- The harness records the preregistration manifest hash into the ProofRecord, so any post-hoc
  edit to prereg or harness is detectable (→ DENY on verification).
- `omni1_verify.py` independently recomputes all witnesses and the record/nonce hashes from the
  released raw counts and ProofRecord, with no dependence on the harness runtime, and emits its
  own ALLOW/HOLD/DENY/GATE-STOP verdict.
