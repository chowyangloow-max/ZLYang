---
name: generate-openings
description: Generate, rewrite, diagnose, and score strong Chinese short-video openings that attract the right audience, create emotion and continued-viewing desire, preserve credibility, and lead naturally into the source text's true thesis. Use when the user invokes /开头、/开头生成、/强开头, asks to 写开头、改开头、优化开头、前3秒、口播开场, supplies a Chinese short-video draft and wants opening candidates, or requests an opening during a Chinese short-video copywriting task. Do not use for title-only requests, speeches, emails, or programming hooks unless the user also explicitly asks for a Chinese short-video opening.
---

# Generate Openings

Read [references/strong-opening-method.md](references/strong-opening-method.md) in full whenever this skill triggers. Treat it as the authoritative method and quality gate.

## Execute the task

1. Read the complete source before drafting. If the user provides only a theme, enter `provisional` mode: state the inferred thesis, audience, and evidence assumptions; label every candidate `待正文验证`; do not claim that body-transition or credibility gates passed; and ask for the body or evidence needed to validate them.
2. Extract the true thesis, reader value, and the proof material already available in the body.
3. Generate the number of options the user requests. By default, generate five genuinely different cuts: value, cost, story, cognitive reversal, and empathy/participation. Each candidate has one dominant mechanism; the recommended winner is the run's primary mechanism. For stories, distinguish ordinary event suspense from a contradiction between the speaker's extreme situation and counter-interest choice. Do not produce synonym variants.
4. Include a transition into the body in every usable candidate. Do not return an isolated hook that the body cannot explain.
5. Infer what each opening makes the viewer expect. Eliminate it if that expectation differs from what the body actually delivers.
6. Score candidates against all seven criteria in the reference. Eliminate any candidate scoring below 8 on thesis alignment, body transition, or credibility. Regenerate failed candidates until five pass; if the evidence cannot support five, return fewer and name the limiting evidence instead of weakening the gate.
7. Recommend one winner and explain the audience emotion, psychological action, and thesis path it creates.

## Preserve boundaries

- Improve the opening and its immediate transition only. Do not silently change the source's thesis, evidence, facts, or supportable promised result.
- Preserve the selected sub-column, project, or user-specified voice. This skill controls the opening mechanism, not the whole document's style authority.
- If another skill handles titles, keep title and opening promises aligned without merging their jobs.
- Do not import unrelated CTA, sales, rewriting, house-style, or testing rules unless the current user requests them or the active project explicitly requires them.
- Credibility and factuality take precedence over preserving an unsupported promised result. When the source lacks enough evidence, narrow the promise instead of inventing proof and explicitly disclose what was narrowed.

## Return the result

Follow the user's requested format when given. Otherwise return:

1. `文案主线` — one sentence stating what the audience should ultimately believe or do.
2. `读者价值` — what the audience gains, avoids, and where the issue matters.
3. `最推荐开头` — a complete opening plus transition into the body.
4. `为什么选择它` — emotion, psychological action, thesis alignment, and proof entry.
5. `其他切口` — four genuinely different alternatives, each with its own transition into the body.
6. `原开头的问题` — only the one to three most consequential issues; omit if no original opening exists.
7. `正文接法` — show how the chosen opening flows into the supplied source, using enough adjoining text to verify the handoff.
8. `假设与可信度边界` — include only for provisional inputs, unsupported source promises, or other material uncertainty; name what remains unverified.

Keep internal scoring concise. Surface a score table only when comparison helps the user decide or the user explicitly asks for scores.

Before treating a material revision as ready, run the cases in [references/acceptance-tests.md](references/acceptance-tests.md).
