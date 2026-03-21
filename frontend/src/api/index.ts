export const API_BASE_URL = 'http://localhost:8000/api/v1'

export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}
