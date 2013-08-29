--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.9
-- Dumped by pg_dump version 9.1.9
-- Started on 2013-07-21 11:16:06 PYT

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 174 (class 1259 OID 25717)
-- Dependencies: 5
-- Name: categoria_tamanho; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE categoria_tamanho (
    id serial NOT NULL,
    descripcion character varying(100),
    tamanho integer
);


ALTER TABLE public.categoria_tamanho OWNER TO postgres;

--
-- TOC entry 175 (class 1259 OID 25720)
-- Dependencies: 174 5
-- Name: categoria_tamanho_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE categoria_tamanho_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categoria_tamanho_id_seq OWNER TO postgres;

--
-- TOC entry 3019 (class 0 OID 0)
-- Dependencies: 175
-- Name: categoria_tamanho_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE categoria_tamanho_id_seq OWNED BY categoria_tamanho.id;


--
-- TOC entry 178 (class 1259 OID 25733)
-- Dependencies: 2987 5
-- Name: muestras; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE muestras (
    id serial NOT NULL,
    id_tipo_dispositivo integer,
    codigo integer,
    descripcion character varying(100),
    fecha timestamp without time zone DEFAULT '2013-03-17 22:09:44.64067'::timestamp without time zone NOT NULL
);


ALTER TABLE public.muestras OWNER TO postgres;

--
-- TOC entry 179 (class 1259 OID 25737)
-- Dependencies: 178 5
-- Name: muestras_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE muestras_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.muestras_id_seq OWNER TO postgres;

--
-- TOC entry 3021 (class 0 OID 0)
-- Dependencies: 179
-- Name: muestras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE muestras_id_seq OWNED BY muestras.id;


--
-- TOC entry 180 (class 1259 OID 25739)
-- Dependencies: 5 1418
-- Name: patios_baldios; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE patios_baldios (
    id serial NOT NULL,
    codigo character varying(15),
    id_categoria integer,
    descripcion character varying(100),
    fecha_inicio timestamp without time zone,
    fecha_fin timestamp without time zone,
    the_geom geometry(Point, 4326)
);


ALTER TABLE public.patios_baldios OWNER TO postgres;

--
-- TOC entry 181 (class 1259 OID 25745)
-- Dependencies: 5 180
-- Name: patios_baldios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE patios_baldios_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.patios_baldios_id_seq OWNER TO postgres;

--
-- TOC entry 3022 (class 0 OID 0)
-- Dependencies: 181
-- Name: patios_baldios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE patios_baldios_id_seq OWNED BY patios_baldios.id;


--
-- TOC entry 182 (class 1259 OID 25747)
-- Dependencies: 1418 5
-- Name: puntos_control; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE puntos_control (
    id serial NOT NULL,
    id_muestras integer,
    descripcion character varying(100),
    codigo character varying(20),
    cantidad integer,
    the_geom geometry(Point, 4326),
    fecha_recoleccion date,
    fecha_instalacion date
);


ALTER TABLE public.puntos_control OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 25753)
-- Dependencies: 182 5
-- Name: puntos_control_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE puntos_control_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.puntos_control_id_seq OWNER TO postgres;

--
-- TOC entry 3023 (class 0 OID 0)
-- Dependencies: 183
-- Name: puntos_control_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE puntos_control_id_seq OWNED BY puntos_control.id;


--
-- TOC entry 184 (class 1259 OID 25755)
-- Dependencies: 5 1418
-- Name: puntos_riesgo; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE puntos_riesgo (
    id serial NOT NULL,
    codigo character varying(15),
    id_tipo integer,
    descripcion character varying(100),
    fecha_inicio timestamp without time zone,
    fecha_fin timestamp without time zone,
    the_geom geometry(Point, 4326)
);


ALTER TABLE public.puntos_riesgo OWNER TO postgres;

--
-- TOC entry 185 (class 1259 OID 25761)
-- Dependencies: 5 184
-- Name: puntos_riesgo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE puntos_riesgo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.puntos_riesgo_id_seq OWNER TO postgres;

--
-- TOC entry 3024 (class 0 OID 0)
-- Dependencies: 185
-- Name: puntos_riesgo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE puntos_riesgo_id_seq OWNED BY puntos_riesgo.id;


--
-- TOC entry 186 (class 1259 OID 25763)
-- Dependencies: 5
-- Name: tipo_dispositivos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tipo_dispositivos (
    id serial NOT NULL,
    descripcion character varying(100),
    image bytea
);


ALTER TABLE public.tipo_dispositivos OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 25769)
-- Dependencies: 5 186
-- Name: tipo_dispositivos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tipo_dispositivos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tipo_dispositivos_id_seq OWNER TO postgres;

--
-- TOC entry 3025 (class 0 OID 0)
-- Dependencies: 187
-- Name: tipo_dispositivos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tipo_dispositivos_id_seq OWNED BY tipo_dispositivos.id;


--
-- TOC entry 188 (class 1259 OID 25771)
-- Dependencies: 5
-- Name: tipo_riesgo; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tipo_riesgo (
    id serial NOT NULL,
    descripcion character varying(100),
    riesgo integer
);


ALTER TABLE public.tipo_riesgo OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 25774)
-- Dependencies: 5 188
-- Name: tipo_riesgo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tipo_riesgo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tipo_riesgo_id_seq OWNER TO postgres;

--
-- TOC entry 3026 (class 0 OID 0)
-- Dependencies: 189
-- Name: tipo_riesgo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tipo_riesgo_id_seq OWNED BY tipo_riesgo.id;


