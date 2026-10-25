import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Calendar, Users, Wallet, MapPin, Sparkles, Loader2 } from 'lucide-react'
import { generateItinerary } from '../services/api'
import { DEFAULT_TRAVEL_STYLES, DEFAULT_INTERESTS } from '../utils/constants'
import { formatDate, calculateDays } from '../utils/helpers'

export default function TripBuilder({ onGenerate }) {
  const [formData, setFormData] = useState({
    destination: '',
    start_date: '',
    end_date: '',
    budget: '',
    group_size: '1',
    travel_style: 'balanced',
    interests: [],
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedInterests, setSelectedInterests] = useState(new Set())
  const navigate = useNavigate()

  const minDate = new Date().toISOString().split('T')[0]

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setError(null)
    if (type === 'number') {
      setFormData({ ...formData, [name]: value })
    } else {
      setFormData({ ...formData, [name]: value })
    }
  }

  const toggleInterest = (interest) => {
    setError(null)
    const newSet = new Set(selectedInterests)
    if (newSet.has(interest)) {
      newSet.delete(interest)
    } else {
      newSet.add(interest)
    }
    setSelectedInterests(newSet)
    setFormData({ ...formData, interests: Array.from(newSet) })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    if (!formData.destination || !formData.start_date || !formData.end_date || !formData.budget) {
      setError('Please fill in all required fields.')
      return
    }

    const start = new Date(formData.start_date)
    const end = new Date(formData.end_date)
    if (end < start) {
      setError('End date must be after start date.')
      return
    }

    setLoading(true)
    try {
      const payload = {
        destination: formData.destination.trim(),
        budget: parseFloat(formData.budget),
        start_date: formData.start_date,
        end_date: formData.end_date,
        group_size: parseInt(formData.group_size, 10),
        travel_style: formData.travel_style,
        interests: formData.interests,
      }
      const data = await generateItinerary(payload)
      onGenerate(data)
    } catch (err) {
      setError(err.message || 'Failed to generate itinerary. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const dayCount =
    formData.start_date && formData.end_date ? calculateDays(formData.start_date, formData.end_date) : 0

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sage-50 text-sage-700 text-xs font-semibold mb-4">
          <span className="w-2 h-2 rounded-full bg-sage-500 animate-pulse" />
          New itinerary builder
        </div>
        <h1 className="text-4xl font-serif font-bold text-soothing-900 mb-3 text-balance">
          Plan Your Perfect Trip
        </h1>
        <p className="text-soothing-500 text-lg max-w-2xl mx-auto">
          Tell us about your journey and we'll craft a personalized itinerary just for you.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="trip-card p-8 md:p-10 space-y-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Destination & Dates */}
          <div className="space-y-6">
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-soothing-700 flex items-center gap-2">
                <MapPin size={18} strokeWidth={2} className="text-travel-indigo" />
                Destination
              </label>
              <input
                name="destination"
                type="text"
                placeholder="e.g. Kyoto, Japan"
                value={formData.destination}
                onChange={handleChange}
                className="input-field"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-soothing-700 flex items-center gap-2">
                  <Calendar size={18} strokeWidth={2} className="text-travel-indigo" />
                  Start Date
                </label>
                <input
                  name="start_date"
                  type="date"
                  min={minDate}
                  value={formData.start_date}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-soothing-700 flex items-center gap-2">
                  <Calendar size={18} strokeWidth={2} className="text-travel-indigo" />
                  End Date
                </label>
                <input
                  name="end_date"
                  type="date"
                  min={minDate}
                  value={formData.end_date}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
            </div>

            {dayCount > 0 && (
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-blue-50 text-blue-700 text-sm font-medium border border-blue-100">
                <Calendar size={16} strokeWidth={2} />
                {dayCount} day trip
              </div>
            )}
          </div>

          {/* Budget & Group */}
          <div className="space-y-6">
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-soothing-700 flex items-center gap-2">
                <Wallet size={18} strokeWidth={2} className="text-travel-indigo" />
                Total Budget (USD)
              </label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">$</span>
                <input
                  name="budget"
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="e.g. 900"
                  value={formData.budget}
                  onChange={handleChange}
                  className="input-field pl-9"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-semibold text-soothing-700 flex items-center gap-2">
                <Users size={18} strokeWidth={2} className="text-travel-indigo" />
                Group Size
              </label>
              <input
                name="group_size"
                type="number"
                min="1"
                value={formData.group_size}
                onChange={handleChange}
                className="input-field"
              />
            </div>
          </div>
        </div>

        {/* Travel Style */}
        <div className="space-y-4">
          <label className="block text-sm font-semibold text-soothing-700 flex items-center gap-2">
            <Sparkles size={18} strokeWidth={2} className="text-travel-indigo" />
            Travel Style
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {DEFAULT_TRAVEL_STYLES.map((style) => (
              <button
                key={style.value}
                type="button"
                onClick={() => {
                  setFormData({ ...formData, travel_style: style.value })
                }}
                className={`flex flex-col items-center gap-2 p-4 rounded-xl border transition-all duration-200 ${
                  formData.travel_style === style.value
                    ? style.color.replace('bg-', 'ring-2 ring-').replace('text-', '-offset-2 ') + ' border-travel-indigo bg-white shadow-md'
                    : 'bg-white border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <span className="text-xl">{style.icon}</span>
                <span className="font-semibold text-soothing-800 text-sm">{style.label}</span>
                <span className="text-xs text-gray-500">{style.description}</span>
              </button>
            ))}
          </div>
          <input
            type="hidden"
            name="travel_style"
            value={formData.travel_style}
            onChange={handleChange}
          />
        </div>

        {/* Interests */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <label className="block text-sm font-semibold text-soothing-700 flex items-center gap-2">
              <Sparkles size={18} strokeWidth={2} className="text-travel-indigo" />
              Interests
            </label>
            <span className="text-xs text-gray-400">{selectedInterests.size} selected</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
            {DEFAULT_INTERESTS.map((interest) => (
              <button
                key={interest}
                type="button"
                onClick={() => toggleInterest(interest)}
                className={`px-4 py-3 rounded-lg border transition-all duration-200 text-sm font-medium ${
                  selectedInterests.has(interest)
                    ? 'bg-travel-indigo border-travel-indigo text-white shadow-md'
                    : 'bg-white border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-100 text-red-700 text-sm flex items-center gap-3">
            <span>⚠️</span>
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full py-4"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Generating your itinerary…
            </>
          ) : (
            <>
              <Sparkles size={20} strokeWidth={2} className="mr-3" />
              Create My Itinerary
            </>
          )}
        </button>
      </form>

      <div className="mt-8 text-center text-gray-400 text-sm">
        No data is stored without your consent. AI generates suggestions based on your inputs.
      </div>
    </div>
  )
}
