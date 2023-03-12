# Convert Japanese text to phonemes which is
# compatible with Julius https://github.com/julius-speech/segmentation-kit

import re
import unicodedata

# DEFAULT SET OF IPA PHONEMES
# Phonemes definition (All IPA characters)
_vowels = "iyɨʉɯuɪʏʊeøɘəɵɤoɛœɜɞʌɔæɐaɶɑɒᵻ"
_non_pulmonic_consonants = "ʘɓǀɗǃʄǂɠǁʛ"
_pulmonic_consonants = "pbtdʈɖcɟkɡqɢʔɴŋɲɳnɱmʙrʀⱱɾɽɸβfvθðszʃʒʂʐçʝxɣχʁħʕhɬɮʋɹɻjɰlɭʎʟ"
_suprasegmentals = "ˈˌːˑ"
_other_symbols = "ʍwɥʜʢʡɕʑɺɧʲ"
_diacrilics = "ɚ˞ɫ"
_phonemes = _vowels + _non_pulmonic_consonants + _pulmonic_consonants + _suprasegmentals + _other_symbols + _diacrilics

_CONVRULES = {
    # Conversion of 1 letter
    "בּ" : "b",
    "דּ" : "d",
    "ד" : "d",
    "פ" : "f",
    "גּ" : "g",
    "ג" : "g",
    "ה" : "h", #TODO: also possible: ɦ?
    "ח" : "χ",
    "י" : "j", #TODO: also possible: i?
    "כּ" : "k",
    "ל" : "l",
    "מ" : "m",
    "נ" : "n",
    "פּ" : "p",
    "ק" : "k",
    "ר" : "ʁ",
    "ס" : "s",
    "שׂ" : "s",
    "צ" : "ts",
    "שׁ" : "ʃ",
    "תּ" : "t",
    "ט" : "t",
    "ת" : "t",
    "ב" : "v",
    "ו" : "v", #TODO: also possible: o/u?
    "כ" : "χ",
    "ז" : "z",
    "ע" : "ʔ",
    "א" : "ʔ",

    "ף" : "f",
    "ם" : "m",
    "ן" : "n",
    "ץ" : "ts",
    "ך" : "χ",

# Conversion of 2 letters
    "ג'" : "dʒ",
    "נג" : "ŋ",
    "ז'" : "ʒ",
    "צ'" : "tʃ",
    "ת'" : "θ",
    "ד'" : "ð",
    "וו" : "w",
    "ע'" : "ɣ",
    "וֹי" : "oi",
    "וּי" : "ui",
    "אוֹ" : "ao", #TODO: also possible: o?
    "יוּ" : "ju",
}

_COLON_RX = re.compile(":+")
_REJECT_RX = re.compile("[^ a-zA-Z:,.?]")


def _makerulemap():
    l = [_CONVRULES.items()]
    return tuple({k: v for k, v in l if len(k) == i} for i in (1, 2))


_RULEMAP1, _RULEMAP2 = _makerulemap()


def heb2phoneme(text: str) -> str:
    """Convert hebrew text to phonemes."""
    text = text.strip()
    res = ""
    while text:
        if len(text) >= 2:
            x = _RULEMAP2.get(text[:2])
            if x is not None:
                text = text[2:]
                res += x
                continue
        x = _RULEMAP1.get(text[0])
        if x is not None:
            text = text[1:]
            res += x
            continue
        res += " " + text[0]
        text = text[1:]
    res = _COLON_RX.sub(":", res)
    return res[1:]


def hebrew_text_to_phonemes(text: str) -> str:
    """Convert Hebrew text to phonemes."""
    res = unicodedata.normalize("NFKC", text)
    res = japanese_convert_numbers_to_words(res)
    return res.replace(" ", "")
