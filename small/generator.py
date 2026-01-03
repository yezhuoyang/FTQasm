from typing import List
import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.qasm3 import dump as qasm_dump, dumps as qasm_dumps


# ---------------------------------------------------------------------------
# 3-qubit bit-flip repetition code (working dynamic decoder)
# ---------------------------------------------------------------------------

class ThreeQubitBitFlipCode:
    """
    3-qubit bit-flip repetition code.
    Uses a dynamic circuit to implement a simple lookup-table decoder.

    Logical encoding:
      - |0_L> = |000>
      - |1_L> = |111> (can be prepared by X on all data qubits, if desired)

    In this small benchmark version, we:
      - Perform repeated syndrome measurement rounds with dynamic decoding.
      - Do logical readout via a single readout qubit (parity of data qubits).
    """

    def __init__(self) -> None:
        # 3 data qubits
        self._dataqubits = QuantumRegister(3, "data")
        # 2 ancilla qubits for the two Z-type stabilizers
        self._ancillaqubits = QuantumRegister(2, "ancilla")
        # 1 logical readout qubit
        self._logicreadout_qubit = QuantumRegister(1, "readout")
        # 2-bit syndrome register (for the two stabilizers)
        self._synclbits = ClassicalRegister(2, "synd")
        # 2 classical bits for two logical readouts
        self._logicbits = ClassicalRegister(2, "logic")

        self._circuit = QuantumCircuit(
            self._dataqubits,
            self._logicreadout_qubit,
            self._ancillaqubits,
            self._synclbits,
            self._logicbits,
        )

    def syndrome_measurement(self):
        """
        One round of syndrome extraction and dynamic correction for
        the 3-qubit bit-flip code.

        Stabilizers:
          S0 = Z0 Z1 (measured into ancilla[0] -> synd[0])
          S1 = Z1 Z2 (measured into ancilla[1] -> synd[1])

        Syndrome interpretation (integer value of 2-bit register synd):
          0 (00) : no error
          1 (01) : error on data[2]
          2 (10) : error on data[0]
          3 (11) : error on data[1]
        """
        self._circuit.barrier(self._dataqubits, self._ancillaqubits)

        # Reset ancillas
        self._circuit.reset(self._ancillaqubits[0])
        self._circuit.reset(self._ancillaqubits[1])

        # S0 = Z0Z1
        self._circuit.cx(self._dataqubits[0], self._ancillaqubits[0])
        self._circuit.cx(self._dataqubits[1], self._ancillaqubits[0])
        self._circuit.measure(self._ancillaqubits[0], self._synclbits[0])

        # S1 = Z1Z2
        self._circuit.cx(self._dataqubits[1], self._ancillaqubits[1])
        self._circuit.cx(self._dataqubits[2], self._ancillaqubits[1])
        self._circuit.measure(self._ancillaqubits[1], self._synclbits[1])

        # Dynamic decoding via lookup table (majority vote)
        with self._circuit.if_test((self._synclbits, 1)):  # 01 -> flip data[2]
            self._circuit.x(self._dataqubits[2])
        with self._circuit.if_test((self._synclbits, 2)):  # 10 -> flip data[0]
            self._circuit.x(self._dataqubits[0])
        with self._circuit.if_test((self._synclbits, 3)):  # 11 -> flip data[1]
            self._circuit.x(self._dataqubits[1])

    def logical_readout(self, k: int = 0):
        """
        Logical Z readout via majority vote, implemented with one readout qubit.
        """
        self._circuit.reset(self._logicreadout_qubit[0])
        self._circuit.cx(self._dataqubits[0], self._logicreadout_qubit[0])
        self._circuit.cx(self._dataqubits[1], self._logicreadout_qubit[0])
        self._circuit.cx(self._dataqubits[2], self._logicreadout_qubit[0])
        self._circuit.measure(self._logicreadout_qubit[0], self._logicbits[k])

    def construct_circuit(self):
        """
        Build a simple small-benchmark circuit:

          syndrome -> logical readout -> syndrome -> logical readout
        """
        self.syndrome_measurement()
        self.logical_readout(0)
        self.syndrome_measurement()
        self.logical_readout(1)

    def draw_circuit(self):
        self._circuit.draw("mpl", filename="bitflip_circuit.png")

    def simulate(self):
        simulator = AerSimulator()
        result = simulator.run(self._circuit, shots=1024).result()
        return result.get_counts(self._circuit)

    def dump_qasm(self, filename: str = "bitflip_small.qasm"):
        """
        Dump the current circuit as OpenQASM 3.0 to a file.
        qasm3.dump expects a file-like object, so we open the file here.
        """
        with open(filename, "w") as f:
            qasm_dump(self._circuit, f)

    def construct_decoding_table(self):
        pass

    def construct_process(self):
        pass


