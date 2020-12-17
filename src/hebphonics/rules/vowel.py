#!/usr/bin/env python
# coding: utf-8
"""Rules for glides and other general vowel rules."""
# pylint: disable=inconsistent-return-statements

# pkg
from . import rule
from .. import tokens as T


## vowel (`holam-haser`, `patah-genuvah`)


@rule("vowel", "vowel-holam-haser-default")
def holam_haser_default(guess):
    """default `holam` is `holam-haser`

    Any `holam` that is not a `holam-male` is a `holam-haser`.
    """
    if guess.vowel == T.NAME_HOLAM:
        return guess.update(vowel=T.NAME_HOLAM_HASER, isopen=True)


@rule("vowel", "vowel-patah-genuvah")
def patah_genuvah(guess, islast):
    """`patah` on last `het|ayin|mapiq-he` is `patah-genuvah`

    Source: [Simanim] 5.1
    > If one of the letters `he`, `het`, `ayin` is at the end of the word
    > and the vowel before it is a `tsere`, `hiriq`, `holam`, or `shuruq` then
    > underneath it is a `patah` and it is called `patah-genuvah` because it is
    > read as if an `alef` with a `patah` was written before the `he`, `het`, or `ayin`
    > [...]
    """
    check = [T.NAME_HET, T.NAME_AYIN, T.NAME_MAPIQ_HE]
    if islast and guess.has(letter=check, vowel=T.NAME_PATAH):
        return guess.update(vowel=T.NAME_PATAH_GENUVAH, isopen=False)  # constant sound


## glides

# NOTE: We unroll these rules for indexing purposes.


@rule("vowel", "glide-av")
def glide_av(guess, next_guess, next_guess2):
    """bare `yod` after `qamats` before `vav` is `yod-glide`"""
    if (
        guess.vowel in [T.NAME_QAMATS, T.NAME_QAMATS_GADOL]
        and next_guess.isbare(T.NAME_YOD)
        and next_guess2.isbare(T.NAME_VAV)
    ):
        return next_guess.update(letter=T.NAME_YOD_GLIDE, isopen=True)


@rule("vowel", "glide-ai-qamats")
def glide_ay_qamats(guess, next_guess):
    """bare `yod` after `qamats` is `yod-glide`"""
    if guess.vowel == T.NAME_QAMATS and next_guess.isbare(T.NAME_YOD):
        return next_guess.update(letter=T.NAME_YOD_GLIDE, isopen=True)


@rule("vowel", "glide-ai-patah")
def glide_ay_patah(guess, next_guess):
    """bare `yod` after `patah` is `yod-glide`"""
    if guess.vowel == T.NAME_PATAH and next_guess.isbare(T.NAME_YOD):
        return next_guess.update(letter=T.NAME_YOD_GLIDE, isopen=True)


@rule("vowel", "glide-aiy")
def glide_aiy(guess, next_guess):
    """`yod+hiriq` after `patah` is `yod-glide`"""
    if guess.vowel == T.NAME_PATAH and next_guess.has(
        letter=T.NAME_YOD, vowel=T.NAME_HIRIQ
    ):
        return next_guess.update(letter=T.NAME_YOD_GLIDE, isopen=True)


@rule("vowel", "glide-oy")
def glide_oy(guess, next_guess2):
    """bare `yod` after `holam` is `yod-glide`"""
    if guess.vowel == T.NAME_HOLAM_MALE_VAV and next_guess2.isbare(T.NAME_YOD):
        return next_guess2.update(letter=T.NAME_YOD_GLIDE, isopen=True)


@rule("vowel", "glide-uy")
def glide_uy(idx, guess, next_guess2):
    """bare `yod` after `shuruq` is `yod-glide`"""
    if idx >= 1 and guess.vowel == T.NAME_SHURUQ and next_guess2.isbare(T.NAME_YOD):
        return next_guess2.update(letter=T.NAME_YOD_GLIDE, isopen=True)
