#!/usr/bin/env python
# coding: utf-8
"""Rules for `qamats`."""
# pylint: disable=inconsistent-return-statements

# pkg
from . import has_sequence, isvowel, rule
from .. import tokens as T


## `qamats-gadol`


@rule("qamats", "qamats-gadol-dagesh-hazaq")
def qamats_gadol_dagesh_hazaq(guess):
    """`qamats` under `dagesh-hazaq` is `qamats-gadol`

    `dagesh-hazaq` emphasizes the letter, so it must be a `qamats-gadol`.
    """
    if guess.has(dagesh=T.NAME_DAGESH_HAZAQ, vowel=T.NAME_QAMATS):
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-yod-glide")
def qamats_gadol_yod_glide(guess, next_guess):
    """`qamats` before `yod-glide` is `qamats-gadol`

    `yod-glide` emphasizes the `qamats`, so it must be a `qamats-gadol`.
    """
    if T.NAME_QAMATS == guess.vowel and next_guess.letter == T.NAME_YOD_GLIDE:
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-mapiq-he")
def qamats_gadol_mapiq_he(guess, next_guess):
    """`qamats` before `mapiq-he` is `qamats-gadol`

    Source: [HaMillon] 1.6.3
    > `dagesh` that comes in the letter `he` at the end of the word
    > shows it is expressed and is not an `eim-qria` (_matres lectionis_).
    """
    if guess.vowel == T.NAME_QAMATS and next_guess.has(
        letter=T.NAME_MAPIQ_HE, vowel=False
    ):
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-eim-qria")
def qamats_gadol_eim_qria(guess, next_guess):
    """`qamats` before `eim-qria` is `qamats-gadol`

    `eim-qria` after a `qamats` indicates a `qamats-gadol`.
    """
    letters = [T.NAME_EIM_QRIA_ALEF, T.NAME_EIM_QRIA_HE, T.NAME_EIM_QRIA_YOD]
    if T.NAME_QAMATS == guess.vowel and next_guess.letter in letters:
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-vowel")
def qamats_gadol_vowel(guess, next_guess, islast):
    """`qamats` before a vowel (or is final vowel) is `qamats-gadol`

    The general rule is that a `qamats` in an open syllable or accented
    syllable is a `qamats-gadol`. A syllable is closed by a letter with
    no vowel or possibly a `sheva`. Therefore, a `qamats` on the last
    letter of a word or a `qamats` that is followed immediately by another
    vowel must be part of an open syllable.
    """
    if T.NAME_QAMATS == guess.vowel and (islast or isvowel(next_guess.vowel)):
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-meteg")
def qamatas_gadol_meteg(has_accents, guess, token):
    """`qamats` with `meteg` is `qamats-gadol`

    Requires: accent information

    Source: [Simanim] 1.5
    > a `meteg` is a line located under a letter on the left side of a vowel [...]
    > and it indicates to lengthen a little bit the syllable under which it is located

    Source: [Simanim] 7.2
    > and in this a `qamats-qatan` is distinguished from `qamats-gadol` [...]
    > and it [a `qamats-qatan`] does not have a `meteg`
    """
    if has_accents and T.NAME_QAMATS == guess.vowel and T.POINT_METEG in token.points:
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-accent")
def qamatas_gadol_accent(has_accents, guess, token):
    """`qamats` with accent is `qamats-gadol`

    Requires: accent information

    Source: [Simanim] 7.2
    > and in this a `qamats-qatan` is distinguished from `qamats-gadol` [...]
    > and it [a `qamats-qatan`] does not have an accent
    """
    if has_accents and T.NAME_QAMATS == guess.vowel and token.accents:
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-next-accent")
def qamats_gadol_next_accent(has_accents, idx, guess, next_guess, tokens, next_token):
    """`qamats` with first accent on next non-vowel letter is `qamats-gadol`

    This rule is essentially the same as [`qamats-gadol-accent`](#qamats-gadol-accent),
    but it handles the case in which the syllable is closed by another letter which
    has the accent.

    Requires: accent information

    See also: [`qamats-gadol-accent`](#qamats-gadol-accent)
    """
    if (
        has_accents
        and T.NAME_QAMATS == guess.vowel
        and not isvowel(next_guess.vowel)
        and next_token.accents  # has accent
        and not tokens[:idx].accents.flat()  # is first accent
    ):
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats", "qamats-gadol-telisha-gedola")
def qamatas_gadol_telish_gedola(has_accents, idx, tokens, guess):
    """`qamats` in word with `telisha-gedola` is `qamats-gadol`

    `telisha-gedola` appears only the first letter of a word (it is _prepositive_).
    In some texts (e.g., [Simanim]), the accent is helpfully indicated over the
    emphasized letter, but in most texts it is not. This rule captures those
    small number of cases where it matters.

    Source: [Gesenius] 15.3.A.IV.18
    > Great _Telisha_ is categorized under:
    >
    > - A. Distinctives (_Domini._)
    > - Class IV. Smallest Distinctives (_Comites_)
    > - _prepositive_

    Source: [Gesenius] 15.3.remarks.I.2
    > Most of the accents stand on the tone-syllable, and properly on its
    > initial consonant. Some, however, stand only on the first letter of a word
    > (_prepositive_), others only on the last letter (_postpositive_).
    """
    if (
        has_accents
        and T.NAME_QAMATS == guess.vowel
        and T.ACCENT_TELISHA_GEDOLA in tokens[:idx].accents.flat()
    ):
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


