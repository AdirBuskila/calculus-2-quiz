# -*- coding: utf-8 -*-
"""Lexicon additions for the chain_rule videos (K01-K08). Merged into every video of the app by lexicon.py,
so only specific shapes: partial-derivative subscripts and g' / g''. A formula with fractions, roots or numbers of
two digits or more still needs an explicit say= in the script."""

TEX_TOKENS = {
    "g''": "גִ'י תָּג תָּג",
    "g'": "גִ'י תָּג",
    "z_x": "זֶד אִקְס", "z_y": "זֶד וַואי",
    "t_x": "טִי אִקְס", "t_y": "טִי וַואי",
    "f_x": "אֶף אִקְס", "f_y": "אֶף וַואי",
    "z_{xx}": "זֶד אִקְס אִקְס", "z_{yy}": "זֶד וַואי וַואי", "z_{xy}": "זֶד אִקְס וַואי",
}

WORDS = {
    "גרדיאנט": "גְּרַדְיֶאנְט",
}
