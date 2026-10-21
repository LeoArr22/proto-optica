import json
from fastapi import FastAPI, Depends, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import engine, get_db, Base, SessionLocal
from models import Cliente, HistorialOptico

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Optica Solo Ojos")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Función para precargar clientes reales de prueba si la base está vacía
def seed_database():
    db = SessionLocal()
    try:
        if db.query(Cliente).count() == 0:
            clientes_prueba = [
                {
                    "nombre": "Carlos Gómez",
                    "dni": "28456789",
                    "telefono": "1145678901",
                    "obs": "Prefiere armazones livianos de titanio. Sensible al sol.",
                    "fichas": [
                        {
                            "tipo": "Armazón y Cristales Nuevos", "medidas": "Sí", "compro": "Sí",
                            "od_esf": "-2.25", "od_cil": "-0.50", "od_eje": "90°", "od_add": "+1.75",
                            "oi_esf": "-2.00", "oi_cil": "-0.75", "oi_eje": "85°", "oi_add": "+1.75",
                            "dip": "63 mm", "cristales": "Multifocales Antirreflejo", "armazon": "Oakley Metálico Gris", "notas": "Seña de 50% abonada. Retira en 5 días."
                        },
                        {
                            "tipo": "Control Visual", "medidas": "No", "compro": "No",
                            "od_esf": "-2.00", "od_cil": "-0.50", "od_eje": "90°", "od_add": "+1.50",
                            "oi_esf": "-1.75", "oi_cil": "-0.50", "oi_eje": "80°", "oi_add": "+1.50",
                            "dip": "63 mm", "cristales": "Stock anterior", "armazon": "Anterior", "notas": "Control de rutina. Visión estable."
                        }
                    ]
                },
                {
                    "nombre": "María Elena Benítez",
                    "dni": "32111222",
                    "telefono": "1167890123",
                    "obs": "Usa lentes exclusivamente para lectura y computadora.",
                    "fichas": [
                        {
                            "tipo": "Recambio de Cristales", "medidas": "Sí", "compro": "Sí",
                            "od_esf": "+1.50", "od_cil": "0.00", "od_eje": "0°", "od_add": "",
                            "oi_esf": "+1.75", "oi_cil": "-0.25", "oi_eje": "110°", "oi_add": "",
                            "dip": "60 mm", "cristales": "Bifocales Orgánicos", "armazon": "Armazón propio", "notas": "Trabajo urgente para entrega en 48hs."
                        }
                    ]
                },
                {
                    "nombre": "Roberto Sánchez",
                    "dni": "20555444",
                    "telefono": "1123456789",
                    "obs": "Cliente histórico del local.",
                    "fichas": [
                        {
                            "tipo": "Control / Examen Visual", "medidas": "Sí", "compro": "Sí",
                            "od_esf": "-4.50", "od_cil": "-1.25", "od_eje": "170°", "od_add": "",
                            "oi_esf": "-4.00", "oi_cil": "-1.00", "oi_eje": "10°", "oi_add": "",
                            "dip": "65 mm", "cristales": "Alto Índice 1.67 Blue Block", "armazon": "Ray-Ban Acetato Negro", "notas": "Cristales especiales de laboratorio."
                        }
                    ]
                },
                {
                    "nombre": "Lucía Fernández",
                    "dni": "38999888",
                    "telefono": "1198765432",
                    "obs": "Primera vez que se atiende en la óptica.",
                    "fichas": [
                        {
                            "tipo": "Control / Examen Visual", "medidas": "Sí", "compro": "No",
                            "od_esf": "0.00", "od_cil": "0.00", "od_eje": "0°", "od_add": "",
                            "oi_esf": "-0.50", "oi_cil": "0.00", "oi_eje": "0°", "oi_add": "",
                            "dip": "59 mm", "cristales": "-", "armazon": "-", "notas": "Se llevó presupuesto impreso para evaluar modelos."
                        }
                    ]
                },
                {
                    "nombre": "Esteban Quito",
                    "dni": "35444333",
                    "telefono": "1133221144",
                    "obs": "Requiere anteojos de sol con graduación.",
                    "fichas": [
                        {
                            "tipo": "Armazón y Cristales Nuevos", "medidas": "Sí", "compro": "Sí",
                            "od_esf": "-1.25", "od_cil": "-0.50", "od_eje": "45°", "od_add": "",
                            "oi_esf": "-1.00", "oi_cil": "0.00", "oi_eje": "0°", "oi_add": "",
                            "dip": "62 mm", "cristales": "Fotocromáticos Gris", "armazon": "Infinit Deportivo", "notas": "Listo para retirar en taller."
                        }
                    ]
                }
            ]

            for c_data in clientes_prueba:
                nuevo_cli = Cliente(
                    nombre_completo=c_data["nombre"],
                    dni=c_data["dni"],
                    telefono=c_data["telefono"],
                    observaciones=c_data["obs"]
                )
                db.add(nuevo_cli)
                db.commit()
                db.refresh(nuevo_cli)

                for idx, f_data in enumerate(c_data["fichas"]):
                    fecha_ficha = datetime.utcnow() - timedelta(days=idx * 120)
                    nueva_f = HistorialOptico(
                        cliente_id=nuevo_cli.id,
                        fecha=fecha_ficha,
                        tipo_atencion=f_data["tipo"],
                        medidas_tomadas=f_data["medidas"],
                        compro=f_data["compro"],
                        od_esfera=f_data["od_esf"],
                        od_cilindro=f_data["od_cil"],
                        od_eje=f_data["od_eje"],
                        od_adicion=f_data["od_add"],
                        oi_esfera=f_data["oi_esf"],
                        oi_cilindro=f_data["oi_cil"],
                        oi_eje=f_data["oi_eje"],
                        oi_adicion=f_data.get("oi_add", ""),
                        distancia_interpupilar=f_data["dip"],
                        cristales=f_data["cristales"],
                        armazon=f_data["armazon"],
                        notas_trabajo=f_data["notas"]
                    )
                    db.add(nueva_f)
                    db.commit()
    finally:
        db.close()

