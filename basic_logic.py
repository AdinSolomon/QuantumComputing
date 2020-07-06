
# we need to load the Libraries
import numpy
import math
from qiskit import *
from qiskit import BasicAer

#We need 5 quantum wires
q = QuantumRegister(5,'q')
#We only need 4 classical bits (3 inputs + 1 output)
c = ClassicalRegister(4,'c')
#Build the Circuit
circ = QuantumCircuit(q,c)

#We are Building
#(A v B) & (~C)

#Wires:
#q[0] = A
#q[1] = B
#q[2] = C
#q[3] = Temp Result
#q[4] = Final Result

#Lets set Values
#A=1,B=0,C=1
circ.x(q[0])
circ.x(q[2])
circ.barrier(q[0],q[1],q[2],q[3],q[4])

#A v B = ~(~A & ~B)
circ.x(q[0])
circ.x(q[1])
circ.ccx(q[0],q[1],q[3])#Res in q[3]
circ.x(q[0])#undo temp change
circ.x(q[1])#undo temp change
circ.x(q[3])#Apply not to result

#~C
circ.x(q[2])

#(A v B) & ~C
#The barrier makes it look prettier
circ.barrier(q[0],q[1],q[2],q[3],q[4])
circ.ccx(q[2],q[3],q[4])
circ.x(q[2])#Undo the not

#Measure the Bits we care about
circ.barrier(q[0],q[1],q[2],q[3],q[4])
circ.measure(q[0],c[0])
circ.measure(q[1],c[1])
circ.measure(q[2],c[2])
circ.measure(q[4],c[3])#Throw are q[3]

X=circ.draw(output="text")
print(X)

#Run an experiment!
backend_sim = BasicAer.get_backend('qasm_simulator')
job_sim = execute(circ,backend_sim,shots=2048)
result_sim = job_sim.result()
counts = result_sim.get_counts()
print(counts)



