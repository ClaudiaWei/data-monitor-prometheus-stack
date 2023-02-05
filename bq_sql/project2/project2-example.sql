WITH temp AS (
    SELECT
        received_timestamp,
        TIMESTAMP_TRUNC(received_timestamp, HOUR) AS hour_ts,
    FROM
        `your-table-name`
    WHERE
        date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
        AND DATE_ADD(CURRENT_DATE(), INTERVAL 1 DAY)
)
SELECT
    hour_ts AS hour,
    count(1) as value
FROM
    temp
WHERE
    received_timestamp <= CURRENT_TIMESTAMP()
    AND received_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
GROUP BY
    hour_ts
ORDER BY
    hour_ts DESC
LIMIT
    1;