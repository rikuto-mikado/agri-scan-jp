function App() {
  return (
    <div className="flex flex-col h-screen w-full bg-slate-50">
      {/* Header */}
      <header className="h-16 bg-white border-b flex items-center px-6 shadow-sm z-10">
        <h1 className="text-xl font-bold text-green-700">Environmental score</h1>
      </header>

      {/* Main Contents */}
      <div className="flex flex-1 overflow-hidden">
        <aside className="w-96 bg-white border-r p-6 overflow-y-auto shadow-sm z-10">

        </aside>
      </div>
    </div>
  )
}

export default App