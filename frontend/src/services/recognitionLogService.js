import api from "./api";

export const getAllRecognitionLogs = async () => {
  const response = await api.get("/recognition-logs");

  return response.data;
};

export const getRecognitionLogsByEmployee = async (employeeId) => {
  const response = await api.get(`/recognition-logs/employee/${employeeId}`);

  return response.data;
};

export const getRecognitionLogsByCamera = async (cameraId) => {
  const response = await api.get(`/recognition-logs/camera/${cameraId}`);

  return response.data;
};
