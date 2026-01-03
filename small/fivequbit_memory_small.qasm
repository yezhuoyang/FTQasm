OPENQASM 3.0;
include "stdgates.inc";
bit[4] synd;
bit[2] logic;
qubit[5] data;
qubit[1] readout;
qubit[4] ancilla;
reset ancilla[0];
reset ancilla[1];
reset ancilla[2];
reset ancilla[3];
h ancilla[0];
h ancilla[1];
h ancilla[2];
h ancilla[3];
cx ancilla[0], data[0];
cz ancilla[0], data[1];
cz ancilla[0], data[2];
cx ancilla[0], data[3];
cx ancilla[1], data[1];
cz ancilla[1], data[2];
cz ancilla[1], data[3];
cx ancilla[1], data[4];
cx ancilla[2], data[0];
cx ancilla[2], data[2];
cz ancilla[2], data[3];
cz ancilla[2], data[4];
cz ancilla[3], data[0];
cx ancilla[3], data[1];
cx ancilla[3], data[3];
cz ancilla[3], data[4];
h ancilla[0];
h ancilla[1];
h ancilla[2];
h ancilla[3];
synd[0] = measure ancilla[0];
synd[1] = measure ancilla[1];
synd[2] = measure ancilla[2];
synd[3] = measure ancilla[3];
if (synd == 8) {
  x data[0];
}
if (synd == 1) {
  x data[1];
}
if (synd == 3) {
  x data[2];
}
if (synd == 6) {
  x data[3];
}
if (synd == 12) {
  x data[4];
}
if (synd == 5) {
  z data[0];
}
if (synd == 10) {
  z data[1];
}
if (synd == 4) {
  z data[2];
}
if (synd == 9) {
  z data[3];
}
if (synd == 2) {
  z data[4];
}
if (synd == 13) {
  y data[0];
}
if (synd == 11) {
  y data[1];
}
if (synd == 7) {
  y data[2];
}
if (synd == 15) {
  y data[3];
}
if (synd == 14) {
  y data[4];
}
reset readout[0];
cx data[0], readout[0];
cx data[1], readout[0];
cx data[2], readout[0];
cx data[3], readout[0];
cx data[4], readout[0];
logic[0] = measure readout[0];
reset ancilla[0];
reset ancilla[1];
reset ancilla[2];
reset ancilla[3];
h ancilla[0];
h ancilla[1];
h ancilla[2];
h ancilla[3];
cx ancilla[0], data[0];
cz ancilla[0], data[1];
cz ancilla[0], data[2];
cx ancilla[0], data[3];
cx ancilla[1], data[1];
cz ancilla[1], data[2];
cz ancilla[1], data[3];
cx ancilla[1], data[4];
cx ancilla[2], data[0];
cx ancilla[2], data[2];
cz ancilla[2], data[3];
cz ancilla[2], data[4];
cz ancilla[3], data[0];
cx ancilla[3], data[1];
cx ancilla[3], data[3];
cz ancilla[3], data[4];
h ancilla[0];
h ancilla[1];
h ancilla[2];
h ancilla[3];
synd[0] = measure ancilla[0];
synd[1] = measure ancilla[1];
synd[2] = measure ancilla[2];
synd[3] = measure ancilla[3];
if (synd == 8) {
  x data[0];
}
if (synd == 1) {
  x data[1];
}
if (synd == 3) {
  x data[2];
}
if (synd == 6) {
  x data[3];
}
if (synd == 12) {
  x data[4];
}
if (synd == 5) {
  z data[0];
}
if (synd == 10) {
  z data[1];
}
if (synd == 4) {
  z data[2];
}
if (synd == 9) {
  z data[3];
}
if (synd == 2) {
  z data[4];
}
if (synd == 13) {
  y data[0];
}
if (synd == 11) {
  y data[1];
}
if (synd == 7) {
  y data[2];
}
if (synd == 15) {
  y data[3];
}
if (synd == 14) {
  y data[4];
}
reset readout[0];
cx data[0], readout[0];
cx data[1], readout[0];
cx data[2], readout[0];
cx data[3], readout[0];
cx data[4], readout[0];
logic[1] = measure readout[0];
