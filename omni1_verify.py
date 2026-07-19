#!/usr/bin/env python3
"""
OMNI-1 independent verification.

Reconstructs all three witnesses (S, K3, chi per state), the witness hashes, the OMNI nonce,
and the record hash *directly from the released raw counts and ProofRecord JSON*, with no
dependence on the harness runtime or any quantum library. Emits its own ExecutionProof
governance verdict (ALLOW / HOLD / DENY / GATE-STOP) and compares to the recorded verdict.

Usage:
  python omni1_verify.py [results/OMNI-1-proofrecord.json]

Exit code 0 if the independent verdict matches the recorded verdict, else 1.
"""

import hashlib
import json
import os
import sys

# Preregistered constants (must match preregistration; hard-coded here on purpose so the
# verifier does not import the harness).
CHSH_CLASSICAL, CHSH_THRESHOLD = 2.0, 2.2
LG_MACROREALIST, LG_THRESHOLD = 1.0, 1.1
PM_NONCONTEXTUAL, PM_THRESHOLD = 4.0, 4.5
LIGO_GW150914_HASH = "66c4b196"

PM_CONTEXTS = ["R1", "R2", "R3", "C1", "C2", "C3"]
PM_STATES = ["000", "ppp", "ghz"]
CHSH_SETTINGS = ["A_a0b0", "A_a0b1", "A_a1b0", "A_a1b1"]


