

-- create all tables related in the ER model designed with your primary keys


/*
 --deprecaded
CREATE TABLE condicion_excepcional (
    id_condicion_excepcional  INTEGER NOT NULL,
    nombre                    VARCHAR(100)
);

ALTER TABLE condicion_excepcional ADD CONSTRAINT condicion_excepcional_pk PRIMARY KEY ( id_condicion_excepcional );
*/

CREATE TABLE reconocimiento_etnico (
    id_reconocimiento_etnico  INTEGER NOT NULL,
    nombre                    VARCHAR(100),
    name_eng                    VARCHAR(100)
);

ALTER TABLE reconocimiento_etnico ADD CONSTRAINT reconocimiento_etnico_pk PRIMARY KEY ( id_reconocimiento_etnico );

CREATE TABLE diversidad_sexual (
    id_diversidad_sexual INTEGER NOT NULL,
    nombre                    VARCHAR(100)
);

ALTER TABLE diversidad_sexual ADD CONSTRAINT diversidad_sexual_pk PRIMARY KEY ( id_diversidad_sexual );






CREATE TABLE delito (
    id_delito  INTEGER NOT NULL,
    id_subtitulo_delito integer not null,
    nombre     VARCHAR(1000),
    name_eng     VARCHAR(1000)
);

ALTER TABLE delito ADD CONSTRAINT delito_pk PRIMARY KEY ( id_delito );

CREATE TABLE departamento (
    id_departamento  INTEGER NOT NULL,
    codigo_dane      VARCHAR(2),
    nombre           VARCHAR(100)
);

ALTER TABLE departamento ADD CONSTRAINT departamento_pk PRIMARY KEY ( id_departamento );

-- drop table establecimiento;
CREATE TABLE establecimiento (
    id_establecimiento      INTEGER NOT NULL,
    nombre                  VARCHAR(100),
    regional   INTEGER NOT NULL,
    municipio INTEGER NOT NULL,
    codigo_establecimiento  VARCHAR(20)
);

ALTER TABLE establecimiento ADD CONSTRAINT establecimiento_pk PRIMARY KEY ( id_establecimiento );

CREATE TABLE estado (
    id_estado  INTEGER NOT NULL,
    nombre     VARCHAR(100),
    name_eng     VARCHAR(100)
);

ALTER TABLE estado ADD CONSTRAINT estado_pk PRIMARY KEY ( id_estado );

CREATE TABLE estado_civil (
    id_estado_civil  INTEGER NOT NULL,
    nombre           VARCHAR(100),
    name_eng           VARCHAR(100)
);

ALTER TABLE estado_civil ADD CONSTRAINT estado_civil_pk PRIMARY KEY ( id_estado_civil );

CREATE TABLE estado_ingreso (
    id_estado_ingreso  INTEGER NOT NULL,
    nombre             VARCHAR(100),
    name_eng             VARCHAR(100)
);

ALTER TABLE estado_ingreso ADD CONSTRAINT estado_ingreso_pk PRIMARY KEY ( id_estado_ingreso );

CREATE TABLE genero (
    id_genero  INTEGER NOT NULL,
    nombre     VARCHAR(100),
    name_eng     VARCHAR(100)
);

ALTER TABLE genero ADD CONSTRAINT genero_pk PRIMARY KEY ( id_genero );
 -- drop table municipio cascade;
CREATE TABLE municipio (
    id_municipio                  INTEGER NOT NULL,
    codigo_dane                   VARCHAR(5),
    nombre                        VARCHAR(100),
    departamento  INTEGER NOT NULL
);

ALTER TABLE municipio ADD CONSTRAINT municipio_pk PRIMARY KEY ( id_municipio );

CREATE TABLE nacionalidad (
    id_pais  INTEGER NOT NULL,
    pais     VARCHAR(100),
    country varchar(100)
);

ALTER TABLE nacionalidad ADD CONSTRAINT nacionalidad_pk PRIMARY KEY ( id_pais );

CREATE TABLE nivel_educativo (
    id_nivel_educativo  INTEGER NOT NULL,
    nombre              VARCHAR(100),
    name_eng               VARCHAR(100)
);

ALTER TABLE nivel_educativo ADD CONSTRAINT nivel_educativo_pk PRIMARY KEY ( id_nivel_educativo );

