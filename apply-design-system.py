#!/usr/bin/env python3
"""Apply SweepstakeSites design system to style.css:
- Update heading font-weights from 700 to 800 for display font elements
- Add JetBrains Mono to promo code elements
- Update logo weight to 700 (per skill spec)
"""
import re

with open('style.css', 'r') as f:
    css = f.read()

# 1. Update .promo-code to use JetBrains Mono
css = css.replace(
    """.casino-offer .promo-code {
  display: inline-block;
  margin-top: 4px;
  padding: 2px 8px;
  background: var(--color-primary-surface);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-primary);
}""",
    """.casino-offer .promo-code {
  display: inline-block;
  margin-top: 4px;
  padding: 2px 8px;
  background: var(--color-primary-surface);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.05em;
  color: var(--color-primary);
}"""
)

css = css.replace(
    """.promo-code {
  display: inline-block;
  margin-top: 4px;
  padding: 2px 8px;
  background: var(--color-primary-surface);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-primary);
}""",
    """.promo-code {
  display: inline-block;
  margin-top: 4px;
  padding: 2px 8px;
  background: var(--color-primary-surface);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.05em;
  color: var(--color-primary);
}"""
)

# 2. Add global heading rule right after the GLOBAL COMPONENTS comment
css = css.replace(
    """/* ═══════════════════════════════════════════════════════
   GLOBAL COMPONENTS
   ═══════════════════════════════════════════════════════ */""",
    """/* ═══════════════════════════════════════════════════════
   GLOBAL COMPONENTS
   ═══════════════════════════════════════════════════════ */

/* Global typography (SweepstakeSites design system) */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: 800;
  letter-spacing: -0.02em;
}

.code, .code-badge, [data-code], .promo-code-box {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 0.05em;
}"""
)

with open('style.css', 'w') as f:
    f.write(css)

print("style.css updated with SweepstakeSites design system typography")
