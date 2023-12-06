WITH CTE1 AS (
    SELECT 
        p.CODE as code,
        ROUND(SUM(NET_VALUE) * 1.0 / SUM(QUANTITY),2) AS company_avg_price
    FROM Market as m
    JOIN Product as p
        ON m.MATERIAL_DESCRIPTION = p.NAME
    WHERE 1 = 1 
        AND SALES_ORGANIZATION = "Company"
        AND m.SIM_PERIOD in (1,2)
        AND m.DISTRIBUTION_CHANNEL in (10,12)
    GROUP BY p.CODE
), CTE2 AS (
    SELECT 
        p.CODE as code,
        ROUND(SUM(NET_VALUE) * 1.0 / SUM(QUANTITY),2) AS market_avg_price 
    FROM Market as m
    JOIN Product as p
        ON m.MATERIAL_DESCRIPTION = p.NAME
    WHERE 1 = 1 
        AND SALES_ORGANIZATION = "Market"
        AND m.SIM_PERIOD in (1,2)
        AND m.DISTRIBUTION_CHANNEL in (10,12)
    GROUP BY p.CODE
)
SELECT 
    CTE1.code,
    CTE1.company_avg_price,
    CTE2.market_avg_price,
    CAST(ROUND(CTE1.company_avg_price * 1.0 / CTE2.market_avg_price * 100, 2) AS TEXT) || "%" AS Percentage
FROM CTE1
JOIN CTE2 ON CTE1.code = CTE2.code
        ORDER BY CTE1.code ASC;