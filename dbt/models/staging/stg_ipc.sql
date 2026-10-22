select
    parse_date('%Y-%m', TIME_PERIOD) as mois,
    OBS_VALUE as ipc
from {{ source('raw', 'ipc_ensemble') }}
