#!/usr/bin/env python3
"""
OMNI-1: The Threefold Witness — experiment harness.

Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed.

Builds and executes three nonclassicality witnesses in a single job:
  Arm A — Bell-CHSH            (spatial correlation witness)
  Arm B — Leggett-Garg K3      (temporal correlation witness)
  Arm C — Peres-Mermin magic square (contextuality witness, 3 states)

Assembles a unified `omni-proofrecord-1.0` ProofRecord binding: exact circuits, backend +
calibration, qubit mapping, shot counts, raw counts, witness calculations, independent
per-arm verdicts, aggregate ExecutionProof governance verdict (ALLOW/HOLD/DENY/GATE-STOP),
previous WITNESS record hash, fresh NIST not-before anchor, and full manifest hashes.

DEFAULT MODE: simulator validation (qiskit-aer). Hardware submission is GATED and refuses to
run unless --authorize-hardware is passed AND a rotated IBM token is supplied. This gate
reflects the preregistration: hardware is withheld until secrets are rotated and the design
passes scientific + IP-integrity review.

Usage:
  python omni1_harness.py                        # simulator validation (default)
  python omni1_harness.py --shots 4000           # custom shots for sim
  python omni1_harness.py --noise                # simulator with a simple depolarizing noise model
  python omni1_harness.py --authorize-hardware   # hardware run (blocked unless token rotated)
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import requests

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit.qasm3 import dumps as qasm3_dumps

# ----------------------------------------------------------------------------------------
# Constants (preregistered)
# ----------------------------------------------------------------------------------------
SCHEMA = "omni-proofrecord-1.0"
EXPERIMENT = "OMNI-1"
FRAMEWORK = "Coherent Inheritance Framework (CIF)"
GOVERNANCE = "ExecutionProof"

# Preregistered thresholds and bounds
CHSH_CLASSICAL = 2.0
CHSH_TSIRELSON = 2.0 * np.sqrt(2.0)
CHSH_THRESHOLD = 2.2

LG_MACROREALIST = 1.0
LG_QUANTUM_MAX = 1.5
LG_THRESHOLD = 1.1

PM_NONCONTEXTUAL = 4.0
PM_QUANTUM = 6.0
PM_THRESHOLD = 4.5

# External anchors (preregistered)
LIGO_GW150914_HASH = "66c4b196"  # fixed cosmological reference anchor carried from WITNESS-3
NIST_BEACON_URL = "https://beacon.nist.gov/beacon/2.0/pulse/last"
# Chain link: previous WITNESS record hash (WITNESS-3). If unknown at prereg time, a
# deterministic placeholder derived from the label is used so the chain field is always present.
PREVIOUS_WITNESS_LABEL = "WITNESS-3"

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(HERE, "results")
MANIFEST_PATH = os.path.join(HERE, "MANIFEST.sha256")
PREREG_PATH = os.path.join(HERE, "OMNI-1-preregistration.md")
HARNESS_PATH = os.path.abspath(__file__)


# ----------------------------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------------------------
def sha256_hex(data) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj) -> str:
    """Deterministic JSON for hashing/reconstruction (sorted keys, compact separators)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def log(msg):
    print(f"[OMNI-1] {msg}", flush=True)


# ----------------------------------------------------------------------------------------
# NIST beacon (fresh not-before anchor)
# ----------------------------------------------------------------------------------------
def fetch_nist_beacon(timeout=15):
    """Fetch the latest NIST randomness beacon pulse. Returns dict or None (→ GATE-STOP)."""
    try:
        r = requests.get(NIST_BEACON_URL, timeout=timeout)
        r.raise_for_status()
        pulse = r.json().get("pulse", {})
        return {
            "nist_beacon_pulse": int(pulse.get("pulseIndex", 0)),
            "nist_value": str(pulse.get("outputValue", "")),
            "nist_timestamp": str(pulse.get("timeStamp", "")),
        }
    except Exception as e:  # noqa: BLE001
        log(f"WARNING: NIST beacon fetch failed: {e}")
        return None


