# ASK_ADIR - calculus-2

Open questions for Adir. One entry per item; the orchestrator moves it to Resolved when answered.

## Open

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
- Status: hold

### 22A-A p.7 Q4b - official maximum is wrong (boundary endpoints missed)
- Path: calculus-2 solution for sitting 22A-A, pages 6-7
- Page: 7
- Question: the key reports max f = 0 but never evaluates f at (+-sqrt2, 0), where f = 6 (sympy + dense grid). Shipped with the standing-ruling minimal fix: solved, official:false, prefix "הפתרון הרשמי עם תיקון".
- Needed: FYI only (no decision needed unless you want it held instead).
- Status: shipped-with-fix

### 22A-B Q3a - no solution in the key file
- Path: calculus-2 solution for sitting 22A-B (8 pages; page 4 starts with Q3b)
- Page: 4
- Question: Q3a (series n/((n^2+1)3^n) x^n) has no solution. Held with reason no-key; route to the solver (verify script hints R=3).
- Needed: solver.
- Status: hold

### Slips corrected in the keys (intermediate lines, no student-facing label)
- 23A-A Q3b p.7: f_t written for f_u. 23A-A Q5a p.11: critical point (6,-6) later written (-6,6). 23A-A Q5b p.12: convergence domain |x|<2 never stated (added).
- 22A-B Q1a p.1: df/dx written for df/dz. 22A-B Q2a p.2: second series printed with 2^n+1 in the heading, exam has 2^(n+1); exponent 2 for 3.
- 22A-A Q1b p.1: "+y^2" for "+2y/3". 22A-A Q2b p.3: division by h dropped in f_x(0,0). 22A-A Q3a p.4: "decreasing from n=2" should be n=4.

## Resolved
