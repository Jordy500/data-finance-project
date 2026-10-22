-- inflation sur 12 mois, calculée sur toute la série IPC avant de couper à 2015
select
    mois,
    ipc,
    (ipc / lag(ipc, 12) over (order by mois) - 1) * 100 as inflation_12m_pct
from {{ ref('stg_ipc') }}
