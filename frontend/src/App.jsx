import { useState } from "react"
import axios from "axios"
import { useEffect } from "react"

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js"

import { Bar } from "react-chartjs-2"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

function LoginScreen({ onLogin, error }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const tryLogin = async () => {
    try {
      await axios.get(
        "http://127.0.0.1:8000/api/history/",
        {
          auth: { username, password }
        }
      )

      onLogin({ username, password })

    } catch {
      alert("Wrong username or password ❌")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-200">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96 space-y-4">

        <h2 className="text-2xl font-bold text-slate-700 text-center">
          Login
        </h2>

        <input
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="w-full border p-2 rounded"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full border p-2 rounded"
        />

        <button
          onClick={tryLogin}
          className="w-full py-2 rounded-lg font-semibold text-white
                     bg-blue-700 hover:bg-blue-800 active:bg-blue-900"
        >
          Login
        </button>

        {error && (
          <div className="text-red-600 text-sm text-center">
            {error}
          </div>
        )}

      </div>
    </div>
  )
}


export default function App() {
  const [file, setFile] = useState(null)
  const [summary, setSummary] = useState(null)
  const [message, setMessage] = useState("")
  const [history, setHistory] = useState([])
  const [currentDatasetId, setCurrentDatasetId] = useState(null)
  const [auth, setAuth] = useState(null)
  const [loginError, setLoginError] = useState("")

  const handleUpload = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        {
          auth: auth
        }
      )

      setSummary(res.data.summary)
      setCurrentDatasetId(res.data.id)
      setMessage("Upload successful ✅")
      loadHistory()

    } catch {
      setMessage("Upload failed ❌")
    }
  }

  const loadHistory = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/api/history/",
      {
        auth: auth
      }
    )
    setHistory(res.data)
  } catch {
    console.log("History fetch failed")
  }
}

useEffect(() => {
  if (auth) {
    loadHistory()
  }
}, [auth])

  const downloadPDF = async (id) => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/api/report/${id}/`,
      {
        responseType: "blob",
        auth: auth
        
      }
    )

    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement("a")
    link.href = url
    link.setAttribute("download", `report_${id}.pdf`)
    document.body.appendChild(link)
    link.click()
  } catch {
    alert("PDF download failed")
  }
}


  const chartData = summary
  ? {
      labels: summary.type_distribution.chart.labels,
      datasets: [
        {
          label: "Equipment Count",
          data: summary.type_distribution.chart.values,
          backgroundColor: "#1f2937",
          borderColor: "#0f3f85",
          borderWidth: 1,
        },
      ],
    }
  : null

if (!auth) {
  return <LoginScreen onLogin={setAuth} error={loginError} />
}

return (
  <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200">
    <div className="max-w-7xl mx-auto p-8 space-y-8">

      <div className="bg-slate-800 text-white rounded-xl p-6 shadow-lg">
  <div className="flex items-center justify-between">

    <div>
      <h1 className="text-3xl font-bold">
        Chemical Equipment Visualizer
      </h1>
      <p className="text-slate-300 mt-1">
        Dataset Analysis • Equipment Distribution • PDF Reports
      </p>
    </div>

    <button
      onClick={() => {
        setAuth(null)
        setSummary(null)
        setHistory([])
      }}
      className="
        bg-red-600 px-4 py-2 rounded-lg font-semibold
        hover:bg-red-700 active:bg-red-800
        transition
      "
    >
      Logout
    </button>

  </div>
</div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <div className="bg-white rounded-xl shadow p-6 space-y-4 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-700">
            Upload Dataset
          </h2>

          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="
              block w-full text-sm
              file:mr-4 file:py-2 file:px-4
              file:rounded-lg file:border-0
              file:bg-slate-700 file:text-white
              hover:file:bg-slate-900
            "
          />

          <button
            onClick={handleUpload}
            disabled={!file}
            className="
    w-full py-2 rounded-lg font-semibold text-white
    bg-blue-700
    hover:bg-blue-800
    active:bg-blue-900
    transition-colors duration-200
  "
          >
            Upload CSV
          </button>

          {message && (
            <div className="bg-slate-100 border border-slate-300 p-3 rounded">
              {message}
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl shadow p-6 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-700 mb-4">
            Upload History
          </h2>

          <div className="space-y-3 max-h-64 overflow-y-auto">
            {history.map((item) => (
              <div
                key={item.id}
                className="
                  flex justify-between items-center
                  border rounded-lg p-3
                  hover:bg-slate-50 transition
                "
              >
                <span className="font-medium text-slate-700">
                  {item.filename}
                </span>

                <div className="flex gap-2">
                  <button
                    onClick={() => {setSummary(item.summary),setCurrentDatasetId(item.id)}}
                    className="
  bg-emerald-600 text-white px-3 py-1 rounded
  hover:bg-emerald-700
  active:bg-emerald-800
  transition
"
                  >
                    View
                  </button>

                  <button
                    onClick={() => downloadPDF(item.id)}
                    className="
  bg-indigo-600 text-white px-3 py-1 rounded ml-2
  hover:bg-indigo-700
  active:bg-indigo-800
  transition
"
                  >
                    PDF
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {(summary || chartData) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {summary && (
  <div className="bg-white rounded-xl shadow p-6 border border-slate-200">
    <h2 className="text-xl font-semibold mb-4 text-slate-700">
      Data Summary
    </h2>

    <div className="space-y-3">

      <div className="flex justify-between border-b pb-2">
        <span>Total Equipment</span>
        <span className="font-semibold">
          {summary.total_equipment}
        </span>
      </div>

      <div className="flex justify-between border-b pb-2">
        <span>Avg Flowrate</span>
        <span className="font-semibold">
          {summary.averages.flowrate}
        </span>
      </div>

      <div className="flex justify-between border-b pb-2">
        <span>Avg Pressure</span>
        <span className="font-semibold">
          {summary.averages.pressure}
        </span>
      </div>

      <div className="flex justify-between">
        <span>Avg Temperature</span>
        <span className="font-semibold">
          {summary.averages.temperature}
        </span>
      </div>

    </div>
    <button
      onClick={() => {
        const match = history.find(h => h.summary === summary)
        if (match) downloadPDF(match.id)
      }}
      className="
        mt-6 w-full py-2 rounded-lg font-semibold text-white
        bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800
        transition
      "
    >
      Download PDF Report
    </button>

  </div>
)}

          {chartData && (
            <div className="bg-white rounded-xl shadow p-6 border border-slate-200">
              <h2 className="text-xl font-semibold mb-4 text-slate-700">
                Equipment Distribution
              </h2>

              <div className="h-96">
                <Bar data={chartData} />
              </div>
            </div>
          )}

        </div>
      )}

    </div>
  </div>
);

}