# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

Of 10 paragraphs I wrote myself, at most 1 gets labelled high-confidence AI.

**Why this target:**

When writing, I sometimes adopt em dashes for emphasis or to insert extra information when I do not necessarily want to use a comma, or a comma might not let the sentence flow the way I want.
Many people think em dashes are a sign of AI writing, so I could easily be wrongly accused, and being told my own work isn't mine would feel very annoying and could cause very hard feelings. I allow 1 instead of 0 because no detector is perfect and there has to be allowance for some margin of error.


---

## 2.

Across my test texts (clearly AI, clearly human, borderline), each of the three labels appears at least once.

**Why this target:**

If a particular label can never appear, for example, if "clearly human" would never appear, an exceptional writer would question their abilities and probably seek out a different service with similar usage to compare results. This service would be deemed faulty and would get bad reviews and would end up getting discarded which is not good for a product.


---

## 3.

Of 10 broken requests (empty text, missing text, null, wrong type, huge text), 0 cause a crash (500 error).

**Why this target:**

For whatever input submitted, the service should never crash as this shuts down the service for everyone by becoming unavailable. Every imaginable input outlier should be handled / sanitized and a meaningful error returned to the user, so it can be corrected. Unexpected outliers should also be handled so that an error message is returned to the user instead of the system going down.


---

## 4.

Every appeal on a real content_id changes the status to under_review and adds a log entry. Every appeal on a made-up ID gets a 404.

**Why this target:**

For any writer that disagrees with the label assigned to their text, an appeal is the writer's record that they disputed the label. If there is no record of an appeal, then there is no way to contest the wrongly assigned label. A 404 on a made-up ID is an alert to the writer that there has been no recorded appeal. So the writer can check the ID and try again in case of some sort of error.


---

## 5.

Clearly AI text scores at least 0.65 (the AI label) and clearly human text scores at most 0.35 (the human label).

**Why this target:**

When AI and human text score a noticeable gap apart, there is more confidence in the labeling system and not just a lucky coin toss.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
