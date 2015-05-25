set terminal X11
set title "100x100 grid of 1ohm (realistic) resistors + decaps "
set xlabel "s"
set ylabel "A"
set grid
unset logscale x 
set xrange [0.000000e+00:6.000000e-09]
unset logscale y 
set yrange [4.634948e-12:5.455869e-12]
#set xtics 1
#set x2tics 1
#set ytics 1
#set y2tics 1
set format y "%g"
set format x "%g"
plot '100by100.data' using 1:2 with lines lw 1 title "-i(Vin)" 
set terminal push
set terminal postscript eps color
set out '100by100.eps'
replot
set term pop
replot
