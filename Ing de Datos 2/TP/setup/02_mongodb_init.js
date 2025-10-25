// setup/02_mongodb_init.js
// Script de inicialización para MongoDB (Base de datos: starbucks_transactions)

// -----------------------------------------------------------
// 1. ELIMINAR COLECCIONES PREVIAS (Idempotencia)
// -----------------------------------------------------------
print("Limpiando colecciones existentes...");
db.transactions.drop();
db.stores.drop();
db.products.drop();

// -----------------------------------------------------------
// 2. Crear las colecciones (si no existen)
// -----------------------------------------------------------
db.createCollection("transactions");
db.createCollection("stores");
db.createCollection("products");

// print("Colecciones 'transactions', 'stores', y 'products' creadas (o verificadas).");

// -----------------------------------------------------------
// 3. Insertar datos de ejemplo
// -----------------------------------------------------------

// Colección 'transactions'
db.transactions.insertMany([
    {
        transaction_id: 1,
        store_id: 101,
        date: new Date("2024-09-01T08:30:00Z"),
        total_amount: 5.25,
        items: [
            { product_id: 501, quantity: 1, price: 5.25 }
        ]
    },
    {
        transaction_id: 2,
        store_id: 102,
        date: new Date("2024-09-01T10:15:00Z"),
        total_amount: 8.50,
        items: [
            { product_id: 502, quantity: 1, price: 3.50 },
            { product_id: 503, quantity: 1, price: 5.00 }
        ]
    }
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