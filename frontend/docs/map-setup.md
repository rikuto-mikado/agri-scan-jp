# Leaflet Map Integration Guide

This guide explains how to set up, integrate, and configure geographical maps in this project using **Leaflet** and **React Leaflet** within a React, Vite, and TypeScript environment.

---

## 1. Installation

To reproduce the map setup, you need to install the core Leaflet library, its React wrapper, and the TypeScript type definitions:

```bash
# Install core Leaflet and React Leaflet wrapper
npm install leaflet react-leaflet

# Install TypeScript type definitions as development dependencies
npm install -D @types/leaflet
```

### Version Configurations (Reference)
As configured in `package.json`:
* `leaflet`: `^1.9.4`
* `react-leaflet`: `^5.0.0`
* `@types/leaflet`: `^1.9.21`

---

## 2. Vite Marker Icon Workaround (Critical)

In React applications built with modern bundlers like Vite, Leaflet's default marker icons often fail to load. This happens because Leaflet dynamically detects asset URLs relative to the library directory, which gets obfuscated during Vite's bundling process.

To resolve this, you must explicitly import the marker assets and merge them into Leaflet's default icon options:

```typescript
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

// Delete the internal method to fetch default icon URLs
delete (L.Icon.Default.prototype as any)._getIconUrl;

// Merge Vite-friendly resolved URLs into Leaflet configuration
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});
```

---

## 3. Styling & Layout Requirements

Leaflet containers require explicit height and width parameters to render correctly. Without these, the map container collapses to `0px` height.

1. **Import CSS Styles**: Import Leaflet's standard CSS in your entry file or component (e.g., `App.tsx` or `main.tsx`):
   ```typescript
   import "leaflet/dist/leaflet.css";
   ```
2. **Define Container Size**: Apply layout classes to `MapContainer`. If using Tailwind CSS, ensure classes like `h-full w-full` (or explicit heights like `h-[500px]`) are set:
   ```tsx
   <MapContainer className="h-full w-full" ...>
     {/* Layers & Markers */}
   </MapContainer>
   ```

---

## 4. Map Component Structure

Here is a standard integration template demonstrating rendering a dark-themed map, displaying a marker with a popup, and handling map click events:

```tsx
import { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Vite marker icon workaround
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});

// Component to handle interactive map events (e.g. clicking to pick coordinates)
function MapEvents({ onClick }: { onClick: (lat: number, lng: number) => void }) {
  useMapEvents({
    click(e) {
      onClick(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

export default function MapComponent() {
  const [position, setPosition] = useState<[number, number]>([35.6895, 139.6917]); // Default: Tokyo

  return (
    <div className="h-screen w-full relative">
      <MapContainer
        center={position}
        zoom={6}
        scrollWheelZoom={true}
        className="h-full w-full"
      >
        {/* CartoDB Dark Matter tiles (Sleek dark theme) */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />

        {/* Marker showing the selected position */}
        <Marker position={position}>
          <Popup>Selected Location</Popup>
        </Marker>

        {/* Listen for user click events to update selected coordinates */}
        <MapEvents onClick={(lat, lng) => setPosition([lat, lng])} />
      </MapContainer>
    </div>
  );
}
```

### Tile Providers
In this codebase, we use **CartoDB Dark Matter** tiles to match the application's modern dark theme UI:
* URL: `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`
* For light themes, standard OpenStreetMap can be used:
  * URL: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
