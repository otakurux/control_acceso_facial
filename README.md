# 🎭 Sistema de Control de Acceso por Reconocimiento Facial

Un sistema de control de acceso inteligente, moderno y seguro desarrollado sobre arquitectura **Serverless** en la nube de **Microsoft Azure**, enfocado en la gestión de entradas de usuarios mediante visión por computadora.

---

## 📌 Descripción del Proyecto

Este proyecto consiste en un sistema de autenticación biométrica en tiempo real. Utilizando la cámara web desde una aplicación cliente en React, el sistema captura el rostro del usuario y valida su identidad mediante el motor de **Azure AI Vision (Face API)**. 

La solución está construida bajo el patrón de arquitectura **Model-View-Controller (MVC)**, garantizando la separación de responsabilidades y permitiendo un escalado automático con costos operativos de $0 USD gracias a la capa gratuita de los servicios Serverless de Azure.

---

## 🚀 Arquitectura y Tecnologías

El proyecto combina un frontend web desacoplado y una API serverless respaldada por servicios cognitivos de Inteligencia Artificial:

* **Frontend (View):** React.js (desplegado en **Azure Static Web Apps**).
* **Backend (Controller):** Python en **Azure Functions** (API Serverless).
* **Inteligencia Artificial (Model):** **Azure AI Vision (Face API)** para detección, registro y comparación de rostros.
* **Almacenamiento (Model):** **Azure Blob Storage** (para imágenes) y **Azure Cosmos DB / Table Storage** (para logs de auditoría de entrada).

---

## 📁 Estructura del Proyecto (MVC)

```text
mi-proyecto-acceso/
├── .github/workflows/        # Integración y despliegue continuo (CI/CD)
├── frontend/                 # Aplicación cliente en React (Vista)
│   ├── public/
│   └── src/
│       ├── components/       # Componentes de la UI (Cámara, interfaz de usuario)
│       ├── services/         # Servicio de peticiones HTTP al backend
│       └── App.jsx
└── api/                      # Backend en Python con Azure Functions (Controlador y Modelo)
    ├── controllers/          # Lógica de negocio y recepción de peticiones HTTP
    │   └── access_controller.py
    ├── models/               # Conexión con Azure AI Vision y almacenamiento de Logs
    │   ├── face_model.py
    │   └── log_model.py
    ├── ProcessAccess/        # Endpoint principal de la Azure Function
    │   └── function.json
    ├── host.json
    └── requirements.txt      # Dependencias de Python