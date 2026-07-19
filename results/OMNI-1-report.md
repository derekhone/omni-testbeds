# OMNI-1 Report — The Threefold Witness

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**

- Experiment: **OMNI-1**  ·  Schema: `omni-proofrecord-1.0`
- Mode: **SIMULATOR**  ·  Backend: `aer_simulator_ideal`  ·  Job: `n/a (simulator)`
- Generated: 2026-07-19T01:58:53.817804+00:00

> **Public claim:** A preregistered demonstration of three independently evaluated
> nonclassicality witnesses bound into one chain-linked, independently reconstructable
> execution record.

## Aggregate ExecutionProof verdict: **GATE-STOP**

`omni_certified = False`

| Witness | Statistic | Value | Bound | Threshold | nσ | Verdict |
|---|---|---|---|---|---|---|
| Spatial (Bell-CHSH) | S | 2.788 | ≤2.0 (Tsirelson 2.8284) | ≥2.2 | 17.6202 | VALID_ABOVE |
| Temporal (Leggett-Garg) | K3 | 1.477 | ≤1.0 (qmax 1.5) | ≥1.1 | 12.3161 | VALID_ABOVE |
| Contextual (Peres-Mermin) | χ_min | 6.0 | ≤4.0 (q 6.0) | ≥4.5 | 36.5148 | VALID_ABOVE |

### Contextuality per-state (state-independence = True)
- χ(|000⟩) = 6.0
- χ(|+++⟩) = 6.0
- χ(GHZ)  = 6.0

## Chain & provenance
- Previous WITNESS record hash: `30e5a0f3cbf1f2351347c9096cc88e6f5fdc85139cbfe647e1a2ad1d7ec49257`
- NIST beacon pulse: `1865675` @ 2026-07-19T01:55:00.000Z
- LIGO GW150914 anchor: `66c4b196`
- Manifest (prereg): `38f7b3c1429ec7e87103937cb32750e581667cf4c28c1dcfaea58d833e13f8c2`
- Manifest (harness): `b95c2672b999547f2eeefc9019082e3e25cfee6730ee390c744259dae7c91d7a`

## Cryptographic binding
- OMNI nonce: `72e982f6f7a8f53d36605b569c0b44b7dbd8a9fd12019630c1d1450c2426e58b`
- Record hash: `0746d29773df066076a77c5dc5b0e019e6243b6939ce47570a82f361d06ac119`

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
