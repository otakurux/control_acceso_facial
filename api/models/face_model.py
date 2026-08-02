import os
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

class FaceModel:
    def __init__(self):
        # Cargar credenciales desde variables de entorno
        self.endpoint = os.getenv("FACE_API_ENDPOINT")
        self.key = os.getenv("FACE_API_KEY")
        self.group_id = os.getenv("PERSON_GROUP_ID", "estudiantes-informatica")
        
        if not self.endpoint or not self.key:
            raise ValueError("Las credenciales de Azure Face API no están configuradas correctamente.")
            
        # Inicializar el cliente SDK de Azure Face
        self.client = FaceClient(self.endpoint, CognitiveServicesCredentials(self.key))

    def verify_face(self, image_stream):
        """
        Detecta un rostro en la imagen recibida y lo compara contra el PersonGroup de Azure.
        """
        try:
            # 1. Detectar rostros en el stream de la imagen
            detected_faces = self.client.face.detect_with_stream(
                image=image_stream,
                return_face_id=True,
                detection_model="detection_03"
            )

            if not detected_faces:
                return {"success": False, "message": "No se detectó ningún rostro en la imagen."}

            face_id = detected_faces[0].face_id

            # 2. Identificar el rostro dentro del grupo de personas autorizadas
            results = self.client.face.identify([face_id], self.group_id)

            if not results or not results[0].candidates:
                return {
                    "success": False, 
                    "authorized": False, 
                    "message": "Acceso Denegado: Rostro no reconocido o no registrado."
                }

            # 3. Obtener el candidato con mayor coincidencia
            candidate = results[0].candidates[0]
            confidence = candidate.confidence * 100

            # Validar umbral mínimo de confianza (ej. 70%)
            if confidence < 70:
                return {
                    "success": True,
                    "authorized": False,
                    "confidence": round(confidence, 2),
                    "message": "Acceso Denegado: Nivel de confianza insuficiente."
                }

            # 4. Obtener datos de la persona registrada en Azure
            person = self.client.person_group_person.get(self.group_id, candidate.person_id)

            return {
                "success": True,
                "authorized": True,
                "user_name": person.name,
                "confidence": round(confidence, 2),
                "message": f"Acceso Permitido. Bienvenido, {person.name}!"
            }

        except Exception as e:
            return {"success": False, "error": str(e)}