import { useState } from 'react'
import './App.css'
import { documentation } from './documentation'

function App() {
  const [code, setCode] = useState(`import logging
import json
from utils.readopense import readopense

logging.getLogger().setLevel("INFO")

payload = {
    "payload": {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    # {"match": {"item": "500007300 D133"}},
                ],
                "must_not": [
                    # {
                    #     "match": {
                    #         "rule": "None"
                    #     }
                    # }
                ],
            }
        },
        "_source": {
            "includes": [
                # "children",
                # "parents",
            ]
        },
        "sort": [
            # {
            #     "inventoryDate": {
            #         "order": "desc"
            #     }
            # }
        ]
    },
    "index": "ai-research-shell-bom-3",
}

response: list[dict] = readopense(payload)

print(json.dumps(response, indent=2))
print(len(response), payload["index"])`)
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)

  const copyDocumentation = async () => {
    try {
      await navigator.clipboard.writeText(documentation)
    } catch (err) {
      console.error('Failed to copy documentation:', err)
    }
  }

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code)
    } catch (err) {
      console.error('Failed to copy code:', err)
    }
  }

  const clearAndCopyCode = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCode('')
    } catch (err) {
      console.error('Failed to copy code:', err)
    }
  }

  const copyOutput = async () => {
    try {
      await navigator.clipboard.writeText(output)
    } catch (err) {
      console.error('Failed to copy output:', err)
    }
  }

  const clearAndCopyOutput = async () => {
    try {
      await navigator.clipboard.writeText(output)
      setOutput('')
    } catch (err) {
      console.error('Failed to copy output:', err)
    }
  }

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
      <h1>Organic Planner Debug</h1>
      <div className="container">
        <div className="input-section">
          <label htmlFor="code-input" className="label-with-icons">
            <span>Python Code:</span>
            <div className="icons">
              <button className="icon-button" onClick={clearAndCopyCode} title="Clear and Copy to Clipboard">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 6h18"></path>
                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                </svg>
              </button>
              <button className="icon-button" onClick={copyCode} title="Copy to Clipboard">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
              </button>
            </div>
          </label>
          <textarea
            id="code-input"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={10}
            cols={50}
          />
        </div>
        <div className="button-container">
          <button onClick={copyDocumentation} className="secondary-button" title="Copy Documentation">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '8px' }}>
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            DOCUMENTATION
          </button>
          <button onClick={executeCode} disabled={loading}>
            {loading ? 'Executing...' : 'Execute'}
          </button>
        </div>
        <div className="output-section">
          <label htmlFor="output" className="label-with-icons">
            <span>Output:</span>
            <div className="icons">
              <button className="icon-button" onClick={clearAndCopyOutput} title="Clear and Copy to Clipboard">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 6h18"></path>
                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                </svg>
              </button>
              <button className="icon-button" onClick={copyOutput} title="Copy to Clipboard">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
              </button>
            </div>
          </label>
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
