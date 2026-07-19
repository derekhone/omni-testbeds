# OMNI-1 — STATUS

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**
**As of:** simulator validation complete; hardware run withheld.

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

## GATED — NOT yet done (blocked by preregistration §8)

- [ ] **IBM Quantum hardware run** — **withheld**. Per user directive and preregistration §8,
      the hardware run is not authorized until:
  1. **Secrets are rotated.** The IBM Quantum API token and the Zenodo token were exposed in
     the working environment / prior context and MUST be rotated before any authenticated
     hardware submission. The harness will refuse to submit unless `--authorize-hardware` AND
     `--allow-unrotated` are both passed (the latter only after rotation).
  2. **Scientific + IP-integrity review** of the design is complete.
- [ ] **Zenodo publication** of the hardware ProofRecord (after a valid hardware run).
- [ ] **GitHub push** to a Remnant Fieldworks / derekhone repository.

## How to run the hardware step (only after the two gate conditions are met)

```bash
# 1. Rotate IBM Quantum + Zenodo tokens; export the NEW IBM token:
export IBM_QUANTUM_TOKEN="<rotated-token>"

# 2. Confirm the manifest still matches (no post-hoc edits):
sha256sum -c <(grep -v '^#' MANIFEST.sha256)

# 3. Execute on hardware (Batch mode, ibm_kingston preferred):
python omni1_harness.py --authorize-hardware --allow-unrotated --backend ibm_kingston --shots 2000

# 4. Independently verify the released record:
python omni1_verify.py results/OMNI-1-proofrecord.json
```

Estimated QPU time for the full 70,000-shot batch is ~40–80 s. If it exceeds the remaining
budget, the preregistered fallback (Arm C → 2 states, 1500 shots/context) applies; invoke by
editing `PM_STATES`/`--shots` per the preregistration (fallback is declared, not post-hoc).

## Security note

The tokens observed in this environment (`/home/ubuntu/.config/abacusai_auth_secrets.json`)
should be treated as **compromised** and rotated at the provider before OMNI-1 hardware
execution or any further authenticated use. No tokens are hard-coded in any committed file.