# ---------------------------------------------------------------------------
# Five-qubit code (your dynamic decoder + QASM 3 dump)
# ---------------------------------------------------------------------------

class FiveQubitCode:
    """
    Five qubit code implementation.
    Uses a dynamic circuit to implement the five qubit code decoder.
    """

    def __init__(self) -> None:
        self._dataqubits = QuantumRegister(5, "data")
        self._ancillaqubits = QuantumRegister(4, "ancilla")
        self._logicreadout_qubit = QuantumRegister(1, "readout")
        self._synclbits = ClassicalRegister(4, "synd")
        self._logicbits = ClassicalRegister(2, "logic")
        self._circuit = QuantumCircuit(
            self._dataqubits,
            self._logicreadout_qubit,
            self._ancillaqubits,
            self._synclbits,
            self._logicbits,
        )

    def syndrome_measurement(self):

        # Reset ancillas
        self._circuit.reset(self._ancillaqubits[0])
        self._circuit.reset(self._ancillaqubits[1])
        self._circuit.reset(self._ancillaqubits[2])
        self._circuit.reset(self._ancillaqubits[3])

        # Put ancillas into |+>
        self._circuit.h(self._ancillaqubits[0])
        self._circuit.h(self._ancillaqubits[1])
        self._circuit.h(self._ancillaqubits[2])
        self._circuit.h(self._ancillaqubits[3])

        # Stabilizer couplings
        self._circuit.cx(self._ancillaqubits[0], self._dataqubits[0])
        self._circuit.cz(self._ancillaqubits[0], self._dataqubits[1])
        self._circuit.cz(self._ancillaqubits[0], self._dataqubits[2])
        self._circuit.cx(self._ancillaqubits[0], self._dataqubits[3])

        self._circuit.cx(self._ancillaqubits[1], self._dataqubits[1])
        self._circuit.cz(self._ancillaqubits[1], self._dataqubits[2])
        self._circuit.cz(self._ancillaqubits[1], self._dataqubits[3])
        self._circuit.cx(self._ancillaqubits[1], self._dataqubits[4])

        self._circuit.cx(self._ancillaqubits[2], self._dataqubits[0])
        self._circuit.cx(self._ancillaqubits[2], self._dataqubits[2])
        self._circuit.cz(self._ancillaqubits[2], self._dataqubits[3])
        self._circuit.cz(self._ancillaqubits[2], self._dataqubits[4])

        self._circuit.cz(self._ancillaqubits[3], self._dataqubits[0])
        self._circuit.cx(self._ancillaqubits[3], self._dataqubits[1])
        self._circuit.cx(self._ancillaqubits[3], self._dataqubits[3])
        self._circuit.cz(self._ancillaqubits[3], self._dataqubits[4])

        # Back to Z basis
        self._circuit.h(self._ancillaqubits[0])
        self._circuit.h(self._ancillaqubits[1])
        self._circuit.h(self._ancillaqubits[2])
        self._circuit.h(self._ancillaqubits[3])

        # Measure ancillas -> syndrome bits
        self._circuit.measure(self._ancillaqubits[0], self._synclbits[0])
        self._circuit.measure(self._ancillaqubits[1], self._synclbits[1])
        self._circuit.measure(self._ancillaqubits[2], self._synclbits[2])
        self._circuit.measure(self._ancillaqubits[3], self._synclbits[3])

        # X error corrections
        with self._circuit.if_test((self._synclbits, 0b1000)):  # 0001 → X_0
            self._circuit.x(self._dataqubits[0])
        with self._circuit.if_test((self._synclbits, 0b0001)):  # 1000 → X_1
            self._circuit.x(self._dataqubits[1])
        with self._circuit.if_test((self._synclbits, 0b0011)):  # 1100 → X_2
            self._circuit.x(self._dataqubits[2])
        with self._circuit.if_test((self._synclbits, 0b0110)):  # 0110 → X_3
            self._circuit.x(self._dataqubits[3])
        with self._circuit.if_test((self._synclbits, 0b1100)):  # 0011 → X_4
            self._circuit.x(self._dataqubits[4])

        # Z error corrections
        with self._circuit.if_test((self._synclbits, 0b0101)):  # 1010 → Z_0
            self._circuit.z(self._dataqubits[0])
        with self._circuit.if_test((self._synclbits, 0b1010)):  # 0101 → Z_1
            self._circuit.z(self._dataqubits[1])
        with self._circuit.if_test((self._synclbits, 0b0100)):  # 0010 → Z_2
            self._circuit.z(self._dataqubits[2])
        with self._circuit.if_test((self._synclbits, 0b1001)):  # 1001 → Z_3
            self._circuit.z(self._dataqubits[3])
        with self._circuit.if_test((self._synclbits, 0b0010)):  # 0100 → Z_4
            self._circuit.z(self._dataqubits[4])

        # Y error corrections
        with self._circuit.if_test((self._synclbits, 0b1101)):  # 1011 → Y_0
            self._circuit.y(self._dataqubits[0])
        with self._circuit.if_test((self._synclbits, 0b1011)):  # 1101 → Y_1
            self._circuit.y(self._dataqubits[1])
        with self._circuit.if_test((self._synclbits, 0b0111)):  # 1110 → Y_2
            self._circuit.y(self._dataqubits[2])
        with self._circuit.if_test((self._synclbits, 0b1111)):  # 1111 → Y_3
            self._circuit.y(self._dataqubits[3])
        with self._circuit.if_test((self._synclbits, 0b1110)):  # 0111 → Y_4
            self._circuit.y(self._dataqubits[4])


    def logical_readout(self, k: int = 0):
        self._circuit.reset(self._logicreadout_qubit[0])
        for q in self._dataqubits:
            self._circuit.cx(q, self._logicreadout_qubit[0])
        self._circuit.measure(self._logicreadout_qubit[0], self._logicbits[k])

    def construct_circuit(self):
        self.syndrome_measurement()
        self.logical_readout(0)
        self.syndrome_measurement()
        self.logical_readout(1)

    def draw_circuit(self):
        self._circuit.draw("mpl", filename="fivequbit_circuit.png")

    def simulate(self):
        simulator = AerSimulator()
        result = simulator.run(self._circuit, shots=1024).result()
        return result.get_counts(self._circuit)

    def dump_qasm(self, filename: str = "fivequbit_small.qasm"):
        with open(filename, "w") as f:
            qasm_dump(self._circuit, f)

    def construct_decoding_table(self):
        pass

    def construct_process(self):
        pass


