set terminal X11

set grid

set xlabel "Time (s)"
set ylabel "Supply Current (A)"

unset logscale x
set xrange [0.000000e+00:4.000000e-09]
unset logscale y

set format y "%g"
set format x "%g"

plot '10by10.data' using 1:2 with lines lw 3 title "one toggle", \
     '10by10.2.data' using 1:2 with lines lw 3 title "two toggles"

set terminal push
set terminal postscript eps color
set out '10by10_with_decaps_with_BPM_wire_model_combined.eps'

replot
