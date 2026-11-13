# procurement-analytics-olist
Procurement analytics on the public Olist dataset: spend concentration (Pareto, HHI), seller dispatch SLA and a weighted supplier scorecard. SQL (DuckDB) + Python. ***Work in progress***
## Data

Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (CC BY-NC-SA 4.0).

| Table | Rows |
| --- | ---: |
| orders | 99,441 |
| order_items | 112,650 |
| payments | 103,886 |
| reviews | 99,224 |
| customers | 99,441 |
| sellers | 3,095 |
| products | 32,951 |
| geolocation | 1,000,163 |
| category_translation | 71 |

Row counts are verified on every load by `python -m src.check_raw`.