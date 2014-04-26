--cantidad de individuos de la poblacion inicial por dia
select count(*)
from evolucion_log 
where expectativa_de_vida != 0 
and id_mosquito_padre = 0
group by dia
order by dia

--cantidad de individuos de la poblacion nueva por dia
select count(*)
from evolucion_log 
where expectativa_de_vida != 0 
and id_mosquito_padre != 0
group by dia
order by dia

--cantidad de muertes por dia agrupados por estado
select count(*), dia, estado 
from evolucion_log 
where expectativa_de_vida = 0 
group by dia, estado
order by dia, estado

--cantidad de muertes por dia
select count(*), dia 
from evolucion_log 
where expectativa_de_vida = 0
group by dia 
order by dia

--cantidad de individuos vivos por dia
select count(*), dia
from evolucion_log
where expectativa_de_vida != 0
group by dia
order by dia

--disminucion de la poblacion inicial en cada dia
select count(*), dia
from evolucion_log 
where id_mosquito_padre = 0 
and expectativa_de_vida != 0
group by dia
order by dia

--distribucion de sexo
select sexo, count(distinct (id_mosquito))
from evolucion_log
group by sexo 

--cantidad promedio de oviposturas
select sum(cantidad_huevos)/count(*)
from evolucion_log
where cantidad_huevos > 0


--cantidad de huevos por cada individuo
select id_mosquito, sum(cantidad_huevos)
from evolucion_log
where cantidad_huevos > 0
group by id_mosquito
order by id_mosquito

--cantidad de individuos que ponen huevo
select count(distinct(id_mosquito))
from evolucion_log
where cantidad_huevos > 0

--cantidad total de oviposturas
select sum(cantidad_huevos)
from evolucion_log
where cantidad_huevos > 0

--tiempo promedio de vida en el estado huevo
select cast(sum(x.c) as float)/max(y.c)
from(select max(edad) as c
from evolucion_log
where estado = 'HUEVO'
and id_mosquito_padre != 0 
group by id_mosquito
order by id_mosquito) x,
(select count(distinct(id_mosquito)) as c
from evolucion_log
where estado = 'HUEVO'
and id_mosquito_padre != 0) y;


--tiempo promedio de vida en el estado larva
select cast(sum(x.c) as float)/max(y.c)
from(select max(edad) as c
from evolucion_log
where estado = 'LARVA' 
and id_mosquito_padre != 0
group by id_mosquito
order by id_mosquito) x,
(select count(distinct(id_mosquito)) as c
from evolucion_log
where estado = 'LARVA' 
and id_mosquito_padre != 0) y;

select count(*)
from evolucion_log

--tiempo promedio de vida en el estado pupa
select cast(sum(x.c) as float)/max(y.c)
from(select max(edad) as c
from evolucion_log
where estado = 'PUPA' 
group by id_mosquito
order by id_mosquito) x,
(select count(distinct(id_mosquito)) as c
from evolucion_log
where estado = 'PUPA') y;

--tiempo promedio de vida en el estado larva
select cast(sum(x.c) as float)/max(y.c)
from(select max(edad) as c
from evolucion_log
where estado = 'ADULTO'
group by id_mosquito
order by id_mosquito) x,
(select count(distinct(id_mosquito)) as c
from evolucion_log
where estado = 'ADULTO'  ) y;

select cast(x.c as float)/y.c
from
(select count(distinct(id_mosquito)) as c
from evolucion_log
where cantidad_huevos > 0) x
,
(select count(distinct(id_mosquito)) c
from evolucion_log 
where estado = 'ADULTO' and sexo = 'HEMBRA') y;

--cantidad de muertes por dia
select count(*), dia, sexo 
from evolucion_log 
where expectativa_de_vida = 0
group by dia,sexo 
order by dia

-- edad de los individuos que pusieron huevo
select distinct (id_mosquito), edad
from evolucion_log
where cantidad_huevos > 0


-- cantidad de huevos, larvas, pupas, y adultos en la poblacion final
select count(*) , estado
from evolucion_log 
where dia = 29  
group by estado