-- drop table persona;
CREATE TABLE persona (
    id_persona                          INTEGER NOT NULL,
    internoen                           VARCHAR(1000),
    genero                    INTEGER NOT NULL,
    nacionalidad                INTEGER not NULL,
    reincidente                         INTEGER NOT NULL,
    anio_nacimiento                     integer not null,
    estado_civil        INTEGER NOT NULL, 
    nivel_educativo  INTEGER NOT null,
    reconocimiento_etnico integer not null,
    diversidad_sexual integer not null,
    extranjero integer not null,
    condicion_exepcional text
);

ALTER TABLE persona ADD CONSTRAINT persona_pk PRIMARY KEY ( id_persona );


create table persona_diversidad_sexual (
    id_persona                          INTEGER NOT NULL,
    id_diversidad_sexual                INTEGER NOT NULL
);




CREATE TABLE regional (
    id_regional  INTEGER NOT NULL,
    nombre       VARCHAR(100)
);

ALTER TABLE regional ADD CONSTRAINT regional_pk PRIMARY KEY ( id_regional );

CREATE TABLE registro (
    persona_id_persona                              INTEGER NOT NULL,
    delito_id_delito                                INTEGER NOT NULL, 
    estado_ingreso                INTEGER NOT NULL,
    id_registro                                     INTEGER NOT NULL,
    fecha_captura                                   DATE,
    fecha_ingreso                                   DATE, 
    establecimiento              INTEGER NOT NULL,
    tentativa                                  INTEGER NOT NULL,
    agravado                                 INTEGER NOT NULL,
    calificado                                 INTEGER NOT NULL,
    fecha_salida                                    DATE,
    edad                                            INTEGER,
    municipio_id_municipio                          INTEGER NOT NULL,
    actividades_estudio                                 INTEGER NOT NULL,
    actividades_trabajo                                 INTEGER NOT NULL,
    actividades_enseñanza                                 INTEGER NOT NULL,
    hijos_menores                                 INTEGER NOT NULL, 
    condicion_excepcional text,
    estado_id_estado                                INTEGER NOT NULL, 
    situacion_juridica      integer NOT null,
    madre_gestante integer not null,
    madre_lactante integer not null,
    discapacidad integer not null,
    adulto_mayor integer not null
);


ALTER TABLE registro ADD CONSTRAINT registro_pk PRIMARY KEY ( id_registro );

CREATE TABLE si_no (
    id_si_no  INTEGER NOT NULL,
    codigo varchar(2),
    nombre    VARCHAR(100),
    name_eng    VARCHAR(100)
);

ALTER TABLE si_no ADD CONSTRAINT si_no_pk PRIMARY KEY ( id_si_no );

CREATE TABLE situacion_juridica (
    id_situacion_juridica  INTEGER,
    nombre                 VARCHAR(1000),
    name_eng                 VARCHAR(100)
);

ALTER TABLE situacion_juridica ADD CONSTRAINT situacion_juridica_pk PRIMARY KEY ( id_situacion_juridica );

CREATE TABLE sociodemografico_registros (
    registro_id_registro                   INTEGER NOT NULL,
    valor                                  VARCHAR(1000), 
    sociodemograficos  INTEGER NOT NULL
);

ALTER TABLE sociodemografico_registros ADD CONSTRAINT sociodemografico_registros_pk PRIMARY KEY ( registro_id_registro,
                                                                                                  sociodemograficos );

CREATE TABLE sociodemograficos (
    id_sociodemografico  INTEGER NOT NULL,
    nombre               VARCHAR(1000)
);

ALTER TABLE sociodemograficos ADD CONSTRAINT sociodemograficos_pk PRIMARY KEY ( id_sociodemografico );


CREATE TABLE subtitulo_delito (
    id_subtitulo_delito             INTEGER NOT NULL,
    nombre                          varchar(1000),
    id_titulo_delito  INTEGER NOT null,
    name_eng                    VARCHAR(1000)
);

ALTER TABLE subtitulo_delito ADD CONSTRAINT subtitulo_delito_pk PRIMARY KEY ( id_subtitulo_delito );

CREATE TABLE titulo_delito (
    id_titulo_delito  INTEGER NOT NULL,
    nombre            varchar(1000),
    name_eng            VARCHAR(1000)
);

ALTER TABLE titulo_delito ADD CONSTRAINT titulo_delito_pk PRIMARY KEY ( id_titulo_delito );




