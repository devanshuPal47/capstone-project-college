import { useState } from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import { ArrowLeft, MapPin, Calendar, Users, Wallet, Sparkles } from 'lucide-react'
import TripBuilder from './components/TripBuilder'
import ItineraryView from './components/ItineraryView'
import Navbar from './components/Navbar'
import { TOAST } from './utils/toast'

export default function App() {
  const [itinerary, setItinerary] = useState(null)
  const navigate = useNavigate()

  const handleGenerate = (data) => {
    setItinerary(data)
    navigate('/itinerary', { state: { itinerary: data } })
  }

  return (
    <div className="min-h-screen bg-soothing-50">
      <Navbar />
      <Routes>
        <Route
          path="/"
          element={
            <TripBuilder onGenerate={handleGenerate} />
          }
        />
        <Route
          path="/itinerary"
          element={
            <ItineraryView
              itinerary={itinerary}
              onBack={() => {
                setItinerary(null)
                navigate('/')
              }}
            />
          }
        />
      </Routes>
    </div>
  )
}
