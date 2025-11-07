import { useState } from 'react'
import MainSchedulerPage from './pages/MainSchedulerPage'
import ResultsPage from './pages/ResultsPage'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('main') // 'main', 'results'
  const [selectedCourses, setSelectedCourses] = useState({})
  const [preferences, setPreferences] = useState(null)
  const [hardBreaks, setHardBreaks] = useState([])
  const [softBreaks, setSoftBreaks] = useState([])

  const handleGenerateSchedules = ({ preferences: prefs, hardBreaks: hard, softBreaks: soft }) => {
    setPreferences(prefs)
    setHardBreaks(hard)
    setSoftBreaks(soft)
    setCurrentPage('results')
  }

  const handleBackToMain = () => {
    setCurrentPage('main')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">Course Scheduler</h1>
        <p className="app-subtitle">Generate your optimal class schedule</p>
      </header>

      <main className="app-main">
        {currentPage === 'main' && (
          <MainSchedulerPage
            onGenerate={handleGenerateSchedules}
            selectedCourses={selectedCourses}
            setSelectedCourses={setSelectedCourses}
          />
        )}

        {currentPage === 'results' && (
          <ResultsPage
            onBack={handleBackToMain}
            selectedCourses={selectedCourses}
            preferences={preferences}
            hardBreaks={hardBreaks}
            softBreaks={softBreaks}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>Made for UIUC students • Data from Course Explorer</p>
      </footer>
    </div>
  )
}

export default App
