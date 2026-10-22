-- renvoie une ligne par valeur hors de la fourchette plausible
select mois, 'taux_habitat_pct' as indicateur, taux_habitat_pct as valeur
from {{ ref('fct_credit_mensuel') }}
where taux_habitat_pct not between 0 and 8

union all

select mois, 'taux_conso_pct' as indicateur, taux_conso_pct as valeur
from {{ ref('fct_credit_mensuel') }}
where taux_conso_pct not between 0 and 12

union all

select mois, 'taux_directeur_pct' as indicateur, taux_directeur_pct as valeur
from {{ ref('fct_credit_mensuel') }}
where taux_directeur_pct not between 0 and 6

union all

select mois, 'inflation_12m_pct' as indicateur, inflation_12m_pct as valeur
from {{ ref('fct_credit_mensuel') }}
where inflation_12m_pct not between -3 and 12

union all

select mois, 'volume_habitat_meur' as indicateur, volume_habitat_meur as valeur
from {{ ref('fct_credit_mensuel') }}
where volume_habitat_meur not between 1000 and 80000

union all

select mois, 'volume_conso_meur' as indicateur, volume_conso_meur as valeur
from {{ ref('fct_credit_mensuel') }}
where volume_conso_meur not between 1000 and 20000
