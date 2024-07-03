reset

# png
set terminal pngcairo dashed size 2000,1600 enhanced font "Verdana,60"
#set terminal pngcairo dashed size 2500,1750 enhanced font "Verdana,50"
# dashed option enables dashed linestyle in pngcairo

# Custom line styles

LW1= 7.0
LW2 = 0.0
PS = 2.0

set style line 1 lt 1 pt 7 ps PS lw LW1 lc rgb '#0072bd' # blue
set style line 2 lt 1 pt 7 ps PS lw LW1 lc rgb '#d95319' # orange
set style line 3 lt 1 pt 7 ps PS lw LW1 lc rgb '#edb120' # yellow
set style line 4 lt 1 pt 7 ps PS lw LW1 lc rgb '#7e2f8e' # purple
set style line 5 lt 1 pt 7 ps PS lw LW1 lc rgb '#77ac30' # green
set style line 6 lt 1 pt 7 ps PS lw LW1 lc rgb '#4dbeee' # light-blue
set style line 7 lt 1 pt 6 ps 3.0 lw LW1 lc rgb '#a2142f' # red
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
NOXTICS = "set xtics ('' 0, '' 0.4, '' 0.8, '' 1.2); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 0.2, 1.6; \
          set xlabel 'RMSD (Å)' offset 0,0.4; \
          set mxtics 2"
NOYTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '10^{-3}' 0.001, '10^{-4}' 0.0001, '10^{-5}' 0.00001, '10^{-6}' 0.000001); \
           set mytics 10 ; \
           unset ylabel"
YTICS = " set ytics add ('' 10, '' 1, '' 0.1, '10^{-2}' 0.01, '10^{-3}' 0.001, '10^{-4}' 0.0001, '10^{-5}' 0.00001, '10^{-6}' 0.000001); \
           set mytics 10 ; \
           set ylabel 'ζ_{signal}' offset 5.5,-3"

NOKEY = "unset key"
KEY = "set key bottom right"

# Margins for each row resp. column
# ---- 0.95
# |  |
# ---- 0.70
# |  |
# ---- 0.45
# |  |
# ---- 0.20

TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.15"
MMARGIN = "set tmargin at screen 0.70; set bmargin at screen 0.45"
BMARGIN = "set tmargin at screen 0.45; set bmargin at screen 0.20"
LMARGIN = "set lmargin at screen 0.18; set rmargin at screen 0.97"
#RMARGIN = "set lmargin at screen 0.55; set rmargin at screen 0.95"

# Placement of the a,b,c,d labels in the graphs
POS = "at graph 0.74, 0.78 font 'helvetica, 50'"
POS2 = "at graph 0.77, 0.25 font 'helvetica, 60'"

# Enable the use of macros
set macros

set output "PLOT_SCATTER_SINGLE_TARGET_QMAX4_VARYING_NOISE_RMSD_FXRAY.png"

XMIN = 0.000
XMAX = 0.44
YMIN = 0.000008
YMAX = 10
YMIN2 = 0.00008
YMAX2 = 0.006
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@XTICS; @YTICS
@KEY
set label 1 'q_{max} = 4 Å^{-1}' @POS
#set logscale x 10
set logscale y 10
p "analysis_20_results_noise0.0_qmax4_nrestarts2_traj094_strong_constraints_chd_single_target_20.dat" u 5:4 t "noise = 0.0" w p ls 6, \
  "analysis_20_results_noise0.1_qmax4_nrestarts2_traj094_strong_constraints_chd_single_target_20.dat" u 5:4 t "= 0.1" w p ls 7, \
  "analysis_20_results_noise1.0_qmax4_nrestarts2_traj094_strong_constraints_chd_single_target_20.dat" u 5:4 t "= 1.0" w p ls 1, \
  "analysis_20_results_noise2.0_qmax4_nrestarts2_traj094_strong_constraints_chd_single_target_20.dat" u 5:4 t "= 2.0" w p ls 2, \
  "analysis_20_results_noise4.0_qmax4_nrestarts2_traj094_strong_constraints_chd_single_target_20.dat" u 5:4 t "= 4.0" w p ls 3, \
  "analysis_20_results_noise8.0_qmax4_nrestarts2_traj094_strong_constraints_chd_single_target_20.dat" u 5:4 t "= 8.0" w p ls 4, \
  "analysis_20_results_noise16.0_qmax4_nrestarts2_traj094_strong_constraints_chd_single_target_20.dat" u 5:4 t "= 16.0" w p ls 5, \

## --- GRAPH b
#@MMARGIN; @LMARGIN
#@XTICS; @YTICS
#@NOKEY
#set yrange [YMIN2 : YMAX2]
#set label 1 '' @POS
#set label 2 'q_{max} = 8 Å^{-1}' @POS
#p "analysis_20_results_noise0.0_qmax4_nrestarts2_traj094_strong_constraints_single_target_20.dat" u 5:4 w p ls 7, \
#  "analysis_20_results_noise0.0_qmax4_nrestarts2_traj094_weak_constraints_single_target_20.dat"   u 5:4 w p ls 1

# --- GRAPH c
@BMARGIN; @LMARGIN
@XTICS; @NOYTICS
@NOKEY
#set label 1 'N = 20,000' @POS
#p "analysis_20_results_noise0.0_qmax4_nrestarts2_traj094_strong_constraints_single_target_20.dat" u 5:4 w p ls 7, \
#  "analysis_20_results_noise0.0_qmax4_nrestarts2_traj094_weak_constraints_single_target_20.dat" u 5:4 w p ls 1, \
#  "analysis_20_results_noise0.0_qmax4_nrestarts2_traj094_strong_constraints_single_target_20.dat" u 5:4 w p ls 5, \
#  "analysis_20_results_noise0.0_qmax4_nrestarts2_traj094_weak_constraints_single_target_20.dat" u 5:4 w p ls 6, \

unset multiplot
### End multiplot

