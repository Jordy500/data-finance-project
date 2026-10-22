-- renvoie une ligne si un mois manque entre le premier et le dernier
with controle as (
    select
        count(*) as nb_lignes,
        date_diff(max(mois), min(mois), month) + 1 as nb_attendu
    from {{ ref('fct_credit_mensuel') }}
)

select * from controle
where nb_lignes != nb_attendu
