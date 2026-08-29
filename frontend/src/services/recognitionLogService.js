import api from "./api";

export const getRecognitionLogs = async () => {
  const response = await api.get("/recognition-logs");

  return response.data;
};
