import matplotlib.pyplot as plt
import numpy as np

from qiskit import IBMQ, Aer, QuantumCircuit, ClassicalRegister, QuantumRegister, execute

from qiskit.visualization import plot_histogram

clause_list = [[0,1], [0,2], [1,3], [2,3]]

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

var_qubits = QuantumRegister(4, name='v')
clause_qubits = QuantumRegister(4, name='c')
output_qubit = QuantumRegister(1, name='out')
cbits = ClassicalRegister(4, name='cbits')
qc = QuantumCircuit(var_qubits, clause_qubits, output_qubit, cbits)


qc.initialize([1, -1]/np.sqrt(2), output_qubit)
qc.h(var_qubits)
qc.barrier()

sudoku_oracle(qc, clause_list, var_qubits, clause_qubits, cbits)
qc.barrier()
qc.append(diffuser(4), [0,1,2,3])

sudoku_oracle(qc, clause_list, var_qubits, clause_qubits, cbits)
qc.barrier()
qc.append(diffuser(4), [0,1,2,3])

qc.measure(var_qubits, cbits)
qc.draw(output="mpl")
plt.savefig("./circuit-diagram.png")

qasm_simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=qasm_simulator, shots=100024)
plot_histogram(job.result().get_counts(), color='midnightblue', title="New Histogram")
plt.savefig("./results-histogram.png")
