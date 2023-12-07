SELECT 
    p.CODE as code,
    SUM(m.QUANTITY) as quantity
FROM Market as m
JOIN Product as p ON m.MATERIAL_DESCRIPTION = p.NAME
WHERE m.SIM_PERIOD in (1)
AND m.AREA in ('North', 'South')
AND m.DISTRIBUTION_CHANNEL in (10, 12)
GROUP BY p.CODE