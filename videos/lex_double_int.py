# -*- coding: utf-8 -*-
"""Lexicon additions for the double-integral videos (I01..I08). Kept specific: "סוג I" / "סוג II" are the region
types (the voice would read the Latin numeral), and a few TeX tokens that only integrals use."""

WORDS = {
    "סוג II": "סוג שתיים",
    "סוג I": "סוג אחת",
    "פוביני": "פוּבִּינִי",
}

TEX_TOKENS = {
    "dx": "דִּי אִקְס",
    "dy": "דִּי וַואי",
    "dr": "דִּי אָר",
    r"d\theta": "דִּי תטא",
    "du": "דִּי יוּ",
    "dv": "דִּי וִי",
    "dA": "דִּי אֵיי",
}
