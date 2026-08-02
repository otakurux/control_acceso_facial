from datetime import datetime

class LogModel:
    @staticmethod
    def create_log(user_name, status, confidence):
        """
        Estructura el registro de acceso para auditoría.
        (Puedes extender esto para guardar en Azure Blob Storage o Cosmos DB).
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "user_name": user_name if user_name else "Desconocido",
            "status": "GRANTED" if status else "DENIED",
            "confidence": f"{confidence}%" if confidence else "0%"
        }