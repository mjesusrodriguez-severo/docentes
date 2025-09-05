from flask import send_file

from . import db
from flask_login import UserMixin
from datetime import datetime

profesor_grupo = db.Table('profesor_grupo',
    db.Column('profesor_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('grupo_id', db.Integer, db.ForeignKey('grupos.id'), primary_key=True)
)

class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    periodo = db.Column(db.String(20), nullable=False)
    orden = db.Column(db.Integer, nullable=False)
    alumnos = db.relationship('Alumno', backref='grupo', lazy=True)

    profesores = db.relationship(
        "Usuario",
        secondary=profesor_grupo,
        back_populates="grupos"
    )

    tutor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    tutor = db.relationship("Usuario", backref=db.backref("grupo_asignado", uselist=False))
    informes = db.relationship("InformeFaltas", back_populates="grupo", lazy=True)

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    identificacion = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(100))
    observaciones = db.Column(db.Text)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))

    informes = db.relationship("InformeAlumno", back_populates="alumno")
    responsables = db.relationship(
        "Responsable",
        secondary="alumno_responsable",
        back_populates="alumnos",
        overlaps="alumno_responsable_asociaciones"
    )

class Responsable(db.Model):
    __tablename__ = 'responsables'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(30))
    email = db.Column(db.String(100))

    alumnos = db.relationship(
        "Alumno",
        secondary="alumno_responsable",
        back_populates="responsables",
        overlaps="alumno_responsable_asociaciones"
    )


class AlumnoResponsable(db.Model):
    __tablename__ = 'alumno_responsable'
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), primary_key=True)
    responsable_id = db.Column(db.Integer, db.ForeignKey('responsables.id'), primary_key=True)
    tipo = db.Column(db.Enum('madre', 'padre', 'tutor legal', 'otro'), default='tutor legal')
    principal = db.Column(db.Boolean, default=False)

    alumno = db.relationship(
        "Alumno",
        backref=db.backref("alumno_responsable_asociaciones", cascade="all, delete-orphan"),
        overlaps="responsables,alumnos"
    )

    responsable = db.relationship(
        "Responsable",
        backref=db.backref("alumno_responsable_asociaciones", cascade="all, delete-orphan"),
        overlaps="responsables,alumnos"
    )

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    rol = db.Column(db.Enum('profesor', 'tutor', 'jefatura', 'tic'), nullable=False)
    telefono = db.Column(db.String(20))
    archivado = db.Column(db.Boolean, default=False)

    @property
    def es_jefatura(self):
        return self.rol == 'jefatura'

    @property
    def es_tutor(self):
        return self.rol == 'tutor'

    @property
    def es_profesor(self):
        return self.rol == 'profesor'

    # Relaciones inversas (opcional)
    grupo_tutorizado = db.relationship("Grupo", back_populates="tutor", uselist=False)
    # Relación con grupos a los que imparte clase
    grupos = db.relationship(
        "Grupo",
        secondary=profesor_grupo,
        back_populates="profesores"
    )

class Sustitucion(db.Model):
    __tablename__ = 'sustituciones'

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria real
    sustituido_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    sustituto_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha = db.Column(db.Date)
    hora_inicio = db.Column(db.String(10), nullable=False)
    hora_fin = db.Column(db.String(10), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))
    observaciones = db.Column(db.Text)
    enlace_drive = db.Column(db.String(300))

    confirmado = db.Column(db.Boolean, default=False)

    sustituido = db.relationship("Usuario", foreign_keys=[sustituido_id])
    sustituto = db.relationship("Usuario", foreign_keys=[sustituto_id])
    grupo = db.relationship("Grupo", backref="sustituciones")

dispositivos_reservados = db.Table(
    'dispositivos_reservados',
    db.Column('reserva_id', db.Integer, db.ForeignKey('reservas_informatica.id', ondelete="CASCADE"), primary_key=True),
    db.Column('dispositivo_id', db.Integer, db.ForeignKey('dispositivos.id', ondelete="CASCADE"), primary_key=True)
)


