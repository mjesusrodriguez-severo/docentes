from datetime import timedelta, date
from flask import render_template
from app.models import Usuario, ReservaSala

ESPACIOS_NOMBRES = {
    "sala-reuniones": "Sala de Reuniones",
    "aula-taller": "Aula Taller",
    "departamento-taquillas": "Departamento Taquillas",
    "aula-laboratorio": "Aula Laboratorio",
    "aula-digital": "Aula Digital",
    "biblioteca": "Biblioteca"
}

FRANJAS_HORARIAS = [
    "08:30-09:25",
    "09:25-10:25",
    "10:25-11:15",
    "11:45-12:40",
    "12:40-13:35",
    "13:35-14:30"
]

def render_calendario_espacio(nombre_espacio, plantilla, nombre_visible):
    hoy = date.today()
    lunes_actual = hoy - timedelta(days=hoy.weekday())
    lunes_siguiente = lunes_actual + timedelta(days=7)

    def dias_lectivos_semana(lunes):
        return [lunes + timedelta(days=i) for i in range(5)]

    dias_semana_actual = dias_lectivos_semana(lunes_actual)
    dias_semana_siguiente = dias_lectivos_semana(lunes_siguiente)

    reservas = ReservaSala.query.filter(
        ReservaSala.fecha.in_(dias_semana_actual + dias_semana_siguiente),
        ReservaSala.espacio == nombre_espacio
    ).all()

    reservas_dict = {(res.fecha, res.franja_horaria): res for res in reservas}

    dias_es = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
    }

    usuario_ids = [res.usuario_id for res in reservas]
    usuarios = Usuario.query.filter(Usuario.id.in_(usuario_ids)).all()
    usuarios_dict = {u.id: u.nombre for u in usuarios}

    return render_template(
        plantilla,
        dias_semana_actual=dias_semana_actual,
        dias_semana_siguiente=dias_semana_siguiente,
        franjas_horarias=FRANJAS_HORARIAS,
        reservas=reservas_dict,
        dias_es=dias_es,
        usuarios=usuarios_dict,
        nombre_visible=nombre_visible
    )