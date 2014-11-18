select * from evolucion_log limit 10

select temperatura, dia, count(*),generacion
from evolucion_log
where --id_mosquito_padre=0
estado != 'ADULTO'
and expectativa_de_vida != 0
--and madurez != 0
and generacion=3
and codigo = 'invierno-py-90'
group by dia,temperatura,generacion
order by dia,generacion


select temperatura, dia, count(*)
from evolucion_log
where --id_mosquito_padre=0
estado = 'ADULTO'
and expectativa_de_vida !=0
and codigo = 'py-2010-full'
--and madurez !=0
group by dia,temperatura
order by dia

--delete from evolucion_log where codigo='pronostico-history-forecast'
--delete from evolucion_log where codigo='alpha-pronostico'
--delete from evolucion_log where codigo='alpha-015-pronostico'