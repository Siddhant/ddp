set terminal X11
set title "10x10 grid of 1ohm (realistic) resistors + decaps "
set xlabel "s"
set ylabel "A"
set grid
unset logscale x 
set xrange [0.000000e+00:4.000000e-09]
unset logscale y 
set yrange [-1.500000e-06:3.150000e-05]
#set xtics 1
#set x2tics 1
#set ytics 1
#set y2tics 1
set format y "%g"
set format x "%g"
plot 'sink.data' using 1:2 with lines lw 1 title "i(Vprobe)" 
set terminal push
set terminal postscript eps color
set out 'sink.eps'
replot
set term pop
replot