# ---------------------------------------------------------------------------
# Steane [[7,1,3]] – skeleton with same interface
# ---------------------------------------------------------------------------

class SteaneSevenQubitCode:
    """
    Skeleton Steane [[7,1,3]] code memory benchmark.

    NOTE:
      - Minimal template with the same interface.
      - Fill in encode_logical_zero and full syndrome/decoder later.
    """

    def __init__(self) -> None:
        self._dataqubits = QuantumRegister(7, "data")
        self._ancillaqubits = QuantumRegister(6, "ancilla")  # 3 X-type, 3 Z-type
        self._logicreadout_qubit = QuantumRegister(1, "readout")
        self._synclbits = ClassicalRegister(6, "synd")
        self._logicbits = ClassicalRegister(2, "logic")

        self._circuit = QuantumCircuit(
            self._dataqubits,
            self._logicreadout_qubit,
            self._ancillaqubits,
            self._synclbits,
            self._logicbits,
        )

    def encode_logical_zero(self):
        # TODO: Steane encoder
        pass

    def syndrome_measurement(self):
        self._circuit.barrier(self._dataqubits, self._ancillaqubits)
        for a in self._ancillaqubits:
            self._circuit.reset(a)

        # Placeholder stabilizer
        self._circuit.cx(self._dataqubits[0], self._ancillaqubits[0])
        self._circuit.cx(self._dataqubits[1], self._ancillaqubits[0])
        self._circuit.measure(self._ancillaqubits[0], self._synclbits[0])
        # TODO: add all 6 stabilizers + decoder

    def logical_readout(self, k: int = 0):
        self._circuit.reset(self._logicreadout_qubit[0])
        for q in self._dataqubits:
            self._circuit.cx(q, self._logicreadout_qubit[0])
        self._circuit.measure(self._logicreadout_qubit[0], self._logicbits[k])

    def construct_circuit(self):
        self.encode_logical_zero()
        self.syndrome_measurement()
        self.logical_readout(0)
        self.syndrome_measurement()
        self.logical_readout(1)

    def draw_circuit(self):
        self._circuit.draw("mpl", filename="steane_circuit.png")

    def simulate(self):
        simulator = AerSimulator()
        result = simulator.run(self._circuit, shots=1024).result()
        return result.get_counts(self._circuit)

    def dump_qasm(self, filename: str = "steane_small.qasm"):
        with open(filename, "w") as f:
            qasm_dump(self._circuit, f)


