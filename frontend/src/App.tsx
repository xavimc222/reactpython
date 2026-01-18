import { useState } from 'react'
import './App.css'

function App() {
  const [code, setCode] = useState("print('Hello, World!')")
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)

  const executeCode = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      })
      const data = await response.json()
      setOutput(data.output || 'Error: ' + JSON.stringify(data))
    } catch (error) {
      setOutput('Error: ' + (error as Error).message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>Python Code Executor</h1>
      <div className="container">
        <div className="input-section">
          <label htmlFor="code-input">Python Code:</label>
          <textarea
            id="code-input"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={10}
            cols={50}
          />
        </div>
        <button onClick={executeCode} disabled={loading}>
          {loading ? 'Executing...' : 'Execute'}
        </button>
        <div className="output-section">
          <label htmlFor="output">Output:</label>
          <textarea
            id="output"
            value={output}
            readOnly
            rows={10}
            cols={50}
          />
        </div>
      </div>
    </div>
  )
}

export default App
