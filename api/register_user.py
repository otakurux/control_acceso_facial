import os
import time
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# ==========================================
# 1. Configuración de Credenciales
# ==========================================
# Reemplaza directamente con tus datos o asegúrate de tener las variables de entorno configuradas
ENDPOINT = os.getenv("FACE_API_ENDPOINT")
KEY = os.getenv("FACE_API_KEY")
PERSON_GROUP_ID = os.getenv("PERSON_GROUP_ID")

# Inicializar cliente de Azure Face
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


def setup_person_group():
    """Crea el PersonGroup si no existe previamente."""
    print(f"📌 Creando grupo de personas: '{PERSON_GROUP_ID}'...")
    try:
        face_client.person_group.create(
            person_group_id=PERSON_GROUP_ID, 
            name="Estudiantes de Informática",
            recognition_model="recognition_04" # Modelo de reconocimiento actualizado
        )
        print("✅ Grupo de personas creado exitosamente.")
    except Exception as e:
        if "PersonGroupExists" in str(e):
            print("ℹ️ El grupo ya existe. Continuando con el registro...")
        else:
            print(f"❌ Error al crear el grupo: {e}")
            return False
    return True


def register_user_with_images(user_name, image_paths):
    """
    Registra un usuario y le asigna una lista de imágenes locales para su entrenamiento.
    :param user_name: Nombre de la persona (ej. 'David Mamani')
    :param image_paths: Lista de rutas a fotos de la persona ['foto1.jpg', 'foto2.jpg']
    """
    try:
        # 1. Crear el perfil de la persona dentro del grupo
        print(f"\n👤 Registrando a: {user_name}...")
        person = face_client.person_group_person.create(PERSON_GROUP_ID, name=user_name)
        person_id = person.person_id
        print(f"✅ Usuario creado con ID: {person_id}")

        # 2. Asignar las fotos al usuario
        for img_path in image_paths:
            if not os.path.exists(img_path):
                print(f"⚠️ La imagen '{img_path}' no existe. Omitiendo...")
                continue

            with open(img_path, "rb") as image_file:
                print(f"📸 Subiendo imagen: {img_path}...")
                face_client.person_group_person.add_face_from_stream(
                    person_group_id=PERSON_GROUP_ID,
                    person_id=person_id,
                    image=image_file,
                    detection_model="detection_03"
                )
            print(f"✅ Imagen '{img_path}' vinculada a {user_name}.")

        # 3. Entrenar el PersonGroup para actualizar el modelo de reconocimento
        print(f"\n⚙️ Entrenando el modelo del grupo '{PERSON_GROUP_ID}'...")
        face_client.person_group.train(PERSON_GROUP_ID)

        # Esperar a que el entrenamiento finalice
        while True:
            training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
            print(f"Estado del entrenamiento: {training_status.status}")
            
            if training_status.status == 'succeeded':
                print(f"🎉 ¡Entrenamiento completado exitosamente! {user_name} ya está listo para ser reconocido.")
                break
            elif training_status.status == 'failed':
                print("❌ El entrenamiento ha fallado.")
                break
            
            time.sleep(2)

    except Exception as e:
        print(f"❌ Error durante el registro: {e}")


# ==========================================
# 2. Ejemplo de Uso / Ejecución Principal
# ==========================================
if __name__ == "__main__":
    # Paso 1: Crear el grupo en Azure
    if setup_person_group():
        
        # Paso 2: Define el nombre del usuario y la ruta de tus fotos locales
        NOMBRE_USUARIO = "David Mamani"
        FOTOS_ENTRENAMIENTO = [
            "mis_fotos/david_1.jpg",  # Asegúrate de colocar fotos reales donde se vea bien tu rostro
            "mis_fotos/david_2.jpg"
        ]

        # Paso 3: Registrar e entrenar
        register_user_with_images(NOMBRE_USUARIO, FOTOS_ENTRENAMIENTO)