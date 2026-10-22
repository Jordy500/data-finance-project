-- un mois par ligne, avec le dernier taux décidé avant la fin du mois
with calendrier as (
    select mois
    from {{ ref('stg_taux_credit_habitat') }}
)

select
    calendrier.mois,
    decisions.taux_directeur_pct
from calendrier
left join {{ ref('stg_taux_directeur_bce') }} as decisions
    on decisions.date_decision <= last_day(calendrier.mois)
qualify row_number() over (
    partition by calendrier.mois
    order by decisions.date_decision desc
) = 1
