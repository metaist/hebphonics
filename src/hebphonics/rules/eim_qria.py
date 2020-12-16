#!/usr/bin/env python
# coding: utf-8
"""Rules for non-voiced letters."""
# pylint: disable=inconsistent-return-statements

# pkg
from . import rule
from .. import tokens as T

## `vav` (`shuruq`, `holam-male`)

# These rules reset the next guess because the letter is actually
# a vowel for the previous letter.


@rule("vav", "eim-qria-vav-is-shuruq-start")
def vav_is_shuruq_start(isfirst, guess):
    """`vav` with `dagesh` at start of word of word is `shuruq`

    Source: [Simanim] 5.1
    > The `shuruq` at the start of a word that comes before a `sheva` or
    > before the letters `bet`, `mem`, `pe` it is called a `melofum-genuvah`
    > because it is read as if there was an `alef` before it.
    """
    if isfirst and guess.has(letter=T.NAME_VAV, dagesh=True, vowel=False):
        return guess.reset().update(vowel=T.NAME_SHURUQ, isopen=True)


@rule("vav", "eim-qria-vav-is-shuruq-middle")
def vav_is_shuruq(guess, next_guess):
    """`vav` with `dagesh` NOT after vowel is `shuruq`

    If a letter doesn't have a vowel on it, but the next letter is a `vav` with
    a `dagesh` (and no vowels of its own), then this letter's vowel is `shuruq`.

    Source: [Simanim] 2.1
    > A `vav` as part of a `melofum` or `holam`.

    Source: [HaMillon] 1.3
    > `vav` - an indication of the vowel `/u/` or `/o/`

    Source: [Gesenius] 12.1.note
    > `dagesh` in `vav` is easily distinguished from `shuruq`, which never admits
    > a vowel or `sheva` under the `vav`, or the letter next preceding it.
    """
    is_shuruq = next_guess.has(letter=T.NAME_VAV, dagesh=True, vowel=False)
    if not guess.vowel and is_shuruq:
        next_guess.reset()
        return guess.update(vowel=T.NAME_SHURUQ, isopen=True)


@rule("vav", "eim-qria-vav-is-holam-male")
def vav_is_holam_male(guess, next_guess):
    """`vav` with `holam` NOT after vowel is `holam-male-vav`

    If a letter doesn't have a vowel on it, but the next letter is a `vav` with
    a `holam` (and no `dagesh`), then this letter's vowel is `holam-male-vav`.

    Source: [Simanim] 2.1
    > A `vav` as part of a `melofum` or `holam`.

    Source: [HaMillon] 1.3
    > `vav` - an indication of the vowel `/u/` or `/o/`
    """
    is_holam = next_guess.has(letter=T.NAME_VAV, vowel=T.NAME_HOLAM, dagesh="")
    if not guess.vowel and is_holam:
        next_guess.reset()
        return guess.update(vowel=T.NAME_HOLAM_MALE_VAV, isopen=True)


# `eim-qria`


@rule("eim-qria", "eim-qria-yod-is-hiriq-male")
def hiriq_male(guess, next_guess):
    """`hiriq` before bare `yod` is `hiriq-male`

    Source: [Simanim] 1.1
    > - `hiriq` with a `yod` is `hiriq-gadol` and is a long vowel;
    > - `hiriq` without a `yod` is `hiriq-qatan` and is a short vowel
    """
    if guess.vowel == T.NAME_HIRIQ and next_guess.isbare(T.NAME_YOD):
        next_guess.update(letter=T.NAME_EIM_QRIA_YOD, isopen=True)
        return guess.update(vowel=T.NAME_HIRIQ_MALE_YOD)


@rule("eim-qria", "eim-qria-alef")
def eim_qria_alef(guess, next_guess, next_guess2):
    """bare `alef` after `qamats|patah|segol|tsere|holam|shuruq` is `eim-qria-alef`

    Source: [HaMillon] 1.3
    > `alef` - essentially an indication of the vowel `/a/` as in
    > [examples with `qamats`, `patah`] and sometimes also for other vowels as in
    > [examples with `segol`, `tsere`, `holam`, `shuruq`].
    """
    next_guess = next_guess or next_guess2
    if next_guess.isbare(T.NAME_ALEF) and guess.vowel in [
        T.NAME_QAMATS,
        T.NAME_QAMATS_GADOL,
        T.NAME_PATAH,
        T.NAME_SEGOL,
        T.NAME_TSERE,
        T.NAME_HOLAM,
        T.NAME_HOLAM_HASER,
        T.NAME_SHURUQ,
    ]:
        return next_guess.update(letter=T.NAME_EIM_QRIA_ALEF, isopen=True)


@rule("eim-qria", "eim-qria-he")
def eim_qria_he(guess, next_guess, next_guess2):
    """bare `he` after `qamats|patah|segol|tsere|holam` is `eim-qria-he`

    Source: [HaMillon] 1.3
    > `he` - an indication of the vowel `/a/` or `/e/` at the ends of words as in
    > [examples with `patah`, `qamats`, `segol`] and sometimes a semi-vowel `/ei/`
    > or the vowel `/o/` as in [examples with `tsere` and `holam`]
    """
    next_guess = next_guess or next_guess2
    if next_guess.isbare(T.NAME_HE) and guess.vowel in [
        T.NAME_QAMATS,
        T.NAME_QAMATS_GADOL,
        T.NAME_PATAH,
        T.NAME_SEGOL,
        T.NAME_TSERE,
        T.NAME_HOLAM,
        T.NAME_HOLAM_HASER,
    ]:
        return next_guess.update(letter=T.NAME_EIM_QRIA_HE, isopen=True)


@rule("eim-qria", "eim-qria-yod")
def eim_qria_yod(guess, next_guess):
    """bare `yod` after `hiriq|tsere|segol` is `eim-qria-yod`

    Source: [HaMillon] 1.3
    > `yod` - an indication of the vowel `/i/` or the semi-vowel `/ei/` as in
    > [examples with `hiriq`, `tsere`] and sometimes also the vowel `/e/` as in
    > [example with `segol`]
    """
    if next_guess.isbare(T.NAME_YOD) and guess.vowel in [
        T.NAME_HIRIQ,
        T.NAME_SEGOL,
        T.NAME_TSERE,
    ]:
        return next_guess.update(letter=T.NAME_EIM_QRIA_YOD, isopen=True)
