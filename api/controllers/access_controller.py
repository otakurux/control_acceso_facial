import base64
import io
from models.face_model import FaceModel
from models.log_model import LogModel

class AccessController:
    def __init__(self):
        self.face_model = FaceModel()

    def process_access_request(self, image_base64):
        """
        Recibe la cadena base64 desde el frontend, la convierte a binario y consulta al modelo.
        """
        if not image_base64:
            return {"status": 400, "body": {"error": "No se proporcionó una imagen válida."}}

        try:
            # Limpiar encabezado base64 si viene con prefijo 'data:image/jpeg;base64,'
            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]

            # Decodificar de base64 a stream binario en memoria
            image_bytes = base64.b64decode(image_base64)
            image_stream = io.BytesIO(image_bytes)

            # Invocar la lógica del Modelo de IA
            result = self.face_model.verify_face(image_stream)

            # Generar log de la transacción
            log = LogModel.create_log(
                user_name=result.get("user_name"),
                status=result.get("authorized", False),
                confidence=result.get("confidence")
            )

            # Retornar respuesta y log
            return {
                "status": 200,
                "body": {
                    "result": result,
                    "log": log
                }
            }

        except Exception as e:
            return {"status": 500, "body": {"error": f"Error interno del servidor: {str(e)}"}}