with company_unit_sold as (
    select
        m.SIM_PERIOD as week,
        p.CODE,
        sum(QUANTITY) as total_quantity
    from Product as p
    left join Market as m
        on m.MATERIAL_DESCRIPTION = p.NAME
    where 1 = 1
        and m.SIM_ROUND = 2
        and m.SIM_PERIOD = 6
        and m.SALES_ORGANIZATION = 'Company'
    group by m.SIM_PERIOD, p.CODE
), market_unit_sold as (
    select
        m.SIM_PERIOD as week,
        p.CODE,
        sum(QUANTITY) as total_quantity
    from Product as p
    left join Market as m
        on m.MATERIAL_DESCRIPTION = p.NAME
    where 1 = 1
        and m.SIM_ROUND = 2
        and m.SIM_PERIOD = 6
        and m.SALES_ORGANIZATION = 'Market'
    group by m.SIM_PERIOD, p.CODE
)
select
    c.CODE,
    c.total_quantity as company_sold,
    m.total_quantity as market_sold,
    round((c.total_quantity * 1.0 / m.total_quantity),3) as proportion,
    rank() over (order by (c.total_quantity * 1.0 / m.total_quantity) desc) as rank
from company_unit_sold as c, market_unit_sold as m
where c.CODE = m.CODE;
