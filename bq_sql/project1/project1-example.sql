SELECT
    dt,
    count(distinct pkgId) as resultValue
FROM
    `your-table-name`
where
    dt = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
group by
    dt