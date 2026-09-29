# Architecture — Retail Demand & Market Basket Lab

**Author:** Faiz Elahi · **Synthetic / educational**

## Components

- `scripts/generate_synthetic_data.py` — creates CSV inputs under `data/`
- `src/run_analysis.py` — metrics + matplotlib exports to `docs/images/`
- `README.md` — full teaching narrative

## Design choices

- Fixed random seeds for reproducible classroom demos
- Deliberately simple metrics suitable for first-pass learning
- No external services required (local Python only)

Refer to the README mermaid diagram for pipeline flow.
