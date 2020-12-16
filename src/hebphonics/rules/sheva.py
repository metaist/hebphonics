#!/usr/bin/env python
# coding: utf-8
"""Rules for `sheva`."""
# pylint: disable=inconsistent-return-statements

# pkg
from .. import tokens as T
from . import (
    has_ending,
    has_sequence,
    issimilar,
    rule,
    NIQQUD_HATAF,
    NIQQUD_LONG,
    NIQQUD_SHORT,
    NIQQUD_TYPES,
    GUTTURAL_LETTERS,
    PREFIX_MORPHEMES,
    SONORORANT_LETTERS,
    T_BEGEDKEFET,
    T_GLOTTAL_LETTERS,
)

## `sheva`


@rule("sheva", "sheva-gaya")
def sheva_gaya(token, guess):
    """`sheva` with a `meteg` is a `sheva-gaya`

    Source: [Wikipedia-Sheva] Shva Ga'ya
    > `sheva-gaya` designates a `sheva` marked under a letter that is
    > also marked with the cantillation mark `ga'ya`, or `meteg` [...].
    > This "strict application" is found in Yemenite Hebrew.
    """
    if guess.vowel == T.NAME_SHEVA and T.POINT_METEG in token.points:
        return guess.update(vowel=T.NAME_SHEVA_GAYA)


@rule("sheva", "sheva-merahef")
def sheva_merahef(last_vowel, guess, next_token):
    """`sheva` without `dagesh` between short vowel and BGDKFT without `dagesh` is `sheva-merahef`

    Source: [Wikipedia-Sheva] Shva Meraḥef
    > `sheva-merahef` is the grammatical designation of a `sheva` which does not comply
    > with all criteria characterizing a `sheva-na` (specifically, one marked under a
    > letter following a letter marked with a "short", not a "long", niqqud-variant),
    > but which does, like a `shva-na`, supersede a vowel (or a `shva-na`) that exists
    > in the basic form of a word but not after this word underwent inflection or
    > declension.
    >
    > The classification of a `sheva` as `sheva-merahef` is relevant to the
    > application of standard niqqud, e.g.: a בג״ד כפ״ת letter following a letter
    > marked with a `sheva-merahef` should not be marked with a `dagesh-qal`, although
    > the vowel preceding this letter could be represented by the "short"
    > niqqud-variant for that vowel.
    """
    if (
        guess.has(vowel=T.NAME_SHEVA, dagesh=False)
        and NIQQUD_TYPES.get(last_vowel) in [NIQQUD_SHORT, NIQQUD_HATAF]
        and next_token.has(letter=T_BEGEDKEFET, dagesh=False)
        and next_token.vowel != T.POINT_SHEVA
    ):
        return guess.update(vowel=T.NAME_SHEVA_MERAHEF, isopen=False)


# @rule("sheva", "sheva-na-after-meteg")
# def sheva_na_after_meteg(token, next_guess):
#     """`sheva` after a `meteg` is `sheva-na`

#     **NOTE**: This rule is disabled by default.

#     Source: [Simanim] 3.4
#     > every `sheva` after a `meteg` is a `sheva-na` whether the vowel with
#     > the `meteg` is a long vowel or a short vowel, it is a `sheva-na`
#     """
#     if T.POINT_METEG in token.points and next_guess.vowel == T.NAME_SHEVA:
#         return next_guess.update(vowel=T.NAME_SHEVA_NA)


@rule("sheva2", "sheva-modern-double-sound")
def sheva_na_double_sound(guess, next_guess):
    """`sheva` before a similar sounding letter is voiced

    This rule applies to modern Hebrew and would supercede
    [`sheva-double-end`](#sheva-double-end) (ex: שָׁדַדְתְּ). However, we apply
    this rule much later to maintain the traditional categorization.

    Source: [Wikipedia-Sheva] Condition 1
    > When under the first of two letters, both representing the same
    > consonant or consonants with identical place and manner of
    > articulation.
    """
    if guess.vowel.startswith(T.NAME_SHEVA) and issimilar(
        guess.letter, next_guess.letter
    ):
        # guess.vowel += "-voiced"
        return guess

        # if guess.vowel == T.NAME_SHEVA:
        #     return guess.update(vowel=T.NAME_SHEVA_NA_VOICED)
        # if guess.vowel == T.NAME_SHEVA_NAH:
        #     return guess.update(vowel=T.NAME_SHEVA_NAH_VOICED)


