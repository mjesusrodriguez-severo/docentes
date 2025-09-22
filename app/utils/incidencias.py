from flask import current_app
from flask_mail import Message
from app import mail


def enviar_correo_incidencia(incidencia, usuario):
    try:
        equipo_nombre = incidencia.equipo.nombre if incidencia.equipo else "No especificado"
        ubicacion = incidencia.ubicacion or "No especificada"
        estado = incidencia.estado or "Activa"
        prioridad = incidencia.prioridad or "Normal"

        # Puedes poner los correos reales aquí o sacarlos de la base de datos si prefieres
        destinatarios = ["mjesusrodriguez@severoochoa.es"]

        msg = Message(
            subject="🛠️ Nueva incidencia registrada",
            sender=("Panel de Docentes", current_app.config["MAIL_USERNAME"]),
            recipients=destinatarios,
            html=f"""
                <h2 style="color:#c0392b;">Nueva incidencia registrada</h2>
                <p><strong>📍 Ubicación:</strong> {ubicacion}</p>
                <p><strong>💻 Equipo:</strong> {equipo_nombre}</p>
                <p><strong>⚠️ Estado:</strong> {estado}</p>
                <p><strong>🔥 Prioridad:</strong> {prioridad}</p>
                <p><strong>📝 Descripción:</strong> {incidencia.descripcion}</p>
                <p><strong>👩‍🏫 Profesor/a:</strong> {usuario.nombre}</p>
                <p><strong>📅 Fecha:</strong> {incidencia.fecha_hora.strftime('%d/%m/%Y %H:%M')}</p>
                <hr>
                <p style="font-size:0.9em; color:#888;">Este mensaje ha sido generado automáticamente por el sistema de incidencias del centro.</p>
            """
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error al enviar correo de incidencia: {e}")

def enviar_correo_comentario_incidencia(comentario, incidencia, autor, destinatario):
    try:
        msg = Message(
            subject=f"💬 Nuevo comentario en tu incidencia",
            sender=("Panel de Docentes", current_app.config["MAIL_USERNAME"]),
            recipients=[destinatario.email],  # Email del docente que creó la incidencia
            html=f"""
                <h2 style="color:#2c3e50;">Nuevo comentario en tu incidencia</h2>
                <p><strong>🆔 Código de incidencia:</strong> INC-{{ incidencia.id }}</p>
                <p><strong>📍 Ubicación:</strong> {incidencia.ubicacion}</p>
                <p><strong>💻 Equipo:</strong> {incidencia.equipo.nombre if incidencia.equipo else 'Sin equipo asignado'}</p>
                <p><strong>📝 Comentario:</strong></p>
                <blockquote style="background-color:#f8f9fa;padding:10px;border-left:4px solid #007bff;">
                    {comentario.contenido}
                </blockquote>
                <p><strong>👨‍💻 Comentado por:</strong> {autor.nombre}</p>
                <hr>
                <p style="font-size:0.9em; color:#888;">Este mensaje ha sido generado automáticamente por el sistema de incidencias del centro.</p>
            """
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error al enviar correo de comentario en incidencia: {e}")