import azure.functions as func
import json
from controllers.access_controller import AccessController

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ProcessAccess", methods=["POST"])
def ProcessAccess(req: func.HttpRequest) -> func.HttpResponse:
    """
    Endpoint HTTP POST /api/ProcessAccess
    """
    try:
        req_body = req.get_json()
        image_base64 = req_body.get('image')

        # Instanciar controlador y procesar la petición
        controller = AccessController()
        response_data = controller.process_access_request(image_base64)

        return func.HttpResponse(
            body=json.dumps(response_data["body"]),
            status_code=response_data["status"],
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "Formato de solicitud JSON no válido."}),
            status_code=400,
            mimetype="application/json"
        )