--
-- TOC entry 2984 (class 2604 OID 25776)
-- Dependencies: 175 174
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY categoria_tamanho ALTER COLUMN id SET DEFAULT nextval('categoria_tamanho_id_seq'::regclass);


--
-- TOC entry 2986 (class 2604 OID 25778)
-- Dependencies: 177 176
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY interpolacion ALTER COLUMN id SET DEFAULT nextval('interpolacion_id_seq'::regclass);


--
-- TOC entry 2988 (class 2604 OID 25779)
-- Dependencies: 179 178
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY muestras ALTER COLUMN id SET DEFAULT nextval('muestras_id_seq'::regclass);


--
-- TOC entry 2989 (class 2604 OID 25780)
-- Dependencies: 181 180
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY patios_baldios ALTER COLUMN id SET DEFAULT nextval('patios_baldios_id_seq'::regclass);


--
-- TOC entry 2990 (class 2604 OID 25781)
-- Dependencies: 183 182
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY puntos_control ALTER COLUMN id SET DEFAULT nextval('puntos_control_id_seq'::regclass);


--
-- TOC entry 2991 (class 2604 OID 25782)
-- Dependencies: 185 184
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY puntos_riesgo ALTER COLUMN id SET DEFAULT nextval('puntos_riesgo_id_seq'::regclass);


--
-- TOC entry 2992 (class 2604 OID 25783)
-- Dependencies: 187 186
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tipo_dispositivos ALTER COLUMN id SET DEFAULT nextval('tipo_dispositivos_id_seq'::regclass);


--
-- TOC entry 2993 (class 2604 OID 25784)
-- Dependencies: 189 188
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tipo_riesgo ALTER COLUMN id SET DEFAULT nextval('tipo_riesgo_id_seq'::regclass);


--
-- TOC entry 2995 (class 2606 OID 25786)
-- Dependencies: 174 174 3016
-- Name: categoria_tamanho_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY categoria_tamanho
    ADD CONSTRAINT categoria_tamanho_pkey PRIMARY KEY (id);


--
-- TOC entry 2997 (class 2606 OID 25790)
-- Dependencies: 176 176 3016
-- Name: interpolacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY interpolacion
    ADD CONSTRAINT interpolacion_pkey PRIMARY KEY (id);


--
-- TOC entry 2999 (class 2606 OID 25792)
-- Dependencies: 178 178 3016
-- Name: muestras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY muestras
    ADD CONSTRAINT muestras_pkey PRIMARY KEY (id);


--
-- TOC entry 3001 (class 2606 OID 25794)
-- Dependencies: 180 180 3016
-- Name: patios_baldios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY patios_baldios
    ADD CONSTRAINT patios_baldios_pkey PRIMARY KEY (id);


--
-- TOC entry 3003 (class 2606 OID 25796)
-- Dependencies: 182 182 3016
-- Name: puntos_control_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY puntos_control
    ADD CONSTRAINT puntos_control_pkey PRIMARY KEY (id);


--
-- TOC entry 3005 (class 2606 OID 25798)
-- Dependencies: 184 184 3016
-- Name: puntos_riesgo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY puntos_riesgo
    ADD CONSTRAINT puntos_riesgo_pkey PRIMARY KEY (id);


--
-- TOC entry 3007 (class 2606 OID 25800)
-- Dependencies: 186 186 3016
-- Name: tipo_dispositivos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY tipo_dispositivos
    ADD CONSTRAINT tipo_dispositivos_pkey PRIMARY KEY (id);


--
-- TOC entry 3009 (class 2606 OID 25802)
-- Dependencies: 188 188 3016
-- Name: tipo_riesgo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY tipo_riesgo
    ADD CONSTRAINT tipo_riesgo_pkey PRIMARY KEY (id);


--
-- TOC entry 3010 (class 2606 OID 25803)
-- Dependencies: 2998 176 178 3016
-- Name: interpolacion_id_muestra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY interpolacion
    ADD CONSTRAINT interpolacion_id_muestra_fkey FOREIGN KEY (id_muestra) REFERENCES muestras(id);


--
-- TOC entry 3011 (class 2606 OID 25808)
-- Dependencies: 186 178 3006 3016
-- Name: muestras_id_tipo_dispositivo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY muestras
    ADD CONSTRAINT muestras_id_tipo_dispositivo_fkey FOREIGN KEY (id_tipo_dispositivo) REFERENCES tipo_dispositivos(id);


--
-- TOC entry 3012 (class 2606 OID 25813)
-- Dependencies: 2994 180 174 3016
-- Name: patios_baldios_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY patios_baldios
    ADD CONSTRAINT patios_baldios_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES categoria_tamanho(id);


--
-- TOC entry 3013 (class 2606 OID 25818)
-- Dependencies: 178 2998 182 3016
-- Name: puntos_control_id_muestras_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY puntos_control
    ADD CONSTRAINT puntos_control_id_muestras_fkey FOREIGN KEY (id_muestras) REFERENCES muestras(id);


--
-- TOC entry 3014 (class 2606 OID 25823)
-- Dependencies: 3008 188 184 3016
-- Name: puntos_riesgo_id_tipo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY puntos_riesgo
    ADD CONSTRAINT puntos_riesgo_id_tipo_fkey FOREIGN KEY (id_tipo) REFERENCES tipo_riesgo(id);


-- Completed on 2013-07-21 11:16:06 PYT

--
-- PostgreSQL database dump complete
--

