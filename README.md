# OMNI-1 — The Threefold Witness

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21436016.svg)](https://doi.org/10.5281/zenodo.21436016)

> **Public claim:** A preregistered demonstration of three independently evaluated nonclassicality witnesses — spatial (Bell-CHSH), temporal (Leggett-Garg K3), and contextual (Peres-Mermin) — bound into one chain-linked, independently reconstructable ExecutionProof governance record.

## The Experiment

OMNI-1 is the world's first single quantum computing job that simultaneously witnesses all three canonical nonclassicality families and binds them into a unified ExecutionProof governance record:

1. **Spatial** — Bell-CHSH inequality (2-qubit entanglement)
2. **Temporal** — Leggett-Garg K3 inequality (single-qubit coherence)
3. **Contextual** — Peres-Mermin magic square (3-qubit measurement contextuality)

Each witness is independently evaluated against preregistered thresholds. The aggregate produces an ExecutionProof verdict: **ALLOW**, **HOLD**, **DENY**, or **GATE-STOP**.

## Hardware Results (IBM Quantum ibm_kingston, Job d9e3064jeosc73fi98e0)

| Witness | Statistic | Measured | Classical Bound | Threshold | σ | Verdict |
|---------|-----------|----------|-----------------|-----------|---|---------|
| Bell-CHSH (S) | S | 2.797 | ≤2.0 | ≥2.2 | 17.82 | VALID_ABOVE ✓ |
| Leggett-Garg (K3) | K3 | 1.502 | ≤1.0 | ≥1.1 | 12.96 | VALID_ABOVE ✓ |
| Peres-Mermin (χ) | χ_min | 5.126 | ≤4.0 | ≥4.5 | 22.90 | VALID_ABOVE ✓ |

**Contextuality state-independence:** χ(|000⟩) = 5.144, χ(|+++⟩) = 5.282, χ(GHZ) = 5.126 — all above threshold.

### Aggregate ExecutionProof Verdict: **ALLOW**

- **omni_certified:** `True`
- **record_hash:** `fcc409ddcee8774586c3437c52ca3925cde25b4afa2562f3836a922644dd7def`
- **Independent verification:** PASS (omni1_verify.py reconstructed all witnesses, verdicts agree)

## ProofRecord Binding

The unified `omni-proofrecord-1.0` binds:
- Exact QASM3 circuit hashes for all 26 circuits
- Backend calibration snapshot (ibm_kingston, Heron r2, 156q)
- Physical qubit mapping
- Raw bitstring counts for all measurements
- Witness calculations (S, K3, χ per state)
- Per-arm and aggregate verdicts
- External entropy: NIST beacon pulse 1865678, LIGO GW150914 hash, IBM job ID
- Chain link to previous WITNESS-3 record hash
- MANIFEST.sha256 preregistration lock hashes
- OMNI nonce and record hash (SHA-256)

## Files

- **OMNI-1-preregistration.md** — Full preregistration document with all arms, thresholds, kill conditions, verdict logic
- **omni1_harness.py** — Experiment harness (builds circuits, submits to IBM Quantum, computes witnesses, assembles ProofRecord)
- **omni1_verify.py** — Independent verification script (reconstructs all witnesses and verdicts from raw counts)
- **MANIFEST.sha256** — Preregistration lock (SHA-256 hashes of prereg + harness, committed before execution)
- **results/OMNI-1-report.md** — Human-readable results report
- **results/OMNI-1-proofrecord.json** — Machine-readable ProofRecord JSON
- **requirements.txt** — Python dependencies
- **STATUS.md** — Experiment status and execution instructions

## Running

### Install dependencies
```bash
pip install -r requirements.txt
```

### Simulator validation (default)
```bash
python3 omni1_harness.py
```

### Independent verification
```bash
python3 omni1_verify.py
```

### Hardware run (requires IBM Quantum token)
```bash
export IBM_QUANTUM_TOKEN="your-token-here"
python3 omni1_harness.py --authorize-hardware --allow-unrotated
```

## Scope & Honesty

Results apply within the tested circuit model, backend (ibm_kingston, Heron r2, 156 qubits), calibration snapshot, shot counts (2000 per Bell-CHSH setting, 2000 per LG circuit, 1500 per PM context), software harnesses, and stated experimental conditions.

This is an experimental evidence record, not a universal security proof or production certification.

**Device-dependent:**
- Bell: locality + detection loopholes open
- Leggett-Garg: non-invasive measurability (NIM) assumption → clumsiness loophole open
- Contextuality: compatibility loophole open

Statistical σ reflects binomial shot noise only.

## Chain & Provenance

- **Previous record:** WITNESS-3 "Cosmic Beacon" (record_hash: `30e5a0f3cbf1f2351347c9096cc88e6f5fdc85139cbfe647e1a2ad1d7ec49257`)
- **NIST beacon:** Pulse 1865678 @ 2026-07-19T01:58:00.000Z
- **LIGO anchor:** GW150914 H1 strain SHA-256 `66c4b196`
- **GitHub:** https://github.com/derekhone/omni-testbeds
- **Zenodo DOI:** 10.5281/zenodo.21436016

## Citation

```bibtex
@dataset{hone_2026_omni1,
  author       = {Hone, Derek},
  title        = {{OMNI-1: The Threefold Witness — Spatial, 
                   Temporal, and Contextual Nonclassicality 
                   Witnesses Bound Into One ExecutionProof 
                   Governance Record}},
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.21436016},
  url          = {https://doi.org/10.5281/zenodo.21436016}
}
```

---

**Coherent Inheritance Framework (CIF) · Remnant Fieldworks Inc.**
