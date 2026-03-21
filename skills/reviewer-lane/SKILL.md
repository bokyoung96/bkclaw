---
name: reviewer-lane
description: Use when research or implementation output needs a second-pass quality check. Especially relevant for overclaiming detection, missing counterarguments, weak assumptions, regression risk, incomplete verification, and cases where a deep-research result should be challenged before being treated as final.
---

# Reviewer Lane

Use this skill when the first answer or artifact should not be accepted at face value.

## Role in the lane model

- **Primary role**: quality gate and challenge function
- **Works after**: research, deep-research, coding, or ops output
- **Not a default first step** for simple lookup or low-stakes drafting

## What this lane owns

- overclaiming detection
- weak-assumption identification
- missing counterevidence checks
- verification gap detection
- edge-case / failure-mode pushback
- merge-readiness style review for meaningful outputs

## When to use

Use this lane when:
- a conclusion feels too confident
- the user asks for risk review or 반대 근거
- a deep-research synthesis needs challenge before adoption
- implementation/reporting quality matters more than speed

## Review checklist

1. What is the strongest claim?
2. What evidence is actually solid?
3. What assumption is carrying too much weight?
4. What counterexample or alternative explanation exists?
5. What remains unverified?
6. What would change the conclusion?

## Output discipline

Return reviews in a compact structure:
- verdict
- strongest support
- main weakness
- missing verification
- recommended next step

## Handoff rule

Typical path:
- research -> deep-research -> reviewer
- coding -> reviewer
- ops change -> reviewer only when risk/impact is meaningful
