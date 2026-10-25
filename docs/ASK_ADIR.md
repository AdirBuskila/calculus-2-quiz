# ASK_ADIR - calculus-2

Open questions for Adir. One entry per item; the orchestrator moves it to Resolved when answered.

## Open

**Short list for Adir (nothing blocks shipping; all are FYI or confirm-the-label):**
1. 26A-A Q3b and 24B-B Q4b: official key had a wrong final line or domain; shipped corrected with the prefix "הפתרון הרשמי עם תיקון". Confirm.
2. 22A-A Q4b (max f=6, key said 0), 25A-B Q2b/Q3b/Q5b: key typos shipped with the prefix "תיקון לפתרון שבקובץ". FYI.
3. 24S-A, 23A-C, 22A-B Q3a: no key in the source; solved, refuted, shipped as official:false. FYI.
4. Intermediate key slips fixed silently (listed below). FYI.

<!-- Entry format:
### <exam code> Q<number> - <short title>
- Path: <absolute file path>
- Page: <page number>
- Question: <what is unclear or missing>
- Needed: <what Adir must provide or decide>
- Status: hold
-->

### 26A-A p.5 Q3b - official final line disagrees with the printed statement
- Path: calculus-2 corrected solution for sitting 26A, page 5 (exam p.2)
- Page: 5
- Question: the exam asks to prove u z_u - v z_v = z x^2/v. The official solution's computation reaches e^{x^2 y} x^2/v (sympy confirms the printed identity), but its last line reads "= z x^2/v^2". The key's final line contradicts the question.
- Needed: confirm the printed RHS z x^2/v is right (then ship with the official computation and the last line corrected), or say which version is intended.
- Solver: the penultimate line x^2 v e/v^2 is right; the concluding line simplifies it to x^2/v^2, so the proof as printed concludes a false identity. For a proof the conclusion is the final answer, so treated as a wrong final answer: last line fixed to z x^2/v, solved, official:false, prefix "הפתרון הרשמי עם תיקון" (tools/verify/26A-A/solve_26A-A.py).
- Status: resolved by solver, refuted (all agree)

### 22A-A p.7 Q4b - official maximum is wrong (boundary endpoints missed)
- Path: calculus-2 solution for sitting 22A-A, pages 6-7
- Page: 7
- Question: the key reports max f = 0 but never evaluates f at (+-sqrt2, 0), where f = 6 (sympy + dense grid). Shipped with the standing-ruling minimal fix: solved, official:false, prefix "תיקון לפתרון שבקובץ" (the source is an unnamed-author key, not official, so GATE1 ruling 2026-10-24 applies).
- Needed: FYI only (no decision needed unless you want it held instead).
- Status: shipped-with-fix

### 22A-B Q3a - no solution in the key file
- Path: calculus-2 solution for sitting 22A-B (8 pages; page 4 starts with Q3b)
- Page: 4
- Question: Q3a (series n/((n^2+1)3^n) x^n) has no solution. Held with reason no-key; route to the solver (verify script hints R=3).
- Needed: solver.
- Solver: R=3; x=3 diverges (limit comparison with 1/n), x=-3 converges conditionally (Leibniz, n/(n^2+1) decreasing for n>=1); domain [-3,3). Solved, official:false (tools/verify/22A-B/solve_22A-B.py).
- Status: resolved by solver, refuted (all agree)

### Slips corrected in the keys (intermediate lines, no student-facing label)
- 23A-A Q3b p.7: f_t written for f_u. 23A-A Q5a p.11: critical point (6,-6) later written (-6,6). 23A-A Q5b p.12: convergence domain |x|<2 never stated (added).
- 22A-B Q1a p.1: df/dx written for df/dz. 22A-B Q2a p.2: second series printed with 2^n+1 in the heading, exam has 2^(n+1); exponent 2 for 3.
- 22A-A Q1b p.1: "+y^2" for "+2y/3". 22A-A Q2b p.3: division by h dropped in f_x(0,0). 22A-A Q3a p.4: "decreasing from n=2" should be n=4.
- 24B-A Q2b: after t=ln(x+1) the key writes the integrand dt/(t ln t); the correct integrand is dt/t (the divergence conclusion is unchanged). Fixed silently (refuter confirmed on the page).
- 25A-B Q2b: the explanation of the inverse-map Jacobian now says the determinant is -1/3 (absolute value 1/3), not +1/3 (explanation text only, not the key).

