-- =============================================================================
-- External Hive Metastore (Regional HA Cloud SQL PostgreSQL 15)
-- Cross-Cloud Storage URI Rewrite (`abfss://` -> `gs://`)
-- =============================================================================
-- Executed after migrating legacy Hive 2.3.9 pg_dump into Cloud SQL PostgreSQL
-- to repoint all database & partition storage descriptors to the GCS HNS bucket.
-- =============================================================================

BEGIN;

-- 1. Rewrite Database Root Locations (`DBS.DB_LOCATION_URI`)
UPDATE "DBS"
SET "DB_LOCATION_URI" = REGEXP_REPLACE(
    "DB_LOCATION_URI",
    '^abfss://[^@]+@[^.]+\.dfs\.core\.windows\.net/',
    'gs://gke-demos-363017-rd-lakehouse-hns/'
)
WHERE "DB_LOCATION_URI" LIKE 'abfss://%';

-- 2. Rewrite Table & Partition Storage Descriptors (`SDS.LOCATION`)
UPDATE "SDS"
SET "LOCATION" = REGEXP_REPLACE(
    "LOCATION",
    '^abfss://[^@]+@[^.]+\.dfs\.core\.windows\.net/',
    'gs://gke-demos-363017-rd-lakehouse-hns/'
)
WHERE "LOCATION" LIKE 'abfss://%';

-- 3. Verify Zero Residual `abfss://` or `wasbs://` URIs Remain
SELECT
    (SELECT COUNT(*) FROM "DBS" WHERE "DB_LOCATION_URI" ~ '^(abfss|wasbs)://') AS residual_db_uris,
    (SELECT COUNT(*) FROM "SDS" WHERE "LOCATION" ~ '^(abfss|wasbs)://')        AS residual_sds_uris;

COMMIT;