@rule("sheva2", "sheva-modern-voiced-sonorant")
def sheva_modern_voiced_sonorant(isfirst, guess):
    """`sheva` at word start when it is on a sonorant letter is voiced

    This rule applies to modern Hebrew.

    Source: [Wikipedia-Sheva] Condition 2
    > When under the first letter of a word, if this letter is a sonorant
    > in modern pronunciation: `yod`, `lamed`, `mem`, `nun`, `resh`.
    """
    if isfirst and guess.has(vowel=T.NAME_SHEVA_NA, letter=SONORORANT_LETTERS):
        # guess.vowel += "-voiced"
        return guess
        # return guess.update(vowel=T.NAME_SHEVA_NA)  # per traditional rules


@rule("sheva2", "sheva-modern-voiced-before-glottal")
def sheva_na_start_before_glottal(isfirst, guess, next_token):
    """`sheva` at word start before glottal letter is voiced

    This rule applies to modern Hebrew.

    Source: [Wikipedia-Sheva] Condition 3
    > When under the first letter of a word, if the second letter is a glottal
    > consonant: `alef`, `he`, `ayin`.
    """
    if (
        isfirst
        and guess.vowel == T.NAME_SHEVA_NA
        and next_token.letter in T_GLOTTAL_LETTERS
    ):
        return guess
        # return guess.update(vowel=T.NAME_SHEVA_NA)  # per traditional rules


@rule("sheva2", "sheva-modern-voiced-prefix")
def sheva_modern_voiced_prefix(isfirst, guess):
    """`sheva` at word start when it is a prefix-morpheme is voiced

    This rule applies to Modern Hebrew.

    **NOTE**: We do not know if this letter is part of the root or is a prefix.

    Source: [Wikipedia-Sheva] Condition 4
    > When under the first letter of a word, if this letter represents one of
    > the prefix-morphemes: `bet`, `vav`, `khaf`, `lamed`
    """
    if isfirst and guess.has(vowel=T.NAME_SHEVA_NA, letter=PREFIX_MORPHEMES):
        return guess
        # return guess.update(vowel=T.NAME_SHEVA_NA)  # per traditional rules


@rule("sheva2", "sheva-modern-muted")
def sheva_modern_muted(isfirst, guess):
    """`sheva` at word start when no other condition applies is muted

    This rule applies to Modern Hebrew.
    """
    if isfirst and guess.vowel == T.NAME_SHEVA_NA:
        return guess


@rule("sheva", "sheva-na-start")
def sheva_na_start(isfirst, guess):
    """`sheva` at word start is `sheva-na`

    Source: [Simanim] 3.1.1
    > every `sheva` at the start of a word is a `sheva-na`

    Source: [HaMillon] 2.16.1
    > `sheva` at the start of a word is `sheva-na`
    """
    if isfirst and guess.vowel == T.NAME_SHEVA:
        return guess.update(vowel=T.NAME_SHEVA_NA)


@rule("sheva", "sheva-nah-end")
def sheva_nah_end(islast, guess):
    """`sheva` at word end is `sheva-nah`

    Source: [HaMillon] 2.16.1
    > `sheva` at the end of a word is `sheva-nah`
    """
    if islast and guess.vowel == T.NAME_SHEVA:
        return guess.update(vowel=T.NAME_SHEVA_NAH, isopen=False)


@rule("sheva", "sheva-nah-alef-end")
def sheva_nah_alef_end(neg_idx, guess, next_guess):
    """`sheva` before last bare `alef` is `sheva-nah`

    This rule is an extension of [`sheva-nah-end`](#sheva-nah-end);
    the `alef` is acting like an `eim-qria-alef` and doesn't add a sound.
    """
    if neg_idx == 1 and guess.vowel == T.NAME_SHEVA and next_guess.isbare(T.NAME_ALEF):
        guess.vowel = T.NAME_SHEVA_NAH
        next_guess.isopen = False
        return guess


