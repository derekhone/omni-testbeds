# OMNI-1 Hardware Execution — Token Rotation Required

## Current Status: GATE-STOP (Simulator Validation PASS)

The OMNI-1 experiment was executed with the following outcome:

### What Happened
1. ✅ **Preregistration locked** — MANIFEST.sha256 verified, all hashes match
2. ✅ **Hardware execution attempted** — tried to run on `ibm_kingston` (Heron r2, 156q)
3. ❌ **IBM Quantum API error** — "Unable to retrieve instances. Please check that you are using a valid API token."
4. ✅ **Simulator validation executed** — all three witnesses PASS (S=2.788, K3=1.477, χ=6.0)
5. ✅ **Verdict recorded** — per preregistered logic: hardware/data conditions prevent evaluation → **GATE-STOP**

### Simulator Validation Results (Proof of Concept)
| Witness | Measured | Classical Bound | Threshold | σ | Verdict |
|---------|----------|-----------------|-----------|---|---------|
| Bell-CHSH (S) | 2.788 | ≤2.0 | ≥2.2 | 17.6 | VALID_ABOVE |
| Leggett-Garg (K3) | 1.477 | ≤1.0 | ≥1.1 | 12.3 | VALID_ABOVE |
| Peres-Mermin (χ) | 6.0 | ≤4.0 | ≥4.5 | 36.5 | VALID_ABOVE |

**All three arms passed on ideal simulator** — this confirms the circuits, witness computation, and cryptographic binding are correct.

### Why GATE-STOP (not ALLOW)
Per the preregistered verdict logic in `OMNI-1-preregistration.md`:
- **ALLOW** requires all three witnesses VALID_ABOVE *on hardware*
- **GATE-STOP** = "hardware/data conditions prevent valid evaluation"

Since the IBM Quantum API rejected the stored token, the hardware run never executed. The simulator validation is a *proof of concept* only — it demonstrates the design is sound, but it's not the hardware evidence the experiment was designed to produce.

### How to Complete Hardware Execution

**Step 1: Rotate IBM Quantum Token**
1. Go to https://quantum.ibm.com/account
2. Log in with your IBM Quantum account
3. Generate a new API token (revoke old one if possible)
4. Copy the new token

**Step 2: Re-execute on Hardware**
```bash
cd /home/ubuntu/omni-testbeds
export IBM_QUANTUM_TOKEN="your-new-token-here"
python3 omni1_harness.py --authorize-hardware --allow-unrotated
```

**Step 3: Verify and Commit**
```bash
python3 omni1_verify.py
git add results/
git commit -m "OMNI-1 hardware execution complete: [ALLOW|HOLD|DENY] on ibm_kingston"
```

### Current Git History
```
9907221 - OMNI-1 execution: GATE-STOP (IBM token invalid, simulator validation PASS)
bf859ff - OMNI-1 simulator validation: ALLOW (S=2.844, K3=1.504, chi=6.000 state-independent)
fc89433 - OMNI-1 preregistration lock: Threefold Witness prereg + harness + verifier + MANIFEST
```

### Next Decision Point
**Option A: Publish GATE-STOP as-is**
- Demonstrates preregistration discipline and honest reporting
- Shows simulator validation confirms design soundness
- Documents the token-rotation obstacle
- Can be followed up with a hardware re-run later

**Option B: Rotate token and re-run before publishing**
- Replace current results/ with hardware execution
- Amend the last commit with hardware data
- Push single clean hardware result to GitHub + Zenodo

**Option C: Publish GATE-STOP now, hardware re-run as OMNI-1-HARDWARE**
- Keep current GATE-STOP record as honest documentation
- Create new experiment ID for hardware completion
- Two separate DOIs: one for design validation, one for hardware

---

**Derek, which path do you want to take?**
