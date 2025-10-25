// setup/04_neo4j_init.cypher
// Comando para asegurar la idempotencia (limpiar si hay datos anteriores)
MATCH (n) DETACH DELETE n;
/*
-- 1. CONSTRAINT AND INDEX CREATION
-- Ensure uniqueness and fast lookup for main nodes
*/
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Cliente) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (r:RedSocial) REQUIRE r.id IS UNIQUE;


/* ----------------------------------------------------
-- 2. NODE CREATION (Customers and Social Groups)
-- The 'mysqlId' property links the graph node to the relational data.
-- ----------------------------------------------------*/

// Customers (linked to MySQL)
MERGE (c1:Cliente {id: 1, name: 'Alice Johnson', mysqlId: 1});
MERGE (c2:Cliente {id: 2, name: 'Bob Smith', mysqlId: 2});
MERGE (c3:Cliente {id: 3, name: 'Charlie Brown', mysqlId: 3});

// Social/Interest Groups
MERGE (g1:RedSocial {id: 101, name: 'Coffee Lovers'});
MERGE (g2:RedSocial {id: 102, name: 'Muffin Fanatics'});


/*----------------------------------------------------
-- 3. RELATIONSHIP CREATION
-- Modeling the "SIGUE" relationship (N:N)
-- ----------------------------------------------------*/

// Alice follows Coffee Lovers and Muffin Fanatics
MATCH (a:Cliente {id: 1}), (g1:RedSocial {id: 101}), (g2:RedSocial {id: 102})
MERGE (a)-[:SIGUE]->(g1)
MERGE (a)-[:SIGUE]->(g2);

// Bob only follows Coffee Lovers
MATCH (b:Cliente {id: 2}), (g1:RedSocial {id: 101})
MERGE (b)-[:SIGUE]->(g1);

// Modeling complex relationships (e.g., A referred B)
MATCH (c1:Cliente {id: 1}), (c2:Cliente {id: 2})
MERGE (c1)-[:REFERRED {date: date()}]->(c2);