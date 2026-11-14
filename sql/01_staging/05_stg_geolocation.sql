-- grain: 1 row per zip prefix; key: zip_prefix
-- median coordinate per prefix, after removing points outside Brazil
CREATE OR REPLACE VIEW stg_geolocation AS
SELECT LPAD(geolocation_zip_code_prefix, 5, '0')       AS zip_prefix,
       MEDIAN(TRY_CAST(geolocation_lat AS DOUBLE))     AS lat,
       MEDIAN(TRY_CAST(geolocation_lng AS DOUBLE))     AS lng,
       COUNT(*)                                        AS n_points
FROM raw.geolocation
WHERE TRY_CAST(geolocation_lat AS DOUBLE) BETWEEN -34 AND 5.5
  AND TRY_CAST(geolocation_lng AS DOUBLE) BETWEEN -74 AND -34
GROUP BY 1;