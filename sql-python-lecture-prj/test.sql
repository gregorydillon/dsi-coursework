SELECT * FROM users limit 5;

SELECT * FROM events limit 10;


SELECT
  type,
  price
FROM meals
WHERE price > (
  SELECT AVG(price) FROM meals
);

with average_per_type as (
  SELECT
    type,
    avg(price) AS avg_price
  FROM meals GROUP BY type
)

SELECT meals.*
FROM meals
JOIN average_per_type ON
  average_per_type.type=meals.type and
  meals.price > average_per_type.avg_price
