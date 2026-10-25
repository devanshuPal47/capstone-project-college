import { Link } from 'react-router-dom'
import { MapPin, Sparkles, Users, Calendar } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 glass-panel">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-travel-indigo to-travel-purple flex items-center justify-center text-white font-bold shadow-md">
              <MapPin size={20} strokeWidth={2} />
            </div>
            <Link to="/" className="flex items-center gap-2">
              <span className="font-serif text-xl font-bold text-soothing-900 tracking-tight">
                Skillwallet<span className="text-travel-indigo">Travel</span>
              </span>
              <span className="ml-1 text-xs font-medium px-2 py-0.5 rounded bg-sage-100 text-sage-700">
                AI Planner
              </span>
            </Link>
          </div>
          <div className="hidden md:flex items-center gap-6 text-sm font-medium text-soothing-600">
            <Link
              to="/"
              className="flex items-center gap-2 hover:text-travel-indigo transition-colors px-3 py-2 rounded-lg hover:bg-gray-50"
            >
              <MapPin size={16} strokeWidth={2} />
              Plan a Trip
            </Link>
            <a
              href="#"
              className="flex items-center gap-2 hover:text-travel-indigo transition-colors px-3 py-2 rounded-lg hover:bg-gray-50"
            >
              <Sparkles size={16} strokeWidth={2} />
              Inspiration
            </a>
          </div>
          <div className="flex items-center gap-3">
            <Link
              to="/"
              className="btn-primary text-sm"
            >
              <Sparkles size={16} strokeWidth={2} className="mr-2" />
              Start Planning
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
