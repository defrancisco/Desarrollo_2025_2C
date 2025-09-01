# Comandos ejecutados desde la shell para mongoDB
mongosh --username rootuser --password rootpassword --authenticationDatabase admin

show dbs
# nombre random ya que tenemos estudiantes, si no existe mongo la crea
use mi_universidad
# declaro la variable del profe:
const estudiantes = [
  {
    "nombre": "Ana",
    "apellido": "López",
    "edad": 22,
    "carrera": "Ingeniería",
    "materias_aprobadas": ["Matemática I", "Física I", "Programación I"]
  },
  {
    "nombre": "Carlos",
    "email": "cmartinez@example.com",
    "edad": 24,
    "situacion_academica": {
      "estado": "regular",
      "promedio": 7.5
    }
  },
  {
    "nombre": "Lucía",
    "apellido": "Gómez",
    "carrera": "Medicina",
    "materias_aprobadas": [],
    "telefono": {
      "tipo": "celular",
      "numero": "+54 9 11 2345-6789"
    }
  },
  {
    "nombre": "Mario",
    "apellido": "Fernández",
    "edad": 20,
    "anio_ingreso": 2022,
    "becado": true
  },
  {
    "nombre": "Isabel",
    "apellido": "Ramírez",
    "edad": 25,
    "carrera": "Psicología",
    "cursos_extracurriculares": [
      { "nombre": "Introducción a la filosofía", "horas": 12 },
      { "nombre": "Lengua de señas", "horas": 20 }
    ]
  },
  {
    "nombre": "Diego",
    "apellido": "Suárez",
    "observaciones": null,
    "edad": "23 años",
    "historial": {
      "cambios_de_carrera": 2,
      "carreras": ["Arquitectura", "Diseño Industrial"]
    }
  },
  {
    "nombre": "Paula",
    "apellido": "Delgado",
    "materias_aprobadas": ["Biología", "Anatomía"],
    "estado": "libre",
    "ultima_conexion": { "$date": "2025-08-01T14:35:00Z" }
  }
];
# me facilita el insert
db.estudiantes.insertMany(estudiantes);
# tuve un output pero lo verifico con:
db.estudiantes.find();
# consultas propuestas:
# 1. 
db.estudiantes.find();
# 2. 
db.estudiantes.find({ carrera: "Medicina" });
# 3. 
db.estudiantes.find({ edad: { $gt: 23 } });
# 4. 
db.estudiantes.find({ email: { $exists: true } });
# 5. 
db.estudiantes.find({ apellido: { $exists: false } });
# 6. 
db.estudiantes.find({ edad: { $type: "string" } });
# 7. 
db.estudiantes.find({ edad: { $type: "int" } });
# 8. 
db.estudiantes.find({ materias_aprobadas: "Biología" });
# 9. 
db.estudiantes.find({ materias_aprobadas: { $exists: true, $ne: [] } });
# 10. 
db.estudiantes.find({ telefono: { $exists: true } });
# 11. 
db.estudiantes.find({ "telefono.tipo": "celular" });
# 12. 
db.estudiantes.find({ "cursos_extracurriculares.horas": { $gt: 15 } });
# 13. 
db.estudiantes.find({ "historial.cambios_de_carrera": { $gt: 1 } });
# 14. 
db.estudiantes.updateOne({ nombre: "Franco" }, { $set: { carrera: "Abogacía" } });
# 15. 
db.estudiantes.updateMany({}, { $set: { activo: true } });
# 16. 
db.estudiantes.updateMany({ "situacion_academica.estado": "regular" },{ $inc: { edad: 1 } });
# 17. 
db.estudiantes.updateMany({ estado: { $exists: true } }, { $unset: { estado: "" } });
# 18. 
db.estudiantes.deleteOne({ nombre: "Franco" });
# 19. 
db.estudiantes.deleteMany({ apellido: { $exists: false } });
# 20. 
db.estudiantes.deleteMany({});
