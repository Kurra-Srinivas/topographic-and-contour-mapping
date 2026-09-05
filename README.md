# Topographic & Contour Mapping for Mining Engineering

A comprehensive geospatial and mine surveying workflow for topographic elevation acquisition, surface interpolation, 2D/3D contour modeling, and AutoCAD engineering drafting.

---

## 📌 Project Overview

This project implements a digital surveying pipeline to translate raw geographic coordinates into high-precision topographic contour maps used in mine planning, slope stability analysis, and surface excavation design.

```text
┌─────────────────┐      ┌───────────────┐      ┌─────────────────────────┐      ┌─────────────────┐
│ Google Earth Pro│ ───► │ TCX Converter │ ───► │ Golden Software Surfer  │ ───► │  AutoCAD Civil  │
│   (.kml data)   │      │  (.csv table) │      │  (Gridding & .srf plots)│      │  (.dxf / .dwg)  │
└─────────────────┘      └───────────────┘      └─────────────────────────┘      └─────────────────┘
```

---

## 🛠️ Software Toolchain

| Stage | Software | Output Format | Purpose |
| :--- | :--- | :--- | :--- |
| **1. Data Capture** | Google Earth Pro | `.kml` | Define study area boundary & topographic waypoints |
| **2. Coordinate Conversion** | TCX Converter | `.csv` | Extract latitude, longitude, and elevation ($X, Y, Z$) |
| **3. Surface Gridding** | QuikGrid / Surfer | `.grd`, `.rtf` | Kriging/linear interpolation of survey elevation grid |
| **4. 2D/3D Visualization** | Golden Software Surfer | `.srf`, `.dxf` | Contour interval rendering and surface plot visualization |
| **5. Engineering Drafting** | Autodesk AutoCAD | `.dwg`, `.dxf` | Final layered contour maps with scale, grids, and annotations |

## 🚀 How to Use

1. **CAD Exploration**: Open `.dwg` or `.dxf` files located in [`cad/`](cad/) using Autodesk AutoCAD or any standard DWG viewer.
2. **Surface Plots**: Open `.srf` project files in [`surfer/`](surfer/) using Golden Software Surfer to interact with 3D elevation meshes and adjust contour intervals.
3. **Survey Points**: Access raw and processed XYZ data in [`data/`](data/) for custom GIS or Python spatial analysis (`numpy`, `scipy.spatial`, `matplotlib`).

---
