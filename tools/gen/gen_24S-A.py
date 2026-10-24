# -*- coding: utf-8 -*-
"""Generator for tools/raw/24S-A.json -- calculus-2 (20252), summer moed 2024 (03/11/2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24S-A.py

Source: sitting 24S-A (orchestrator's code for exam 3.11.24). Exam: 3 pages, 5 questions of 25 points
(a=12, b=13), solve 4 of 5. NO answer key exists for this sitting (GATE1: the solver writes the solution and
the refuter checks it), so every item is held with reason "no-key"; the orchestrator routes them to the solver.
Exam header (lecturer and TA names) is not transcribed.

Transcription notes
- The text layers are garbled; everything is transcribed from page renders.
- Q1a is printed "f(x,y,) = y cos(xy)" (stray comma); transcribed as f(x,y).
- Q2a: parts 1 (3 pts, continuity) and 2 (9 pts, partials and differentiability) are one item (12 pts).
- Q2b: the two series are one item (6 + 7 pts).
- Q3: the page break leaves a stray "ב." label at the bottom of the page, and the extremum question is printed
  as "1." (13 pts). It is the second part of Q3 and is transcribed as Q3b.
- Q5a: the two sub-questions (6 + 6 pts) are one item.
- tools/verify/24S-A/check.py holds the transcriber's own sympy workings for the solver (not a key).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24S-A.json"
NOKEY = "no-key"


def H(num, kind, topic, question, part, points):
    return {"num": num, "part": part, "kind": kind, "topic": topic, "points": points,
            "question": question, "hold": NOKEY}


questions = []

questions.append(H(1, "computation", "gradient_directional", r"""באיזה כיוון הנגזרת הכיוונית של הפונקציה $f(x,y)=y\cdot\cos(xy)$ בנקודה $(1,0)$ שווה ל-1.""", "א", 12))

questions.append(H(1, "proof", "partials_differentiability", r"""הוכיחו כי עבור הפונקציה הבאה:
$$z(x,y)=e^{x-y}\cdot\sin(x+y)$$
לכל $(x,y)$ בתחום הגדרתה, מתקיים: $z''_{xx}(x,y)+z''_{yy}(x,y)=0$""", "ב", 13))

questions.append(H(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{xy^3}{x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
1. (3 נקודות) האם הפונקציה רציפה בנקודה $(0,0)$?
2. (9 נקודות) האם $f'_x(0,0)$ ו-$f'_y(0,0)$ קיימים? אם כן חשבו אותם.
האם הפונקציה דיפרנציאבילית בנקודה $(0,0)$?""", "א", 12))

questions.append(H(2, "computation", "numeric_series", r"""קבעו לגבי כל אחד מהטורים הבאים אם הוא מתכנס בהחלט, מתכנס בתנאי או מתבדר, נמקו!
1. (6 נקודות) $\displaystyle\sum_{n=1}^{\infty}\frac{\cos(n)}{\sqrt[4]{n^5+2}}$
2. (7 נקודות) $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt{n\cdot(n+1)}}$""", "ב", 13))

questions.append(H(3, "computation", "power_series", r"""מצאו את תחום ההתכנסות של הטור $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot4^n}(x-2)^n$.""", "א", 12))

questions.append(H(3, "computation", "absolute_extrema", r"""נתונה הפונקציה:
$$f(x,y)=2x^2-3y^2+xy-3x+8y$$
מצאו את נקודות המקסימום והמינימום המוחלטים של הפונקציה בתחום $D$ כאשר $D$ הוא משולש שקודקודיו $A(0,0),B(0,1),C(1,1)$""", "ב", 13))

questions.append(H(4, "computation", "chain_rule_identity", r"""תהי $f(x,y)$ פונקציה דיפרנציאבילית בכל המישור כך שלכל $t$ ממשי מתקיים $f(2t+1,e^t)=3$.
כמו כן, מתקיים כי $f'_x(2t+1,e^t)=\dfrac{e^t}{2}$. חשבו את $f'_y(2t+1,e^t)$""", "א", 12))

questions.append(H(4, "computation", "gradient_directional", r"""כתבו את משוואת המישור המשיק למשטח $f(x,y)=\ln\left(x+\dfrac1y\right)$ בכל הנקודות $(x,y)$ בהם $\nabla f(x,y)=\vec i-\dfrac{16}{9}\vec j$""", "ב", 13))

questions.append(H(5, "computation", "implicit_function", r"""נתונה המשוואה: $5z^3+3xyz-x^2\cdot y^2+1=0$
1. (6 נקודות) הראו כי המשוואה מגדירה בסביבת הנקודה $(1,-1,0)$ פונקציה יחידה $z=z(x,y)$.
2. (6 נקודות) חשבו את ערך הביטוי $z_x(1,-1)+z_y(1,-1)$""", "א", 12))

questions.append(H(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה
$$f(x,y)=xy(6-x-y)$$""", "ב", 13))

exam = {
    "examCode": "24S-A",
    "examLabel": "מבחן סוף סמסטר, מועד קיץ תשפ\"ד",
    "year": 2024,
    "examDate": "03/11/2024",
    "sourceFile": "calculus-2/24S-A exam.pdf",
    "solutionFile": "none (no key)",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions (all held: no-key)")
