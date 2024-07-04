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

# STATS
stats "analysis_18_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t18"
stats "analysis_19_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t19"
stats "analysis_20_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t20"
stats "analysis_21_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t21"
stats "analysis_22_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t22"
stats "analysis_23_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t23"
stats "analysis_24_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t24"
stats "analysis_25_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t25"
stats "analysis_26_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t26"
stats "analysis_27_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t27"
stats "analysis_28_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t28"
stats "analysis_29_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t29"
stats "analysis_30_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t30"
stats "analysis_31_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t31"
stats "analysis_32_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t32"
stats "analysis_33_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t33"
stats "analysis_34_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t34"
stats "analysis_35_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t35"
stats "analysis_36_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t36"
stats "analysis_37_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 6 prefix "t37"

t18_range = t18_lo_quartile  # t20_median 
t19_range = t19_lo_quartile  # t20_median 
t20_range = t20_lo_quartile  # t30_median 
t21_range = t21_lo_quartile  # t30_median 
t22_range = t22_lo_quartile  # t30_median 
t23_range = t23_lo_quartile  # t40_median 
t24_range = t24_lo_quartile  # t40_median 
t25_range = t25_lo_quartile
t26_range = t26_lo_quartile
t27_range = t27_lo_quartile
t28_range = t28_lo_quartile
t29_range = t29_lo_quartile
t30_range = t30_lo_quartile
t31_range = t31_lo_quartile
t32_range = t32_lo_quartile
t33_range = t33_lo_quartile
t34_range = t34_lo_quartile
t35_range = t35_lo_quartile
t36_range = t36_lo_quartile
t37_range = t37_lo_quartile

# f_signal stats
stats "analysis_18_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f18"
stats "analysis_19_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f19"
stats "analysis_20_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f20"
stats "analysis_21_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f21"
stats "analysis_22_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f22"
stats "analysis_23_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f23"
stats "analysis_24_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f24"
stats "analysis_25_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f25"
stats "analysis_26_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f26"
stats "analysis_27_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f27"
stats "analysis_28_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f28"
stats "analysis_29_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f29"
stats "analysis_30_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f30"
stats "analysis_31_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f31"
stats "analysis_32_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f32"
stats "analysis_33_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f33"
stats "analysis_34_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f34"
stats "analysis_35_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f35"
stats "analysis_36_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f36"
stats "analysis_37_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u 4 prefix "f37"

f18_range = f18_max+1  # t20_median 
f19_range = f19_max+1  # t20_median 
f20_range = f20_max+1  # t30_median 
f21_range = f21_max+1  # t30_median 
f22_range = f22_max+1  # t30_median 
f23_range = f23_max+1  # t40_median 
f24_range = f24_max+1  # t40_median 
f25_range = f25_max+1
f26_range = f26_max+1
f27_range = f27_max+1
f28_range = f28_max+1
f29_range = f29_max+1
f30_range = f30_max+1
f31_range = f31_max+1
f32_range = f32_max+1
f33_range = f33_max+1
f34_range = f34_max+1
f35_range = f35_max+1
f36_range = f36_max+1
f37_range = f37_max+1


# MACROS
# x- and ytics for each row resp. column
NOXTICS = "set xtics ('' 0, '' 8, '' 16, '' 24); \
          unset xlabel; \
          set mxtics 2 "
XTICS = "set xtics 0, 1, 24; \
          set xlabel 't' offset 0,0.4; \
          set mxtics 2"
NOYTICS = " set ytics add ('' 10, '1' 1, '' 0.1, '10^{-2}' 0.01, '' 0.001, '10^{-4}' 0.0001); \
           set mytics 2 ; \
           unset ylabel"
YTICS = "set ytics -100, 20, 100; \
           set mytics 2 ; \
           set ylabel 'torsion_{0} (degrees)' offset 1.5,0"

NOKEY = "unset key"
KEY = "set key bottom right font ',35'"
KEY = "set key top left font ',35'"

# Margins for each row resp. column
# ---- 0.95
# |  |
# ---- 0.70
# |  |
# ---- 0.45
# |  |
# ---- 0.20

TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.20"
MMARGIN = "set tmargin at screen 0.60; set bmargin at screen 0.25"
BMARGIN = "set tmargin at screen 0.45; set bmargin at screen 0.20"
LMARGIN = "set lmargin at screen 0.18; set rmargin at screen 0.97"
#RMARGIN = "set lmargin at screen 0.55; set rmargin at screen 0.95"

# Placement of the a,b,c,d labels in the graphs
POS = "at graph 0.22, 0.89 font 'helvetica, 60'"
POS2 = "at graph 0.15, 0.32 font 'helvetica, 40'"
POS3 = "at graph 0.55, 0.45 font 'helvetica, 40'"

# Enable the use of macros
set macros

set output "PLOT_TORSION_NRESTARTS2_TRAJ000_NMM_B.png"

XMIN = 0
XMAX = 20
YMIN = -65
YMAX = 115
set yrange [YMIN : YMAX]
set xrange [XMIN : XMAX]

# Start multiplot
set multiplot layout 3,1 rowsfirst
# --- GRAPH a
@TMARGIN; @LMARGIN
@XTICS; @YTICS
@NOKEY
#set label 1 'η = 0' @POS
#set label 1 '^↖ CHF_3' @POS
#set label 2 'CHD ^↗' @POS2
#set label 3 '_↙ Naphthalene' @POS3
#set logscale x 10
#set logscale y 10
LW = 4
LW2 = 1
DT1 = 1
DT2 = 2
DT3 = 3
array point1[1]
array point2[1]
array point3[1]
array point4[1]

p "analysis_18_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (0):($6 < t18_range & $4 < f18_range ? $3 : 1/0) t "18" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_19_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (1):($6 < t19_range & $4 < f19_range ? $3 : 1/0) t "19" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_20_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (2):($6 < t20_range & $4 < f20_range ? $3 : 1/0) t "20" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_21_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (3):($6 < t21_range & $4 < f21_range ? $3 : 1/0) t "21" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_22_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (4):($6 < t22_range & $4 < f22_range ? $3 : 1/0) t "22" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_23_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (5):($6 < t23_range & $4 < f23_range ? $3 : 1/0) t "23" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_24_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (6):($6 < t24_range & $4 < f24_range ? $3 : 1/0) t "24" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_25_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (7):($6 < t25_range & $4 < f25_range ? $3 : 1/0) t "25" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_26_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (8):($6 < t26_range & $4 < f26_range ? $3 : 1/0) t "26" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_27_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (9):($6 < t27_range & $4 < f27_range ? $3 : 1/0) t "27" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_28_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (10):($6 < t28_range & $4 < f28_range ? $3 : 1/0) t "28" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_29_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (11):($6 < t29_range & $4 < f29_range ? $3 : 1/0) t "29" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_30_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (12):($6 < t30_range & $4 < f30_range ? $3 : 1/0) t "30" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_31_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (13):($6 < t31_range & $4 < f31_range ? $3 : 1/0) t "31" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_32_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (14):($6 < t32_range & $4 < f32_range ? $3 : 1/0) t "32" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_33_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (15):($6 < t33_range & $4 < f33_range ? $3 : 1/0) t "33" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_34_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (16):($6 < t34_range & $4 < f34_range ? $3 : 1/0) t "34" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_35_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (17):($6 < t35_range & $4 < f35_range ? $3 : 1/0) t "35" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_36_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (18):($6 < t36_range & $4 < f36_range ? $3 : 1/0) t "36" w p pt 6 ps 2 lw 3 lc 8,\
  "analysis_37_results_noise0.0_qmax4.3727_nrestarts2_traj000_strong_constraints_nmm_b.dat" u (19):($6 < t37_range & $4 < f37_range ? $3 : 1/0) t "37" w p pt 6 ps 2 lw 3 lc 8,\
     "nmm_geommovie_dihedral_6_3_10_5_modified.dat" u 1:($2 + 180) t "" w p pt 3 ps 4 lw 3 lc 7,\
     #"nmm_geommovie_dihedral_6_3_1_0_modified.dat" u 1:($2 + 180) t "" w p pt 1 ps 3 lw 3 lc 2,\


unset multiplot
### End multiplot

