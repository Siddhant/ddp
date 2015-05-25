Creating large power grids with decaps and wire inductance
---------------------------------------

The main file is "netGenerate_large_nx_ny.py". It will generate a uniformly spaced
power gird for you.

Edit the file to change:

1. The number of _nodes_ you want in x-direcion (variable: "no_x_nodes")
and in y-direction (variable: "no_y_nodes").

2. The value of decap added at each node. (variable: "decap")

3. Currently, the segment of wire uses the following model:

```
.subckt Rseg 1 3
R1 1 2 0.583
L1 2 3 0.003n
C1 1 0 0.25e-12
C2 3 0 0.25e-12
.ends
```

    Edit the values to change the electrical parameters of the pi-model of the wire segment.
