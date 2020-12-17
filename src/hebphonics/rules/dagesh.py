#!/usr/bin/env python
# coding: utf-8
"""Rules for `dagesh`."""
# pylint: disable=inconsistent-return-statements

# pkg
from . import isvowel, rule, T_BEGEDKEFET, NON_DAGESH_LETTERS
from .. import tokens as T

## `dagesh-`, `mapiq-`


@rule("dagesh", "dagesh-none-bgdkft")
def dagesh_none_bgdkft(token, guess):
    """BGDKFT letter _without_ dagesh has a different name

    Source: [Simanim] 1.3
    > There is a difference in the pronunciation of these letters when
    > they have a `dagesh` and when they do not.
    """
    if token.has(letter=T_BEGEDKEFET, dagesh=False):
        guess.letter, _ = T_BEGEDKEFET[token.letter]
        return guess


@rule("dagesh", "dagesh-qal-bgdkft")
def dagesh_qal_bgdkft(token, prev, guess):
    """`dagesh` in BGDKFT NOT after vowel is `dagesh-qal`

    This includes the start of a word which has no vowel preceding it
    and a `dagesh` after a `sheva` (see
    [`sheva-nah-before-bgdkft-dagesh`](#sheva-nah-before-bgdkft-dagesh)).

    Source: [Simanim] 1.3
    > Every `dagesh` at the start of a word is `dagesh-qal`. And every `dagesh` in
    > the middle of a word after a `sheva-nah` is `dagesh-qal` because it is like
    > the start of a word after there is a little break with the `sheva-nah`.

    Source: [Gesenius] 13.2.note
    > The learner will perceive that `dagesh-hazaq` must always be immediately
    > preceded by a vowel, which is never the case with `dagesh-qal`.

    See also: [`dagesh-hazaq-bgdkft`](#dagesh-hazaq-bgdkft),
    [`sheva-nah-before-bgdkft-dagesh`](#sheva-nah-before-bgdkft-dagesh)
    """
    if token.has(letter=T_BEGEDKEFET, dagesh=True) and not isvowel(prev.vowel):
        _, guess.letter = T_BEGEDKEFET[token.letter]
        guess.dagesh = T.NAME_DAGESH_QAL
        return guess


@rule("dagesh", "dagesh-hazaq-bgdkft")
def dagesh_hazaq_bgdkft(token, prev, guess):
    """`dagesh` in BGDKFT after vowel is `dagesh-hazaq`

    `dagesh` after a `sheva-na` is also a `dagesh-hazaq`, however
    this cannot occur in a BGDKFT letter because a `sheva` followed
    by BGDKFT with `dagesh` is `sheva-nah`
    (see [`sheva-nah-before-bgdkft-dagesh`](#sheva-nah-before-bgdkft-dagesh)).

    Source: [Simanim] 1.3
    > Every `dagesh` in the middle of a word after a vowel is called a `dagesh-hazaq`.

    Source: [Gesenius] 13.2.note
    > The learner will perceive that `dagesh-hazaq` must always be immediately
    > preceded by a vowel, which is never the case with `dagesh-qal`.

    See also: [`dagesh-qal-bgdkft`](#dagesh-qal-bgdkft),
    [`sheva-nah-before-bgdkft-dagesh`](#sheva-nah-before-bgdkft-dagesh)
    """
    if token.has(letter=T_BEGEDKEFET, dagesh=True) and isvowel(prev.vowel):
        _, guess.letter = T_BEGEDKEFET[token.letter]
        prev.isopen = False  # syntactic doubling closes previous syllable
        guess.dagesh = T.NAME_DAGESH_HAZAQ
        return guess


@rule("dagesh", "dagesh-is-mapiq-alef")
def dagesh_is_mapiq_alef(token, guess):
    """`dagesh` in `alef` is `mapiq-alef`

    This is a rare exception to the rule that guttural letters cannot
    receive a `dagesh`.

    Source: [Wikipedia-Mapiq]

    See also: [`dagesh-in-guttural`](#dagesh-in-guttural)
    """
    if token.has(letter=T.LETTER_ALEF, dagesh=True):
        return guess.update(letter=T.NAME_MAPIQ_ALEF, dagesh=T.NAME_MAPIQ)


@rule("dagesh", "dagesh-is-mapiq-he")
def dagesh_is_mapiq_he(token, guess, islast):
    """`dagesh` in **last** `he` is `mapiq-he`

    This is a somewhat common exception to the rule against `dagesh` in a
    guttural in which a `he` at the end of a word is emphasized.

    Source: [Simanim] 2.2
    > The `he` is sometimes also `nireh` after a `qamats`, `tsere`, or `holam`
    > and then it received a dot within it called a `mapiq`
    > and after a `tsere` and `holam` there is also a `patah-genuvah` under it.

    Source: [HaMillon] 1.6.3
    > `dagesh` that comes in the letter `he` at the end of the word
    > shows it is expressed and is not an `eim-qria`. This `dagesh` is called
    > a `mapiq` (which means "removes" because it removes the `he` from the rule
    > of `eim-qria` and expresses it like a captive).

    Source: [Wikipedia-Mapiq]

    See also: [`dagesh-in-guttural`](#dagesh-in-guttural)
    """
    if islast and token.has(letter=T.LETTER_HE, dagesh=True):
        return guess.update(letter=T.NAME_MAPIQ_HE, dagesh=T.NAME_MAPIQ)


@rule("dagesh", "dagesh-in-guttural")
def dagesh_in_guttural(prev, guess):
    """`dagesh` in a guttural is a **non-standard** `dagesh-hazaq`

    We consider the previous syllable closed because we assume this was
    meant to indicate gemination, even when this doesn't make sense in principle.

    Source: [Simanim] 1.3
    > `dagesh-hazaq` can be in any of the letters except for the letters
    > `alef`, `he`, `het`, `ayin`, `resh` that are not able to accept a `dagesh`,
    > but there are exceptions.

    Source: [Khan] I.3.1.1
    > _`dagesh`_ is not marked, however, on the laryngeals and
    > pharyngeals (אהעח in the Standard Tiberian tradition), except in
    > a few isolated cases to ensure correct reading [...].
    > In principle, therefore, these consonants are not geminated. [...]
    > The letter `resh`, like the laryngeal and pharyngeal consonants,
    > is generally not geminated by `dagesh`. Occasionally, however, the `resh`
    > does have dagesh [...].
    > When it is marked in cases such as these, it should be identified as
    > _`dagesh-hazaq`_, indicating the gemination of the consonant.

    See also: [`mapiq-alef`](#mapiq-alef), [`mapiq-he`](#mapiq-he)
    """
    if guess.has(letter=NON_DAGESH_LETTERS, dagesh=True):
        prev.isopen = False  # syntactic doubling closes previous syllable
        return guess.update(dagesh=T.NAME_DAGESH_HAZAQ)


@rule("dagesh", "dagesh-hazaq-default")
def dagesh_hazaq_default(prev, guess):
    """default `dagesh` is `dagesh-hazaq`

    Because `dagesh-qal` can only appear in BGDKFT letters, any other `dagesh`
    must be a `dagesh-hazaq`.
    """
    if T.NAME_DAGESH == guess.dagesh:
        prev.isopen = False  # syntactic doubling closes previous syllable
        return guess.update(dagesh=T.NAME_DAGESH_HAZAQ)