ALTER TABLE delito
    ADD CONSTRAINT delito_subtitulo_delito_fk FOREIGN KEY ( id_subtitulo_delito )
        REFERENCES subtitulo_delito ( id_subtitulo_delito );


ALTER TABLE subtitulo_delito
    ADD CONSTRAINT subtitulo_delito_titulo_delito_fk FOREIGN KEY ( id_titulo_delito )
        REFERENCES titulo_delito ( id_titulo_delito );

ALTER TABLE establecimiento
    ADD CONSTRAINT establecimiento_municipio_fk FOREIGN KEY ( municipio )
        REFERENCES municipio ( id_municipio );

ALTER TABLE establecimiento
    ADD CONSTRAINT establecimiento_regional_fk FOREIGN KEY ( regional )
        REFERENCES regional ( id_regional );

ALTER TABLE municipio
    ADD CONSTRAINT municipio_departamento_fk FOREIGN KEY ( departamento )
        REFERENCES departamento ( id_departamento );

ALTER TABLE persona
    ADD CONSTRAINT persona_estado_civil_fk FOREIGN KEY ( estado_civil )
        REFERENCES estado_civil ( id_estado_civil );

ALTER TABLE persona
    ADD CONSTRAINT persona_genero_fk FOREIGN KEY ( genero )
        REFERENCES genero ( id_genero );

ALTER TABLE persona
    ADD CONSTRAINT persona_nacionalidad_fk FOREIGN KEY ( nacionalidad )
        REFERENCES nacionalidad ( id_pais );

ALTER TABLE persona
    ADD CONSTRAINT persona_nivel_educativo_fk FOREIGN KEY ( nivel_educativo )
        REFERENCES nivel_educativo ( id_nivel_educativo );

ALTER TABLE persona
    ADD CONSTRAINT persona_si_no_fk FOREIGN KEY ( reincidente )
        REFERENCES si_no ( id_si_no );
       
ALTER TABLE persona
    ADD CONSTRAINT reconocimiento_etnico_fk FOREIGN KEY ( reconocimiento_etnico )
        REFERENCES reconocimiento_etnico( id_reconocimiento_etnico );
       
ALTER TABLE persona_diversidad_sexual
    ADD CONSTRAINT persona_diversidad_sexual_diversidad_fk FOREIGN KEY ( id_diversidad_sexual )
        REFERENCES diversidad_sexual( id_diversidad_sexual );
       
ALTER TABLE persona_diversidad_sexual
    ADD CONSTRAINT persona_diversidad_sexual_persona_fk FOREIGN KEY ( id_persona )
        REFERENCES persona( id_persona );
       
ALTER TABLE persona
    ADD CONSTRAINT extranjero_fk FOREIGN KEY ( extranjero )
         REFERENCES si_no ( id_si_no );

       
       
       
       
       

/*
 deprecade
 ALTER TABLE registro
    ADD CONSTRAINT registro_condicion_excepcional_fk FOREIGN KEY ( condicion_excepcional )
        REFERENCES condicion_excepcional ( id_condicion_excepcional );
*/
ALTER TABLE registro
    ADD CONSTRAINT registro_delito_fk FOREIGN KEY ( delito_id_delito )
        REFERENCES delito ( id_delito );

ALTER TABLE registro
    ADD CONSTRAINT registro_establecimiento_fk FOREIGN KEY ( establecimiento )
        REFERENCES establecimiento ( id_establecimiento );

ALTER TABLE registro
    ADD CONSTRAINT registro_estado_fk FOREIGN KEY ( estado_id_estado )
        REFERENCES estado ( id_estado );

ALTER TABLE registro
    ADD CONSTRAINT registro_estado_ingreso_fk FOREIGN KEY ( estado_ingreso )
        REFERENCES estado_ingreso ( id_estado_ingreso );

ALTER TABLE registro
    ADD CONSTRAINT registro_municipio_fk FOREIGN KEY ( municipio_id_municipio )
        REFERENCES municipio ( id_municipio );

ALTER TABLE registro
    ADD CONSTRAINT registro_persona_fk FOREIGN KEY ( persona_id_persona )
        REFERENCES persona ( id_persona );

ALTER TABLE registro
    ADD CONSTRAINT registro_si_no_fk FOREIGN KEY ( tentativa )
        REFERENCES si_no ( id_si_no );

