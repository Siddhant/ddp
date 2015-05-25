set grid

set xlabel "Time (s)"
set ylabel "Supply Current (A)"

unset logscale x
set yrange[:1.8e-06]
unset logscale y

set format y "%g"
set format x "%g"

plot 'without_fault.data' using 1:(-1*$2) with lines lw 2 title "u36 s-a-1",\
     'last_fault.data' using 1:(-1*$2) with lines lw 2 title "n69 s-a-0",\
     'middle_fault.data' using 1:(-1*$2) with lines lw 2 title "n70 s-a-1 / n71 s-a-1"
     

set terminal push
set terminal postscript eps color
set out 'combined.eps'

replot