@rule("qamats2", "qamats-gadol-before-sheva-na")
def qamats_gadol_before_sheva_na(idx, guess, guesses):
    """`qamats` before `sheva-na` without `dagesh` is `qamats-gadol`

    This rule is applied after we resolve `sheva` and is an inverse of
    [`sheva-na-after-long-vowel`](#sheva-na-after-long-vowel).
    """
    pattern = [
        {"vowel": T.NAME_QAMATS},
        {"dagesh": False, "vowel": T.NAME_SHEVA_NA},
    ]
    if has_sequence(idx, guesses, pattern):
        return guess.update(vowel=T.NAME_QAMATS_GADOL)


## `qamats-qatan`


@rule("qamats", "qamats-qatan-in-maqaf")
def qamats_qatan_in_maqaf(has_maqaf, token, guess, next_guess):
    """`qamats` in closed syllable in non-last word with `maqaf` is `qamats-qatan`

    The general rule is that a `qamats` in an unaccented closed syllable
    is a `qamats-qatan`.  A word connected to another word with a `maqaf` is
    unaccented, so when there's no `meteg` on the `qamats` and the syllable
    is closed, this is our best guess that it is a `qamats-qatan`.

    Requires: accent information

    Source: [Simanim] 1.6
    > a `maqaf` is a line placed in the middle of the line height between two words [...]
    > the first word of the connected words is without accent rather the accent is
    > always on the last word of the words connected with a `maqaf`

    Source: [Gesenius] 9.1
    > In distinguishing `qamets` (`/a/`) and from `qamats-qatan` (`/o/`), a knowledge
    > of grammatical forms is the only sure guide; but to the learner the following
    > general rule may be of service; viz.
    > The sign (`qamats`) _is `/o/` in a closed, unaccented syllable_; for such a
    > syllable cannot have a long vowel, section 26, 3.

    See also:
    [`qamats-gadol-meteg`](#qamats-gadol-meteg),
    [`qamats-gadol-accent`](#qamats-gadol-accent)
    """
    if (
        T.NAME_QAMATS == guess.vowel
        and has_maqaf
        and (not guess.isopen or not next_guess.isopen)
        and T.POINT_METEG not in token.points
    ):
        guess.vowel = T.NAME_QAMATS_QATAN
        return guess


