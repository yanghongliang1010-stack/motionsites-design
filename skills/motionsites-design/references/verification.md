# Verification checklist

## Functional

- Existing navigation, forms, fields, API calls, permissions, and state transitions still work.
- Loading, empty, error, success, and disabled states exist where relevant.
- Scroll containers are intentional and important content remains reachable.

## Responsive

- Test near 1440px, 1024px, 768px, and 390px.
- Check overflow, sidebar collapse order, touch targets, and primary-action visibility.

## Accessibility

- Preserve semantic landmarks, reading order, keyboard access, visible focus, contrast, accessible names, and reduced-motion behavior.

## Runtime

- Check console errors and failed requests.
- Give images dimensions and appropriate loading behavior.
- Keep the page usable before animation or enhancement code runs.

## Handoff

Report files changed, tests run, viewports inspected, and anything not verified. Separate code checks, browser evidence, and real-service validation.
