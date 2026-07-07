import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"

function App() {
  return (
    <div className="flex flex-col h-screen w-full bg-background text-foreground">
      {/* Header */}
      <header className="h-16 bg-card flex items-center px-6 shadow-sm z-10">
        <h1 className="text-xl font-bold text-indigo-400">Environmental score</h1>
      </header>

      {/* Main Contents */}
      <div className="flex flex-1 overflow-hidden">
        
        <aside className="w-96 bg-card border-r border-border p-6 overflow-y-auto shadow-sm z-10">

          <div>
            <h2 className="text-lg font-semibold mb-4">Potential Environmental Analyses</h2>
            <p className="p-4 border rounded-md bg-slate-50 text-slate-500 text-sm">Select an analysis to view its details.</p>
          </div>

          <Tabs defaultValue="overview" className="w-full mb-6">

            <TabsList className="grid w-full grid-cols-2 gap-2 mt-6">
              <TabsTrigger value="overview" className="bg-indigo-500 hover:bg-fuchsia-500">Overview</TabsTrigger>
              <TabsTrigger value="simulation" className="bg-indigo-500 hover:bg-fuchsia-500">Simulation</TabsTrigger>
            </TabsList>

          </Tabs>

          <div className="flex flex-col gap-4">
            <Card className="flex-1">

              <CardHeader className="pb-2">
                <CardTitle className="text-base">Selected Location</CardTitle>
              </CardHeader>

              <CardContent className="flex flex-col justify-between h-full gap-2">
                <div>
                  <p className="text-sm text-slate-500">Latitude: 35.6895, Longitude: 139.6917</p>
                </div>
                <Button className="w-full mt-2">Get Results</Button>
              </CardContent>

            </Card>

            <Card className="flex-1 ">

              <CardHeader className="pb-2">
                <CardTitle className="text-base">Analysis Details</CardTitle>
              </CardHeader>
              <CardContent className="h-full flex items-center justify-center">
                <p className="w-fill p-4 border border-dashed rounded-md bg-slate-50 text-slate-500 text-sm text-center">
                  Click on the map to get the results.
                </p>
              </CardContent>

            </Card>

          </div>

        </aside>

        {/* Right side content */}
        <main className="flex-1 bg-slate-200 flex items-center justify-center relative">
          <p className="text-slate-400 font-medium">Select an analysis to view details</p>
        </main>

      </div>
    </div>
  )
}

export default App