@rule("sheva", "sheva-double-end")
def sheva_double_end(neg_idx, guess, next_guess):
    """two `sheva` at word end are `sheva-nah`, `sheva-nah`

    This rule is a combination of [`sheva-double-middle`](#sheva-double-middle)
    and [`sheva-nah-end`](#sheva-nah-end).
    """
    if (
        neg_idx == 1
        and guess.vowel == T.NAME_SHEVA
        and next_guess.vowel == T.NAME_SHEVA
    ):
        guess.update(vowel=T.NAME_SHEVA_NAH, isopen=False)
        next_guess.update(vowel=T.NAME_SHEVA_NAH, isopen=False)
        return guess


@rule("sheva", "sheva-na-double-letter")
def sheva_na_double_letter(guess, next_guess):
    """`sheva` before same letter is `sheva-na`

    Source: [Simanim] 3.1.5
    > Two of the same letter, and the first one has a `sheva`, it is a `sheva-na`
    > because you cannot read them with a `sheva-nah` for then the first of
    > the letters will be swallowed in the pronunciation.
    """
    if guess.has(
        vowel=T.NAME_SHEVA, letter=next_guess.letter
    ) and not next_guess.vowel.startswith(T.NAME_SHEVA):
        return guess.update(vowel=T.NAME_SHEVA_NA)


@rule("sheva", "sheva-double-middle")
def sheva_double_middle(neg_idx, guess, next_guess):
    """two `sheva` midword are `sheva-nah`, `sheva-na`

    Source: [Simanim] 3.1.2
    > Two `sheva` in the middle of a word are `sheva-nah`, `sheva-na`.

    Source: [HaMillon] 2.16.2
    > Two `sheva` in the middle of a word, the first is `sheva-nah`, the second is
    > `sheva-na`.
    """
    if (
        neg_idx > 1
        and guess.vowel in [T.NAME_SHEVA, T.NAME_SHEVA_MERAHEF]
        and next_guess.vowel == T.NAME_SHEVA
    ):
        guess.update(vowel=T.NAME_SHEVA_NAH, isopen=False)
        next_guess.vowel = T.NAME_SHEVA_NA
        return guess


@rule("sheva", "sheva-na-dagesh-hazaq")
def sheva_na_dagesh_hazaq(guess):
    """`sheva` under `dagesh-hazaq` is `sheva-na`

    `sheva` under `dagesh-qal` is also usually a `sheva-na` except at the end
    of a word where it is a `sheva-nah`.

    Source: [Simanim] 3.1.4
    > `sheva` on a letter that has a `dagesh-hazaq` is a `sheva-na` because the
    > `dagesh` doubles the letter and makes it as though there is a double
    > `sheva` and a double `sheva` in the middle of a word is `sheva-nah`, `sheva-na`

    Source: [HaMillon] 2.16.4
    > `sheva` under a letter with a `dagesh-hazaq` is always a `sheva-na`.
    """
    if guess.has(vowel=T.NAME_SHEVA, dagesh=T.NAME_DAGESH_HAZAQ):
        return guess.update(vowel=T.NAME_SHEVA_NA)


# @rule("sheva", "sheva-nah-yod-after-he")
# def sheva_nah_yod_after_he(prev, guess):
#     """`sheva` under `yod` with no `dagesh` after `he` is `sheva-nah`

#     Source: [Simanim] 3.1.4
#     > every `yod` with a `sheva` that is after a `he`, if it doesn't have a `dagesh`,
#     > is a `sheva-nah`
#     """
#     if (
#         guess.has(letter=T.NAME_YOD, dagesh=False, vowel=T.NAME_SHEVA)
#         and prev.letter == T.NAME_HE
#     ):
#         return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-after-shuruq-start")
def sheva_nah_after_shuruq_start(idx, prev, guess):
    """`sheva` after shuruq at word start in non-dagesh letter is `sheva-nah`

    This rule follows the Minchat Shai who does NOT classify a `sheva` preceded
    by a `meteg` as a `sheva-na`.

    Source: [Simanim] 3.7
    > A `vav` that is a `shuruq` at the start of a word, and after it a `sheva`,
    > like in [...] the `sheva` is a `sheva-nah`.
    """
    if (
        idx == 1  # 2nd letter
        and prev.vowel == T.NAME_SHURUQ
        and guess.has(vowel=T.NAME_SHEVA, dagesh=False)
    ):
        return guess.update(vowel=T.NAME_SHEVA_NAH, isopen=False)


