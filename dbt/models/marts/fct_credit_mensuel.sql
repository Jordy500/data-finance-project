-- une ligne par mois : coût, inflation, taux réel et volume du crédit aux ménages
with base as (
    select
        taux_dir.mois,
        taux_dir.taux_directeur_pct,
        th.taux_habitat_pct,
        tc.taux_conso_pct,
        vh.volume_habitat_meur,
        vc.volume_conso_meur,
        inflation.inflation_12m_pct
    from {{ ref('int_taux_directeur_mensuel') }} as taux_dir
    left join {{ ref('stg_taux_credit_habitat') }} as th on th.mois = taux_dir.mois
    left join {{ ref('stg_taux_credit_conso') }} as tc on tc.mois = taux_dir.mois
    left join {{ ref('stg_volume_credit_habitat') }} as vh on vh.mois = taux_dir.mois
    left join {{ ref('stg_volume_credit_conso') }} as vc on vc.mois = taux_dir.mois
    left join {{ ref('int_inflation') }} as inflation on inflation.mois = taux_dir.mois
)

select
    mois,
    taux_directeur_pct,
    inflation_12m_pct,
    taux_habitat_pct,
    round(taux_habitat_pct - inflation_12m_pct, 2) as taux_reel_habitat_pct,
    taux_conso_pct,
    round(taux_conso_pct - inflation_12m_pct, 2) as taux_reel_conso_pct,
    volume_habitat_meur,
    round((volume_habitat_meur / lag(volume_habitat_meur, 12) over (order by mois) - 1) * 100, 1) as volume_habitat_var_an_pct,
    case
        when count(volume_habitat_meur) over fenetre_12m = 12
        then round(avg(volume_habitat_meur) over fenetre_12m)
    end as volume_habitat_moy12m_meur,
    volume_conso_meur,
    round((volume_conso_meur / lag(volume_conso_meur, 12) over (order by mois) - 1) * 100, 1) as volume_conso_var_an_pct,
    case
        when count(volume_conso_meur) over fenetre_12m = 12
        then round(avg(volume_conso_meur) over fenetre_12m)
    end as volume_conso_moy12m_meur
from base
window fenetre_12m as (order by mois rows between 11 preceding and current row)
order by mois
