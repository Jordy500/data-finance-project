-- le taux réel doit valoir taux - inflation, à l'arrondi près (0,01)
select mois, 'habitat' as credit, taux_reel_habitat_pct as taux_reel,
    taux_habitat_pct - inflation_12m_pct as attendu
from {{ ref('fct_credit_mensuel') }}
where abs(taux_reel_habitat_pct - (taux_habitat_pct - inflation_12m_pct)) > 0.01

union all

select mois, 'conso', taux_reel_conso_pct,
    taux_conso_pct - inflation_12m_pct
from {{ ref('fct_credit_mensuel') }}
where abs(taux_reel_conso_pct - (taux_conso_pct - inflation_12m_pct)) > 0.01
