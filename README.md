# OMNI-1 — The Threefold Witness

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**

> **A preregistered demonstration of three independently evaluated nonclassicality witnesses
> bound into one chain-linked, independently reconstructable execution record.**

OMNI-1 tests whether a single governed execution record can bind — and an independent party can
reconstruct — three distinct quantum evidence classes measured in one job:

| Arm | Witness | Statistic | Classical bound | PASS threshold |
|-----|---------|-----------|-----------------|----------------|
| A | Bell-CHSH (spatial) | S | ≤ 2.0 | ≥ 2.2 |
| B | Leggett-Garg (temporal) | K3 | ≤ 1.0 | ≥ 1.1 |
| C | Peres-Mermin (contextual) | χ (3 states) | ≤ 4.0 | ≥ 4.5 (all states) |

The unified `omni-proofrecord-1.0` ProofRecord binds: exact circuits, backend + calibration,
qubit mapping, shot counts, raw counts, witness calculations, independent per-arm verdicts, the
aggregate ExecutionProof verdict, the previous WITNESS record hash (chain link), a fresh NIST
not-before anchor, and full manifest hashes.

## Aggregate ExecutionProof verdict

- **ALLOW** — all three witnesses valid & above threshold, record reconstructs, provenance valid
- **HOLD** — any witness inconclusive, none invalid
- **DENY** — tampering, reconstruction mismatch, or invalid provenance (or a witness below its classical bound)
- **GATE-STOP** — hardware/data conditions prevent a valid evaluation
- Precedence: **DENY > GATE-STOP > HOLD > ALLOW**

## Files

```
omni-testbeds/
├── README.md
├── OMNI-1-preregistration.md      # Full preregistration (locked before execution)
├── MANIFEST.sha256                # SHA-256 of prereg + harness (preregistration lock)
├── omni1_harness.py               # Experiment harness (simulator default; hardware GATED)
├── omni1_verify.py                # Independent reconstruction + verdict
├── requirements.txt
├── STATUS.md                      # Current status / what remains
└── results/
    ├── OMNI-1-report.md           # Human-readable report
    └── OMNI-1-proofrecord.json    # Full ProofRecord
```

## Running

```bash
pip install -r requirements.txt

# Simulator validation (DEFAULT — validates harness + verdict logic, not a physics claim)
python omni1_harness.py --shots 2000
python omni1_harness.py --noise            # with a simple depolarizing noise model

# Independent verification of the released record
python omni1_verify.py results/OMNI-1-proofrecord.json
```

## Hardware run — GATED (not yet authorized)

Per preregistration §8, the IBM Quantum hardware run is **withheld** until:
1. Exposed secrets (IBM Quantum + Zenodo tokens) are **rotated**, and
2. The design passes **scientific + IP-integrity review**.

The harness refuses to submit to hardware unless `--authorize-hardware` **and**
`--allow-unrotated` are both passed (the latter only after the two conditions above are met):

```bash
# Only after tokens are rotated AND design reviewed:
python omni1_harness.py --authorize-hardware --allow-unrotated --backend ibm_kingston
```

Target hardware: IBM Quantum `ibm_kingston` (preferred) / `ibm_fez` (fallback), Heron r2,
channel `ibm_quantum_platform`, Batch execution mode.

## Scope & honesty

Results apply within the tested circuit model, backend, qubits, calibration, shot counts,
software harnesses, and stated experimental conditions. **This is an experimental evidence
record, not a universal security proof or production certification.** Witnesses are
device-dependent. Bell locality + detection loopholes remain open; Leggett-Garg relies on the
non-invasive measurability (NIM) assumption (clumsiness loophole open); contextuality retains
the compatibility loophole. Statistical σ reflects binomial shot noise only.

CIF is the current framework of record for Remnant Fieldworks. (UIP was the former working
title.)
