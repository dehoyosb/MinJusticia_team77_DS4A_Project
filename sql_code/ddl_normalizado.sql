CREATE TABLE condicion_excepcional (
    id_condicion_excepcional  INTEGER NOT NULL,
    nombre                    VARCHAR(100)
);

ALTER TABLE condicion_excepcional ADD CONSTRAINT condicion_excepcional_pk PRIMARY KEY ( id_condicion_excepcional );

CREATE TABLE delito (
    id_delito  INTEGER NOT NULL,
    nombre     VARCHAR(1000)
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
    nombre     VARCHAR(100)
);

ALTER TABLE estado ADD CONSTRAINT estado_pk PRIMARY KEY ( id_estado );

CREATE TABLE estado_civil (
    id_estado_civil  INTEGER NOT NULL,
    nombre           VARCHAR(100)
);

ALTER TABLE estado_civil ADD CONSTRAINT estado_civil_pk PRIMARY KEY ( id_estado_civil );

CREATE TABLE estado_ingreso (
    id_estado_ingreso  INTEGER NOT NULL,
    nombre             VARCHAR(100)
);

ALTER TABLE estado_ingreso ADD CONSTRAINT estado_ingreso_pk PRIMARY KEY ( id_estado_ingreso );

CREATE TABLE genero (
    id_genero  INTEGER NOT NULL,
    nombre     VARCHAR(100)
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
    pais     VARCHAR(100)
);

ALTER TABLE nacionalidad ADD CONSTRAINT nacionalidad_pk PRIMARY KEY ( id_pais );

CREATE TABLE nivel_educativo (
    id_nivel_educativo  INTEGER NOT NULL,
    nombre              VARCHAR(100)
);

ALTER TABLE nivel_educativo ADD CONSTRAINT nivel_educativo_pk PRIMARY KEY ( id_nivel_educativo );

-- drop table persona;
CREATE TABLE persona (
    id_persona                          INTEGER NOT NULL,
    internoen                           VARCHAR(1000),
    genero                    INTEGER NOT NULL,
    nacionalidad                INTEGER NOT NULL,
    reincidente                         INTEGER NOT NULL,
    anio_nacimiento                     integer not null,
    estado_civil        INTEGER NOT NULL, 
    nivel_educativo  INTEGER NOT NULL
);

ALTER TABLE persona ADD CONSTRAINT persona_pk PRIMARY KEY ( id_persona );

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
    condicion_excepcional INTEGER NOT NULL,
    estado_id_estado                                INTEGER NOT NULL, 
    situacion_juridica      integer NOT NULL
);


ALTER TABLE registro ADD CONSTRAINT registro_pk PRIMARY KEY ( id_registro );

CREATE TABLE si_no (
    id_si_no  INTEGER NOT NULL,
    codigo varchar(2),
    nombre    VARCHAR(100)
);

ALTER TABLE si_no ADD CONSTRAINT si_no_pk PRIMARY KEY ( id_si_no );

CREATE TABLE situacion_juridica (
    id_situacion_juridica  INTEGER,
    nombre                 VARCHAR(1000)
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

ALTER TABLE registro
    ADD CONSTRAINT registro_condicion_excepcional_fk FOREIGN KEY ( condicion_excepcional )
        REFERENCES condicion_excepcional ( id_condicion_excepcional );

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

ALTER TABLE sociodemografico_registros
    ADD CONSTRAINT sociodemografico_registros_registro_fk FOREIGN KEY ( registro_id_registro )
        REFERENCES registro ( id_registro );

ALTER TABLE sociodemografico_registros
    ADD CONSTRAINT sociodemografico_registros_sociodemograficos_fk FOREIGN KEY ( sociodemograficos )
        REFERENCES sociodemograficos ( id_sociodemografico );