import React, { useRef, useState, useEffect } from 'react';
import { verifyAccess } from '../services/apiService';

export const CameraView = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  // Inicializar la cámara web al cargar el componente
  useEffect(() => {
    startCamera();
    return () => stopCamera(); // Limpieza al desmontar
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Error al acceder a la cámara:", err);
      setErrorMessage("No se pudo acceder a la cámara web. Verifica los permisos del navegador.");
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
    }
  };

  const captureAndVerify = async () => {
    setLoading(true);
    setResult(null);
    setErrorMessage('');

    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas) return;

    // Dibujar el fotograma actual del video en el canvas
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convertir el lienzo a base64 (JPEG)
    const base64Image = canvas.toDataURL('image/jpeg', 0.8);

    try {
      // Enviar la imagen a la API de Azure
      const response = await verifyAccess(base64Image);
      setResult(response.result);
    } catch (err) {
      setErrorMessage(err.message || "Ocurrió un error al procesar la imagen.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Control de Acceso Facial</h2>
      
      {errorMessage && <div style={styles.errorBanner}>{errorMessage}</div>}

      <div style={styles.videoWrapper}>
        <video 
          ref={videoRef} 
          autoPlay 
          playsInline 
          muted 
          style={styles.video} 
        />
        {/* Canvas oculto para procesar la captura de pantalla */}
        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>

      <button 
        onClick={captureAndVerify} 
        disabled={loading}
        style={loading ? { ...styles.button, ...styles.buttonDisabled } : styles.button}
      >
        {loading ? 'Procesando...' : '📷 Validar Acceso'}
      </button>

      {/* Renderizado de Resultados */}
      {result && (
        <div style={{
          ...styles.resultCard,
          borderColor: result.authorized ? '#2e7d32' : '#c62828',
          backgroundColor: result.authorized ? '#e8f5e9' : '#ffebee'
        }}>
          <h3 style={{ color: result.authorized ? '#2e7d32' : '#c62828', margin: '0 0 10px 0' }}>
            {result.authorized ? '✅ ACCESO PERMITIDO' : '❌ ACCESO DENEGADO'}
          </h3>
          <p><strong>Mensaje:</strong> {result.message}</p>
          {result.user_name && <p><strong>Usuario:</strong> {result.user_name}</p>}
          {result.confidence && <p><strong>Confianza:</strong> {result.confidence}%</p>}
        </div>
      )}
    </div>
  );
};

// Estilos básicos en JS para una presentación limpia sin depender de frameworks CSS
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px'
  },
  videoWrapper: {
    width: '100%',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
    backgroundColor: '#000',
    marginBottom: '20px'
  },
  video: {
    width: '100%',
    height: 'auto',
    display: 'block'
  },
  button: {
    padding: '12px 24px',
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: '#0078d4',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  },
  buttonDisabled: {
    backgroundColor: '#a6a6a6',
    cursor: 'not-allowed'
  },
  resultCard: {
    marginTop: '20px',
    padding: '15px 20px',
    borderRadius: '6px',
    borderLeft: '6px solid',
    width: '100%',
    boxSizing: 'border-box'
  },
  errorBanner: {
    backgroundColor: '#fde8e8',
    color: '#9b1c1c',
    padding: '10px 15px',
    borderRadius: '4px',
    marginBottom: '15px',
    width: '100%'
  }
};