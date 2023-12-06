WITH CTE1 AS (
    SELECT 
        SIM_PERIOD AS week,
        SUM(QUANTITY) AS company_quantity
    FROM Market
    WHERE SALES_ORGANIZATION = 'Company'
    GROUP BY SIM_PERIOD
), CTE2 AS (
    SELECT 
        SIM_PERIOD AS week,
        SUM(QUANTITY) AS market_quantity
    FROM Market
    WHERE SALES_ORGANIZATION = 'Market'
    GROUP BY SIM_PERIOD
)
SELECT 
    CTE1.week,
    CTE1.company_quantity,
    CTE2.market_quantity,
    CAST(ROUND(CTE1.company_revenue * 1.0 / CTE2.market_revenue * 100, 2) AS TEXT) || "%" AS Percentage
FROM CTE1
JOIN CTE2 ON CTE1.week = CTE2.week
ORDER BY CTE1.week ASC;