@rule("sheva", "sheva-nah-after-short-vowel")
def sheva_nah_after_short_vowel(last_vowel, guess):
    """`sheva` after short vowel is `sheva-nah`

    Source: [Simanim] 3.5
    > According to the opinion of the _Minchat Shai_, after a short vowel it
    > is a `sheva-nah` even when there is a `meteg` near the short vowel.

    Source: [HaMillon] 2.16.3
    > `sheva` after a short vowel is `sheva-nah` [...].
    """
    if guess.vowel == T.NAME_SHEVA and NIQQUD_TYPES.get(last_vowel) in [
        NIQQUD_SHORT,
        NIQQUD_HATAF,
    ]:
        return guess.update(vowel=T.NAME_SHEVA_NAH, isopen=False)


@rule("sheva", "sheva-nah-after-accent")
def sheva_nah_after_accent(has_accents, prev_token, guess):
    """`sheva` after accent is `sheva-nah`

    Requires: accent information

    Source: [Simanim] 3.1.3
    > If there is an accent before the `sheva`, whether or not it is a long
    > vowel or short vowel, it is a `sheva-nah`.
    """
    if (
        has_accents
        and guess.vowel == T.NAME_SHEVA
        and prev_token.accents
        and T.ACCENT_MUNAH not in prev_token.accents
    ):
        return guess.update(vowel=T.NAME_SHEVA_NAH, isopen=False)


@rule("sheva", "sheva-nah-before-bgdkft-dagesh")
def sheva_nah_before_bgdkft_dagesh(guess, next_token):
    """`sheva` before BGDKFT with `dagesh` is `sheva-nah`

    While the actual rule requires a `dagesh-qal`, we can actually infer that
    any `dagesh` in BGDKFT after a `sheva` must be a `dagesh-qal` and the `sheva`
    is a `sheva-nah` based on the description in [HaMillon] 2.17.

    **NOTE**: The converse of this rule--`sheva` before BGDKFT _without_ `dagesh` is
    `sheva-na`--is not reliable.

    Source: [Simanim] 1.3
    > Every `dagesh` in the middle of a word after a `sheva-nah` is `dagesh-qal`
    > because it is like the start of a word after there is a little break with
    > the `sheva-nah`.

    Source: [HaMillon] 2.17
    > Our sages of pointing instituted a clear rule: "The letters BGDKFT receive
    > a `dagesh-qal` when they come at the start of a word and when they come in the
    > middle of a word if and only if they come after a `sheva-nah`.
    >
    > This rule is called "The Principle of BGDKFT" and its great importance is that
    > it can establish the type of `sheva` that occurs before these letters, for it
    > is clear that: If we pronounce them hard, and before them is a `sheva`, there
    > is no doubt that we have in our hands a `sheva-nah`!
    """
    if guess.vowel == T.NAME_SHEVA and next_token.has(letter=T_BEGEDKEFET, dagesh=True):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-na-after-long-vowel")
def sheva_na_after_long_vowel(last_vowel, prev, guess):
    """`sheva` after long vowel is `sheva-na`

    Source: [Simanim] 3.1.3
    > `sheva` after a long vowel without an accent is a `sheva-na`.

    Source: [HaMillon] 2.16.3
    > `sheva` after a long vowel is `sheva-na`.
    """
    if (
        guess.vowel == T.NAME_SHEVA
        and NIQQUD_LONG == NIQQUD_TYPES.get(last_vowel)
        and prev.vowel != T.NAME_QAMATS  # because it's unclassified
    ):
        return guess.update(vowel=T.NAME_SHEVA_NA)


## `sheva-na` endings (implies `qamats-gadol`)


@rule("sheva", "sheva-na-ending-sah")
def sheva_na_ending_sah(neg_idx, guess, guesses):
    """`sheva` before `sav+qamats`, `he` is `sheva-na`

    This rule was emperically checked for the Pentateuch.

    Example: פָשְׂתָה ([Leviticus 13:28])
    """
    pattern = pattern = [
        {"vowel": T.NAME_SHEVA},
        {"letter": T.NAME_SAV, "vowel": T.NAME_QAMATS_GADOL},
        {"letter": T.NAME_EIM_QRIA_HE},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NA)


