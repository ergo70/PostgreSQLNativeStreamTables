-- public.stream definition

-- Drop table

-- DROP TABLE public.stream;

CREATE UNLOGGED TABLE public.stream (
	ts timestamptz NOT NULL DEFAULT clock_timestamp(),
	payload jsonb NOT NULL
) WITH (autovacuum_vacuum_threshold = 25, autovacuum_vacuum_scale_factor = 0.1,autovacuum_analyze_threshold = 10, autovacuum_analyze_scale_factor = 0.05, autovacuum_vacuum_cost_delay = 10, autovacuum_vacuum_cost_limit = 1000);

CREATE INDEX idx_stream ON public.stream USING brin (ts) WITH (pages_per_range='64');
