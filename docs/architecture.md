# Architecture Notes

## Why Staging Exists

Staging is a technical buffer between OLTP and analytical layers.
It helps isolate production transactions from heavy analytical reads and gives a stable landing zone for ETL.

Staging benefits:
- keeps raw copied data close to source format
- allows repeatable backfills and reprocessing
- reduces direct load on OLTP

## Why DWH Exists

A DWH is optimized for analytics and historical reporting, not for transactional writes.
In this project, DWH stores conformed dimensions (`dim_users`, `dim_products`) and measurable events (`fact_sales`).

DWH benefits:
- faster aggregation queries
- easier reporting model (star schema)
- controlled business definitions for KPIs

## OLTP vs DWH

OLTP:
- supports real-time app operations (insert/update/delete)
- normalized schema
- optimized for many small transactions

DWH:
- supports analytics (select, group by, trend analysis)
- denormalized or dimensional schema
- optimized for scan and aggregation workloads

## Data Flow

`OLTP -> Staging -> DWH -> Data Marts`

- OLTP: operational source tables
- Staging: raw copied data for controlled processing
- DWH: dimensional model for analytics
- Marts: business-focused aggregated views