@rule("sheva", "sheva-na-ending-a|kh|l|f-ah")
def sheva_na_ending_alkhf_ah(neg_idx, prev, guess, guesses):
    """`sheva` after `gimel|yod|mem` before `alef|khaf|lamed|fe + qamats`, `he` is `sheva-na`

    This rule was emperically checked for the Pentateuch.

    The purpose of this rule is to capture the exceptions to the
    [`sheva-nah-ending-ah`](#sheva-nah-ending-ah) rule.

    See also: [`sheva-nah-ending-ah`](#sheva-nah-ending-ah)

    Examples:

        - `/ga-lah/`: גָדְלָה ([Genesis 19:13])
        - `/ya-lah/`: יָכְלָה ([Exodus 2:3])
        - `/ya-fah`: יָסְפָה ([Genesis 8:12])
        - `/ma-ah/`: מָלְאָה ([Genesis 6:13])
        - `/ma-khah`: מָשְׁכָה ([Deuteronomy 21:3])
    """
    prev_letters = [T.NAME_GIMEL, T.NAME_YOD, T.NAME_MEM]
    letters = [T.NAME_ALEF, T.NAME_KHAF, T.NAME_LAMED, T.NAME_FE]
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"letter": letters, "vowel": [T.NAME_QAMATS, T.NAME_QAMATS_GADOL]},
        {"letter": T.NAME_EIM_QRIA_HE},
    ]
    if prev.letter in prev_letters and has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NA)


@rule("sheva", "sheva-na-ending-u")
def sheva_na_shuruq_end(neg_idx, guess, guesses):
    """`sheva` before `shuruq` at end of word is `sheva-na`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [{"vowel": T.NAME_SHEVA}, {"vowel": T.NAME_SHURUQ}]
    if has_ending(neg_idx, guesses, pattern, extra=1):  # include shuruq
        return guess.update(vowel=T.NAME_SHEVA_NA)


@rule("sheva", "sheva-na-ending-l|sh|s-kha")
def sheva_na_khaf_sofit_qamats(idx, neg_idx, guess, guesses):
    """`sheva` on `lamed|shin|sav` before `khaf-sofit+qamats-gadol` is `sheva-na`

    This rule was emperically checked for the Pentateuch.

    Examples:

        - `/lkha/`: יִשְׁאָלְךָ ([Deuteronomy 6:20])
        - `/shkha/`: יִירָשְׁךָ ([Genesis 15:4])
        - `/skha/`: בְּכֹרָתְךָ ([Genesis 25:31])
    """
    pattern = [
        {
            "letter": [T.NAME_LAMED, T.NAME_SHIN, T.NAME_TAV, T.NAME_SAV],
            "vowel": T.NAME_SHEVA,
        },
        {"letter": T.NAME_KHAF_SOFIT, "vowel": T.NAME_QAMATS_GADOL},
    ]
    if idx > 2 and has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NA)


@rule("sheva", "sheva-na-ending-eim")
def sheva_na_tsere_mem_sofit(neg_idx, prev, guess, guesses):
    """`sheva` after non-guttural before `tsere`, `mem-sofit` is `sheva-na`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_TSERE},
        {"letter": T.NAME_MEM_SOFIT},
    ]
    if prev.letter not in GUTTURAL_LETTERS and has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NA)


## `sheva-nah` endings (implies `qamats-qatan`)


### `he`