# Ejecutamos la carga inicial de prueba
seed_database()


# Vista principal: Búsqueda y listado de clientes
@app.get("/")
def buscar_clientes(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    query_filter = db.query(Cliente)
    if q:
        query_filter = query_filter.filter(
            (Cliente.nombre_completo.ilike(f"%{q}%")) |
            (Cliente.dni.ilike(f"%{q}%")) |
            (Cliente.telefono.ilike(f"%{q}%"))
        )
    clientes = query_filter.order_by(Cliente.nombre_completo).all()
    return templates.TemplateResponse("buscar.html", {"request": request, "clientes": clientes, "query": q})


# Vista de la Ficha del Cliente
@app.get("/cliente/{cliente_id}")
def ver_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("index.html", {"request": request, "cliente": cliente})


# Formulario Alta Cliente
@app.get("/clientes/nuevo")
def formulario_nuevo_cliente(request: Request):
    return templates.TemplateResponse("nuevo_cliente.html", {"request": request})


@app.post("/clientes/nuevo")
def crear_cliente(
    nombre_completo: str = Form(...),
    dni: str = Form(None),
    telefono: str = Form(None),
    observaciones: str = Form(None),
    db: Session = Depends(get_db)
):
    nuevo = Cliente(
        nombre_completo=nombre_completo,
        dni=dni,
        telefono=telefono,
        observaciones=observaciones
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return RedirectResponse(url=f"/cliente/{nuevo.id}", status_code=303)


# 1. Mostrar formulario de nueva ficha (GET)
@app.get("/ficha/nueva/{cliente_id}")
def formulario_nueva_ficha(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("nueva_ficha.html", {"request": request, "cliente": cliente})


# 2. Guardar la nueva ficha en la base de datos (POST)
@app.post("/ficha/nueva/{cliente_id}")
def crear_ficha(
    cliente_id: int,
    tipo_atencion: str = Form(...),
    medidas_tomadas: str = Form("No"),
    compro: str = Form("No"),
    distancia_interpupilar: str = Form(""),
    od_esfera: str = Form("0.00"),
    od_cilindro: str = Form("0.00"),
    od_eje: str = Form("0°"),
    od_adicion: str = Form(""),
    oi_esfera: str = Form("0.00"),
    oi_cilindro: str = Form("0.00"),
    oi_eje: str = Form("0°"),
    oi_adicion: str = Form(""),
    cristales: str = Form(""),
    armazon: str = Form(""),
    notas_trabajo: str = Form(""),
    db: Session = Depends(get_db)
):
    nueva_ficha = HistorialOptico(
        cliente_id=cliente_id,
        tipo_atencion=tipo_atencion,
        medidas_tomadas=medidas_tomadas,
        compro=compro,
        distancia_interpupilar=distancia_interpupilar,
        od_esfera=od_esfera,
        od_cilindro=od_cilindro,
        od_eje=od_eje,
        od_adicion=od_adicion,
        oi_esfera=oi_esfera,
        oi_cilindro=oi_cilindro,
        oi_eje=oi_eje,
        oi_adicion=oi_adicion,
        cristales=cristales,
        armazon=armazon,
        notas_trabajo=notas_trabajo
    )
    db.add(nueva_ficha)
    db.commit()
    return RedirectResponse(url=f"/cliente/{cliente_id}", status_code=303)


# Backup JSON (Corregido de .recetas a .fichas)
@app.get("/backup/download")
def descargar_backup_db(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    backup_data = []
    for c in clientes:
        backup_data.append({
            "id": c.id,
            "nombre": c.nombre_completo,
            "dni": c.dni,
            "telefono": c.telefono,
            "observaciones": c.observaciones,
            "historial": [
                {
                    "fecha": h.fecha.strftime("%Y-%m-%d %H:%M"),
                    "tipo": h.tipo_atencion,
                    "od": {"esfera": h.od_esfera, "cilindro": h.od_cilindro, "eje": h.od_eje, "add": h.od_adicion},
                    "oi": {"esfera": h.oi_esfera, "cilindro": h.oi_cilindro, "eje": h.oi_eje, "add": h.oi_adicion},
                    "armazon": h.armazon,
                    "cristales": h.cristales,
                    "dip": h.distancia_interpupilar
                } for h in c.fichas  # <-- Corregido aquí de c.recetas a c.fichas
            ]
        })

    content = json.dumps(backup_data, indent=4, ensure_ascii=False)
    headers = {'Content-Disposition': 'attachment; filename="backup_optica_completo.json"'}
    return Response(content=content, media_type="application/json", headers=headers)