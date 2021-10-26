-- RESULTS TABLE
-- Table: public.results

-- DROP TABLE public.results;

CREATE TABLE IF NOT EXISTS public.results
(
    student character varying COLLATE pg_catalog."default" NOT NULL,
    test_id character varying COLLATE pg_catalog."default" NOT NULL,
    available integer,
    obtained integer,
    CONSTRAINT results_pkey PRIMARY KEY (student, test_id),
    CONSTRAINT results_student_fkey FOREIGN KEY (student)
        REFERENCES public.students (student_number) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.results
    OWNER to postgres;
-- Index: ix_results_student

-- DROP INDEX public.ix_results_student;

CREATE INDEX ix_results_student
    ON public.results USING btree
    (student COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_results_test_id

-- DROP INDEX public.ix_results_test_id;

CREATE INDEX ix_results_test_id
    ON public.results USING btree
    (test_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

-- STUDENTS TABLE
-- Table: public.students

-- DROP TABLE public.students;

CREATE TABLE IF NOT EXISTS public.students
(
    student_number character varying COLLATE pg_catalog."default" NOT NULL,
    first_name character varying COLLATE pg_catalog."default",
    last_name character varying COLLATE pg_catalog."default",
    CONSTRAINT students_pkey PRIMARY KEY (student_number)
)

TABLESPACE pg_default;

ALTER TABLE public.students
    OWNER to postgres;
-- Index: ix_students_student_number

-- DROP INDEX public.ix_students_student_number;

CREATE INDEX ix_students_student_number
    ON public.students USING btree
    (student_number COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;