@rule("sheva", "sheva-nah-ending-iyah")
def sheva_nah_ending_iah(neg_idx, guess, guesses):
    """`sheva` before `hiriq`, `yod+qamats`, `he` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_HIRIQ},
        {"letter": T.NAME_YOD, "vowel": T.NAME_QAMATS_GADOL},
        {"letter": T.NAME_EIM_QRIA_HE},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-ah")
def sheva_nah_ending_ah(neg_idx, guess, guesses):
    """`sheva` before `qamats`, `he` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    See also: [`sheva-na-ending-a|kh|l|f-ah`](#sheva-na-ending-a|kh|l|f-ah)

    Examples:

        - `/ah/`: וְהָרְאָה ([Leviticus 13:49])
        - `/vah/`: נָקְבָה
        - `/kha/`: קָרְחָה
        - `/kha/`: שָׁפְכָה
        - `/la/`: עָרְלָה
        - `/ma/`: בְעָרְמָה
        - `/na/`: אָמְנָה
        - `/a/`: וְצָרְעָה
        - `/tsa/`: לְרָחְצָה
        - `/qa/`: בְּדָפְקָה
        - `/ra/`: וְעָפְרָה
    """
    # letters = [
    #     T.NAME_ALEF,
    #     T.NAME_VET,
    #     T.NAME_HET,
    #     T.NAME_KHAF,
    #     T.NAME_LAMED,
    #     T.NAME_MEM,
    #     T.NAME_NUN,
    #     T.NAME_AYIN,
    #     T.NAME_TSADI,
    #     T.NAME_QOF,
    #     T.NAME_RESH,
    # ]
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_QAMATS_GADOL},
        {"letter": T.NAME_EIM_QRIA_HE},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


### `vav`


@rule("sheva", "sheva-nah-ending-o")
def sheva_nah_ending_o(neg_idx, guess, guesses):
    """`sheva` before `holam-male` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    Example: אָזְנוֹ ([Exodus 21:6])
    """
    pattern = [{"vowel": T.NAME_SHEVA}, {"vowel": T.NAME_HOLAM_MALE_VAV}]
    if has_ending(neg_idx, guesses, pattern, extra=1):  # include holam-male
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-av")
def sheva_nah_ending_av(neg_idx, guess, guesses):
    """`sheva` before `qamats`, `yod`, `vav` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    Example: בְּמָתְנָיו ([Genesis 37:34])
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_QAMATS_GADOL},
        {"letter": T.NAME_YOD_GLIDE},
        {"letter": T.NAME_VAV},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-a|ei-s|n-u|o")
def sheva_nah_vowel_letter_vav_vowel(neg_idx, guess, guesses):
    """`sheva` before `qamats|tsere`, `nun|sav`, `shuruq|holam-male` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    - `/asu/`: None
    - `/aso/`: חָכְמָתוֹ
    - `/anu/`: וְשָׂכְלְתָנוּ
    - `/ano/`: קָרְבָּנוֹ
    - `/eisu/`: None
    - `/eiso/`: None
    - `/einu/`: עָנְיֵנוּ
    - `/eino/`: None
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": [T.NAME_QAMATS_GADOL, T.NAME_TSERE]},
        {
            "letter": [T.NAME_SAV, T.NAME_NUN],
            "vowel": [T.NAME_HOLAM_MALE_VAV, T.NAME_SHURUQ],
        },
    ]
    if has_ending(neg_idx, guesses, pattern, extra=1):  # include holam-male / shuruq
        return guess.update(vowel=T.NAME_SHEVA_NAH)


### `yod`


@rule("sheva", "sheva-nah-ending-iy|eiy|ay")
def sheva_nah_vowel_yod_end(neg_idx, guess, guesses):
    """`sheva` before `hiriq|tsere|patah|qamats`, `yod` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    - `/iy/`: עָנְיִי (Genesis 31:42)
    - `/eiy/`: קָדְשֵׁי (Leviticus 22:15)
    - `/ay/`: בְּאָזְנַי
    - `/ay/`: בְּאָזְנָי
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {
            "vowel": [
                T.NAME_HIRIQ,
                T.NAME_HIRIQ_MALE_YOD,
                T.NAME_TSERE,
                T.NAME_PATAH,
                T.NAME_QAMATS,
                T.NAME_QAMATS_GADOL,
            ]
        },
        {"letter": [T.NAME_EIM_QRIA_YOD, T.NAME_YOD_GLIDE, T.NAME_YOD]},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-ei-i")
def sheva_nah_ending_tsere_hiriq_male(neg_idx, guess, guesses):
    """`sheva` before `tsere`, `hiriq-male` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_TSERE},
        {"vowel": T.NAME_HIRIQ_MALE_YOD},
        {"letter": T.NAME_EIM_QRIA_YOD},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


### `khaf-sofit`


@rule("sheva", "sheva-nah-ending-eikh")
def sheva_nah_ending_eikh(neg_idx, guess, guesses):
    """`sheva` before `tsere`, `khaf-sofit` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    Example: עָנְיֵךְ ([Genesis 16:11])
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_TSERE},
        {"letter": T.NAME_KHAF_SOFIT},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-ekha")
