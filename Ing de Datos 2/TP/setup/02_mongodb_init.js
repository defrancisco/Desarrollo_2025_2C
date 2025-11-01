// setup/02_mongodb_init.js
// Script de inicialización para MongoDB (Base de datos: starbucks_transactions)

// -----------------------------------------------------------
// 1. ELIMINAR COLECCIONES PREVIAS (Idempotencia)
// -----------------------------------------------------------
print("Limpiando colecciones existentes...");
db.ticket.drop();
db.stores.drop();
db.products.drop();

// -----------------------------------------------------------
// 2. Crear las colecciones (si no existen)
// -----------------------------------------------------------
db.createCollection("ticket");
db.createCollection("stores");
db.createCollection("products");

// print("Colecciones 'transactions', 'stores', y 'products' creadas (o verificadas).");

// -----------------------------------------------------------
// 3. Insertar datos de ejemplo
// -----------------------------------------------------------

// Colección 'transactions'
db.ticket.insertMany([
    {
        ticket_id: 1,
        sucursal_id: 1,
        cliente_id:1,
        fecha: new Date("2024-09-01T08:30:00Z"),
        total: 6,
        metodo_pago: 'Efectivo',
        promocion_id: 1,
        detalles: [
            { producto_id: 1, cantidad: 2, precio: 3 }
        ]
    },
    {
        ticket_id: 2,
        sucursal_id: 2,
        cliente_id: 2,
        fecha: new Date("2025-09-01T08:30:00Z"),
        total: 7,
        metodo_pago: 'Tarjeta',
        promocion_id: 2,
        detalles: [
            { producto_id: 2, cantidad: 1, precio: 7 }
        ]
    },
    {
        ticket_id: 3,
        sucursal_id: 2,
        cliente_id:1,
        fecha: new Date("2025-09-01T08:30:00Z"),
        total: 32,
        metodo_pago: 'Efectivo',
        promocion_id: 1,
        detalles: [
            { producto_id: 1, cantidad: 2, precio: 16 }
        ]
    },
        {
        ticket_id: 3,
        sucursal_id: 3,
        cliente_id:2,
        fecha: new Date("2025-09-01T08:30:00Z"),
        total: 32,
        metodo_pago: 'Efectivo',
        promocion_id: 1,
        detalles: [
            { producto_id: 3, cantidad: 2, precio: 16 }
        ]
    },
]);

// Colección 'stores'
db.stores.insertMany([
    {
        store_id: 101,
        location: "Centro",
        manager: "Ana Lopez",
        opening_date: new Date("2020-01-15T00:00:00Z")
    },
    {
        store_id: 102,
        location: "Periferia",
        manager: "Carlos Ruiz",
        opening_date: new Date("2018-05-20T00:00:00Z")
    }
]);

// Colección 'products'
db.products.insertMany([
    {
        product_id: 501,
        name: "Latte Grande",
        category: "Bebidas",
        price: 5.25
    },
    {
        product_id: 502,
        name: "Muffin de Arándanos",
        category: "Comida",
        price: 3.50
    },
    {
        product_id: 503,
        name: "Capuccino Chico",
        category: "Bebidas",
        price: 5.00
    }
]);

// print("Datos de prueba insertados exitosamente en las colecciones.");

// -----------------------------------------------------------
// 4. Crear índices (opcional pero recomendado)
// -----------------------------------------------------------
db.transactions.createIndex({ transaction_id: 1 }, { unique: true });
db.stores.createIndex({ store_id: 1 }, { unique: true });
db.products.createIndex({ product_id: 1 }, { unique: true });

// print("Índices creados.");