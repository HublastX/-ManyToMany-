import uuid
from datetime import datetime
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class RoleEnum(Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    RECEPTIONIST = "receptionist"
    PATIENT = "patient"


class Clinic(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", backref="clinic", lazy=True)
    patients = db.relationship("Patient", backref="clinic", lazy=True)
    doctors = db.relationship("Doctor", backref="clinic", lazy=True)
    receptionists = db.relationship("Receptionist", backref="clinic", lazy=True)
    appointments = db.relationship("Appointment", backref="clinic", lazy=True)
    messages = db.relationship("Message", backref="clinic", lazy=True)
    medical_records = db.relationship("MedicalRecord", backref="clinic", lazy=True)

    def __repr__(self):
        return f"<Clinic {self.name}>"


class User(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(SQLAEnum(RoleEnum), nullable=False)
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


class Doctor(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    specialty = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("doctor", uselist=False))

    def __repr__(self):
        return f"<Doctor {self.user.username}>"


class Admin(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("admin", uselist=False))

    def __repr__(self):
        return f"<Admin {self.user.username}>"


class Receptionist(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("receptionist", uselist=False))

    def __repr__(self):
        return f"<Receptionist {self.user.username}>"


class Patient(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    date_of_birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("patient", uselist=False))

    def __repr__(self):
        return f"<Patient {self.user.username}>"


class Appointment(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    patient_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("patient.id"), nullable=False
    )
    doctor_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("doctor.id"), nullable=False
    )
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref=db.backref("appointments", lazy=True))
    doctor = db.relationship("Doctor", backref=db.backref("appointments", lazy=True))

    def __repr__(self):
        return f"<Appointment {self.id}>"


class Message(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False
    )
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship(
        "User", foreign_keys=[sender_id], backref=db.backref("sent_messages", lazy=True)
    )
    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        backref=db.backref("received_messages", lazy=True),
    )

    def __repr__(self):
        return f"<Message {self.id}>"


class MedicalRecord(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    patient_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("patient.id"), nullable=False
    )
    doctor_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("doctor.id"), nullable=False
    )
    clinic_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("clinic.id"), nullable=False
    )
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship(
        "Patient", backref=db.backref("medical_records", lazy=True)
    )
    doctor = db.relationship("Doctor", backref=db.backref("medical_records", lazy=True))

    def __repr__(self):
        return f"<MedicalRecord {self.id}>"
