-- setup/03_cassandra_init.cql

-- ----------------------------------------------------
-- 1. KEYSPACE CREATION
-- We use SimpleStrategy as it's common for single-datacenter local setups
-- ----------------------------------------------------
CREATE KEYSPACE IF NOT EXISTS starbucks_analytics
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE starbucks_analytics;

-- ----------------------------------------------------
-- 2. TABLE CREATION (HistorialCompra)
-- Partition Key (idCliente) ensures data for one customer is on one node.
-- Clustering Key (fecha) ensures data is ordered chronologically.
-- This design is ideal for fetching "all purchases made by client X".
-- ----------------------------------------------------
CREATE TABLE IF NOT EXISTS HistorialCompra (
    idCliente int,
    fecha timestamp,
    idTicket text, -- Reference to the MongoDB _id
    total decimal,
    productosComprados list<text>, -- List of product names or IDs
    PRIMARY KEY (idCliente, fecha)
) WITH CLUSTERING ORDER BY (fecha DESC);


-- ----------------------------------------------------
-- 3. INITIAL DATA INSERT
-- Example historical record
-- ----------------------------------------------------
INSERT INTO HistorialCompra (idCliente, fecha, idTicket, total, productosComprados)
VALUES (
    1, 
    toTimestamp(now()), 
    '650a310c9d78e348f936b9c7', -- Dummy MongoDB ID
    7.50, 
    ['Latte', 'Muffin']
);