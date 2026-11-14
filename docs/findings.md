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

## Q2 · Seller dispatch performance

Source: `notebooks/03_delivery.ipynb` · figures `03_monthly_sla.png`, `04_dispatch_persistence.png`

- **Sellers dispatch 92.2% of orders on time in the median month; Black Friday cut it to 87.0%.** November 2017 carried 1.6x the median monthly volume and dispatch on time fell 5.2 points; customer on-time delivery fell from 95.6% to 87.5% in the same month.
  *Implication:* seasonal peaks are where supplier capacity breaks; capacity commitments should be agreed before the peak, not reviewed after it.

- **Late dispatch is structural, not circumstantial.** 62% of sellers in the 2017 bottom quartile were still in the bottom quartile in 2018, against 25% expected by chance (Spearman 0.59, 338 sellers with 15+ orders in each year). 53 sellers were laggards in both years.
  *Implication:* a seller's past dispatch rate predicts its future rate, so it belongs in the scorecard and justifies corrective action plans for the persistent laggards.

## Q3 · Seller vs logistics delay

Source: `notebooks/03_delivery.ipynb` · figures `05_delay_decomposition.png`, `06_delivery_slack.png`

- **Measuring suppliers at delivery hides their failures.** 78.8% of orders the seller dispatched late still reached the customer on time, because the median order arrives 12 days before the estimated date.
  *Implication:* supplier performance must be measured at the hand-off the supplier controls (dispatch vs shipping limit), not at final delivery.

- **Seller delay matters, but most customer delay starts downstream.** When the seller is late, the customer is late 3.9x as often (21.2% vs 5.5%); still, the seller was also late in only 27.8% of the orders that reached the customer late.
  *Implication:* improving seller SLA alone would address about a quarter of customer delays; the rest sits in the logistics leg and needs a carrier-side review.

## Q4 · Reviews, distance and freight

Source: `notebooks/03_delivery.ipynb` · figure `07_reviews_by_delay.png`

- **Lateness drives reviews.** 79% of orders delivered 8+ days late get a 1- or 2-star review, against 9% of on-time orders (9.1x); the share already reaches 32% at 1 to 3 days late.
  *Implication:* even small delays carry a visible quality cost, which supports a high weight for delivery reliability in the scorecard.

- **Distance is a logistics problem, not a seller problem.** Seller late rate stays between 8.6% and 9.6% across distance bands, while customer late rate rises from 4.5% (under 100 km) to 10.5% (1,000+ km) and median freight from 17% to 30% of item price.
  *Implication:* sellers should not be penalized for distance; distance belongs to carrier and network decisions.

## Q5 · Supplier scorecard

Source: `notebooks/04_scorecard.ipynb` · figures `08_score_distribution.png`, `09_action_matrix.png` · export `data/processed/scorecard_sellers.csv`

- **633 sellers with 30+ orders are scored, covering 77.1% of spend.** Weights: dispatch on time 35%, review (Bayesian, m = 20) 30%, freight ratio 15%, dispatch lead time p90 10%, cancellation 5%, negative reviews 5%. Cancellation was cut from 15% to 5% by a rule set before the result: 77.3% of eligible sellers have zero cancellations.
  *Implication:* metrics that do not discriminate between suppliers add noise, not information, and should carry little weight.

- **The ranking is robust to the weights.** Against three alternative weightings, Spearman is 0.95 to 0.97 and the top 20 overlaps by 70% to 85%.
  *Implication:* who is a strong or weak supplier does not depend on a debatable weighting choice; adjustable weights in the dashboard are for exploration, not a requirement.

- **60 sellers form the action shortlist: high spend and bottom-tier score, holding 14.7% of eligible spend.** For 80% of them the largest gap is dispatch on time. Their median dispatch on-time rate is 77.7% against 95.0% for all eligible sellers, and their p90 dispatch lead time is 8.6 days against 4.3.
  *Implication:* corrective action plans should target dispatch capacity and lead time for these 60 sellers; their freight ratio (18.2% vs 21.0%) shows the problem is reliability, not cost.

## Limitations

- Orders without items (0.78% of orders) carry no seller, so cancellation by seller is understated.
- Early 2017 months have low volume (800 orders in Jan 2017) and lower dispatch rates; trends start being reliable from Mar 2017.
- End-of-window censoring is negligible: 0.4% of Aug 2018 orders had no dispatch date at extraction.
- All relationships are associations; no causal claim is made.