# ---------------------------------------------------------------------------
# Shor [[9,1,3]] – skeleton
# ---------------------------------------------------------------------------

class ShorNineQubitCode:
    """
    Skeleton Shor [[9,1,3]] code memory benchmark.
    """

    def __init__(self) -> None:
        self._dataqubits = QuantumRegister(9, "data")
        self._ancillaqubits = QuantumRegister(8, "ancilla")
        self._logicreadout_qubit = QuantumRegister(1, "readout")
        self._synclbits = ClassicalRegister(8, "synd")
        self._logicbits = ClassicalRegister(2, "logic")

        self._circuit = QuantumCircuit(
            self._dataqubits,
            self._logicreadout_qubit,
            self._ancillaqubits,
            self._synclbits,
            self._logicbits,
        )

    def encode_logical_zero(self):
        # TODO: full Shor encoder
        pass

    def syndrome_measurement(self):
        self._circuit.barrier(self._dataqubits, self._ancillaqubits)
        for a in self._ancillaqubits:
            self._circuit.reset(a)

        # Placeholder stabilizer
        self._circuit.cx(self._dataqubits[0], self._ancillaqubits[0])
        self._circuit.cx(self._dataqubits[1], self._ancillaqubits[0])
        self._circuit.measure(self._ancillaqubits[0], self._synclbits[0])

    def logical_readout(self, k: int = 0):
        self._circuit.reset(self._logicreadout_qubit[0])
        for q in self._dataqubits:
            self._circuit.cx(q, self._logicreadout_qubit[0])
        self._circuit.measure(self._logicreadout_qubit[0], self._logicbits[k])

    def construct_circuit(self):
        self.encode_logical_zero()
        self.syndrome_measurement()
        self.logical_readout(0)
        self.syndrome_measurement()
        self.logical_readout(1)

    def draw_circuit(self):
        self._circuit.draw("mpl", filename="shor_circuit.png")

    def simulate(self):
        simulator = AerSimulator()
        result = simulator.run(self._circuit, shots=1024).result()
        return result.get_counts(self._circuit)

    def dump_qasm(self, filename: str = "shor_small.qasm"):
        with open(filename, "w") as f:
            qasm_dump(self._circuit, f)