### 24B-B p.3-4 Q3d - key's boundary line and critical-point name are wrong
- Path: calculus-2 typed solution for sitting 24B-B (question embedded), pages 3-4
- Page: 4
- Question: the key writes f(1,y) = 1-2(y+1)-2+3 = -2y (true value 2-2y) and says (0,0) is the unique critical point (part c found (0,-1)). The final max 6 at (1,-2) and min 0 at (1,1) are correct (sympy + grid).
- Needed: say whether to ship with a labelled correction (suggested) or keep held.
- Solver: intermediate slip with a correct final answer, so fixed silently (f(1,y)=2-2y, critical point (0,-1) with f=3 listed), label kept lecturer-solution (tools/verify/24B-B/solve_24B-B.py).
- Status: resolved by solver, refuted (all agree)

### 24B-B p.5 Q4b - key's convergence domain has the wrong left endpoint
- Path: calculus-2 typed solution for sitting 24B-B (question embedded), pages 5-6
- Page: 6
- Question: the key ends with domain [-1/2; 3/2), but |x-1|<1/2 gives endpoints 1/2 and 3/2 (x=1/2 converges by Leibniz, x=3/2 diverges), so the domain is [1/2, 3/2). Its text also calls the x=3/2 series convergent.
- Needed: confirm shipping the corrected domain [1/2, 3/2) with a labelled correction.
- Solver: wrong final answer, so minimal fix (x=3/2 diverges, domain [1/2, 3/2)), solved, official:false, prefix "הפתרון הרשמי עם תיקון" (tools/verify/24B-B/solve_24B-B.py).
- Status: resolved by solver, refuted (all agree)

### 25A-B Q2b, Q3b, Q5b - key typos shipped with a labelled correction (FYI)
- Q2b p.3: inverse map printed y=(1/3)(v+1t), should be (v+2t); Jacobian and answer fine. Q3b p.4: dt/dx written for dt/dy. Q5b p.7: decimal 1.71166 should be 1.7104 (exact 3325/1944).
- Status: shipped-with-fix (prefix "תיקון לפתרון שבקובץ")

### 24S-A all items - no answer key
- The exam file for sitting 24S-A has no solution. All 10 items held "no-key" for the solver (sympy workings in tools/verify/24S-A/workings.json are not a key).
- Solver: all 10 solved from the page renders (Q3b transcription re-checked: the "1." and stray "ב." are a page-break artefact, Q3b is correct), every computation verified in tools/verify/24S-A/solve_24S-A.py; shipped as solved, official:false. They agree with the transcriber's workings.
- Status: resolved by solver, refuted (all agree)

### 24A-B p.6-7 Q3a - key's endpoint comparison is inconsistent
- Path: calculus-2 solution file for sitting 24A-B (misnamed 6.5.25), pages 6-7
- Page: 6-7
- Question: the key gets R=1 and the domain [-6,-4], both correct (sympy). But the endpoint step divides by 1/cuberoot(n^2) (ratio tends to 0, not 1) and then cites sum 1/n^(3/2); the terms really behave like n^(-4/3).
- Needed: allow shipping the question with the correct comparison (n^(-4/3), p>1) in place of the key's step, or keep it held.
- Solver: re-derived: at x=-4 the terms are limit-comparable to n^(-4/3) (ratio -> 1), p=4/3>1, converges; x=-6 converges absolutely. The final answer [-6,-4] holds, so the step was fixed silently; label kept student-solution (tools/verify/24A-B/solve_24A-B.py).
- Status: resolved by solver, refuted (all agree)

### 23A-C all items - no answer key
- The exam file for sitting 23A-C (27.4.23) has no solution. All 10 items solved by the solver (solved, official:false), every computation checked in tools/verify/23A-C/solve_23A-C.py (sympy + numeric).
- Status: resolved by solver, refuted (all agree)

## Resolved
