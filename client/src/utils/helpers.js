export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

export function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  })
}

export function formatDay(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  })
}

export function calculateDays(start, end) {
  const startDate = new Date(start)
  const endDate = new Date(end)
  const diffTime = Math.abs(endDate - startDate)
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1
}

export function getTravelStyleIcon(style) {
  const icons = {
    relaxed: '☁️',
    balanced: '⚖️',
    packed: '🚀',
  }
  return icons[style] || '⚖️'
}

export function getTravelStyleColor(style) {
  const colors = {
    relaxed: 'bg-blue-50 text-blue-700 border-blue-100',
    balanced: 'bg-indigo-50 text-indigo-700 border-indigo-100',
    packed: 'bg-purple-50 text-purple-700 border-purple-100',
  }
  return colors[style] || colors.balanced
}