ALTER TABLE registro
    ADD CONSTRAINT registro_si_no_fkv2 FOREIGN KEY ( agravado )
        REFERENCES si_no ( id_si_no );

ALTER TABLE registro
    ADD CONSTRAINT registro_si_no_fkv3 FOREIGN KEY ( calificado )
        REFERENCES si_no ( id_si_no );

ALTER TABLE registro
    ADD CONSTRAINT registro_si_no_fkv4 FOREIGN KEY ( actividades_estudio )
        REFERENCES si_no ( id_si_no );

ALTER TABLE registro
    ADD CONSTRAINT registro_si_no_fkv5 FOREIGN KEY ( actividades_trabajo )
        REFERENCES si_no ( id_si_no );

ALTER TABLE registro
    ADD CONSTRAINT registro_si_no_fkv6 FOREIGN KEY ( actividades_enseñanza )
        REFERENCES si_no ( id_si_no );

ALTER TABLE registro
    ADD CONSTRAINT registro_si_no_fkv7 FOREIGN KEY ( hijos_menores )
        REFERENCES si_no ( id_si_no );

ALTER TABLE registro
    ADD CONSTRAINT registro_situacion_juridica_fk FOREIGN KEY ( situacion_juridica )
        REFERENCES situacion_juridica ( id_situacion_juridica );

       
       
ALTER TABLE registro
    ADD CONSTRAINT madre_gestante_fk FOREIGN KEY ( madre_gestante )
        REFERENCES si_no ( id_si_no );
ALTER TABLE registro
    ADD CONSTRAINT madre_lactante_fk FOREIGN KEY ( madre_lactante )
        REFERENCES si_no ( id_si_no );
ALTER TABLE registro
    ADD CONSTRAINT discapacidad_fk FOREIGN KEY ( discapacidad )
        REFERENCES si_no ( id_si_no );
ALTER TABLE registro
    ADD CONSTRAINT adulto_mayor_fk FOREIGN KEY ( adulto_mayor )
        REFERENCES si_no ( id_si_no );
  
    
ALTER TABLE sociodemografico_registros
    ADD CONSTRAINT sociodemografico_registros_registro_fk FOREIGN KEY ( registro_id_registro )
        REFERENCES registro ( id_registro );

ALTER TABLE sociodemografico_registros
    ADD CONSTRAINT sociodemografico_registros_sociodemograficos_fk FOREIGN KEY ( sociodemograficos )
        REFERENCES sociodemograficos ( id_sociodemografico );
        
       

-- procedimientos almacenados para las tablas de personas

create sequence public.personas_seq start 1;

--drop tcompararpersonas;
CREATE OR REPLACE FUNCTION public.tcompararpersonas()
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
begin
INSERT INTO public.persona
(id_persona, internoen, genero, nacionalidad, reincidente, anio_nacimiento, estado_civil, nivel_educativo, reconocimiento_etnico, extranjero, diversidad_sexual, condicion_exepcional)
SELECT nextval('public.personas_seq') as id_persona,
"INTERNOEN" as internoen, 
g.id_genero as genero , 
case when n.id_pais is null then 22 else n.id_pais end as nacionalidad ,
2 as reincidente, 
"ANO_NACIMIENTO" as anio_nacimiento, 
case when ec.id_estado_civil is null then 3 else ec.id_estado_civil end as estado_civil, 
ne.id_nivel_educativo as nivel_educativo,
re.id_reconocimiento_etnico as reconocimiento_etnico , 
ext.id_si_no as extranjero,
ds.id_si_no as diversidad_sexual,
ptmp."CONDIC_EXPECIONAL" as condicion_exepcional

FROM public.personas_tmp ptmp
left join genero g on g.nombre = ptmp."GENERO" 
left join nacionalidad n on n.pais =ptmp."PAIS_INTERNO" 
left join estado_civil ec on ec.nombre = ptmp."ESTADO_CIVIL" 
left join nivel_educativo ne on ne.nombre =ptmp."NIVEL_EDUCATIVO"
left join reconocimiento_etnico re on re.nombre = ptmp.reconocimiento_etnico
left join si_no ext on ext.codigo = ptmp.extranjero
left join si_no ds on ds.codigo = ptmp.diversidad_sexual

