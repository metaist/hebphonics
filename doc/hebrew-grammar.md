# Hebrew Grammar Rules

## Assumptions

1. The text contains _[niqqud][wiki-niqqud]_ (vowels). Text without vowels is parsable, but unlikely to be as useful for teaching introductory students how to read Hebrew.

2. We can safely ignore cantillation marks, even though they might help determine which syllables are stressed / unstressed.

[wiki-niqqud]: http://en.wikipedia.org/wiki/Niqqud

## Unicode Symbols

A **Unicode symbol** is Unicode code point (a character) that appears in a text. The primary concern of the Unicode Consortium is defining the so-called "presentation forms" of characters (how characters appear on a screen), although they also account for various grammatical roles that similar-looking symbols play. For consistency, we generally use the Unicode naming conventions (except for "Final-" letters which we designate with a "-Sofit" suffix). The relevant Unicode pages for Hebrew are:

- [Hebrew](https://www.unicode.org/charts/PDF/U0590.pdf)
- [Alphabetic Presentation Forms](https://www.unicode.org/charts/PDF/UFB00.pdf)

We represent Unicode characters in UPPERCASE with underscores connecting multiple words.

- Niqqud: `DAGESH`, `SHEVA`, `HIRIQ`, `TSERE`, `SEGOL`, `HATAF_SEGOL`, `PATAH`, `HATAF_PATAH`, `QAMATS`, `HATAF_QAMATS`, `QAMATS_QATAN`, `HOLAM`, `QUBUTS`, `SHIN_DOT`, `SIN_DOT`

- Letters: `ALEF`, `BET`, `GIMEL`, `DALET`, `HE`, `VAV`, `ZAYIN`, `HET`, `TET`, `YOD`, `KAF`, `KAF_SOFIT`, `LAMED`, `MEM`, `MEM_SOFIT`, `NUN`, `NUN_SOFIT`, `SAMEKH`, `AYIN`, `PE`, `PE_SOFIT`, `TSADI`, `TSADI_SOFIT`, `QOF`, `RESH`, `SHIN`, `TAV`,

## Grammatical Symbols

A **grammatical symbol** is the name of a grouping of one or more Unicode symbols and the grammatical role it plays. For example, a `SHEVA` may be a `sheva-na` or a `sheva-nah` depending on its position within a word. Similarly, a `patah` at the end of a word is a `patah-genuvah`.

We represent grammatical names in lowercase with dashes connecting multiple words.

- Niqqud: `mapiq`, `dagesh` (unclassified), `dagesh-qal`, `dagesh-hazaq`, `sheva` (unclassified), `sheva-na`, `sheva-nah`, `hiriq`, `hiriq-male`, `tsere`, `tsere-male`, `segol`, `segol-male`, `hataf-segol`, `patah`, `patah-male`, `patah-genuvah`, `hataf-patah`, `qamats`, `qamats-male`, `hataf-qamats`, `qamats-qatan`, `holam-male`, `holam-haser`, `qubuts`, `shuruq`

- Letters: `alef`, `mapiq-alef`, `bet`, `vet`, `gimel`, `dalet`, `he`, `mapiq-he`, `vav`, `zayin`, `het`, `tet`, `yod`, `kaf`, `kaf-sofit`, `khaf`, `khaf-sofit`, `lamed`, `mem`, `mem-sofit`, `nun`, `nun-sofit`, `samekh`, `ayin`, `pe`, `pe-sofit`, `fe`, `fe-sofit`, `tsadi`, `tsadi-sofit`, `qof`, `resh`, `shin`, `sin`, `tav`, `sav`

The purpose of this document is to explain how to translate a sequence of Unicode symbols into grammatical symbols.

## Symbol Classes

- **BGDKFT letters**: `bet`, `gimel`, `dalet`, `kaf`, `pe`, `tav`
- [yht-1] **Guttural letters**: `alef`, `he`, `het`, `ayin`
- [yht-1] **Semi-guttural**: `resh`
- [yesod] Each short vowel has a corresponding long vowel.
  - Short: `patah`, `qubuts`, `hiriq-haser`, `qamats-qatan`, `segol`
  - Long: `qamats`, `shuruq`, `hiriq-male`, `holam-male`,`holam-haser`, `tsere`

## Syllables

- [x] H001: syllable break before a vowel (lax includes hataf-vowel)
- [x] H002: syllable break before and after `sheva-na` (but not `sheva-nah`)
  - "שָׁרְצוּ" (`sheva-na`)
  - "יִשְׁרְצוּ" (`sheva-nah`)
- [x] H003: (strict) no syllable break after hataf-vowel
  - "אֲשֶׁר"

### Notes

- [h4c-3.1] The number of syllables is the number of vowels.
- [h4c-3.1] A syllable is _open_ if it ends with a vowel sound.
- [h4c-3.1] A syllable is _closed_ if it ends with a letter without a vowel.
- [h4c-3.2] A `hataf-` vowel can be classified either as part of the next syllable or on its own. In practice, a `sheva-na` (and `hataf-` vowels) should be considered part of the next syllable.

## `dagesh-`

- [x] H101 `dagesh` in `alef` is `mapiq-alef` (rare)
  - "רֻאּֽוּ" [Job 33:21]
- [x] H102 `dagesh` in last `he` is `mapiq-he`
  - "בָּהּ" [Exodus 2:3]
- [x] H103 `dagesh` in non-last `he` is (`he`, `dagesh-hazaq`)
  - "חֲמֹרֵיהֶּם" [Genesis 34:28]
- [x] H104 [h4c-3.4] `dagesh` in BGDKFT after vowel is `dagesh-hazaq`
  - "שַׁבָּת" [Exodus 16:23]
- [x] H105 [h4c-3.4] [yesod] `dagesh` in BGDKFT NOT after vowel is `dagesh-qal` (including start of word)
  - "בָּרָא" [Genesis 1:1]
- [x] H106 any other `dagesh` is a `dagesh-hazaq`
  - "הַמַּיִם" [Genesis 1:7]
  - > "וַיֹּאמֶר" [Genesis 1:3]
  - > "הַטּוֹבָה" [Exodus 18:9]

### Notes

- [yesod] `dagesh-qal` can only appear in a BGDKFT letter.
- [yesod] `dagesh-hazaq` can appear in any consonant. Some say that it cannot appear in gutturals (and `resh`), but they do appear in Tanach.
- [yesod] In classical Hebrew, no `dagesh` is put in words that follow closely a word ending in (`alef`, `he`, `vav`, `yod`).
- [yesod] `dagesh-hazaq` denotes syntactic doubling.
  - Examples: [yesod] `bikkur`, `chazzan`
- [h4c-3.4] `dagesh-hazaq` closes the previous syllable (due to the doubling)

## `sheva-`

- [x] H201 [yesod] [h4c-3.5] `sheva` at the start of a word is a `sheva-na`
  - "וְאֵת" [Genesis 1:1] (**contains prefix**)
  - "בְּלִי" [Exodus 31:20]
- [x] H202 [h4c-3.6] `sheva` at the end of a word is `sheva-nah`
  - "הַחֹשֶׁךְ" [Genesis 1:2]
- [x] H203 [h4c-3.5] `sheva` under a `dagesh-hazaq` is `sheva-na`
  - "הַמְּאֹרֹת" [Genesis 1:16]
- [x] H204 [h4c-3.5] `sheva` after a long vowel is `sheva-na`
  - "הָיְתָה" [Genesis 1:2]
- [x] H205 [h4c-3.6] `sheva` after a short vowel is `sheva-nah`
  - "וַיְהִי" [Genesis 1:3] (**contains prefix**)
  - "פַּרְעֹה" [Genesis 12:15]
- [x] H206 `sheva` before last no niqqud `alef` is `sheva-nah`
  - "חֵטְא"
- [x] H207 [h4c-3.5] `sheva` before the same (or same sounding) letter is `sheva-na`
  - "הַלְלוּ" [Psalms 148:1]
- [x] H208 [h4c-3.5] two `sheva` in the middle of a word are (`sheva-nah`, `sheva-na`)
  - "עֶזְרְךָ" [Psalms 20:3]
- [x] H209 two `sheva` at the end of a word are (`sheva-na`, `sheva-na`)
  - "וְיֵשְׁתְּ" [Genesis 9:21]

### Notes

- [yesod] A `sheva` at the start of a syllable is pronounced like a semi "e". This
  includes a `sheva` at the start of a word.
  - Example: [yesod] `k'aru`
- [yesod] A `sheva` at the end of a syllable is silent.
  - Examples: [yesod] `at` (you f.), `kach`

## `hataf-`

### Notes

- [yesod] A `patah`, `segol` or `qamats` under a guttural is given a `sheva` resulting in a `hataf-` vowel.
- [yesod] A `hataf-qamats` is pronounced like an "o".
- [yesod] See "Segolate Nouns".

## `-male`

- [x] H301 [wiki-4] `hiriq` before no niqqud `yod` is `hiriq-male`
  - "כִּי" [Genesis 1:4]
- [x] H302 [wiki-5] `tsere` before no niqqud (`alef`, `he`, `yod`) is `tsere-male`
  - "צֵאת" [Genesis 24:11] (`alef`)
  - "עֲשֵׂה" [Genesis 6:14] (`he`)
  - "בֵּין" [Genesis 1:4] (`yod`)
- [x] H303 [wiki-6] `segol` before no niqqud (`alef`, `he`, `yod`) is `segol-male`
  - "וַתֵּרֶא" [Genesis 3:6] (`alef`)
  - "תַּעֲשֶׂה" [Genesis 24:11] (`he`)
  - "עֶגְלֵי" [I Kings 12:28] (`yod`)
- [x] H304 [wiki-2] `patah` before no niqqud (`alef`, `he`) is `patah-male`
  - "לִקְרַאת" [Genesis 15:10] (`alef`)
  - "מַה" [Genesis 2:19] (`he`)
- [x] H305 [wiki-3] `qamats` before no niqqud (`alef`, `he`) is `qamats-male`
  - "קָרָא" [Genesis 1:5] (`alef`)
  - "שָׁנָה" [Genesis 5:3] (`he`)
- [x] H306 [wiki-7] `holam` before no niqqud (`alef`, `he`) is `holam-male`
  - "צֹאנְךָ" (`alef`)

## `patah-genuvah`

- [x] H401 [wiki-2] last `patah` on a `het`, `ayin`, or `mapiq-he` is `patah-genuvah`

## `qamats-qatan`

- H501 [ulpan] A `qamats` is a `qamats-qatan` if the syllable is unstressed and closed.
  - "כָּל" [Genesis 1:21]
- [x] H502 [ulpan] `qamats` in non-last word with a `maqaf` is `qamats-qatan`
  - "כָּל־" [Genesis 1:21]
- [x] H503 [ulpan] [yesod] `qamats` before `hataf-qamats` is `qamats-qatan`
  - "בַּצָּהֳרָיִם" [Genesis 43:16]
- H504 [ulpan] `qamats` in an unstressed syllable after a `be`-prefix or `le`-prefix is `qamtas-qatan`
  - "בְּחָכְמָה" [Exodus 31:3]

### Notes

- See "Segolate Noun" [yesod].
- Pronounced like an "o" [yesod].
- [ulpan] A `qamats` in an unstressed syllable after a `be`-prefix or `le`-prefix.
- [ulpan] A `qamats` is a `qamats-qatan` if the syllable is unstressed and closed. (including non-last word with `maqaf`)
  - Examples: [ulpan]
    - `kol`
    - `chochma`
    - `chofshi`
- [ulpan] A `qamats` in segolate noun, in a noun with a segolate ending, or in words
  with a theoretical segolate basis is a `qamats-qatan`.
  - Examples: [ulpan]
    - `chodesh` : `chodsho`
    - `kotel` : `kotlo`
    - `kotevet` : `ktovtam`
    - `tilboshet` : `tilboshta`
    - `chorban`
    - `korban`
    - `rono`

### Segolate Nouns

[yesod] p. 314:

- The segolate noun undergoes inner vowel changes in the inflection.
- The `segol` of the 2nd syllable always changes to a sheva (in gutturals,
  to a `hataf-patah`).
- The vowel of the 1st syllable will undergo one of the following changes:
  [...] 3. In nouns whose initial syllable is vocalized by a `holam`, the `holam`
  changes to a `qamats-qatan`.
  - Examples: [yesod]
    - `osher` : `oshri`
    - `chodesh` : `chodshi`
    - `ozen` : `ozni`

## `vav`

- [x] H601 `VAV` followed by `HOLAM_HASER_FOR_VAV` is (`vav`, `holam-haser`)
- [x] H602 `vav` with `HOLAM_HASER` NOT after vowel or sheva is `holam-male`
  - "אוֹר" [Genesis 1:3]
- [x] H603 `VAV` with `HOLAM_HASER` after vowel or sheva (`vav`, `holam-haser`)
  - "עֲוֺן" [Genesis 15:16]
  - "מִצְוֺת" [Leviticus 4:2]
- [x] H604 `VAV` with `DAGESH` NOT after vowel is `shuruq`
  - "תֹהוּ" [Genesis 1:2]
- [x] H605 `VAV` with `DAGESH` after vowel (or has vowel) is (`vav`, `dagesh-hazaq`)
  - "חַוָּה" [Genesis 3:20]
  - "וְיִשְׁתַּחֲוּוּ" [Exodus 4:31]

## References

- [h4c-3.1], [h4c-3.2], [h4c-3.4], [h4c-3.5]
- [ki-1]
- [shaila-1]
- [ulpan]
- [wiki-1], [wiki-2], [wiki-3], [wiki-4], [wiki-5], [wiki-6], [wiki-7]
- [yesod] Uveeler, Luba, Norman M. Bronznick. _Ha-Yesod: Fundamentals of Hebrew_. New York: Feldheim, 1980.
- [yht-1], [yht-2]

[hs-1]: https://hebrewsyntax.org/rbh1/RBH_02%D7%90_Hebrew_vowels.pdf
[ki-1]: http://kingdominfo.net/Dagesh_Rules.pdf
[shaila-1]: http://www.shailamorah.com/kriah-roundtable/teaching-shva-rules
[ulpan]: http://www.ulpan.net/kamatz-katan
[yesod]: https://www.amazon.com/Ha-yesod-Fundamentals-Hebrew-English/dp/0873062140
[yht-1]: https://yourhebrewtutor.com/2015/12/11/the-guttural-letters/
[yht-2]: https://yourhebrewtutor.com/2016/01/14/a-friendly-reminder-the-shewa/

<!-- -->

[h4c-3.1]: http://www.hebrew4christians.com/Grammar/Unit_Three/The_Two_Rules/the_two_rules.html
[h4c-3.2]: http://www.hebrew4christians.com/Grammar/Unit_Three/Syllable_Classification/syllable_classification.html
[h4c-3.4]: https://www.hebrew4christians.com/Grammar/Unit_Three/Dotted_Letters/dotted_letters.html
[h4c-3.5]: http://www.hebrew4christians.com/Grammar/Unit_Three/Sheva_Na/sheva_na.html
[h4c-3.6]: https://www.hebrew4christians.com/Grammar/Unit_Three/Sheva_Nach/sheva_nach.html

<!-- -->

[wiki-1]: https://en.wikipedia.org/wiki/Dagesh
[wiki-2]: https://en.wikipedia.org/wiki/Patach
[wiki-3]: https://en.wikipedia.org/wiki/Kamatz
[wiki-4]: https://en.wikipedia.org/wiki/Hiriq
[wiki-5]: https://en.wikipedia.org/wiki/Tzere
[wiki-6]: https://en.wikipedia.org/wiki/Segol
[wiki-7]: https://en.wikipedia.org/wiki/Holam

<!-- -->

[genesis 1:1]: https://www.sefaria.org/Genesis.1.1?lang=bi
[genesis 1:2]: https://www.sefaria.org/Genesis.1.2?lang=bi
[genesis 1:3]: https://www.sefaria.org/Genesis.1.3?lang=bi
[genesis 1:4]: https://www.sefaria.org/Genesis.1.4?lang=bi
[genesis 1:5]: https://www.sefaria.org/Genesis.1.5?lang=bi
[genesis 1:7]: https://www.sefaria.org/Genesis.1.7?lang=bi
[genesis 1:16]: https://www.sefaria.org/Genesis.1.16?lang=bi
[genesis 1:21]: https://www.sefaria.org/Genesis.1.21?lang=bi
[genesis 2:19]: https://www.sefaria.org/Genesis.2.19?lang=bi
[genesis 3:6]: https://www.sefaria.org/Genesis.3.6?lang=bi
[genesis 3:20]: https://www.sefaria.org/Genesis.3.20?lang=bi
[genesis 5:3]: https://www.sefaria.org/Genesis.5.3?lang=bi
[genesis 6:14]: https://www.sefaria.org/Genesis.6.14?lang=bi
[genesis 9:21]: https://www.sefaria.org/Genesis.9.21?lang=bi
[genesis 12:15]: https://www.sefaria.org/Genesis.12.15?lang=bi
[genesis 15:10]: https://www.sefaria.org/Genesis.15.10?lang=bi
[genesis 15:16]: https://www.sefaria.org/Genesis.15.16?lang=bi
[genesis 18:6]: https://www.sefaria.org/Genesis.18.6?lang=bi
[genesis 24:11]: https://www.sefaria.org/Genesis.24.11?lang=bi
[genesis 43:16]: https://www.sefaria.org/Genesis.43.16?lang=bi
[genesis 34:28]: https://www.sefaria.org/Genesis.34.28?lang=bi
[exodus 2:3]: https://www.sefaria.org/Exodus.2.3?lang=bi
[exodus 4:31]: https://www.sefaria.org/Exodus.4.31?lang=bi
[exodus 16:23]: https://www.sefaria.org/Exodus.16.23?lang=bi
[exodus 18:9]: https://www.sefaria.org/Exodus.18.9?lang=bi
[exodus 31:3]: https://www.sefaria.org/Exodus.31.3?lang=bi
[exodus 31:20]: https://www.sefaria.org/Exodus.31.20?lang=bi
[leviticus 4:2]: https://www.sefaria.org/Leviticus.4.2?lang=bi
[i kings 12:28]: https://www.sefaria.org/I_Kings.12.28?lang=bi
[job 33:21]: https://www.sefaria.org/Job.32.21?lang=bi
[psalms 20:3]: https://www.sefaria.org/Psalms.20.3?lang=bi
[psalms 148:1]: https://www.sefaria.org/Psalms.148.1?lang=bi
