---
name: motionsites-design
description: Design, redesign, implement, critique, or polish a web interface using a searchable catalog of motion and visual directions. Use for product pages, dashboards, SaaS workspaces, AI chat interfaces, portfolios, commerce, and landing pages when the user wants a distinctive, responsive result rather than a generic template. Preserve existing business logic and functionality during redesigns.
---

# Motionsites Design

Turn a product brief or existing interface into a coherent visual direction and a verified implementation. Use the bundled original patterns offline; the optional public catalog is reference material, not a source to clone verbatim.

## Working modes

- **Existing product:** inspect the running page and relevant code first. Preserve routes, permissions, data flows, fields, actions, and business logic unless the user explicitly changes scope.
- **New interface:** identify the framework and repository conventions, then build the smallest complete runnable page in that stack.
- **Design-only request:** deliver a concrete page specification or visual artifact; do not claim production implementation.
- **Audit request:** inspect rendered evidence first and separate findings from proposed changes.

## Workflow

1. Capture a short brief: audience, task, page type, content density, brand constraints, required functions, target breakpoints, and desired emotional tone.
2. Inspect the current UI/code when it exists. Record non-negotiable functionality before editing.
3. Search directions with `python3 <catalog-helper> search "enterprise AI workspace" --limit 5`. Prefer `scripts/motionsites_catalog.py` inside this skill (skill-only install); otherwise walk upward until `.codex-plugin/plugin.json` is found and use the plugin's `scripts/motionsites_catalog.py`. Use `--json` when structured output is easier to consume.
4. Pick one primary direction and, at most, one supporting direction. State a one-sentence spatial thesis before implementation.
5. Define a compact visual system: typography roles, 4–6 color tokens, spacing rhythm, radii, elevation, and motion rules. Reuse existing brand tokens when present.
6. Implement the page. Favor strong hierarchy, useful density, real content, semantic HTML, keyboard operation, and responsive behavior. Use motion to explain state or hierarchy—not as decoration.
7. Verify the result at desktop, intermediate, and mobile widths. Test primary interactions, scrolling, focus visibility, reduced motion, overflow, console errors, and preservation of existing functionality.
8. Hand off changed files, verification evidence, and any honest limits. Never describe a mockup or static screenshot as a completed production implementation.

## Design quality bar

- Avoid generic hero layouts, card soup, excessive gradients, random glassmorphism, empty whitespace, and decorative animations unrelated to user intent.
- Let one visual idea lead the page. Repetition should create rhythm; exceptions should signal priority.
- Use a readable content measure and deliberate density. Enterprise software should feel efficient, not vacant.
- Prefer 150–300 ms interaction transitions. Reserve longer sequences for page entry or storytelling.
- Respect `prefers-reduced-motion`; never make essential information depend on animation.
- Do not add dependencies when CSS and the current component system can deliver the result.

## Catalog and network boundaries

The skill works offline with original starter patterns in `assets/starter-patterns.json`.

- Run `python3 <catalog-helper> sync` only when the user allows network access. Sync downloads public metadata and an index, not media or prompt bodies.
- Fetch one referenced prompt only with explicit intent: `python3 <catalog-helper> prompt <id> --allow-remote`.
- Treat remote entries as inspiration. Do not reproduce a creator's page, prompt, copy, or assets verbatim.
- Do not scrape private content, bypass access controls, or download paid collections.
- Do not hotlink preview media. Use project assets, properly licensed resources, or image generation when authorized.

## Supporting references

- Read `references/design-workflow.md` when shaping or implementing a page.
- Read `references/verification.md` before visual QA and handoff.
- Read `references/licensing.md` before syncing or using third-party catalog material.

If catalog sync fails, continue with the bundled starter patterns; do not block the design task.