where "INTERNOEN" not in (select internoen from public.persona p );
drop table public.personas_tmp;
return 1;
END;
$function$
;



--------------------------------------------------------
---------- add severity index

ALTER TABLE registro
ADD COLUMN severity float;



-- procedimientos almacenados para las tablas de general
       
--select count(*) from public.registros_tmp rt 

create sequence public.registro_seq start 1;

--drop function public.tcompararreg;
CREATE OR REPLACE FUNCTION public.tcompararreg()
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
begin
INSERT INTO public.registro
(persona_id_persona, delito_id_delito, estado_ingreso, id_registro, fecha_captura, fecha_ingreso, establecimiento, 
tentativa, agravado, calificado, fecha_salida, edad, municipio_id_municipio, actividades_estudio, actividades_trabajo, 
actividades_enseñanza, hijos_menores, condicion_excepcional, estado_id_estado, situacion_juridica,madre_gestante, 
madre_lactante,discapacidad,adulto_mayor, severity)

SELECT 
p.id_persona as persona_id_persona,
d.id_delito as delito_id_delito, 
case when ei.id_estado_ingreso is null then 4 else ei.id_estado_ingreso end as estado_ingreso, 
nextval('public.registro_seq') as id_registro,
to_date("FECHA_CAPTURA", 'dd/mm/yy') as fecha_captura, 
to_date("FECHA_INGRESO", 'dd/mm/yy') as fecha_ingreso, 
es.id_establecimiento as establecimiento, 
ten.id_si_no as tentativa, 
case when agr.id_si_no is null then 1 else  agr.id_si_no end as agravado,
case when cal.id_si_no is null then 1 else cal.id_si_no end as calificado,
to_date("FECHA_SALIDA", 'dd/mm/yy') as fecha_salida, 
"EDAD" as edad,
1 as municipio_id_municipio, 
case when "ACTIVIDADES_ESTUDIO" = 'SI' then 2 else 1 end as actividades_estudio,
case when "ACTIVIDADES_TRABAJO"= 'SI' then 2 else 1 end as actividades_trabajo, 
case when "ACTIVIDADES_ENSEÑANZA" = 'SI' then 2 else 1 end as actividades_enseñanza,
case when "HIJOS_MENORES"  = 'SI' then 2 else 1 end as hijos_menores, 
reg."CONDIC_EXPECIONAL" as condicion_excepcional, 
est.id_estado as estado_id_estado, 
sj.id_situacion_juridica as situacion_juridica,
case when mg.id_si_no is null then 1 else  mg.id_si_no end as madre_gestante,
case when ml.id_si_no is null then 1 else  ml.id_si_no end as madre_lactante,
case when disc.id_si_no is null then 1 else  disc.id_si_no end as discapacidad,
case when adm.id_si_no is null then 1 else  adm.id_si_no end as adulto_mayor,
reg.severity as severity
FROM public.registros_tmp reg
left join persona p on p.internoen = reg."INTERNOEN" 
left join (select id_delito, concat(del.nombre, sub_del.nombre ) as compuesto from delito del left join subtitulo_delito sub_del on del.id_subtitulo_delito = sub_del.id_subtitulo_delito) d on d.compuesto = concat(reg."DELITO", reg."SUBTITULO_DELITO")
left join estado_ingreso ei on ei.nombre = reg."ESTADO_INGRESO" 
left join establecimiento es on es.nombre = reg."ESTABLECIMIENTO" 
left join si_no ten on ten.codigo = reg."TENTATIVA"
left join si_no agr on agr.codigo = reg."AGRAVADO" 
left join si_no cal on cal.codigo = reg."CALIFICADO" 
left join estado est on est.nombre = reg."ESTADO"
left join situacion_juridica sj on sj.nombre = reg."SITUACION_JURIDICA"
left join si_no mg on mg.codigo = reg.madre_gestante 
left join si_no ml on ml.codigo = reg.madre_lactante 
left join si_no disc on disc.codigo = reg.discapacidad 
left join si_no adm on adm.codigo = reg.adulto_mayor;
return 1;
END;
$function$
;
       




