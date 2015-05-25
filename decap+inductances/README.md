Creating large power grids with decaps and wire inductance
---------------------------------------

The main file is "netGenerate_large_nx_ny.py". It will generate a uniformly spaced
power gird for you.

Edit the file to change:

- The number of _nodes_ you want in x-direcion (variable: "no_x_nodes")
and in y-direction (variable: "no_y_nodes").

- The value of decap added at each node. (variable: "decap")

- Currently, the segment of wire uses the following model, which can be edited to change the values
of the pi-model:
```
.subckt Rseg 1 3
R1 1 2 0.583
L1 2 3 0.003n
C1 1 0 0.25e-12
C2 3 0 0.25e-12
.ends
```
- The name of the ".cir" file generated.
