set terminal X11
# set title "10x10 grid of 1ohm (realistic) resistors + decaps "
set xlabel "Time (s)"
set ylabel "Supply Current (A)"
set grid
unset logscale x 
set xrange [0.000000e+00:4.000000e-09]
unset logscale y 
set yrange [-9.034860e-07:1.897321e-05]
#set xtics 1
#set x2tics 1
#set ytics 1
#set y2tics 1
set format y "%g"
set format x "%g"
plot '10by10.2.data' using 1:2 with lines lw 5 title "" 
set terminal push
set terminal postscript eps color
set out '10by10_with_decaps_with_BPM_wire_model_with_two_sink.eps'
replot
set term pop
replot
