-- Table: puntos_control

-- Script para agregar las columnas 
-- de fecha de recoleccion y instalacion
-- a la entidad punto de control

ALTER TABLE 
	puntos_control
ADD COLUMN 
	fecha_recoleccion date;
  
ALTER TABLE 
	puntos_control 
ADD COLUMN 
	fecha_instalacion date; 