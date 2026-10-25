export const API_BASE = '/api'

export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `Request failed: ${response.status}`)
  }

  return response.json()
}

export const generateItinerary = (payload) =>
  apiRequest('/generate-itinerary', {
    method: 'POST',
    body: JSON.stringify(payload),
  })

export const getDestinations = () => apiRequest('/destinations')
export const getTrips = () => apiRequest('/trips')
export const getTrip = (id) => apiRequest(`/trips/${id}`)
export const saveTrip = (trip) => apiRequest('/trips', { method: 'POST', body: JSON.stringify(trip) })
