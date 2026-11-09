"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

# Size of the sliding window for the type-token ratio, in words.
TTR_WINDOW = 50

# Punctuation that counts toward punctuation_density. Full stops are left out.
PUNCTUATION_MARKS = ",;:—–()!?"

# Where each raw measure reads as fully AI-like vs fully human-like:
# (ai_end, human_end). Set from the calibration run — see README.
SPREAD_RANGE = (0.20, 0.60)
TTR_RANGE = (0.65, 0.85)
PUNCT_RANGE = (0.04, 0.15)

# How much each measure counts toward style_signal. Sentence-length spread
# gets the most because it's the measure least moved by text length.
STYLE_WEIGHTS = {"spread": 0.5, "vocab": 0.3, "punct": 0.2}

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.

    My version: standard deviation of sentence lengths (in words) divided by
    the mean — the coefficient of variation. 0.0 means every sentence is the
    same length; human prose often lands around 0.5–0.8. **Higher means more
    human.** Fewer than two sentences has no spread to measure, so it returns
    0.0 and `style_signal` treats that case as neutral instead.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4) if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.

    My version deals with that by averaging the ratio over a sliding window of
    TTR_WINDOW words (a "moving-average type-token ratio"), so a long piece
    isn't punished just for being long. Texts shorter than the window use the
    plain ratio. **Higher means more human.**
    """
    w = words(text)
    if not w:
        return 0.0
    if len(w) <= TTR_WINDOW:
        return round(len(set(w)) / len(w), 4)
    ratios = [
        len(set(w[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(w) - TTR_WINDOW + 1)
    ]
    return round(statistics.mean(ratios), 4)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.

    My version counts everything except full stops — commas, semicolons,
    colons, dashes, brackets, ! and ? — per word. Full stops are skipped
    because every writer uses them. **Higher means more human.**
    """
    w = words(text)
    if not w:
        return 0.0
    count = sum(text.count(mark) for mark in PUNCTUATION_MARKS)
    return round(count / len(w), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    spread = sentence_length_spread(text)
    enough_sentences = len(sentences(text)) >= 2

    # All three measures point "higher = more human", so each one is flipped
    # onto 0–1 where 1.0 means AI-like.
    parts = {
        "spread": _ai_likeness(spread, *SPREAD_RANGE) if enough_sentences else 0.5,
        "vocab": _ai_likeness(type_token_ratio(text), *TTR_RANGE),
        "punct": _ai_likeness(punctuation_density(text), *PUNCT_RANGE),
    }
    score = sum(STYLE_WEIGHTS[name] * value for name, value in parts.items())
    return round(min(max(score, 0.0), 1.0), 4)


def _ai_likeness(value: float, ai_end: float, human_end: float) -> float:
    """
    Put one raw measure on a 0–1 AI-likeness scale.

    At or beyond `ai_end` it scores 1.0; at or beyond `human_end` it scores
    0.0; in between it moves in a straight line.
    """
    position = (value - human_end) / (ai_end - human_end)
    return min(max(position, 0.0), 1.0)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
