import formatter

query = """
-- test commentaires tout en haut

(select distinct
  case when x != 0 then 1 else case when x > 0 then 2 else 3 end end as toto_le_zigoto
, 
([  f  ] . f1 + '-' + f.f2)
, f.id in (1 ,2 ,42),
'(' + 'oui' + '`@)' + @ + 1 + (1 * 1) "select" carapuce --test
, F.je_suis_un_champ_avec_un_${uuid}, coalesce(null,null,f.champ1, f.champ2), ma_function(hex(f.est_true, b.est_true))[ 0 ]
where (m = true or m = false) and m is null and ((1 != 0) or (m.is_false or case when 1=1 or 2=2 or case when 7=7 then ahah end then true else false end)) and o and i and j or a
where (m = true or m = false) and m is null and ((1 != 0) or (m.is_false or case when 1=1 or 2=2 or case when 7=7 then ahah end then true else false end)) and o and i and j or a
from (select aa from (select * from (select * from non where (1 is 1)))) where 1=1 AND 2=2
--slt les copains
order by 1 asc and 2 desc limit 15
inner natural left join ( --non
select * from oui.data.visits where non == non) on (2=2 and 1+1=1+1) and 1=1
inner natural left join ma_table)
except( -- moui
select * from oui)

-- test commentaire tout en bas

-- un deuxième
"""

print(formatter.format_query(query))