def sheva_nah_khaf_sofit_after_segol(neg_idx, guess, guesses):
    """`sheva` before `segol`, `khaf-sofit+qamats` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_SEGOL},
        {"letter": T.NAME_KHAF_SOFIT, "vowel": T.NAME_QAMATS_GADOL},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-eykha")
def sheva_nah_khaf_sofit_after_segol_yod(neg_idx, guess, guesses):
    """`sheva` before `segol`, `yod`, `khaf-sofit+qamats` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_SEGOL},
        {"letter": T.NAME_EIM_QRIA_YOD},
        {"letter": T.NAME_KHAF_SOFIT, "vowel": T.NAME_QAMATS_GADOL},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-a-ekha")
def sheva_nah_khaf_sofit_after_qamats_segol(neg_idx, guess, guesses):
    """`sheva` before `qamats`, `segol`, `khaf-sofit+qamats` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_QAMATS_GADOL},
        {"vowel": T.NAME_SEGOL},
        {"letter": T.NAME_KHAF_SOFIT, "vowel": T.NAME_QAMATS_GADOL},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-kha-after-hataf")
def sheva_nah_ending_khaf_sofit_after_hataf(idx, guess, guesses):
    """`sheva` after `hataf-`, `qamats` and before `khaf-sofit+qamats` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": [T.NAME_HATAF_PATAH, T.NAME_HATAF_QAMATS, T.NAME_HATAF_SEGOL]},
        {"vowel": [T.NAME_QAMATS, T.NAME_QAMATS_GADOL]},
        {"vowel": T.NAME_SHEVA},
        {"letter": T.NAME_KHAF_SOFIT, "vowel": T.NAME_QAMATS_GADOL},
    ]
    if idx >= 2 and has_sequence(idx - 2, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-a|e-h|m|n")
def sheva_nah_vowel_letter_end(neg_idx, guess, guesses):
    """`sheva` before `qamats|segol`, (`mapiq-he|mem-sofit|nun-sofit`) is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    Examples:

        - `/ah/`: לְעָבְדָהּ (Genesis 2:15)
        - `/am/`: אָכְלָם (Genesis 14:11)
        - `/an/`: יָקְטָן (Genesis 10:25)
        - `/eh/`: None
        - `/em/`: חָקְכֶם
        - `/en/`: None
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": [T.NAME_QAMATS, T.NAME_QAMATS_GADOL, T.NAME_SEGOL]},
        {"letter": [T.NAME_MAPIQ_HE, T.NAME_MEM_SOFIT, T.NAME_NUN_SOFIT]},
    ]
    if has_ending(neg_idx, guesses, pattern):
        if guesses[-2].vowel == T.NAME_QAMATS:
            guesses[-2].vowel = T.NAME_QAMATS_GADOL
        return guess.update(vowel=T.NAME_SHEVA_NAH)


### `mem-sofit`


@rule("sheva", "sheva-nah-ending-guttural-eim")
def sheva_nah_guttural_tsere_mem_sofit(idx, guess, guesses):
    """`sheva` after guttural before `tsere`, `mem-sofit` is `sheva-na`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"letter": GUTTURAL_LETTERS},
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_TSERE},
        {"letter": T.NAME_MEM_SOFIT},
    ]
    if idx >= 1 and has_sequence(idx - 1, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-a-a-h|m|n")
def sheva_nah_ending_qamats_qamats_mem_sofit(neg_idx, guess, guesses):
    """`sheva` before `qamats`, `qamats`, `he|mem-sofit|nun-sofit` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    Examples:

        - `/a-a/`: בְּיָטְבָתָה ([Numbers 33:33])
        - `/a-ah/`: בְּחָכְמָתָהּ ([II Samuel 20:22])
        - `/a-am/`: מָשְׁחָתָם
        - `/a-an/`: כָרְסָוָן ([Daniel 7:9]) - _unverified_
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": [T.NAME_QAMATS, T.NAME_QAMATS_GADOL]},
        {"vowel": [T.NAME_QAMATS, T.NAME_QAMATS_GADOL]},
        {
            "letter": [
                T.NAME_HE,
                T.NAME_EIM_QRIA_HE,
                T.NAME_MAPIQ_HE,
                T.NAME_MEM_SOFIT,
                T.NAME_NUN_SOFIT,
            ]
        },
    ]
    if has_ending(neg_idx, guesses, pattern):
        guesses[-2].update(vowel=T.NAME_QAMATS_GADOL)
        guesses[-3].update(vowel=T.NAME_QAMATS_GADOL)
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-eiy-em")
def sheva_nah_ending_tsere_segol_mem_sofit(neg_idx, guess, guesses):
    """`sheva` before `tsere`, `yod`, `segol`, `mem-sofit` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_TSERE},
        {"letter": T.NAME_EIM_QRIA_YOD},
        {"vowel": T.NAME_SEGOL},
        {"letter": T.NAME_MEM_SOFIT},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-a-i-m|kh")
