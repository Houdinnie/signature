import Head from 'next/head'
import { useState, useEffect } from 'react'

export default function Home() {
  const [agents, setAgents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Fetch agents from the backend API
    fetch('/api/v1/agents/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then(data => {
        setAgents(data)
        setLoading(false)
      })
      .catch(error => {
        setError(error.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <Head>
          <title>Signature - AI Business Operating System</title>
          <meta name="description" content="Signature - Autonomous AI Business Operating System" />
        </Head>

        <div className="space-y-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900">
            Signature
          </h2>
          <p className="text-base text-gray-500">
            Autonomous AI Business Operating System
          </p>
          <div className="animate-spin rounded-full border-4 border-t-2 border-blue-500 w-16 h-16"></div>
          <p className="mt-4 text-sm text-gray-500">
            Loading your AI agents...
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <Head>
          <title>Error - Signature</title>
        </Head>

        <div className="space-y-6 text-center">
          <h2 className="text-2xl font-bold text-gray-900">
            Something went wrong
          </h2>
          <p className="text-base text-gray-500">
            {error}
          </p>
          <a href="/" className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded">
            Try again
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <Head>
        <title>Dashboard - Signature</title>
        <meta name="description" content="Signature Dashboard - Your AI Business Operating System" />
      </Head>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Signature Dashboard
        </h1>
        <p className="mt-2 text-lg text-gray-600">
          Your AI Business Operating System
        </p>

        {agents.length === 0 ? (
          <div className="mt-8 text-center text-gray-500">
            No agents configured yet. Check your backend setup.
          </div>
        ) : (
          <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {agents.map(agent => (
              <div key={agent.id} className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:px-6">
                  <h3 className="text-lg font-medium text-gray-900">
                    {agent.name}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {agent.agent_type}
                  </p>
                  {agent.description && (
                    <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                      {agent.description}
                    </p>
                  )}
                </div>
                <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${agent.status === 'active' ? 'bg-green-100 text-green-800' : 
                      agent.status === 'idle' ? 'bg-yellow-100 text-yellow-800' : 
                      agent.status === 'running' ? 'bg-blue-100 text-blue-800' : 
                      agent.status === 'failed' ? 'bg-red-100 text-red-800' : 
                      'bg-gray-100 text-gray-800'}`}>
                    {agent.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-10">
          <h2 className="sr-only">System Status</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg font-medium text-gray-900">
                  System Status
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  Operational
                </p>
              </div>
            </div>
            
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg font-medium text-gray-900">
                  Active Agents
                </h3>
                <p className="mt-1 text-3xl font-bold text-gray-900">
                  {agents.filter(a => a.status === 'active' || a.status === 'running').length}
                </p>
                <p className="mt-1 text-sm text-gray-500">
                  of {agents.length} agents
                </p>
              </div>
            </div>
            
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg font-medium text-gray-900">
                  Uptime
                </h3>
                <p className="mt-1 text-3xl font-bold text-gray-900">
                  99.9%
                </p>
                <p className="mt-1 text-sm text-gray-500">
                  Last 24 hours
                </p>
              </div>
            </div>
            
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg font-medium text-gray-900">
                  Tasks Processed
                </h3>
                <p className="mt-1 text-3xl font-bold text-gray-900">
                  0
                </p>
                <p className="mt-1 text-sm text-gray-500">
                  Today
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}