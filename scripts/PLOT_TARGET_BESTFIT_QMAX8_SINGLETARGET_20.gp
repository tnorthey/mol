reset

# png
set terminal pngcairo dashed size 2000,1600 enhanced font "Verdana,60"
#set terminal pngcairo dashed size 1000,800 enhanced font "Verdana,30"
#set terminal pngcairo dashed size 2500,1750 enhanced font "Verdana,50"
# dashed option enables dashed linestyle in pngcairo

# Custom line styles
PS = 1
LW1 = 1
set style line 1 lt 1 pt 7 ps PS lw LW1 lc rgb '#0072bd' # blue
set style line 2 lt 1 pt 7 ps PS lw LW1 lc rgb '#d95319' # orange
set style line 3 lt 1 pt 7 ps PS lw LW1 lc rgb '#edb120' # yellow
set style line 4 lt 1 pt 7 ps PS lw LW1 lc rgb '#7e2f8e' # purple
set style line 5 lt 1 pt 7 ps PS lw LW1 lc rgb '#77ac30' # green
set style line 6 lt 1 pt 7 ps PS lw LW1 lc rgb '#4dbeee' # light-blue
set style line 7 lt 1 pt 7 ps PS lw LW1 lc rgb '#a2142f' # red
set style line 8 lt 1 pt 7 ps PS lw LW1 lc rgb '#666666' # grey
set style line 9 lt 1 pt 7 ps PS lw LW1 lc rgb '#99ae52' # olive
set style line 10 lt 1 pt 7 ps PS lw LW1 lc rgb '#000000' # black

set style line 102 lc rgb '#808080' lt 0 lw 3
set grid back ls 102

# Set the border using the linestyle 80 that we defined
# 3 = 1 + 2 (1 = plot the bottom line and 2 = plot the left line)
# back means the border should be behind anything else drawn
# set style line 80 lt 0 lw 3 lc rgb "#808080"
# set border 3 back ls 80

# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 8, '' 16, '' 24); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 2, 24; \
          set xlabel 'q (Å^{-1})' offset 0,0.4; \
          set mxtics 2"
NOYTICS = "set ytics 0, 100, 20000; \
           set mytics 2 ; \
           unset ylabel"
YTICS = "set ytics 0, 10, 10000; \
           set mytics 10 ; \
           set ylabel 'I(q)' offset 1.5,0"

NOKEY = "unset key"
KEY = "set key top right"

# Margins for each row resp. column
# ---- 0.95
# |  |
# ---- 0.70
# |  |
# ---- 0.45
# |  |
# ---- 0.20

#TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.75"
TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.45"
MMARGIN = "set tmargin at screen 0.45; set bmargin at screen 0.15"
MMARGIN2 = "set tmargin at screen 0.55; set bmargin at screen 0.35"
BMARGIN = "set tmargin at screen 0.35; set bmargin at screen 0.15"
LMARGIN = "set lmargin at screen 0.18; set rmargin at screen 0.97"
#RMARGIN = "set lmargin at screen 0.55; set rmargin at screen 0.95"

# Placement of the a,b,c,d labels in the graphs
POS = "at graph 0.70, 0.16 font 'helvetica, 40'"
POS2 = "at graph 0.15, 0.32 font 'helvetica, 40'"
POS3 = "at graph 0.55, 0.45 font 'helvetica, 40'"

# Enable the use of macros
set macros

set output "PLOT_TARGET_BESTFIT_QMAX8_SINGLETARGET_20.png"

XMIN = 0.0
XMAX = 8.0
YMIN = 10
YMAX = 2000
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@NOXTICS; @YTICS
@KEY
#set label 1 '^↖ CHF_3' @POS
#set label 2 'CHD ^↗' @POS2
#set label 3 '_↙ Naphthalene' @POS3
#set logscale x 10
set logscale y 10
LW = 1
LW2 = 1
DT1 = 1
DT2 = 2
DT3 = 3
p "TARGET_FUNCTION_20_1d.dat" u 1:2 t "target" w l ls 7 lw LW dt DT1, \
  "20_1d_000.00012485.dat" u 1:2 t "fit" w l ls 1 lw LW dt DT1, \

# --- GRAPH b
@MMARGIN; @LMARGIN
@XTICS; @YTICS
@KEY
unset logscale y
set yrange [-0.0001 : 0.001]
set label 1 '' @POS
p "<paste 20_1d_000.00012485.dat TARGET_FUNCTION_20_1d.dat" u 1:((($2-$4)**2)/$4) t "(x - y)^2/y" w l ls 10 lw 2 dt 5, \
  "<paste 20_1d_000.00012485.dat TARGET_FUNCTION_20_1d.dat" u 1:(0.01*($2-$4)**2) t "0.01(x - y)^2" w l ls 10 lw 2 dt 4, \

# --- GRAPH c
@MMARGIN2; @LMARGIN
@NOXTICS; @NOYTICS
@NOKEY
#plot "../results_/tmp_/TARGET_IAM_40_1d.dat" u 1:($2*$1) t "" w l ls 7 lw LW dt DT1, \
     #"../results_/tmp_/TARGET_FUNCTION_40_1d.dat" u 1:($2*$1) t "" w p ls 1 lw LW dt 4, \

# --- GRAPH d
@BMARGIN; @LMARGIN
@XTICS; @NOYTICS
@NOKEY
#plot "../results_/tmp_/TARGET_IAM_50_1d.dat" u 1:($2*$1) t "" w l ls 7 lw LW dt DT1, \
     #"../results_/tmp_/TARGET_FUNCTION_50_1d.dat" u 1:($2*$1) t "" w p ls 1 lw LW dt 4, \

unset multiplot
### End multiplot

