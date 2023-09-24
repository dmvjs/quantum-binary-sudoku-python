import matplotlib.pyplot as plt
import numpy as np

from qiskit import Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit_ionq import IonQProvider
provider = IonQProvider()

from qiskit.visualization import plot_histogram

clause_list = [[0,1],[1,2],[2,3],[4,5],[5,6],[6,7],[8,9],[9,10],[10,11],[12,13],[13,14],[14,15],[0,4],[4,8],[8,12],[1,5],[5,9],[9,13],[2,6],[6,10],[10,14],[3,7],[7,11],[11,15]]

def XOR(qc, a, b, output):
    qc.cx(a, output)
    qc.cx(b, output)

def sudoku_oracle(qc, clause_list, var_qubits, clause_qubits, cbits):
    i = 0
    for clause in clause_list:
        XOR(qc, clause[0], clause[1], clause_qubits[i])
        i += 1
    qc.mct(clause_qubits, output_qubit)

    i = 0
    for clause in clause_list:
        XOR(qc, clause[0], clause[1], clause_qubits[i])
        i += 1

def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    for qubit in range(nqubits):
        qc.h(qubit)
    for qubit in range(nqubits):
        qc.x(qubit)
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)
    qc.h(nqubits-1)
    for qubit in range(nqubits):
        qc.x(qubit)
    for qubit in range(nqubits):
        qc.h(qubit)
    U_s = qc.to_gate()
    U_s.name = "$U_s$"
    return U_s

var_qubits = QuantumRegister(24, name='v')
clause_qubits = QuantumRegister(24, name='c')
output_qubit = QuantumRegister(1, name='out')
cbits = ClassicalRegister(24, name='cbits')
qc = QuantumCircuit(var_qubits, clause_qubits, output_qubit, cbits)

qc.initialize([1, -1]/np.sqrt(2), output_qubit)
qc.h(var_qubits)
qc.barrier()

sudoku_oracle(qc, clause_list, var_qubits, clause_qubits, cbits)
qc.barrier()
qc.append(diffuser(24), [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])

sudoku_oracle(qc, clause_list, var_qubits, clause_qubits, cbits)
qc.barrier()
qc.append(diffuser(24), [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])

qc.measure(var_qubits, cbits)
qc.draw(output="mpl")
plt.savefig("./circuit-diagram-4x4.png")

qasm_simulator = provider.get_backend('ionq_simulator')
job = execute(qc, backend=qasm_simulator, shots=1)
plot_histogram(job.result().get_counts(), title="sudoku", figsize=(10, 20), sort="value_desc", number_to_keep=20)
plt.savefig("./results-histogram-4x4.png")