# ---------------------------------------------------------------------------
# Small 3x3 surface-like code – skeleton
# ---------------------------------------------------------------------------

class Surface3x3Code:
    """
    Skeleton small 3x3 surface-code-like patch.

    Not a full planar code yet; just a small toy with same interface.
    """

    def __init__(self) -> None:
        self._dataqubits = QuantumRegister(9, "data")   # 3x3 patch
        self._ancillaqubits = QuantumRegister(4, "ancilla")
        self._logicreadout_qubit = QuantumRegister(1, "readout")
        self._synclbits = ClassicalRegister(4, "synd")
        self._logicbits = ClassicalRegister(2, "logic")

        self._circuit = QuantumCircuit(
            self._dataqubits,
            self._logicreadout_qubit,
            self._ancillaqubits,
            self._synclbits,
            self._logicbits,
        )

    def encode_logical_zero(self):
        # TODO: proper surface-code logical zero
        pass

    def syndrome_measurement(self):
        self._circuit.barrier(self._dataqubits, self._ancillaqubits)
        for a in self._ancillaqubits:
            self._circuit.reset(a)

        # Example Z-type stabilizer on a 2x2 plaquette (0,1,3,4)
        self._circuit.cx(self._dataqubits[0], self._ancillaqubits[0])
        self._circuit.cx(self._dataqubits[1], self._ancillaqubits[0])
        self._circuit.cx(self._dataqubits[3], self._ancillaqubits[0])
        self._circuit.cx(self._dataqubits[4], self._ancillaqubits[0])
        self._circuit.measure(self._ancillaqubits[0], self._synclbits[0])

        # Example X-type stabilizer via H + CZ (toy)
        self._circuit.h(self._ancillaqubits[1])
        self._circuit.cz(self._ancillaqubits[1], self._dataqubits[4])
        self._circuit.cz(self._ancillaqubits[1], self._dataqubits[5])
        self._circuit.cz(self._ancillaqubits[1], self._dataqubits[7])
        self._circuit.cz(self._ancillaqubits[1], self._dataqubits[8])
        self._circuit.h(self._ancillaqubits[1])
        self._circuit.measure(self._ancillaqubits[1], self._synclbits[1])

        # TODO: add more checks + decoder

    def logical_readout(self, k: int = 0):
        self._circuit.reset(self._logicreadout_qubit[0])
        for q in self._dataqubits:
            self._circuit.cx(q, self._logicreadout_qubit[0])
        self._circuit.measure(self._logicreadout_qubit[0], self._logicbits[k])

    def construct_circuit(self):
        self.encode_logical_zero()
        self.syndrome_measurement()
        self.logical_readout(0)
        self.syndrome_measurement()
        self.logical_readout(1)

    def draw_circuit(self):
        self._circuit.draw("mpl", filename="surface3x3_circuit.png")

    def simulate(self):
        simulator = AerSimulator()
        result = simulator.run(self._circuit, shots=1024).result()
        return result.get_counts(self._circuit)

    def dump_qasm(self, filename: str = "surface3x3_small.qasm"):
        with open(filename, "w") as f:
            qasm_dump(self._circuit, f)


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    bitflip = ThreeQubitBitFlipCode()
    bitflip.construct_circuit()
    bitflip.dump_qasm("bitflip_memory_small.qasm")

    five = FiveQubitCode()
    five.construct_circuit()
    five.dump_qasm("fivequbit_memory_small.qasm")

    steane = SteaneSevenQubitCode()
    steane.construct_circuit()
    steane.dump_qasm("steane_memory_skeleton.qasm")

    shor = ShorNineQubitCode()
    shor.construct_circuit()
    shor.dump_qasm("shor_memory_skeleton.qasm")

    surface = Surface3x3Code()
    surface.construct_circuit()
    surface.dump_qasm("surface3x3_memory_skeleton.qasm")
