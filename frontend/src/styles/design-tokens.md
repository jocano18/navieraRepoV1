# Naviera Design Tokens

Single source of truth for brand colors. CSS variables live in `tokens.css`; Tailwind maps them in `globals.css`.

## Primary palette

| Token | Hex | Usage |
|-------|-----|--------|
| `--color-primary-900` | `#270045` | Brand base, headers, nav |
| `--color-accent-500` | `#F54D02` | Primary CTAs, active states |
| `--color-lilac-300` | `#C3B6D2` | Surfaces, borders, muted bg |
| `--color-cream-100` | `#FCFCBE` | Soft highlights, diff match bg |

## Secondary palette

| Token | Hex | Usage |
|-------|-----|--------|
| `--color-violet-500` | `#8C5BE8` | Info, secondary actions, links |
| `--color-coral-400` | `#FC6844` | Warnings, needs attention |
| `--color-blue-600` | `#002BE8` | Focus rings, informational emphasis |

## Semantic mapping

- **Primary action** → accent-500 (hover: `--color-accent-600`)
- **Success** → `--color-success-600` (harmonized green)
- **Diff mismatch** → cream bg + coral left border
- **Diff match** → subtle lilac background

Do not hard-code hex in components; use Tailwind utilities (`bg-brand`, `text-accent`, etc.).
