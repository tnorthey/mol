
# Simple tasks...

- [x] Add dihedral terms to Eq. (8) and associated text.
- [x] Fix formatting of Eq. (8) into two lines.
- [ ] Brighten colouring of Fig. 4; remove grid lines.
- [ ] ChatGPT-ise the NMM discussion I wrote in my notebook.
  - [ ] Edit this appropriately and add to paper.
- [ ] 

# Must-Do Before Submission

- [ ] Investigate why using a larger qmax does not improve results.
  - [ ] Test different q-ranges ([0,2], [0,4], [0,8], [0,12], [0,24]).
  - [ ] Compare Ewald sphere results for qmax = 8 vs qmax = 4.

- [ ] Examine trajectory fitting issues at large t (Fig. 4).
  - [ ] Test fitting backwards (assume final structure known → work towards t = 0).
  - [ ] Test using structure-independent Iat(q) in denominator (△I(q,t)/Iat(q)) instead of reference signal.

- [ ] Assess whether problems arise from:
  - [ ] Target function choice (percent difference, elastic/inelastic, reference signal, etc.).
  - [ ] Sampling sufficiency.
  - [ ] Getting stuck in local minima.

- [ ] Minor revisions essential for clarity:
  - [ ] Label subfigures in Fig. 1 (a, b, c).
  - [ ] Clarify reanchoring of H-atoms.
  - [ ] Specify which Kabsch algorithm implementation is used.

- [ ] Introduction restructuring:
  - [ ] Present ultrafast experiments.
  - [ ] Place QMD simulations before inversion discussion.
  - [ ] Discuss inverse problems more generally.
  - [ ] Move to molecular geometry inversion (with examples).
  - [ ] Conclude with simulated annealing and this paper.

- [ ] Cross-check citations:
  - [ ] Prior work on distributions [35, 36].
  - [ ] Relevant MD citations (protein folding, large molecules) [38].
  - [ ] Reference on dividing squared difference signal by standard deviation (Jayatilika, quantum crystallography book chapter).

---

# Nice-to-Have Improvements

- [ ] Check if fitting improves when using only elastic scattering.
  - [ ] If yes, discuss potential contradiction with previous paper.

- [ ] Debug qmax-dependence using a simpler artificial molecule (3–4 atoms).

- [ ] Test using smaller timesteps (more time points) for trajectory fitting.

- [ ] Visualization refinements:
  - [ ] Change Fig. 1b to a circular plot.
  - [ ] Show distribution for qmax = 8 in Fig. 1c.

