-- grain: 1 row per Portuguese category; key: category_pt
CREATE OR REPLACE VIEW stg_category_translation AS
SELECT product_category_name AS category_pt,
       product_category_name_english AS category
FROM raw.category_translation
UNION ALL
SELECT * FROM (VALUES
    ('pc_gamer', 'pc_gamer'),
    ('portateis_cozinha_e_preparadores_de_alimentos', 'kitchen_portables_and_food_preparers')
) AS manual(category_pt, category);