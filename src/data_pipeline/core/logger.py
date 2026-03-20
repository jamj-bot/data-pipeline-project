import logging
"""
Logger
-- Genera mensajes (info, error, etc.)
-- Filtra por nivel (INFO, ERROR, etc.)

Handler
-- Recibe el mensaje
-- Lo envía a un destino específico

Destino
-- Consola
-- Archivo
-- Red
-- Sistema externo
"""
def get_logger(name: str) -> logging.Logger:
    # Busca un logger con ese nombre
        # Si existe, lo devuelve; si no, crea uno nuevo
    logger = logging.getLogger(name)

    # Si el logger ya tiene handlers no lo vuelve a configurar
    if logger.handlers:
        return logger

    # Define qué severidad minima se va a registrar
    logger.setLevel(logging.INFO)

    # El handler define dónde se escribe el log
    handler = logging.StreamHandler() # Para escribirlo en consola

    # Define el formato del mensaje del log
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
    )

    # Se asocia el formato definido al handler
    handler.setFormatter(formatter)

    # Se conecta el handler y el logger: Logger → Handler → Output
    logger.addHandler(handler)

    return logger
