# Usage

## Recommended prompt shape

Give the Skill four things:

1. What page or flow is being designed.
2. Who uses it and what they must accomplish.
3. Which functions and technical constraints cannot change.
4. What evidence counts as complete: code checks, browser widths, interactions, or a design-only artifact.

Example:

```text
$motionsites-design Redesign the existing knowledge-base upload page for operations staff. Preserve every field, validation rule, API call, chunk-size control, overlap behavior, and duplicate-file warning. Improve hierarchy and alignment, then verify at 1440px, 1024px, and 390px with keyboard and reduced-motion checks.
```

## Useful requests

- “Search three suitable directions first and explain the tradeoff before implementing.”
- “Use the selected direction but keep our current design tokens.”
- “Audit only; do not modify files.”
- “Create a design specification, not production code.”
- “Implement the selected direction in the existing React stack without new dependencies.”

## What the Skill should return

For implementation work, expect:

- the selected design direction and spatial thesis;
- the files changed;
- the preserved functions and constraints;
- test and rendered-page evidence;
- any unverified external service, browser, or real-user behavior.

## Catalog search strategy

Search with concrete terms: page type + domain + tone. Examples:

```bash
python3 scripts/motionsites_catalog.py search "AI chat enterprise calm"
python3 scripts/motionsites_catalog.py search "retail analytics dashboard"
python3 scripts/motionsites_catalog.py search "editorial SaaS launch"
```

Use one primary direction. Combining too many visual references usually produces an incoherent result.