-------------------------------------------------------------------------
--- add human index data
ALTER TABLE registro ADD COLUMN shdi float;
ALTER TABLE registro ADD COLUMN healthindex float;
ALTER TABLE registro ADD COLUMN incindex float;
ALTER TABLE registro ADD COLUMN edindex float;
ALTER TABLE registro ADD COLUMN lifexp float;
ALTER TABLE registro ADD COLUMN gnic float;
ALTER TABLE registro ADD COLUMN esch float;
ALTER TABLE registro ADD COLUMN msch float;
ALTER TABLE registro ADD COLUMN pop float;


CREATE OR REPLACE FUNCTION public.tsdhi_registro()
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
begin

UPDATE public.registro reg
    SET 
        shdi=tb1.shdi, 
        healthindex=tb1.healthindex, 
        incindex=tb1.incindex, 
        edindex=tb1.edindex, 
        lifexp=tb1.lifexp, 
        gnic=tb1.gnic, 
        esch=tb1.esch, 
        msch=tb1.msch, 
        pop=tb1.pop
    from (select id_registro, sdhi.shdi, sdhi.healthindex, sdhi.incindex, sdhi.edindex, sdhi.lifexp, sdhi.gnic, sdhi.esch, sdhi.msch, sdhi.pop from public.registro reg
    left join  public.establecimiento est on reg.establecimiento = est.id_establecimiento
    left join public.municipio munic on est.municipio= munic.id_municipio
    left join public."GDLCODE" sdhi on  munic.departamento= sdhi.id_departamento and sdhi.year = extract(year from reg.fecha_ingreso)) tb1
    WHERE tb1.id_registro = reg.id_registro;
return 1;
END;
$function$
;




---- add context data

CREATE TABLE context_minjusticia (year int, capacity int, population int);





--- views to simplify the scripts 

create view etl_select_8 as
select registro.persona_id_persona, m.departamento ,registro.delito_id_delito, registro.estado_ingreso,
                            registro.id_registro, registro.fecha_captura, registro.fecha_ingreso, registro.establecimiento, 
                            registro.fecha_salida, registro.edad, registro.municipio_id_municipio, registro.estado_id_estado, 
                            registro.situacion_juridica, registro.severity, registro.shdi, 
                            
                            persona.id_persona, persona.genero, persona.internoen, persona.nivel_educativo,
                           departamento.nombre, delito.name_eng as delito, sd.name_eng as subtitulo, 
                           td.name_eng as titulo , 2020-anio_nacimiento as "actual age" , 
                                                case when registro.condicion_excepcional like 'NINGUNO' then 1 else 2 
                                                    end as condicion_excepcional,
                                             case when fecha_salida is null then now()::date else fecha_salida end as fecha_salida2, 
                                             row_number() OVER (PARTITION BY id_persona ORDER BY fecha_salida desc) AS numero_evento,
                                             row_number() OVER (PARTITION BY id_persona ORDER BY fecha_salida asc) AS numero,

                                            actividades_estudio.nombre  as actividades_estudio, 
                                            actividades_trabajo.nombre as actividades_trabajo, 
                                            actividades_enseñanza.nombre  as actividades_enseñanza, 
                                            hijos_menores.nombre  as hijos_menores, 
                                            madre_gestante.nombre as madre_gestante, 
                                            madre_lactante.nombre  as madre_lactante, 
                                            discapacidad.nombre  as discapacidad, 
                                            adulto_mayor.nombre  as adulto_mayor,
                                            sd.name_eng as subtitulo_delito

                                             from registro
                                             left join (select id_establecimiento, municipio from establecimiento) e
                                             on registro.establecimiento = e.id_establecimiento 
                                             left join (select id_municipio, 
                                                               departamento, 
                                                               nombre as mun_name from municipio) m 
                                             on e.municipio = m.id_municipio  
                                             left join departamento 
                                             on m.departamento = departamento.id_departamento
                                             left join persona on registro.persona_id_persona = persona.id_persona 
                                             left join delito on registro.delito_id_delito = delito.id_delito
                                             left join public.subtitulo_delito sd on delito.id_subtitulo_delito= sd.id_subtitulo_delito
                                             left join public.titulo_delito td on sd.id_titulo_delito = td.id_titulo_delito
                                             left join public.si_no actividades_estudio on actividades_estudio.id_si_no =registro.actividades_estudio 
                                            left join public.si_no actividades_trabajo on actividades_trabajo.id_si_no =registro.actividades_trabajo 
                                            left join public.si_no actividades_enseñanza on actividades_enseñanza.id_si_no =registro.actividades_enseñanza 
                                            left join public.si_no hijos_menores on hijos_menores.id_si_no =registro.hijos_menores 
                                            left join public.si_no madre_gestante on madre_gestante.id_si_no =registro.madre_gestante 
                                            left join public.si_no madre_lactante on madre_lactante.id_si_no =registro.madre_lactante 
                                            left join public.si_no discapacidad on discapacidad.id_si_no =registro.discapacidad 
                                            left join public.si_no adulto_mayor on adulto_mayor.id_si_no =registro.adulto_mayor


                                            ;

