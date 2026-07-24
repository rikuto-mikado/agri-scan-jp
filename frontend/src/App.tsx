import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
// import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"

import { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css"
import L from "leaflet"

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png"
import markerIcon from "leaflet/dist/images/marker-icon.png"
import markerShadow from "leaflet/dist/images/marker-shadow.png"

delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
})

function MapEvents({ onClick }: { onClick: (lat: number, lng: number) => void }) {
  useMapEvents({
    click(e) {
      onClick(e.latlng.lat, e.latlng.lng)
    }
  })
  return null
}

interface CropeScore {
  name: string;
  score: number;
}

type AnalysisResult = Record<string, CropeScore>;

function App() {

  const [position, setPosition] = useState<[number, number]>([35.6895, 139.6917])
  const [isLoading, setIsLoading] = useState(false)

  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)

  const handleGetResults = async () => {
    setIsLoading(true)
    try {
      const res = await fetch(`http://localhost:8000/api/score/?lat=${position[0]}$lng=${position[1]}`)
      const data = await res.json()
      setAnalysisResult(data)
    } catch (error) {
      console.log('fall to get data', error)
    } finally {
      setIsLoading(false)
    }
  }

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
            {/* <p className="p-4 border rounded-md bg-slate-50 text-slate-500 text-sm">Select an analysis to view its details.</p> */}
          </div>

          {/* <Tabs defaultValue="overview" className="w-full mb-6">

            <TabsList className="grid w-full grid-cols-2 gap-2 mt-6">
              <TabsTrigger value="overview" className="bg-indigo-500 hover:bg-fuchsia-500">Overview</TabsTrigger>
              <TabsTrigger value="simulation" className="bg-indigo-500 hover:bg-fuchsia-500">Simulation</TabsTrigger>
            </TabsList>

          </Tabs> */}

          <div className="flex flex-col gap-4">
            <Card className="flex-1">

              <CardHeader className="pb-2">
                <CardTitle className="text-base">Selected Location</CardTitle>
              </CardHeader>

              <CardContent className="flex flex-col justify-between h-full gap-2">
                <div>
                  <p className="text-sm text-slate-500">
                    Latitude: {position[0].toFixed(4)}, Longitude: {position[1].toFixed(4)}
                  </p>
                </div>
                {/* <Button className="w-full mt-2">Get Results</Button> */}
                <Button
                  className="w-full mt-2"
                  onClick={handleGetResults}
                  disabled={isLoading}
                >
                  {isLoading ? "Fetching..." : "Get Results"}
                </Button>
              </CardContent>

            </Card>

            <Card className="flex-1 ">

              <CardHeader className="pb-2">
                <CardTitle className="text-base">Analysis Details</CardTitle>
              </CardHeader>
              {/* <CardContent className="h-full flex items-center justify-center">
                <p className="w-fill p-4 border border-dashed rounded-md bg-slate-50 text-slate-500 text-sm text-center">
                  Click on the map to get the results.
                </p>
              </CardContent> */}
              <CardContent className="h-full flex item-center justify-center p-6">
                {isLoading ? (
                  <p className="text-slate-500">Loading data...</p>
                ) : analysisResult ? (
                  // <div className="w-full h-full text-sm text-slate-700">
                  //   <p className="font-bold mb-2">Total Score: {analysisResult.score}</p>
                  //   <pre className="bg-slate-100 p-2 rounded overflow-auto max-h-32">
                  //     {JSON.stringify(analysisResult, null, 2)}
                  //   </pre>
                  // </div>
                  <div className="w-full h-full text-sm text-slate-700">
                    <div className="flex flex-col gap-2 mb-4">
                      {Object.entries(analysisResult).map(([cropId, item]) => (
                        <div key={cropId} className="flex justify-between border-b pb-1">
                          <span>{item.name}</span>
                          <span className="font-semibold text-indigo-600">{item.score}</span>
                        </div>
                      ))}
                    </div>
                    <pre className="bg-slate-100 p-2 rounded overflow-auto max-h-32">
                      {JSON.stringify(analysisResult, null, 2)}
                    </pre>
                  </div>
                ) : (
                  <p className="w-full p-4 border border-dashed rounded-md bg-slate-50 text-slate500 text-sm text-center">
                    Click on the map and press get result
                  </p>
                )}
              </CardContent>

            </Card>

          </div>

        </aside>

        {/* Right side content */}
        <main className="flex-1 relative z-0">
          <MapContainer
            center={position}
            zoom={6}
            scrollWheelZoom={true}
            className="h-full w-full"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            />
            <Marker position={position}>
          <Popup>Selected Location</Popup>
        </Marker>
        <MapEvents onClick={(lat, lng) => setPosition([lat, lng])} />
          </MapContainer>
        </main>
      </div>
    </div>
  )
}

export default App