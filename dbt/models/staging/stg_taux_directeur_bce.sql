select
    cast(TIME_PERIOD as date) as date_decision,
    OBS_VALUE as taux_directeur_pct
from {{ source('raw', 'taux_directeur_bce') }}
