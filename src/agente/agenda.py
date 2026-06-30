from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from config import DB_URI
import psycopg

class EventoCalendario(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    ubicacion: Optional[str] = None


class EventosCalendarioDAO:

    def __init__(self):
        self.__initdb()

    def __initdb(self):
        with psycopg.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS eventos_calendario (
                        id SERIAL PRIMARY KEY,
                        titulo TEXT NOT NULL,
                        descripcion TEXT,
                        fecha_inicio TIMESTAMP NOT NULL,
                        fecha_fin TIMESTAMP NOT NULL,
                        ubicacion TEXT
                    )
                """)
                conn.commit()

    def __enter__(self):
        self.conn = psycopg.connect(DB_URI)
        self.cur = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
        self.conn.close()

    def agregar_evento(self, evento: EventoCalendario):
        with self.conn:
            self.cur.execute("""
                INSERT INTO eventos_calendario (titulo, descripcion, fecha_inicio, fecha_fin, ubicacion)
                VALUES (%s, %s, %s, %s, %s)
            """, (evento.titulo, evento.descripcion, evento.fecha_inicio.isoformat(), evento.fecha_fin.isoformat(), evento.ubicacion))
            self.conn.commit()

    def listar_eventos(self):
        with self.conn:
            self.cur.execute("SELECT id, titulo, descripcion, fecha_inicio, fecha_fin, ubicacion FROM eventos_calendario")
            rows = self.cur.fetchall()
            eventos = [
                EventoCalendario(id=row[0], titulo=row[1], descripcion=row[2], fecha_inicio=row[3], fecha_fin=row[4], ubicacion=row[5])
                for row in rows
            ]
            return eventos
        
    def eliminar_evento(self, evento_id: int):
        with self.conn:
            self.cur.execute("DELETE FROM eventos_calendario WHERE id = %s", (evento_id,))
            self.conn.commit()