@rule("qamats", "qamats-qatan-closed-unaccented")
def qamatas_qatan_closed_unaccented(
    has_accents, idx, islast, token, tokens, guess, next_guess
):
    """`qamats` in an unaccented, closed syllable is `qamats-qatan`

    Source: [Simanim] 7.2
    > and similarly `qamats-qatan` cannot receive accent [...]
    > and in this a `qamats-qatan` is distinguished from `qamats-gadol`:
    > every `qamats` in a closed syllable, that does not have an accent,
    > and does not have a `meteg`, it is a `qamats-qatan`.

    Requires: accent information
    """
    closed = not islast and next_guess.has(isopen=False, vowel=["", T.NAME_SHEVA_NAH])
    prev_accents = tokens[:idx].accents.flat()

    unaccented = (
        not T.POINT_METEG in token.points
        and not token.accents
        and T.ACCENT_TELISHA_GEDOLA not in prev_accents
    )
    if has_accents and T.NAME_QAMATS == guess.vowel and unaccented and closed:
        return guess.update(vowel=T.NAME_QAMATS_QATAN)


@rule("qamats", "qamats-qatan-before-dagesh-sheva")
def qamats_qatan_before_dagesh_sheva(token, guess, next_guess):
    """`qamats` without accent or `meteg` before `dagesh` + `sheva` is `qamats-qatan`

    There is a chain of logic that establishes this `qamats` as a `qamats-qatan`:

    - We don't yet know if the `sheva` is a `sheva-na` or `sheva-nah`.
    - But the subsequent letter has a `dagesh`.
    - This `dagesh` must be a `dagesh-hazaq` either because:
        - it is in a BGDKFT letter after a vowel, per
          [`dagesh-hazaq-bgdkft`](#dagesh-hazaq-bgdkft)
        - or because it is some other letter which always gets a `dagesh-hazaq`,
          per [`dagesh-hazaq-default`](#dagesh-hazaq-default)
    - And every letter with a `dagesh-hazaq` is syntactically doubled, per [Simanim] 1.3
    - And it is as if there was a `sheva-nah` and then a `sheva-na`, per [Simanim] 3.1
    - Therefore, the previous syllable is closed (the one containing this `qamats`).
    - So if it does not have any accents, it is a `qamats-qatan`.

    ---

    Source: [Simanim] 1.3
    > because every letter written with a `dagesh-hazaq` is read as double:
    > once with a with a `sheva-nah` and then again with the vowel

    Source: [Simanim] 3.1
    > `sheva` on a letter that has a `dagesh-hazaq` is a `sheva-na` because the
    > `dagesh` doubles the letter and makes it as though there is a double `sheva`;
    > and a double `sheva` in the middle of a word is `sheva-nah`, `sheva-na`.
    """
    if (
        T.NAME_QAMATS == guess.vowel
        and not T.POINT_METEG in token.points
        and not token.accents
        and next_guess.has(dagesh=True, vowel=T.NAME_SHEVA)
    ):
        return guess.update(vowel=T.NAME_QAMATS_QATAN)


# @rule("qamats", "qamats-qatan-before-hataf-qamats")
# def qamats_qatan_before_hataf_qamats(token, guess, next_guess):
#     """`qamats` without meteg immediately before `hataf-qamats` is `qamats-qatan`"""
#     if (
#         T.NAME_QAMATS == guess.vowel
#         and T.POINT_METEG not in token.points
#         and T.NAME_HATAF_QAMATS == next_guess.vowel
#     ):
#         return guess.update(vowel=T.NAME_QAMATS_QATAN)


@rule("qamats2", "qamats-qatan-before-sheva-nah")
def qamats_qatan_before_sheva_nah(guess, next_guess):
    """`qamats` before `sheva-nah` is `qamats-qatan`

    This rule is applied after we resolve `sheva` and is an inverse of
    [`sheva-nah-after-short-vowel`](#sheva-nah-after-short-vowel).
    """
    if T.NAME_QAMATS == guess.vowel and next_guess.vowel.startswith(T.NAME_SHEVA_NAH):
        return guess.update(vowel=T.NAME_QAMATS_QATAN)