class Ubicacion(db.Model):
    __tablename__ = "ubicaciones"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    numero_puerta = db.Column(db.String(50), nullable=True)
    planta = db.Column(db.Integer, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Ubicacion {self.nombre} ({self.tipo})>"

class Dispositivo(db.Model):
    __tablename__ = 'dispositivos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    etiqueta = db.Column(db.String(100))
    tipo = db.Column(db.Enum('portatil', 'allinone', 'sobremesa', 'pizarra', 'tablet', 'monitor', 'impresora', 'otro'), nullable=False)
    marca = db.Column(db.String(100), nullable=True)
    modelo = db.Column(db.String(100), nullable=True)
    numero_serie = db.Column(db.String(50), unique=True)  # CAMPO NUEVO
    estado = db.Column(db.Enum('activo', 'incidencia', 'baja'), default='activo')
    observaciones = db.Column(db.Text)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'), nullable=True)
    ubicacion = db.relationship('Ubicacion', backref='dispositivos')

class ReservaInformatica(db.Model):
    __tablename__ = 'reservas_informatica'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    franja_horaria = db.Column(db.String(50), nullable=False)
    tipo_equipo = db.Column(db.String(20), nullable=False, default='portátil')
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    estado = db.Column(db.String(20), nullable=False, default='PENDIENTE')
    observaciones = db.Column(db.Text, nullable=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True)
    hoja_firmada_nombre = db.Column(db.String(255), nullable=True)  # nombre o ruta del archivo subido
    hoja_firmada_id = db.Column(db.String(255))  # ID en Google Drive

    # Relaciones
    grupo = db.relationship('Grupo', backref='reservas_informatica')
    usuario = db.relationship('Usuario', backref='reservas_informatica')

    # Relación con Dispositivos (muchos a muchos)
    dispositivos = db.relationship('Dispositivo', secondary='dispositivos_reservados', backref='reservas')

class Amonestacion(db.Model):
    __tablename__ = "amonestaciones"

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='pendiente')

    alumno = db.relationship("Alumno", backref="amonestaciones")
    profesor = db.relationship("Usuario", backref="amonestaciones_hechas")

class ReservaSala(db.Model):
    __tablename__ = "reservas_sala"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    franja_horaria = db.Column(db.String(50), nullable=False)
    motivo = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    # Campo nuevo: tipo de espacio reservado
    espacio = db.Column(db.Enum(
        'sala_reuniones',
        'aula_taller',
        'departamento_taquillas',
        'aula_laboratorio',
        'aula_digital',
        'biblioteca'
    ), nullable=False)

    usuario = db.relationship("Usuario", backref="reservas_sala")


class Incidencia(db.Model):
    __tablename__ = 'incidencias'

    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(100), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('dispositivos.id'), nullable=True)
    equipo = db.relationship('Dispositivo', backref='incidencias')
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(20), default='Normal')
    estado = db.Column(db.String(20), default='Activa')
    fecha_hora = db.Column(db.DateTime, default=db.func.current_timestamp())

    docente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    docente = db.relationship('Usuario', backref='incidencias')

class IncidenciaMantenimiento(db.Model):
    __tablename__ = 'incidencias_mantenimiento'

    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='Activa')    # Activa, Resuelta, Cancelada
    prioridad = db.Column(db.String(20), default='Normal') # Alta, Normal, Baja
    fecha_hora = db.Column(db.DateTime, default=db.func.current_timestamp())
    fecha_resolucion = db.Column(db.DateTime)

    docente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    docente = db.relationship('Usuario', backref='mantenimiento')

class InformeFaltas(db.Model):
    __tablename__ = "informe_faltas"

    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey("grupos.id"), nullable=False)
    mes = db.Column(db.String(20), nullable=False)  # ejemplo: "junio"
    anio = db.Column(db.Integer, nullable=False)    # ejemplo: 2025
    fecha_subida = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    archivo_csv = db.Column(db.String(255), nullable=True)  # ruta al archivo en disco o Drive

    grupo = db.relationship("Grupo", back_populates="informes")
    alumnos = db.relationship("InformeAlumno", backref="informe", cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("grupo_id", "mes", "anio", name="uq_grupo_mes_anio"),
    )


class InformeAlumno(db.Model):
    __tablename__ = "informe_alumno"

    id = db.Column(db.Integer, primary_key=True)
    informe_id = db.Column(db.Integer, db.ForeignKey('informe_faltas.id'), nullable=False)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)

    faltas_justificadas = db.Column(db.Integer, nullable=False)
    faltas_injustificadas = db.Column(db.Integer, nullable=False)
    porcentaje_injustificadas = db.Column(db.Float, nullable=False)
    absentista = db.Column(db.Boolean, default=False)

    alumno = db.relationship("Alumno", back_populates="informes")

    __table_args__ = (
        db.UniqueConstraint("informe_id", "alumno_id", name="uq_informe_alumno"),
    )


