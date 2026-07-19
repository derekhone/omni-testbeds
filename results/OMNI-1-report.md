# OMNI-1 Report — The Threefold Witness

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**

- Experiment: **OMNI-1**  ·  Schema: `omni-proofrecord-1.0`
- Mode: **HARDWARE**  ·  Backend: `ibm_kingston`  ·  Job: `d9e3064jeosc73fi98e0`
- Generated: 2026-07-19T02:02:25.278208+00:00

> **Public claim:** A preregistered demonstration of three independently evaluated
> nonclassicality witnesses bound into one chain-linked, independently reconstructable
> execution record.

## Aggregate ExecutionProof verdict: **ALLOW**

`omni_certified = True`

| Witness | Statistic | Value | Bound | Threshold | nσ | Verdict |
|---|---|---|---|---|---|---|
| Spatial (Bell-CHSH) | S | 2.797 | ≤2.0 (Tsirelson 2.8284) | ≥2.2 | 17.8215 | VALID_ABOVE |
| Temporal (Leggett-Garg) | K3 | 1.502 | ≤1.0 (qmax 1.5) | ≥1.1 | 12.9616 | VALID_ABOVE |
| Contextual (Peres-Mermin) | χ_min | 5.126 | ≤4.0 (q 6.0) | ≥4.5 | 20.5579 | VALID_ABOVE |

### Contextuality per-state (state-independence = True)
- χ(|000⟩) = 5.144
- χ(|+++⟩) = 5.282
- χ(GHZ)  = 5.126

## Chain & provenance
- Previous WITNESS record hash: `30e5a0f3cbf1f2351347c9096cc88e6f5fdc85139cbfe647e1a2ad1d7ec49257`
- NIST beacon pulse: `1865678` @ 2026-07-19T01:58:00.000Z
- LIGO GW150914 anchor: `66c4b196`
- Manifest (prereg): `38f7b3c1429ec7e87103937cb32750e581667cf4c28c1dcfaea58d833e13f8c2`
- Manifest (harness): `b95c2672b999547f2eeefc9019082e3e25cfee6730ee390c744259dae7c91d7a`

## Cryptographic binding
- OMNI nonce: `f6fa824cca3fb05b2ef64684dac2c46ae8c5f41176820a80fa574a4492417042`
- Record hash: `fcc409ddcee8774586c3437c52ca3925cde25b4afa2562f3836a922644dd7def`

## Verdict logic (preregistered)
- **ALLOW** — all three VALID_ABOVE, reconstructs, provenance valid
- **HOLD** — any INCONCLUSIVE, none INVALID
- **DENY** — tampering / reconstruction mismatch / invalid provenance (or a witness INVALID below classical bound)
- **GATE-STOP** — hardware/data conditions prevent valid evaluation
- Precedence: DENY > GATE-STOP > HOLD > ALLOW

## Scope & honesty
Results apply within the tested circuit model, backend, qubits, calibration, shot counts,
software harnesses, and stated experimental conditions. This is an experimental evidence
record, not a universal security proof or production certification. Device-dependent;
Bell locality + detection loopholes open; Leggett-Garg relies on the NIM assumption
(clumsiness loophole open); contextuality compatibility loophole open. Statistical σ reflects
binomial shot noise only.