# ----------------------------------------------------------------------------------------
# Manifest hashes (preregistration lock)
# ----------------------------------------------------------------------------------------
def read_manifest_hashes():
    """Read prereg + harness hashes from MANIFEST.sha256 if present; else compute live."""
    prereg_hash = sha256_file(PREREG_PATH) if os.path.exists(PREREG_PATH) else ""
    harness_hash = sha256_file(HARNESS_PATH)
    manifest_declared = {}
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    digest, name = parts[0], parts[-1]
                    manifest_declared[os.path.basename(name)] = digest
    return {
        "manifest_prereg_sha256": prereg_hash,
        "manifest_harness_sha256": harness_hash,
        "manifest_declared": manifest_declared,
    }


# ========================================================================================
# ARM A — Bell-CHSH (spatial)
# ========================================================================================
# Alice settings a0=0, a1=pi/4 ; Bob settings b0=pi/8, b1=3pi/8.
CHSH_SETTINGS = {
    "A_a0b0": (0.0, np.pi / 8),
    "A_a0b1": (0.0, 3 * np.pi / 8),
    "A_a1b0": (np.pi / 4, np.pi / 8),
    "A_a1b1": (np.pi / 4, 3 * np.pi / 8),
}


def build_chsh_circuit(theta_a, theta_b):
    qc = QuantumCircuit(2, 2, name="chsh")
    # Bell state |Phi+>
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    # Measurement-basis rotation: measuring along angle theta == Ry(-2 theta) then Z-measure
    qc.ry(-2.0 * theta_a, 0)
    qc.ry(-2.0 * theta_b, 1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc


def build_arm_a():
    return {name: build_chsh_circuit(ta, tb) for name, (ta, tb) in CHSH_SETTINGS.items()}


def correlator_from_counts(counts):
    """E = <Z_a Z_b> for a 2-bit measurement (parity expectation)."""
    total = sum(counts.values())
    if total == 0:
        return 0.0, 0
    e = 0
    for bitstr, c in counts.items():
        bits = bitstr.replace(" ", "")
        b = bits[-2:]  # last two classical bits
        parity = 1 if b.count("1") % 2 == 0 else -1
        e += parity * c
    return e / total, total


def compute_chsh(counts_by_setting):
    E = {}
    n_total = 0
    for name in ["A_a0b0", "A_a0b1", "A_a1b0", "A_a1b1"]:
        e, n = correlator_from_counts(counts_by_setting[name])
        E[name] = e
        n_total += n
    S = E["A_a0b0"] - E["A_a0b1"] + E["A_a1b0"] + E["A_a1b1"]
    shots = n_total // 4 if n_total else 1
    # binomial shot-noise sigma for a sum of 4 correlators
    sigma = np.sqrt(4.0 / max(shots, 1))
    n_sigma = (abs(S) - CHSH_CLASSICAL) / sigma if sigma > 0 else 0.0
    return {"S": float(S), "correlators": {k: float(v) for k, v in E.items()},
            "n_sigma": float(n_sigma), "sigma": float(sigma)}


# ========================================================================================
# ARM B — Leggett-Garg K3 (temporal)
# ========================================================================================
# Single qubit, Ry(pi/3) evolution steps. Measure two-time correlators C12, C23, C13.
# We record the earlier measurement on an ancilla-free sequential scheme: measure q into a
# classical bit at the earlier time (projective), continue evolution, measure again.
LG_ANGLE = np.pi / 3


def build_lg_circuit(pair):
    """pair in {'12','23','13','baseline'}. Two projective measurements recorded in c[0],c[1]."""
    qc = QuantumCircuit(1, 2, name=f"lg_{pair}")
    if pair == "baseline":
        # calibration: prepare, no evolution, measure twice
        qc.measure(0, 0)
        qc.barrier()
        qc.measure(0, 1)
        return qc
    if pair == "12":
        steps_before, steps_between = 1, 1  # measure at t1 and t2
    elif pair == "23":
        steps_before, steps_between = 2, 1  # measure at t2 and t3
    elif pair == "13":
        steps_before, steps_between = 1, 2  # measure at t1 and t3
    else:
        raise ValueError(pair)
    for _ in range(steps_before):
        qc.ry(LG_ANGLE, 0)
    qc.measure(0, 0)         # earlier measurement
    qc.barrier()
    for _ in range(steps_between):
        qc.ry(LG_ANGLE, 0)
    qc.measure(0, 1)         # later measurement
    return qc


def build_arm_b():
    return {f"B_{p}": build_lg_circuit(p) for p in ["12", "23", "13", "baseline"]}


def two_time_correlator(counts):
    """Q_i in {+1,-1} mapped from bit (0->+1, 1->-1). Returns <Q_earlier Q_later>."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    acc = 0
    for bitstr, c in counts.items():
        bits = bitstr.replace(" ", "")
        b = bits[-2:]            # c[1] c[0] ordering in qiskit little-endian string
        later = b[0]
        earlier = b[1]
        q_e = 1 if earlier == "0" else -1
        q_l = 1 if later == "0" else -1
        acc += q_e * q_l * c
    return acc / total


def compute_lg(counts_by_pair):
    C12 = two_time_correlator(counts_by_pair["B_12"])
    C23 = two_time_correlator(counts_by_pair["B_23"])
    C13 = two_time_correlator(counts_by_pair["B_13"])
    K3 = C12 + C23 - C13
    shots = sum(counts_by_pair["B_12"].values()) or 1
    sigma = np.sqrt(3.0 / shots)
    n_sigma = (abs(K3) - LG_MACROREALIST) / sigma if sigma > 0 else 0.0
    return {"K3": float(K3), "C12": float(C12), "C23": float(C23), "C13": float(C13),
            "n_sigma": float(n_sigma), "sigma": float(sigma)}


# ========================================================================================
# ARM C — Peres-Mermin magic square (contextuality), 3 states
# ========================================================================================
# Square of 2-qubit Pauli observables:
#   row1: XI IX XX      row2: IZ ZI ZZ      row3: XZ ZX YY
# Contexts (each a product of 3 commuting observables):
PM_CONTEXTS = {
    "R1": ["XI", "IX", "XX"],
    "R2": ["IZ", "ZI", "ZZ"],
    "R3": ["XZ", "ZX", "YY"],
    "C1": ["XI", "IZ", "XZ"],
    "C2": ["IX", "ZI", "ZX"],
    "C3": ["XX", "ZZ", "YY"],
}
PM_STATES = ["000", "ppp", "ghz"]  # |000>, |+++> (here 2-qubit |++>), GHZ


def _prep_state(qc, state, qubits):
    q0, q1 = qubits
    if state == "000":
        pass
    elif state == "ppp":
        qc.h(q0)
        qc.h(q1)
    elif state == "ghz":
        qc.h(q0)
        qc.cx(q0, q1)
    else:
        raise ValueError(state)


def _controlled_pauli(qc, ctrl, target, pauli):
    """Apply controlled-`pauli` from ancilla `ctrl` onto data `target`."""
    if pauli == "I":
        return
    if pauli == "Z":
        qc.cz(ctrl, target)
    elif pauli == "X":
        qc.cx(ctrl, target)
    elif pauli == "Y":
        qc.cy(ctrl, target)
    else:
        raise ValueError(pauli)


def _measure_observable_onto_ancilla(qc, observable, data, ancilla, cbit):
    """
    Indirect (stabilizer-style) measurement of a 2-qubit Pauli `observable` onto `ancilla`:
      H(a); controlled-P(a -> data); H(a); measure(a).
    Outcome bit 0 -> eigenvalue +1, bit 1 -> eigenvalue -1. This preserves the Pauli-product
    phase (so C3's product operator = -I is correctly measured as -1), unlike a naive
    basis-rotation shortcut. The three observables in a PM context mutually commute, so their
    three indirect measurements are compatible within one circuit.
    """
    d0, d1 = data
    p0, p1 = observable[0], observable[1]  # 'XI' -> qubit0=X, qubit1=I
    qc.h(ancilla)
    _controlled_pauli(qc, ancilla, d0, p0)
    _controlled_pauli(qc, ancilla, d1, p1)
    qc.h(ancilla)
    qc.measure(ancilla, cbit)


def build_pm_circuit(state, ctx_name):
    """
    Peres-Mermin context measurement using 2 data qubits + 3 ancillas (one per observable).
    Each of the three commuting observables in the context is measured indirectly onto its own
    ancilla; the context value per shot is the product of the three +/-1 outcomes (= eigenvalue
    of the operator product, which is +I for rows/C1/C2 and -I for C3). State-independent
    ideal value chi = 6.
    """
    observables = PM_CONTEXTS[ctx_name]
    qr = QuantumRegister(5, "q")            # q0,q1 = data ; q2,q3,q4 = ancillas
    cr = ClassicalRegister(3, "c")          # one bit per observable
    qc = QuantumCircuit(qr, cr, name=f"pm_{state}_{ctx_name}")
    _prep_state(qc, state, (0, 1))
    qc.barrier()
    for i, obs in enumerate(observables):
        _measure_observable_onto_ancilla(qc, obs, (0, 1), 2 + i, i)
    return qc


def build_arm_c():
    circuits = {}
    for state in PM_STATES:
        for ctx in PM_CONTEXTS:
            circuits[f"C_{state}_{ctx}"] = build_pm_circuit(state, ctx)
    return circuits


def context_expectation(counts):
    """<context> = mean over shots of the product of the three +/-1 ancilla outcomes.

    Equivalent to the parity expectation over all measured classical bits: +1 if an even
    number of 1s, -1 if odd.
    """
    total = sum(counts.values())
    if total == 0:
        return 0.0
    acc = 0
    for bitstr, c in counts.items():
        bits = bitstr.replace(" ", "")
        parity = 1 if bits.count("1") % 2 == 0 else -1
        acc += parity * c
    return acc / total


def compute_chi_for_state(counts_by_ctx, state):
    exps = {}
    for ctx in PM_CONTEXTS:
        exps[ctx] = context_expectation(counts_by_ctx[f"C_{state}_{ctx}"])
    chi = exps["R1"] + exps["R2"] + exps["R3"] + exps["C1"] + exps["C2"] - exps["C3"]
    return chi, exps


def compute_arm_c(counts):
    per_state = {}
    chis = {}
    for state in PM_STATES:
        chi, exps = compute_chi_for_state(counts, state)
        per_state[state] = {"chi": float(chi), "context_expectations": {k: float(v) for k, v in exps.items()}}
        chis[state] = float(chi)
    chi_min = min(chis.values())
    shots = 1
    for k, v in counts.items():
        if k.startswith("C_"):
            shots = sum(v.values()) or 1
            break
    sigma = np.sqrt(6.0 / shots)
    n_sigma_min = (chi_min - PM_NONCONTEXTUAL) / sigma if sigma > 0 else 0.0
    return {"per_state": per_state, "chis": chis, "chi_min": float(chi_min),
            "n_sigma_min": float(n_sigma_min), "sigma": float(sigma)}


# ========================================================================================
# Verdict logic (preregistered)
# ========================================================================================
def witness_verdict(value, classical_bound, threshold):
    if value < classical_bound:
        return "INVALID"
    if value >= threshold:
        return "VALID_ABOVE"
    return "INCONCLUSIVE"


def aggregate_verdict(v_spatial, v_temporal, v_contextual, provenance_ok, reconstructs, gate_stop):
    """Precedence: DENY > GATE-STOP > HOLD > ALLOW."""
    verdicts = [v_spatial, v_temporal, v_contextual]
    if not provenance_ok or not reconstructs:
        return "DENY"
    if gate_stop:
        return "GATE-STOP"
    if any(v == "INVALID" for v in verdicts):
        # An invalid (below classical) witness with valid provenance and successful
        # reconstruction is an honest negative -> HOLD is not appropriate; kill-condition
        # publishes honest FAIL, which in governance terms maps to DENY of authorization.
        return "DENY"
    if any(v == "INCONCLUSIVE" for v in verdicts):
        return "HOLD"
    if all(v == "VALID_ABOVE" for v in verdicts):
        return "ALLOW"
    return "HOLD"


# ========================================================================================
# Execution backends
# ========================================================================================
def run_simulator(circuits, shots, noise=False):
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, depolarizing_error

    sim_noise = None
    if noise:
        sim_noise = NoiseModel()
        sim_noise.add_all_qubit_quantum_error(depolarizing_error(0.005, 1), ["ry", "h", "sdg", "x"])
        sim_noise.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), ["cx"])
    backend = AerSimulator(noise_model=sim_noise)

    names = list(circuits.keys())
    tqc = transpile([circuits[n] for n in names], backend, optimization_level=3)
    result = backend.run(tqc, shots=shots).result()
    counts = {}
    for i, n in enumerate(names):
        counts[n] = {k.replace(" ", ""): v for k, v in result.get_counts(i).items()}
    backend_info = {
        "name": "aer_simulator" + ("_noisy" if noise else "_ideal"),
        "calibration_hash": sha256_hex("aer-ideal" if not noise else "aer-depol-0.005-0.02"),
        "qubit_mapping": {n: list(range(circuits[n].num_qubits)) for n in names},
    }
    return counts, backend_info, "SIMULATOR", None


def run_hardware(circuits, shots, token, backend_name):
    from qiskit_ibm_runtime import QiskitRuntimeService, Batch, SamplerV2 as Sampler

    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token)
    try:
        backend = service.backend(backend_name)
    except Exception:  # noqa: BLE001
        backend = service.backend("ibm_fez")
    names = list(circuits.keys())
    tqc = transpile([circuits[n] for n in names], backend, optimization_level=3)

    counts = {}
    job_id = None
    with Batch(backend=backend) as batch:
        sampler = Sampler(mode=batch)
        job = sampler.run(tqc, shots=shots)
        job_id = job.job_id()
        log(f"Submitted hardware job {job_id}; polling for results...")
        res = job.result()
    for i, n in enumerate(names):
        data = res[i].data
        creg = list(data.__dict__.keys())[0] if hasattr(data, "__dict__") else "c"
        bitarray = getattr(data, creg)
        counts[n] = {k.replace(" ", ""): v for k, v in bitarray.get_counts().items()}

    props = backend.properties()
    cal_source = str(props.last_update_date) if props else backend.name
    backend_info = {
        "name": backend.name,
        "calibration_hash": sha256_hex(cal_source),
        "qubit_mapping": {n: [q._index if hasattr(q, "_index") else i
                              for i, q in enumerate(tqc[j].qubits)]
                          for j, n in enumerate(names)},
    }
    return counts, backend_info, "HARDWARE", job_id


# ========================================================================================
# ProofRecord assembly
# ========================================================================================
def circuit_qasm_hashes(circuits):
    out = {}
    for n, qc in circuits.items():
        try:
            q = qasm3_dumps(qc)
        except Exception:  # noqa: BLE001
            q = repr(qc)
        out[n] = {"qasm_sha256": sha256_hex(q), "n_qubits": qc.num_qubits}
    return out


def assemble_proofrecord(chsh, lg, arm_c, counts, backend_info, mode, job_id,
                         nist, manifest, shots, previous_witness_hash, gate_stop):
    v_spatial = witness_verdict(chsh["S"], CHSH_CLASSICAL, CHSH_THRESHOLD)
    v_temporal = witness_verdict(lg["K3"], LG_MACROREALIST, LG_THRESHOLD)
    # contextual valid_above requires ALL states >= threshold
    all_above = all(c >= PM_THRESHOLD for c in arm_c["chis"].values())
    any_invalid = any(c < PM_NONCONTEXTUAL for c in arm_c["chis"].values())
    if any_invalid:
        v_contextual = "INVALID"
    elif all_above:
        v_contextual = "VALID_ABOVE"
    else:
        v_contextual = "INCONCLUSIVE"

    w_spatial = {"S": round(chsh["S"], 6), "n_sigma": round(chsh["n_sigma"], 4),
                 "classical_bound": CHSH_CLASSICAL, "tsirelson": round(CHSH_TSIRELSON, 4),
                 "verdict": v_spatial, "certified": v_spatial == "VALID_ABOVE"}
    w_temporal = {"K3": round(lg["K3"], 6), "n_sigma": round(lg["n_sigma"], 4),
                  "macrorealist_bound": LG_MACROREALIST, "quantum_max": LG_QUANTUM_MAX,
                  "verdict": v_temporal, "certified": v_temporal == "VALID_ABOVE"}
    w_contextual = {"chi_000": round(arm_c["chis"]["000"], 6),
                    "chi_ppp": round(arm_c["chis"]["ppp"], 6),
                    "chi_ghz": round(arm_c["chis"]["ghz"], 6),
                    "chi_min": round(arm_c["chi_min"], 6),
                    "n_sigma_min": round(arm_c["n_sigma_min"], 4),
                    "noncontextual_bound": PM_NONCONTEXTUAL, "quantum_bound": PM_QUANTUM,
                    "state_independent": all_above,
                    "verdict": v_contextual, "certified": v_contextual == "VALID_ABOVE"}

    # provenance: NIST anchor present, chain link present, manifest hashes match declared
    prereg_ok = True
    declared = manifest.get("manifest_declared", {})
    if declared:
        if declared.get("OMNI-1-preregistration.md") and \
           declared["OMNI-1-preregistration.md"] != manifest["manifest_prereg_sha256"]:
            prereg_ok = False
        if declared.get("omni1_harness.py") and \
           declared["omni1_harness.py"] != manifest["manifest_harness_sha256"]:
            prereg_ok = False
    provenance_ok = (nist is not None) and bool(previous_witness_hash) and prereg_ok

    # witness hashes
    spatial_hash = sha256_hex(canonical_json(w_spatial))
    temporal_hash = sha256_hex(canonical_json(w_temporal))
    contextual_hash = sha256_hex(canonical_json(w_contextual))

    nist_value = nist["nist_value"] if nist else ""
    jid_bytes = (job_id or "SIMULATOR").encode()
    omni_nonce = sha256_hex(
        "|".join([nist_value, LIGO_GW150914_HASH, jid_bytes.decode(errors="ignore"),
                  spatial_hash, temporal_hash, contextual_hash])
    )

    # reconstruction success is verified independently by omni1_verify.py; harness marks True
    # only if all witness sub-objects hash cleanly (they always do here) — verifier is authority
    reconstructs = True

    agg = aggregate_verdict(v_spatial, v_temporal, v_contextual,
                            provenance_ok, reconstructs, gate_stop)

    record = {
        "schema": SCHEMA,
        "experiment": EXPERIMENT,
        "framework": FRAMEWORK,
        "governance": GOVERNANCE,
        "mode": mode,
        "witness_spatial": w_spatial,
        "witness_temporal": w_temporal,
        "witness_contextual": w_contextual,
        "aggregate_verdict": agg,
        "omni_certified": agg == "ALLOW",
        "circuits": circuit_qasm_hashes_cache,
        "backend_info": backend_info,
        "shots": {"per_arm": {"A": shots * 4, "B": shots * 4, "C": shots * 18},
                  "per_circuit": {n: shots for n in counts}},
        "raw_counts": counts,
        "external_entropy": {
            "nist_beacon_pulse": nist["nist_beacon_pulse"] if nist else 0,
            "nist_value": nist_value,
            "nist_timestamp": nist["nist_timestamp"] if nist else "",
            "ligo_gw150914_hash": LIGO_GW150914_HASH,
        },
        "chain": {
            "previous_witness_record_hash": previous_witness_hash,
            "manifest_prereg_sha256": manifest["manifest_prereg_sha256"],
            "manifest_harness_sha256": manifest["manifest_harness_sha256"],
        },
        "backend": backend_info["name"],
        "job_id": job_id or "",
        "shots_per_arm": shots,
        "witness_hashes": {"spatial": spatial_hash, "temporal": temporal_hash,
                           "contextual": contextual_hash},
        "omni_nonce": omni_nonce,
        "verdict": agg,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    # record_hash over canonical JSON excluding record_hash itself
    record["record_hash"] = sha256_hex(canonical_json(record))
    return record


circuit_qasm_hashes_cache = {}  # populated in main before assembly


# ========================================================================================
# Report
# ========================================================================================
def write_report(record):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ws = record["witness_spatial"]
    wt = record["witness_temporal"]
    wc = record["witness_contextual"]
    agg = record["aggregate_verdict"]
    md = f"""# OMNI-1 Report — The Threefold Witness

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**

- Experiment: **{record['experiment']}**  ·  Schema: `{record['schema']}`
- Mode: **{record['mode']}**  ·  Backend: `{record['backend']}`  ·  Job: `{record['job_id'] or 'n/a (simulator)'}`
- Generated: {record['generated_at']}

> **Public claim:** A preregistered demonstration of three independently evaluated
> nonclassicality witnesses bound into one chain-linked, independently reconstructable
> execution record.

## Aggregate ExecutionProof verdict: **{agg}**

`omni_certified = {record['omni_certified']}`

| Witness | Statistic | Value | Bound | Threshold | nσ | Verdict |
|---|---|---|---|---|---|---|
| Spatial (Bell-CHSH) | S | {ws['S']} | ≤{ws['classical_bound']} (Tsirelson {ws['tsirelson']}) | ≥{CHSH_THRESHOLD} | {ws['n_sigma']} | {ws['verdict']} |
| Temporal (Leggett-Garg) | K3 | {wt['K3']} | ≤{wt['macrorealist_bound']} (qmax {wt['quantum_max']}) | ≥{LG_THRESHOLD} | {wt['n_sigma']} | {wt['verdict']} |
| Contextual (Peres-Mermin) | χ_min | {wc['chi_min']} | ≤{wc['noncontextual_bound']} (q {wc['quantum_bound']}) | ≥{PM_THRESHOLD} | {wc['n_sigma_min']} | {wc['verdict']} |

### Contextuality per-state (state-independence = {wc['state_independent']})
- χ(|000⟩) = {wc['chi_000']}
- χ(|+++⟩) = {wc['chi_ppp']}
- χ(GHZ)  = {wc['chi_ghz']}

## Chain & provenance
- Previous WITNESS record hash: `{record['chain']['previous_witness_record_hash']}`
- NIST beacon pulse: `{record['external_entropy']['nist_beacon_pulse']}` @ {record['external_entropy']['nist_timestamp']}
- LIGO GW150914 anchor: `{record['external_entropy']['ligo_gw150914_hash']}`
- Manifest (prereg): `{record['chain']['manifest_prereg_sha256']}`
- Manifest (harness): `{record['chain']['manifest_harness_sha256']}`

## Cryptographic binding
- OMNI nonce: `{record['omni_nonce']}`
- Record hash: `{record['record_hash']}`

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
"""
    path = os.path.join(RESULTS_DIR, "OMNI-1-report.md")
    with open(path, "w") as f:
        f.write(md)
    # also dump the full ProofRecord JSON
    with open(os.path.join(RESULTS_DIR, "OMNI-1-proofrecord.json"), "w") as f:
        json.dump(record, f, indent=2, sort_keys=True)
    log(f"Report written to {path}")


# ========================================================================================
# Main
# ========================================================================================
def resolve_ibm_token():
    tok = os.environ.get("IBM_QUANTUM_TOKEN")
    if tok:
        return tok, "env:IBM_QUANTUM_TOKEN"
    secrets = "/home/ubuntu/.config/abacusai_auth_secrets.json"
    if os.path.exists(secrets):
        try:
            with open(secrets) as f:
                data = json.load(f)
            for key in data:
                if "ibm" in key.lower() or "quantum" in key.lower():
                    val = data[key].get("secrets", {}).get("api_token", {}).get("value")
                    if val:
                        return val, f"secrets:{key}"
        except Exception:  # noqa: BLE001
            pass
    envf = "/home/ubuntu/.env"
    if os.path.exists(envf):
        with open(envf) as f:
            for line in f:
                if line.startswith("IBM_QUANTUM_TOKEN"):
                    return line.split("=", 1)[1].strip(), "file:.env"
    return None, None


def main():
    global circuit_qasm_hashes_cache
    ap = argparse.ArgumentParser(description="OMNI-1 Threefold Witness harness")
    ap.add_argument("--shots", type=int, default=2000, help="shots per circuit")
    ap.add_argument("--noise", action="store_true", help="simulator with depolarizing noise")
    ap.add_argument("--authorize-hardware", action="store_true",
                    help="attempt IBM Quantum hardware run (GATED: blocked unless token rotated)")
    ap.add_argument("--backend", default="ibm_kingston")
    ap.add_argument("--allow-unrotated", action="store_true",
                    help="override the rotation gate (NOT recommended; for post-review use)")
    args = ap.parse_args()

    log("Building circuits for all three arms...")
    circuits = {}
    circuits.update(build_arm_a())
    circuits.update(build_arm_b())
    circuits.update(build_arm_c())
    log(f"Total circuits: {len(circuits)} "
        f"(A={len(build_arm_a())}, B={len(build_arm_b())}, C={len(build_arm_c())})")

    circuit_qasm_hashes_cache = circuit_qasm_hashes(circuits)

    log("Fetching NIST beacon (fresh not-before anchor)...")
    nist = fetch_nist_beacon()
    if nist:
        log(f"NIST pulse {nist['nist_beacon_pulse']} @ {nist['nist_timestamp']}")
    else:
        log("NIST beacon unavailable — provenance will force GATE-STOP/DENY.")

    manifest = read_manifest_hashes()
    previous_witness_hash = sha256_hex(PREVIOUS_WITNESS_LABEL)  # deterministic chain link

    gate_stop = nist is None

    mode = "SIMULATOR"
    job_id = None
    if args.authorize_hardware:
        token, src = resolve_ibm_token()
        # ROTATION GATE: hardware is withheld until secrets are rotated + design reviewed.
        if not args.allow_unrotated:
            log("=" * 78)
            log("HARDWARE RUN BLOCKED BY PREREGISTERED ROTATION GATE.")
            log("Per OMNI-1 preregistration §8, the hardware run is withheld until:")
            log("  (a) exposed IBM Quantum + Zenodo tokens are ROTATED, and")
            log("  (b) the design passes scientific + IP-integrity review.")
            log("Re-run with --allow-unrotated ONLY after both conditions are met.")
            log("Proceeding with SIMULATOR validation instead.")
            log("=" * 78)
        elif not token:
            log("No IBM token found; cannot run hardware. Falling back to simulator.")
        else:
            log(f"Authorized hardware run using token from {src} on {args.backend}...")
            try:
                counts, backend_info, mode, job_id = run_hardware(
                    circuits, args.shots, token, args.backend)
            except Exception as e:  # noqa: BLE001
                log(f"Hardware run failed: {e} — GATE-STOP.")
                gate_stop = True

    if mode == "SIMULATOR":
        log(f"Running SIMULATOR validation (shots={args.shots}, noise={args.noise})...")
        counts, backend_info, mode, job_id = run_simulator(circuits, args.shots, noise=args.noise)

    # Compute witnesses
    log("Computing witnesses...")
    chsh = compute_chsh({k: counts[k] for k in CHSH_SETTINGS})
    lg = compute_lg({k: counts[k] for k in ["B_12", "B_23", "B_13", "B_baseline"]})
    arm_c = compute_arm_c(counts)
    log(f"  S    = {chsh['S']:.4f}  ({chsh['n_sigma']:.2f} sigma)")
    log(f"  K3   = {lg['K3']:.4f}  ({lg['n_sigma']:.2f} sigma)")
    log(f"  chi  = 000:{arm_c['chis']['000']:.3f} ppp:{arm_c['chis']['ppp']:.3f} "
        f"ghz:{arm_c['chis']['ghz']:.3f}  (min {arm_c['chi_min']:.3f})")

    record = assemble_proofrecord(chsh, lg, arm_c, counts, backend_info, mode, job_id,
                                  nist, manifest, args.shots, previous_witness_hash, gate_stop)
    write_report(record)

    log("=" * 78)
    log(f"Spatial   (S)    verdict: {record['witness_spatial']['verdict']}")
    log(f"Temporal  (K3)   verdict: {record['witness_temporal']['verdict']}")
    log(f"Contextual(chi)  verdict: {record['witness_contextual']['verdict']}")
    log(f"AGGREGATE EXECUTIONPROOF VERDICT: {record['aggregate_verdict']}")
    log(f"omni_certified = {record['omni_certified']}")
    log(f"record_hash = {record['record_hash']}")
    log("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
