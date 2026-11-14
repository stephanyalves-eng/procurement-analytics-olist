# Findings

Each finding states the number, its denominator and period, and the decision it supports.
Numbers come from the notebooks in `notebooks/`; window Jan 2017 to Aug 2018, valid orders only.

## Q1 · Spend concentration

Source: `notebooks/02_spend_concentration.ipynb` · figures `reports/figures/01_pareto_spend.png`, `02_category_concentration.png`

- **18% of sellers hold 80% of spend.** 537 of 3,029 sellers account for 80% of BRL 13.4M item spend; the top 10% hold 67.4%.
  *Implication:* supplier performance management can cover most of the money with a short list of about 540 sellers.

- **Concentration is a category problem, not a portfolio problem.** Spend-weighted HHI is 788 (low), but two material categories show single-source dependency: computers (9 sellers, top seller 75%, HHI 5,796) and office furniture (34 sellers, top seller 64%, HHI 4,284), together 3.7% of spend.
  *Implication:* in office furniture, alternative sellers already exist, so the lever is volume reallocation; in computers, the base itself is narrow, so the lever is new-source development.
  *Robustness:* the result holds for materiality cuts of 0.5%, 1% and 2% of spend; spend at risk never exceeds 3.7%.

- **Most high-HHI categories are immaterial.** Categories above HHI 2,500 hold only 5.1% of spend.
  *Implication:* ranking categories by HHI alone would direct sourcing effort to categories that carry little money.
