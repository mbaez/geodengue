select codigo,2,sum(tmp.cg_dias)/count(tmp)
from (
	select codigo, id_mosquito,cantidad_oviposicion, ciclo_gonotrofico as cg_dias
	from evolucion_log
	where ciclo_gonotrofico is not null
	and ciclo_gonotrofico > 0
	and estado='ADULTO'
	and sexo = 'HEMBRA'
	and se_alimenta = 'TRUE'
	and cantidad_oviposicion > 0
	group by codigo, id_mosquito,cantidad_oviposicion ,ciclo_gonotrofico
) as tmp
where  codigo= 'invierno-py-90'
group by codigo
--order by codigo

UNION

select codigo,1, sum(tmp.cg_dias)/count(tmp)
from (
	select codigo, id_mosquito,cantidad_oviposicion, ciclo_gonotrofico as cg_dias
	from evolucion_log
	where ciclo_gonotrofico is not null
	and ciclo_gonotrofico > 0
	and estado='ADULTO'
	and sexo = 'HEMBRA'
	and se_alimenta = 'TRUE'
	and cantidad_oviposicion = 0
	group by codigo, id_mosquito,cantidad_oviposicion ,ciclo_gonotrofico
) as tmp
where  codigo= 'invierno-py-90'
group by codigo
order by codigo


select x.codigo, x.estado, round (sum(x.c - x.m)*1.0/count(x),2) as dias
    from(
        select codigo,estado, min(dia) as m, max(dia) as c
        from evolucion_log tmp
       where ciclo_gonotrofico is not null
	and ciclo_gonotrofico > 0
	and estado='ADULTO'
	and sexo = 'HEMBRA'
	--and se_alimenta = 'TRUE'
	and cantidad_oviposicion =3
        and exists (
        select *
        from evolucion_log
        where id_mosquito = tmp.id_mosquito
        --and id != tmp.id
		and estado='ADULTO'
		and sexo = 'HEMBRA'
		and cantidad_oviposicion = tmp.cantidad_oviposicion +1
        and codigo = tmp.codigo
        )
        group by codigo, id_mosquito, estado
        --order by id_mosquito
    ) x
    where  x.codigo= 'invierno-py-90'
    group by x.codigo,x.estado
    


    
