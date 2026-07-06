import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

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
          <div>
            <h2 className="text-lg font-semibold mb-4 text-slate-800">Potential Environmental Analyses</h2>
            <p className="p-4 border rounded-md bg-slate-50 text-slate-500 text-sm">
              Select an analysis to view its details.
            </p>
          </div>

          <Tabs defaultValue="overview" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="simulation">Simulation</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="mt-4 flex flex-col gap-4">

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">Selected Location</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-sm font-medium text-slate-700">Sapporo, Hokkaido, Japan</p>
                    <p className="text-sm text-slate-500">Latitude: 43.0621, Longitude: 141.3544</p>
                  <Button className="w-full">Get results</Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">Analysis Details</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="p-4 border border-dashed rounded-md bg-slate-50 text-slate-500 text-sm text-center">
                    Click on the map to get the results
                  </p>
                </CardContent>
              </Card>

            </TabsContent>

            <TabsContent value="simulation" className="mt-4">
              <Card>
                <CardContent className="pt-6">
                  <p className="text-sm text-slate-500 mb-4">
                    Let's simulate the environmental impact of the selected location
                  </p>
                  <Button className="w-full">Run simulation</Button>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
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