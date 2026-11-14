-- grain: 1 row per order (latest review); key: order_id
CREATE OR REPLACE VIEW stg_reviews AS
SELECT order_id,
       review_id,
       TRY_CAST(review_score AS INTEGER)               AS review_score,
       TRY_CAST(review_creation_date AS TIMESTAMP)     AS review_created_at,
       TRY_CAST(review_answer_timestamp AS TIMESTAMP)  AS review_answered_at
FROM raw.reviews
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY order_id
    ORDER BY TRY_CAST(review_answer_timestamp AS TIMESTAMP) DESC NULLS LAST, review_id
) = 1;