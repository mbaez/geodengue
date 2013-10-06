--agregar el path correcto $GEODENGUE_SRC/log/
--el archivo de origen tiene un time stamp asociado ej> event_log2398423.log
copy event_log from '/home/hduser/Documents/tesis/geodengue/src/log/event_log.log' DELIMITERS ',' CSV;
