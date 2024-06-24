reset

# png
set terminal pngcairo dashed size 2000,1600 enhanced font "Verdana,60"
#set terminal pngcairo dashed size 1000,800 enhanced font "Verdana,30"
#set terminal pngcairo dashed size 2500,1750 enhanced font "Verdana,50"
# dashed option enables dashed linestyle in pngcairo

# Custom line styles

LW1= 2.5
LW2 = 0.0
PS = 1

set style line 1 lt 1 pt 7 ps PS lw LW1 lc rgb '#0072bd' # blue
set style line 2 lt 1 pt 7 ps PS lw LW1 lc rgb '#d95319' # orange
set style line 3 lt 1 pt 7 ps PS lw LW1 lc rgb '#edb120' # yellow
set style line 4 lt 1 pt 7 ps PS lw LW1 lc rgb '#7e2f8e' # purple
set style line 5 lt 1 pt 7 ps PS lw LW1 lc rgb '#77ac30' # #7f0000
set style line 6 lt 1 pt 7 ps PS lw LW1 lc rgb '#4dbeee' # light-blue
set style line 7 lt 1 pt 7 ps PS lw LW1 lc rgb '#a2142f' # #0090ff
set style line 8 lt 1 pt 7 ps PS lw LW1 lc rgb '#666666' # grey
set style line 9 lt 1 pt 7 ps PS lw LW1 lc rgb '#99ae52' # olive
set style line 10 lt 1 pt 7 ps PS lw LW1 lc rgb '#000000' # #7f0000

set style line 102 lc rgb '#808080' lt 0 lw 3
set grid back ls 102

# matlab palette
set palette defined ( 0 '#000090',\
                      1 '#000fff',\
                      2 '#0090ff',\
                      3 '#0fffee',\
                      4 '#90ff70',\
                      5 '#ffee00',\
                      6 '#ff7000',\
                      7 '#ee0000',\
                      8 '#7f0000')

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
XTICS = "set xtics ('0' 0, '0.1' 1, '1' 2, '2' 3, '4' 4, '8' 5, '16' 6); \
          set xlabel 'noise (σ)' offset 0,0.4; \
          set mxtics 2"
NOYTICS = "set ytics 0, 100, 20000; \
           set mytics 2 ; \
           unset ylabel"
YTICS = "set ytics 0, 1.0, 20; \
           set mytics 2 ; \
           set ylabel '〈〈d_{05}〉〉 (Å)' offset 1.5,0"

NOKEY = "unset key"
KEY = "set key top left"

# Margins for each row resp. column
# ---- 0.95
# |  |
# ---- 0.70
# |  |
# ---- 0.45
# |  |
# ---- 0.20

#TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.75"
TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.15"
MMARGIN = "set tmargin at screen 0.75; set bmargin at screen 0.55"
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

set output "PLOT_D05_LOWEST_QUARTILE_ADD_TRAJECTORIES_D.png"

XMIN = 0
XMAX = 6
YMIN = 1.5
YMAX = 3.50
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]
set key font ",40"

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@XTICS; @YTICS
@KEY
#set label 1 '^↖ CHF_3' @POS
#set label 2 'CHD ^↗' @POS2
#set label 3 '_↙ Naphthalene' @POS3
#set logscale x 10
#set logscale y 10
LW1= 15
LW2 = 10
DT1 = 1
DT2 = 2
DT3 = 3
PS1 = 8
PS2 = 4
PT1 = 2
PT2 = 6
c1 = "#0025ad"  # dark-blue
#c2 = "#007cad"  # turquoise
c2 = "#09ad00"  # green
c3 = "#7f0000" 

mean_d05(x) = 2.8725449487

p    "<paste rmsd_lowest_quartile_qmax4_traj090_d.dat rmsd_lowest_quartile_qmax4_traj099_d.dat rmsd_lowest_quartile_qmax4_traj094_d.dat"                 u (($4+$8+$12)/3) t "q_{max} = 4 Å^{-1}"     w lp lc rgb c1 lw LW1 dt DT1 pt PT1 ps PS1, \
     "<paste rmsd_lowest_quartile_qmax8_traj090_d.dat rmsd_lowest_quartile_qmax8_traj099_d.dat rmsd_lowest_quartile_qmax8_traj094_d.dat"                 u (($4+$8+$12)/3) t " = 8 Å^{-1}"     w lp lc rgb c2 lw LW1 dt DT1 pt PT2 ps PS1, \
     "<paste rmsd_lowest_quartile_qmax4_traj090_low_constraints_c3.dat rmsd_lowest_quartile_qmax4_traj099_low_constraints_c3.dat rmsd_lowest_quartile_qmax4_traj094_low_constraints_c3.dat"                 u (($4+$8+$12)/3) t ""     w lp lc rgb c1 lw LW2 dt DT2 pt PT1 ps PS2, \
     "<paste rmsd_lowest_quartile_qmax8_traj090_low_constraints_c3.dat rmsd_lowest_quartile_qmax8_traj099_low_constraints_c3.dat rmsd_lowest_quartile_qmax8_traj094_low_constraints_c3.dat"                 u (($4+$8+$12)/3) t ""     w lp lc rgb c2 lw LW2 dt DT2 pt PT2 ps PS2, \
     mean_d05(x) t "Target 〈〈d_{05}〉〉" w l lc rgb "black" lw 4 dt 2, \

# color definitions
#set style line 2  lc rgb '#0025ad' lt 1 lw 2
#set style line 3  lc rgb '#0042ad' lt 1 lw 2
#set style line 4  lc rgb '#0060ad' lt 1 lw 2
#set style line 5  lc rgb '#007cad' lt 1 lw 2
#set style line 6  lc rgb '#0099ad' lt 1 lw 2
#set style line 7  lc rgb '#00ada4' lt 1 lw 2
#set style line 8  lc rgb '#00ad88' lt 1 lw 2
#set style line 9  lc rgb '#00ad6b' lt 1 lw 2
#set style line 10 lc rgb '#00ad4e' lt 1 lw 2
#set style line 11 lc rgb '#00ad31' lt 1 lw 2
#set style line 12 lc rgb '#00ad14' lt 1 lw 2
#set style line 13 lc rgb '#09ad00' lt 1 lw 2

# --- GRAPH b
@MMARGIN; @LMARGIN
@NOXTICS; @YTICS
@NOKEY
set label 1 '' @POS
#plot "../results_/tmp_/TARGET_IAM_30_1d.dat" u 1:($2*$1) t "" w l ls 7 lw LW dt DT1, \
     #"../results_/tmp_/TARGET_FUNCTION_30_1d.dat" u 1:($2*$1) t "" w p ls 1 lw LW dt 4, \

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

