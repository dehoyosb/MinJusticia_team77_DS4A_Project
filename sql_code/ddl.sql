
CREATE DATABASE minjusticia;

drop table public.reincidencia_postpenados;
create table reincidencia_postpenados (
INTERNOEN varchar(100),
SITUACION_JURIDICA	varchar(5),
DELITO	varchar(1000),
FECHA_CAPTURA date,
FECHA_INGRESO	date,
AÑO_INGRESO	int,
MES_INGRESO	varchar(100),
ESTADO_INGRESO	varchar(100),
EDAD	int,
GENERO	varchar(100),
REINCIDENTE	varchar(100),
ESTABLECIMIENTO	varchar(100),
REGIONAL varchar(100)
);

