OPENQASM 3.0;
include "stdgates.inc";
bit[2] synd;
bit[2] logic;
qubit[3] data;
qubit[1] readout;
qubit[2] ancilla;
barrier data[0], data[1], data[2], ancilla[0], ancilla[1];
reset ancilla[0];
reset ancilla[1];
cx data[0], ancilla[0];
cx data[1], ancilla[0];
synd[0] = measure ancilla[0];
cx data[1], ancilla[1];
cx data[2], ancilla[1];
synd[1] = measure ancilla[1];
if (synd == 1) {
  x data[2];
}
if (synd == 2) {
  x data[0];
}
if (synd == 3) {
  x data[1];
}
reset readout[0];
cx data[0], readout[0];
cx data[1], readout[0];
cx data[2], readout[0];
logic[0] = measure readout[0];
barrier data[0], data[1], data[2], ancilla[0], ancilla[1];
reset ancilla[0];
reset ancilla[1];
cx data[0], ancilla[0];
cx data[1], ancilla[0];
synd[0] = measure ancilla[0];
cx data[1], ancilla[1];
cx data[2], ancilla[1];
synd[1] = measure ancilla[1];
if (synd == 1) {
  x data[2];
}
if (synd == 2) {
  x data[0];
}
if (synd == 3) {
  x data[1];
}
reset readout[0];
cx data[0], readout[0];
cx data[1], readout[0];
cx data[2], readout[0];
logic[1] = measure readout[0];
