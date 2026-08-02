const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:7071/api';

export const verifyAccess = async (base64Image) => {
  try {
    const response = await fetch(`${API_BASE_URL}/ProcessAccess`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image: base64Image }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `Error del servidor: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error al verificar acceso:', error);
    throw error;
  }
};