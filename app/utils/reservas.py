from datetime import timedelta, date
from flask import render_template
from app.models import Usuario, ReservaSala
from flask_mail import Message
from flask import current_app
from app import mail  # Asegúrate de importar tu instancia de mail

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

def render_calendario_espacio(nombre_espacio, plantilla, nombre_visible, franjas_bloqueadas=None):
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
        franjas_bloqueadas=franjas_bloqueadas or {},
        dias_semana_actual=dias_semana_actual,
        dias_semana_siguiente=dias_semana_siguiente,
        franjas_horarias=FRANJAS_HORARIAS,
        reservas=reservas_dict,
        dias_es=dias_es,
        usuarios=usuarios_dict,
        nombre_visible=nombre_visible
    )

def enviar_correo_reserva_espacio(reserva, espacio, usuario):
    try:
        espacio_visible = espacio.replace('_', ' ').title()
        msg = Message(
            subject="📌 Nueva reserva de espacio",
            sender=("Panel de Docentes", current_app.config["MAIL_USERNAME"]),
            recipients=["concertada.mariapaz.catarecha@educeuta.es"],
            html=f"""
                <h2 style="color:#2c3e50;">Nueva reserva de espacios comunes</h2>
                <p><strong>📌 Espacio:</strong> {espacio_visible}</p>
                <p><strong>📅 Fecha:</strong> {reserva.fecha}</p>
                <p><strong>🕒 Franja horaria:</strong> {reserva.franja_horaria}</p>
                <p><strong>👩‍🏫 Profesor/a:</strong> {usuario.nombre}</p>
                <hr>
                <p style="font-size:0.9em; color:#888;">Este mensaje ha sido generado automáticamente por el sistema de reservas del centro.</p>
            """
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error al enviar correo de reserva: {e}")