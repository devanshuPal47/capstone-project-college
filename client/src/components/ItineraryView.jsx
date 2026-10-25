import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { ArrowLeft, MapPin, Clock, Bed, Utensils, Bus, Share2, Download, Moon, Sun, Heart } from 'lucide-react'
import { formatCurrency, formatDay } from '../utils/helpers'

const ICONS = {
  morning: MapPin,
  afternoon: Clock,
  evening: Utensils,
  dining: Utensils,
  accommodation: Bed,
  transportation: Bus,
}

const LABELS = {
  morning: 'Morning',
  afternoon: 'Afternoon',
  evening: 'Evening',
  dining: 'Dining',
  accommodation: 'Stay',
  transportation: 'Getting Around',
}

export default function ItineraryView({ itinerary: propItinerary, onBack }) {
  const location = useLocation()
  const navigate = useNavigate()
  const [theme, setTheme] = useState('light')
  const [saved, setSaved] = useState(false)

  const data = propItinerary || (location.state?.itinerary || null)
  const totalCost = data?.itinerary?.reduce((sum, day) => sum + (day.estimated_cost || 0), 0) || 0

  useEffect(() => {
    if (!data) {
      navigate('/')
    }
  }, [data, navigate])

  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  const handleDownload = () => {
    const content = `
TRIP ITINERARY
Destination: ${data.destination}
Dates: ${data.start_date} to ${data.end_date}
Group: ${data.group_size} traveler(s)
Style: ${data.travel_style}
Budget: $${data.total_budget}

${data.itinerary.map((day) => `
Day ${day.day} - ${day.date}
  Morning: ${day.morning}
  Afternoon: ${day.afternoon}
  Evening: ${day.evening}
  Dining: ${day.dining}
  Stay: ${day.accommodation}
  Transport: ${day.transportation}
  Cost: $${day.estimated_cost}
`).join('\n')}
    `
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${data.destination}_itinerary.txt`
    a.click()
  }

  const handleShare = async () => {
    if (navigator.share) {
      await navigator.share({
        title: `Trip to ${data.destination}`,
        text: `My ${data.days}-day itinerary for ${data.destination}`,
        url: window.location.href,
      })
    } else {
      await navigator.clipboard.writeText(window.location.href)
    }
  }

  if (!data) return null

  return (
    <div className="min-h-screen bg-soothing-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
          <div>
            <button
              onClick={onBack}
              className="inline-flex items-center gap-2 text-travel-indigo hover:text-travel-indigo/90 font-medium mb-4"
            >
              <ArrowLeft size={18} strokeWidth={2} />
              Back to planner
            </button>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-travel-indigo/10 text-travel-indigo text-xs font-semibold">
                {data.generated_with_ai ? 'AI-Powered' : 'Smart Template'}
              </span>
              <span className="ml-2 px-3 py-1 rounded-full bg-sage-100 text-sage-700 text-xs font-semibold">
                {data.days} Days
              </span>
            </div>
          </div>

          <div className="flex gap-3">
            <button onClick={handleSave} className="p-3 rounded-xl bg-white border border-gray-200 text-soothing-600 hover:bg-gray-50 transition-all shadow-sm">
              <Heart size={20} strokeWidth={2} className={`${saved ? 'text-red-500 fill-red-500' : ''}`} />
              <span className="hidden sm:inline ml-1 text-sm font-medium">{saved ? 'Saved' : 'Save'}</span>
            </button>
            <button onClick={handleShare} className="p-3 rounded-xl bg-white border border-gray-200 text-soothing-600 hover:bg-gray-50 transition-all shadow-sm">
              <Share2 size={20} strokeWidth={2} />
            </button>
            <button onClick={handleDownload} className="p-3 rounded-xl bg-white border border-gray-200 text-soothing-600 hover:bg-gray-50 transition-all shadow-sm">
              <Download size={20} strokeWidth={2} />
            </button>
            <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} className="p-3 rounded-xl bg-white border border-gray-200 text-soothing-600 hover:bg-gray-50 transition-all shadow-sm">
              {theme === 'light' ? <Moon size={20} strokeWidth={2} /> : <Sun size={20} strokeWidth={2} />}
            </button>
          </div>
        </div>

        {/* Hero Section */}
        <div className="relative rounded-3xl overflow-hidden shadow-soft-lg mb-8 bg-white border border-gray-100">
          <div className="absolute inset-0 bg-gradient-to-br from-travel-indigo/5 to-travel-purple/10" />
          <div className="relative p-8 md:p-12 z-10">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-2xl bg-sage-200 flex items-center justify-center text-sage-800 font-bold">
                <MapPin size={20} strokeWidth={2} />
              </div>
              <h1 className="text-3xl font-serif font-bold text-soothing-900 leading-tight">
                {data.destination}
              </h1>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="p-3 rounded-xl bg-gray-50 border border-gray-100">
                <div className="text-gray-500 text-xs uppercase tracking-wider font-semibold">Dates</div>
                <div className="font-medium text-soothing-800">
                  {data.start_date} → {data.end_date}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-gray-50 border border-gray-100">
                <div className="text-gray-500 text-xs uppercase tracking-wider font-semibold">Travelers</div>
                <div className="font-medium text-soothing-800">{data.group_size}</div>
              </div>
              <div className="p-3 rounded-xl bg-gray-50 border border-gray-100">
                <div className="text-gray-500 text-xs uppercase tracking-wider font-semibold">Style</div>
                <div className="font-medium text-soothing-800 capitalize">{data.travel_style}</div>
              </div>
              <div className="p-3 rounded-xl bg-gray-50 border border-gray-100">
                <div className="text-gray-500 text-xs uppercase tracking-wider font-semibold">Budget</div>
                <div className="font-medium text-soothing-800">${data.total_budget}</div>
              </div>
            </div>
            <p className="mt-6 text-soothing-500 max-w-xl leading-relaxed">
              Your personalized {data.days}-day journey through {data.destination}, crafted to match your {data.travel_style} pace and interests.
            </p>
          </div>
        </div>

        {/* Map Preview */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-soothing-900">Route Overview</h2>
            <div className="flex items-center gap-2 text-xs text-gray-500 uppercase tracking-wider font-semibold">
              <span className="w-2 h-2 rounded-full bg-travel-indigo" />
              <span>Planned route</span>
            </div>
          </div>
          <div className="rounded-2xl border border-gray-200 bg-gray-50/50 overflow-hidden shadow-sm aspect-video relative flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-white/80 backdrop-blur flex items-center justify-center mx-auto mb-3 shadow-soft">
                <MapPin size={24} strokeWidth={2} className="text-travel-indigo" />
              </div>
              <p className="text-soothing-500 text-sm">Interactive map preview</p>
              <p className="text-xs text-gray-400 mt-1">Enable location services for map</p>
            </div>
          </div>
        </div>

        {/* Itinerary Days */}
        <div className="space-y-6">
          <h2 className="text-2xl font-serif font-bold text-soothing-900 mb-2">Day-by-Day Plan</h2>
          <div className="space-y-4">
            {data.itinerary.map((day) => (
              <div
                key={day.day}
                className="trip-card group animate-slide-up"
                style={{ animationDelay: `${day.day * 0.1}s` }}
              >
                <div className="px-6 py-5 border-b border-gray-50 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-travel-indigo/10 text-travel-indigo flex items-center justify-center font-bold text-lg">
                      {day.day}
                    </div>
                    <div>
                      <h3 className="font-bold text-soothing-900">Day {day.day}</h3>
                      <p className="text-gray-500 text-sm">{formatDay(day.date)}</p>
                    </div>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-gray-100 text-gray-600 text-xs font-medium">
                    ${day.estimated_cost}
                  </span>
                </div>

                <div className="px-6 py-5">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[['morning', day.morning], ['afternoon', day.afternoon], ['evening', day.evening]].map(
                      ([key, value], idx) => {
                        const Icon = ICONS[key]
                        return (
                          <div key={key} className="p-4 rounded-xl border border-gray-100 bg-gray-50/50">
                            <div className="flex items-center gap-2 mb-2">
                              <Icon size={16} strokeWidth={2} className="text-travel-indigo" />
                              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                {LABELS[key]}
                              </span>
                            </div>
                            <p className="text-soothing-800 text-sm leading-relaxed">{value}</p>
                          </div>
                        )
                      }
                    )}
                  </div>

                  <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[
                      ['dining', day.dining, 'Dining'],
                      ['accommodation', day.accommodation, 'Stay'],
                      ['transportation', day.transportation, 'Transport'],
                    ].map(([key, value, label]) => {
                      const Icon = ICONS[key]
                      return (
                        <div key={key} className="p-4 rounded-xl border border-gray-100 bg-white shadow-sm">
                          <div className="flex items-center gap-2 mb-2">
                            <Icon size={16} strokeWidth={2} className="text-gray-400" />
                            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                              {label}
                            </span>
                          </div>
                          <p className="text-soothing-700 text-sm leading-relaxed">{value}</p>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Budget Summary */}
          <div className="trip-card p-6 mt-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-soothing-900">Budget Summary</h3>
              <span className="font-bold text-travel-indigo">{formatCurrency(totalCost)}</span>
            </div>
            <div className="h-px bg-gray-100 mb-4"></div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wider">Total Budget</p>
                <p className="text-soothing-800 font-medium">${data.total_budget}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wider">Planned Cost</p>
                <p className="text-soothing-800 font-medium">{formatCurrency(totalCost)}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wider">Remaining</p>
                <p className={`text-soothing-800 font-medium ${totalCost <= data.total_budget ? 'text-green-600' : 'text-red-500'}`}>
                  {formatCurrency(data.total_budget - totalCost)}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase tracking-wider">Per Day</p>
                <p className="text-soothing-800 font-medium">{formatCurrency(totalCost / data.days)}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 text-center text-gray-400 text-sm">
          Made with ☁️ by Skillwallet Travel Planner
        </div>
      </div>
    </div>
  )
}
