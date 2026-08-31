# Verification rules

## Source tiers

- **Tier A:** primary evidence, official record, signed decision, direct observation, or authoritative system of record.
- **Tier B:** independent expert analysis or reliable secondary source with explicit citations.
- **Tier C:** unsourced summary, recollection, promotional material, generated text, or derivative repetition.

Tier is not truth. A Tier A source can be stale, out of scope, or internally inconsistent.

## Verdict gates

- `verified`: supported by sufficient in-scope evidence with no unresolved material contradiction.
- `partially_verified`: some components or scope are supported; limits are explicit.
- `conflicted`: credible evidence supports incompatible conclusions.
- `unverified`: evidence is missing or inadequate.
- `rejected`: contradicted by stronger evidence or invalid for the stated scope.

Confidence is a number from 0 to 1 and should reflect source independence, authority, freshness, scope match, and contradiction risk. Record why confidence is capped.

## Required checks

For each material claim capture source origin, author or owner if known, created and accessed dates, version, applicable scope, exact supporting location, and dependency on other claims.

## Independent review

For `dual_independent`, two reviewers separately extract or verify material claims before seeing each other's draft. Compare claim boundaries, source locations, verdicts, confidence limits, and omitted details. Preserve disagreements in `review-plan.json`; consensus without a recorded comparison is not independent review.
