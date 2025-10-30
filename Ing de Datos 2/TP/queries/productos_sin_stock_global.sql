SELECT
    p.nombre,
    s.idSucursal
FROM
    Producto p
LEFT JOIN
    Stock s ON p.id = s.idProducto
GROUP BY
    p.nombre,idSucursal
HAVING
    SUM(s.cantidad) IS NULL OR SUM(s.cantidad) = 0
ORDER BY
    p.nombre;