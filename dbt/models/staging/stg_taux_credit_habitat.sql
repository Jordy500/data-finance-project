select
    parse_date('%Y-%m', TIME_PERIOD) as mois,
    OBS_VALUE as taux_habitat_pct
from {{ source('raw', 'taux_credit_habitat') }}
