# -*- coding: utf-8 -*-
"""Generator for tools/raw/23A-C.json -- calculus-2 (20252), semester A 2023, moed C (27/04/2023).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_23A-C.py

Source: exam 27.4.23 (3 pages, 5 questions of 25 points, a=12, b=13, solve 4 of 5).
There is NO key for this sitting, so every item is held with reason "no-key"; the orchestrator routes them to the solver.
Header (lecturer names) is not transcribed. Text layers are garbled; everything is transcribed from page renders.

Transcription notes
- Q1b: the printed question asks by what factor the rate of change in the direction u is smaller than the maximal rate.
- Q2a asks for two series in one part; stored as one item. arctan^n means the n-th power of arctan.
- Q4b: the region is the part of the unit disk in the first quadrant lying between y=0 and y=sqrt(3)x.

Geometry for Q1a, Q4a, Q4b, Q5a (regions.json and contours.json) is in tools/verify/23A-C/check.py; the values there
are provisional and are NOT an answer key.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "23A-C.json"
NOKEY = "no-key"


def H(num, part, kind, topic, question, points):
    return {"num": num, "part": part, "kind": kind, "topic": topic, "points": points, "question": question,
            "hold": NOKEY}


questions = [
    H(1, "א", "computation", "double_integrals",
      "מצאו שטח של צורה מישורית המוגבלת בין שני המעגלים:\n$$x^2+y^2=2x,\\quad x^2+y^2=4x$$", 12),
    H(1, "ב", "computation", "gradient_directional",
      r"""נתונה הפונקציה $f(x,y,z)=x^2y\sqrt{z}$. פי כמה קצב שינוי הפונקציה בנקודה $(2,1,1)$ בכיוון של הוקטור $\vec u=\vec i+2\vec j+2\vec k$ קטן מקצב השינוי המקסימלי של הפונקציה בנקודה זו?""", 13),
    H(2, "א", "computation", "numeric_series",
      r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=1}^{\infty}\frac{2^n\cos n}{3^n}$$
$$\sum_{n=1}^{\infty}\arctan^n\!\left(\frac{n+2}{n+3}\right)$$""", 12),
    H(2, "ב", "computation", "partials_differentiability",
      r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{x^3+y^3}{2x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""", 13),
    H(3, "א", "computation", "power_series",
      r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}x^n\,\frac{1}{2^n+3^n}$$""", 12),
    H(3, "ב", "proof", "chain_rule_identity",
      r"""הראו כי הפונקציה $z=y\cdot g\left(x^2-y^2\right)$ כאשר $g(t)$ גזירה עבור כל $t$ ו-$x,y\neq0$ מקיימת את המשוואה:
$$\frac{1}{x}\cdot\frac{\partial z}{\partial x}+\frac{1}{y}\cdot\frac{\partial z}{\partial y}=\frac{z}{y^2}.$$""", 13),
    H(4, "א", "computation", "double_integrals",
      r"""החליפו את סדר האינטגרציה באינטגרל
$$\int_{-4}^{0}dx\int_{0}^{\sqrt{x+4}}f(x,y)\,dy+\int_{0}^{2}dx\int_{0}^{2-x}f(x,y)\,dy$$""", 12),
    H(4, "ב", "computation", "absolute_extrema",
      r"""מצאו אקסטרמומים מוחלטים של הפונקציה $f(x,y)=x^2+y^2+4xy$ בתחום המוגבל ע"י $x^2+y^2=1,\ \ y=0,\ \ y=\sqrt{3}x$ ברביע הראשון $(x\ge0,\ y\ge0)$.""", 13),
    H(5, "א", "computation", "local_extrema",
      r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=\left(x^2-2y^2\right)e^{x-y}$$""", 12),
    H(5, "ב", "computation", "taylor_maclaurin",
      r"""פתחו את הפונקציה $f(x)=\dfrac{1}{x^2+x-2}$ לטור מקלורן. מהו תחום התכנסות הטור?
הסיקו את הערך של $f^{(10)}(0)$.""", 13),
]

exam = {
    "examCode": "23A-C",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ג, מועד ג'",
    "year": 2023,
    "examDate": "27/04/2023",
    "sourceFile": "calculus-2/23A-C exam 27.4.23.pdf",
    "solutionFile": "none (no key exists for this sitting)",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