def sheva_nah_ending_ai_m_kh(neg_idx, guess, guesses):
    """`sheva` before `qamats|patah`, `hiriq`, `khaf-sofit|mem-sofit` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": [T.NAME_QAMATS, T.NAME_QAMATS_GADOL, T.NAME_PATAH]},
        {"vowel": T.NAME_HIRIQ},
        {"letter": [T.NAME_KHAF_SOFIT, T.NAME_MEM_SOFIT]},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


### `tav` / `sav`


@rule("sheva", "sheva-nah-ending-iy-m|s")
def sheva_nah_ending_iym_iys(neg_idx, guess, guesses):
    """`sheva` before `hiriq`, `yod`, `mem-sofit|sav` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    Examples:

    - `/iym/`: בָּטְנִים ([Genesis 43:11])
    - `/iys/`: גָּפְרִית ([Deuteronomy 29:22])
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": [T.NAME_HIRIQ, T.NAME_HIRIQ_MALE_YOD]},
        {"letter": [T.NAME_YOD, T.NAME_EIM_QRIA_YOD]},
        {"letter": [T.NAME_MEM_SOFIT, T.NAME_SAV]},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-os")
def sheva_nah_ending_ot(neg_idx, guess, guesses):
    """`sheva` before letter, `holam-male`, `sav` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": T.NAME_HOLAM_MALE_VAV},
        {},  # vav placeholder
        {"letter": T.NAME_SAV},
    ]
    if has_ending(neg_idx, guesses, pattern):
        return guess.update(vowel=T.NAME_SHEVA_NAH)


@rule("sheva", "sheva-nah-ending-a-d|n|r|s")
def sheva_nah_ending_a_dnrs(neg_idx, guess, guesses):
    """`sheva` before `patah|qamats`, `dalet|nun-sofit|ayin|resh|sav` is `sheva-nah`

    This rule was emperically checked for the Pentateuch.

    Examples:

        - `/ad/`: הָפְקַד ([Leviticus 5:23])
        - `/ad/`: צְלָפְחָד ([Numbers 26:33])
        - `/an/`: בְּאָבְדַן ([Esther 8:6])
        - `/an/`: None
        - `/a/`: חָפְרַע ([Jeremiah 44:30])
        - `/a/`: None
        - `/ar/`: None
        - `/ar/`: מָשְׁזָר ([Exodus 26:1])
        - `/as/`: חָכְמַת ([Exodus 35:35])
        - `/as/`: גָּלְיָת ([I Samuel 17:4])
    """
    pattern = [
        {"vowel": T.NAME_SHEVA},
        {"vowel": [T.NAME_PATAH, T.NAME_QAMATS, T.NAME_QAMATS_GADOL]},
        {
            "letter": [
                T.NAME_DALET,
                T.NAME_NUN_SOFIT,
                T.NAME_AYIN,
                T.NAME_RESH,
                T.NAME_SAV,
            ]
        },
    ]
    if has_ending(neg_idx, guesses, pattern):
        if guesses[-2].vowel == T.NAME_QAMATS:
            guesses[-2].vowel = T.NAME_QAMATS_GADOL
        return guess.update(vowel=T.NAME_SHEVA_NAH)
