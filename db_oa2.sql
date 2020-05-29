select name, revenue, number from
(
    select * from companies as c
    inner join
    (select company_id, count(*) as number from offices group by company_id
        having count(*) < 5
        order by number asc
    ) as o
    on c.company_id = o.company_id
) as co;