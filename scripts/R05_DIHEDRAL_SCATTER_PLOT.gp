reset

# png
#set terminal pngcairo dashed size 1000,800 enhanced font "Verdana,30"
set terminal pngcairo dashed size 2500,1750 enhanced font "Verdana,60"
# dashed option enables dashed linestyle in pngcairo

# Custom line styles

LW1= 0.0
LW2 = 0.0
PS = 1.2

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
set style line 11 lt 1 pt 6 ps 3 lw 4 lc rgb '#000000' # black

set style line 102 lc rgb '#808080' lt 0 lw 3
set grid back ls 102

# Set the border using the linestyle 80 that we defined
# 3 = 1 + 2 (1 = plot the bottom line and 2 = plot the left line)
# back means the border should be behind anything else drawn
# set style line 80 lt 0 lw 3 lc rgb "#808080"
# set border 3 back ls 80

# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 0.4, '' 0.8, '' 1.2); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 0.5, 5.0; \
          set xlabel 'D_{05} (Å)' offset 0,0.4; \
          set mxtics 2"
NOYTICS = "set ytics 0, 50, 400; \
           set mytics 2 ; \
           unset ylabel"
YTICS = "set ytics 0, 50, 400; \
           set mytics 2 ; \
           set ylabel 'ϕ_{0145} (°)' offset 0,0"

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

TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.70"
MMARGIN = "set tmargin at screen 0.70; set bmargin at screen 0.45"
BMARGIN = "set tmargin at screen 0.45; set bmargin at screen 0.20"
LMARGIN = "set lmargin at screen 0.18; set rmargin at screen 0.97"
#RMARGIN = "set lmargin at screen 0.55; set rmargin at screen 0.95"

# Placement of the a,b,c,d labels in the graphs
POS1 = "at graph 0.70, 0.77 font 'helvetica, 30'"
POS2 = "at graph 0.04, 0.84 font 'helvetica, 50'"

# Enable the use of macros
set macros

set output "R05_DIHEDRAL_SCATTER_PLOT.png"

XMIN = 2.05
XMAX = 3.4
YMIN = 0.0
YMAX = 95.0
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@NOXTICS; @NOYTICS
@KEY
set label 1 't = 52 fs' @POS2
#set logscale x 10
#set logscale y 10
array point[1]
f20(x) = 44.648400950
#2.199008600 44.648400950
plot "tmp_/qmax4_results/r05_dihedral_20.dat" u 1:2 t "q_{max} = 4 Å^{-1}" w p ls 1, \
     "tmp_/qmax8_results/r05_dihedral_20.dat" u 1:2 t "q_{max} = 8 Å^{-1}" w p ls 7, \
     point us (2.199008600):(44.648400950) lc 0 pt 6 ps 3 lw 6 t "R_{targ}", \

     #"server_results_qmax4_40_r05_dihedral.dat" u 1:2 w p ls 4, \
     #"server_results_qmax8_40_r05_dihedral.dat" u 1:2 w p ls 5, \

# --- GRAPH b
@MMARGIN; @LMARGIN
@NOXTICS; @YTICS
@NOKEY
set label 1 '' @POS1
set label 2 't = 78 fs' @POS2
#2.474916195 50.428268119
plot "tmp_/qmax4_results/r05_dihedral_30.dat" u 1:2 w p ls 1, \
     point us (2.474916195):(50.428268119) lc 0 pt 6 ps 3 lw 6 t "", \
     "tmp_/qmax8_results/r05_dihedral_30.dat" u 1:2 w p ls 7, \

# --- GRAPH c
@BMARGIN; @LMARGIN
@XTICS; @NOYTICS
@NOKEY
set label 1 '' @POS1
set label 2 '' @POS2
set label 3 't = 104 fs' @POS2
#3.104794065 80.191168850
plot "tmp_/qmax4_results/r05_dihedral_40.dat" u 1:2 w p ls 1, \
     point us (3.104794065):(80.191168850) lc 0 pt 6 ps 3 lw 6 t "", \
     "tmp_/qmax8_results/r05_dihedral_40.dat" u 1:2 w p ls 7, \

#3.348700098 99.667722065
#plot "server_results_qmax4_50_r05_dihedral.dat" u 1:2 w p ls 1, \
#     "server_results_qmax8_50_r05_dihedral.dat" u 1:2 w p ls 7, \
#     point us (3.348700098):(99.667722065) pt 2 ps 2 lc 10 t "", \

unset multiplot
### End multiplot