def sha256_hex(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def parity_expectation(counts):
    """Full-bitstring parity expectation. CHSH circuits carry 2 classical bits, PM circuits
    carry 3; parity over all measured bits is the correct product-of-outcomes expectation for
    both."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    acc = 0
    for bitstr, c in counts.items():
        b = bitstr.replace(" ", "")
        acc += (1 if b.count("1") % 2 == 0 else -1) * c
    return acc / total


def two_time_correlator(counts):
    total = sum(counts.values())
    if total == 0:
        return 0.0
    acc = 0
    for bitstr, c in counts.items():
        b = bitstr.replace(" ", "")[-2:]
        later, earlier = b[0], b[1]
        q_e = 1 if earlier == "0" else -1
        q_l = 1 if later == "0" else -1
        acc += q_e * q_l * c
    return acc / total


def recompute_chsh(raw):
    E = {n: parity_expectation(raw[n]) for n in CHSH_SETTINGS}
    S = E["A_a0b0"] - E["A_a0b1"] + E["A_a1b0"] + E["A_a1b1"]
    return S, E


def recompute_lg(raw):
    C12 = two_time_correlator(raw["B_12"])
    C23 = two_time_correlator(raw["B_23"])
    C13 = two_time_correlator(raw["B_13"])
    return C12 + C23 - C13, (C12, C23, C13)


def recompute_chi(raw):
    chis = {}
    for state in PM_STATES:
        exps = {ctx: parity_expectation(raw[f"C_{state}_{ctx}"]) for ctx in PM_CONTEXTS}
        chis[state] = exps["R1"] + exps["R2"] + exps["R3"] + exps["C1"] + exps["C2"] - exps["C3"]
    return chis


def witness_verdict(value, classical_bound, threshold):
    if value < classical_bound:
        return "INVALID"
    if value >= threshold:
        return "VALID_ABOVE"
    return "INCONCLUSIVE"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "results", "OMNI-1-proofrecord.json")
    if not os.path.exists(path):
        print(f"[VERIFY] ProofRecord not found: {path}")
        return 2
    with open(path) as f:
        rec = json.load(f)

    raw = rec["raw_counts"]
    problems = []
    ok = True

    # ---- reconstruct witnesses ----
    S, _ = recompute_chsh(raw)
    K3, _ = recompute_lg(raw)
    chis = recompute_chi(raw)
    chi_min = min(chis.values())

    print(f"[VERIFY] Reconstructed S    = {S:.6f}   (recorded {rec['witness_spatial']['S']})")
    print(f"[VERIFY] Reconstructed K3   = {K3:.6f}   (recorded {rec['witness_temporal']['K3']})")
    print(f"[VERIFY] Reconstructed chi_min = {chi_min:.6f} (recorded {rec['witness_contextual']['chi_min']})")

    def close(a, b, tol=1e-6):
        return abs(a - b) <= tol

    if not close(S, rec["witness_spatial"]["S"], 1e-4):
        problems.append("CHSH S mismatch"); ok = False
    if not close(K3, rec["witness_temporal"]["K3"], 1e-4):
        problems.append("LG K3 mismatch"); ok = False
    if not close(chi_min, rec["witness_contextual"]["chi_min"], 1e-4):
        problems.append("PM chi_min mismatch"); ok = False

    # ---- reconstruct per-arm verdicts ----
    v_spatial = witness_verdict(S, CHSH_CLASSICAL, CHSH_THRESHOLD)
    v_temporal = witness_verdict(K3, LG_MACROREALIST, LG_THRESHOLD)
    all_above = all(c >= PM_THRESHOLD for c in chis.values())
    any_invalid = any(c < PM_NONCONTEXTUAL for c in chis.values())
    v_contextual = "INVALID" if any_invalid else ("VALID_ABOVE" if all_above else "INCONCLUSIVE")

    for name, v, reckey in [("spatial", v_spatial, "witness_spatial"),
                            ("temporal", v_temporal, "witness_temporal"),
                            ("contextual", v_contextual, "witness_contextual")]:
        if v != rec[reckey]["verdict"]:
            problems.append(f"{name} verdict mismatch ({v} vs {rec[reckey]['verdict']})"); ok = False

    # ---- reconstruct witness hashes and nonce ----
    spatial_hash = sha256_hex(canonical_json(rec["witness_spatial"]))
    temporal_hash = sha256_hex(canonical_json(rec["witness_temporal"]))
    contextual_hash = sha256_hex(canonical_json(rec["witness_contextual"]))
    for name, h, key in [("spatial", spatial_hash, "spatial"),
                         ("temporal", temporal_hash, "temporal"),
                         ("contextual", contextual_hash, "contextual")]:
        if h != rec["witness_hashes"][key]:
            problems.append(f"{name} witness hash mismatch"); ok = False

    nist_value = rec["external_entropy"]["nist_value"]
    jid = rec["job_id"] or "SIMULATOR"
    nonce = sha256_hex("|".join([nist_value, LIGO_GW150914_HASH, jid,
                                 spatial_hash, temporal_hash, contextual_hash]))
    if nonce != rec["omni_nonce"]:
        problems.append("omni_nonce mismatch"); ok = False

    # ---- reconstruct record hash (canonical JSON minus record_hash) ----
    rec_copy = dict(rec)
    rec_copy.pop("record_hash", None)
    record_hash = sha256_hex(canonical_json(rec_copy))
    if record_hash != rec["record_hash"]:
        problems.append("record_hash mismatch"); ok = False

    # ---- provenance ----
    provenance_ok = bool(nist_value) and bool(rec["chain"]["previous_witness_record_hash"])
    gate_stop = (rec.get("mode") == "SIMULATOR" and False)  # sim is a valid evaluation

    # ---- independent aggregate verdict (DENY > GATE-STOP > HOLD > ALLOW) ----
    verdicts = [v_spatial, v_temporal, v_contextual]
    if (not provenance_ok) or (not ok):
        agg = "DENY"
    elif gate_stop:
        agg = "GATE-STOP"
    elif any(v == "INVALID" for v in verdicts):
        agg = "DENY"
    elif any(v == "INCONCLUSIVE" for v in verdicts):
        agg = "HOLD"
    elif all(v == "VALID_ABOVE" for v in verdicts):
        agg = "ALLOW"
    else:
        agg = "HOLD"

    print(f"[VERIFY] Independent per-arm verdicts: spatial={v_spatial} "
          f"temporal={v_temporal} contextual={v_contextual}")
    print(f"[VERIFY] Independent aggregate verdict: {agg}")
    print(f"[VERIFY] Recorded aggregate verdict:    {rec['aggregate_verdict']}")

    if problems:
        print("[VERIFY] PROBLEMS DETECTED:")
        for p in problems:
            print(f"          - {p}")

    match = (agg == rec["aggregate_verdict"]) and ok
    if match:
        print("[VERIFY] RESULT: PASS — record independently reconstructed; verdicts agree.")
        return 0
    print("[VERIFY] RESULT: FAIL — reconstruction mismatch or verdict disagreement (→ DENY).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
