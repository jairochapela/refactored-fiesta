from langchain.tools import tool
from datetime import datetime
from agenda import EventosCalendarioDAO, EventoCalendario

@tool(parse_docstring=True)
def get_fecha_actual(format_str: str) -> str:
    """
    Devuelve la fecha y/o la hora actual formateada según el patrón proporcionado
    en el parámetro 'format_str'.
    El patrón de formato de fecha y hora debe ser compatible con el formato de strftime de Python.
    Por ejemplo:
    - '%Y-%m-%d' para obtener solo la fecha en formato '2024-06-30'
    - '%H:%M:%S' para obtener solo la hora en formato '14:30:00'
    - '%Y-%m-%d %H:%M:%S' para obtener fecha y hora completas en formato '2024-06-30 14:30:00'
    Si el formato proporcionado no es válido, se lanzará una excepción indicando que el
    formato no es compatible con strftime.

    Args:
        format_str (str): El patrón de formato de fecha y hora compatible con strftime.


    Returns:
        str: La fecha y/o hora actual formateada según el patrón proporcionado.
    """
    now = datetime.now()
    try:
        return now.strftime(format_str)
    except ValueError:
        raise ValueError("El formato proporcionado no es válido para strftime")
    
@tool(parse_docstring=True)
def agregar_evento_calendario(titulo: str, descripcion: str, fecha_inicio: str, fecha_fin: str, ubicacion: str = None) -> str:
    """
    Agrega un evento al calendario con los detalles proporcionados.

    Args:
        titulo (str): El título del evento.
        descripcion (str): Una descripción del evento.
        fecha_inicio (str): La fecha y hora de inicio del evento en formato ISO 8601 (YYYY-MM-DD HH:MM:SS).
        fecha_fin (str): La fecha y hora de finalización del evento en formato ISO 8601 (YYYY-MM-DD HH:MM:SS).
        ubicacion (str, optional): La ubicación del evento. Por defecto es None.

    Returns:
        str: Un mensaje indicando que el evento ha sido agregado correctamente al calendario.
    """
    try:
        fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
        fecha_fin_dt = datetime.fromisoformat(fecha_fin)
    except ValueError:
        raise ValueError("Las fechas deben estar en formato ISO 8601 (YYYY-MM-DD HH:MM:SS)")

    evento = EventoCalendario(
        titulo=titulo,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio_dt,
        fecha_fin=fecha_fin_dt,
        ubicacion=ubicacion
    )

    with EventosCalendarioDAO() as dao:
        dao.agregar_evento(evento)

    return f"Evento '{titulo}' agregado al calendario correctamente."


@tool(parse_docstring=True)
def listar_eventos_calendario() -> list[EventoCalendario]:
    """
    Lista todos los eventos del calendario.

    Returns:
        list[EventoCalendario]: Una lista de objetos EventoCalendario que representan los eventos en el calendario.
    """
    with EventosCalendarioDAO() as dao:
        eventos = dao.listar_eventos()
    return eventos

@tool(parse_docstring=True)
def eliminar_evento_calendario(evento_id: int) -> str:
    """
    Elimina un evento del calendario según su ID.

    Args:
        evento_id (int): El ID del evento a eliminar.

    Returns:
        str: Un mensaje indicando que el evento ha sido eliminado correctamente del calendario.
    """
    with EventosCalendarioDAO() as dao:
        dao.eliminar_evento(evento_id)
    return f"Evento con ID {evento_id} eliminado del calendario correctamente."