create table radar_plot_data (id int, feature_name varchar(200), feature_importance int , "label" int);


CREATE OR REPLACE VIEW public.surv_view AS
select * , row_number() OVER (PARTITION BY id_persona ORDER BY fecha_salida2 DESC) AS numero_evento,
    row_number() OVER (PARTITION BY id_persona ORDER BY fecha_salida2) AS numero from (
 SELECT  distinct on (persona_id_persona, fecha_salida2) registro.persona_id_persona,
    m.departamento,
    registro.delito_id_delito,
    registro.estado_ingreso,
    registro.id_registro,
    registro.fecha_captura,
    registro.fecha_ingreso,
    registro.establecimiento,
    registro.fecha_salida,
    registro.edad,
    registro.municipio_id_municipio,
    registro.estado_id_estado,
    registro.situacion_juridica,
    registro.severity,
    registro.shdi,
    persona.id_persona,
    persona.genero,
    persona.internoen,
    persona.nivel_educativo,
    departamento.nombre,
    delito.name_eng AS delito,
    sd.name_eng AS subtitulo,
    td.name_eng AS titulo,
    2020 - persona.anio_nacimiento AS "actual age",
        CASE
            WHEN registro.condicion_excepcional ~~ 'NINGUNO'::text THEN 1
            ELSE 2
        END AS condicion_excepcional,
        CASE
            WHEN registro.fecha_salida IS NULL THEN now()::date
            ELSE registro.fecha_salida
        END AS fecha_salida2,
    actividades_estudio.nombre AS actividades_estudio,
    actividades_trabajo.nombre AS actividades_trabajo,
    "actividades_enseñanza".nombre AS "actividades_enseñanza",
    hijos_menores.nombre AS hijos_menores,
    madre_gestante.nombre AS madre_gestante,
    madre_lactante.nombre AS madre_lactante,
    discapacidad.nombre AS discapacidad,
    adulto_mayor.nombre AS adulto_mayor,
    sd.name_eng AS subtitulo_delito
   FROM registro
     LEFT JOIN ( SELECT establecimiento.id_establecimiento,
            establecimiento.municipio
           FROM establecimiento) e ON registro.establecimiento = e.id_establecimiento
     LEFT JOIN ( SELECT municipio.id_municipio,
            municipio.departamento,
            municipio.nombre AS mun_name
           FROM municipio) m ON e.municipio = m.id_municipio
     LEFT JOIN departamento ON m.departamento = departamento.id_departamento
     LEFT JOIN persona ON registro.persona_id_persona = persona.id_persona
     LEFT JOIN delito ON registro.delito_id_delito = delito.id_delito
     LEFT JOIN subtitulo_delito sd ON delito.id_subtitulo_delito = sd.id_subtitulo_delito
     LEFT JOIN titulo_delito td ON sd.id_titulo_delito = td.id_titulo_delito
     LEFT JOIN si_no actividades_estudio ON actividades_estudio.id_si_no = registro.actividades_estudio
     LEFT JOIN si_no actividades_trabajo ON actividades_trabajo.id_si_no = registro.actividades_trabajo
     LEFT JOIN si_no "actividades_enseñanza" ON "actividades_enseñanza".id_si_no = registro."actividades_enseñanza"
     LEFT JOIN si_no hijos_menores ON hijos_menores.id_si_no = registro.hijos_menores
     LEFT JOIN si_no madre_gestante ON madre_gestante.id_si_no = registro.madre_gestante
     LEFT JOIN si_no madre_lactante ON madre_lactante.id_si_no = registro.madre_lactante
     LEFT JOIN si_no discapacidad ON discapacidad.id_si_no = registro.discapacidad
     LEFT JOIN si_no adulto_mayor ON adulto_mayor.id_si_no = registro.adulto_mayor) tb1;


