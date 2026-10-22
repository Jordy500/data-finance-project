select
    parse_date('%Y-%m', TIME_PERIOD) as mois,
    OBS_VALUE as volume_habitat_meur
from {{ source('raw', 'volume_credit_habitat') }}
