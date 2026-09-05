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

---

## 📂 Repository Structure

```text
CONTOUR/
├── cad/
│   ├── 22MI31013_KURRA SRINIVAS.dwg   # Master AutoCAD drawing file
│   ├── 22MI31013_KURRA SRINIVAS_.dwg  # Alternate CAD revision
│   ├── contour map for cad.dxf        # Intermediate DXF exchange export
│   ├── final contour map.dxf          # High-resolution final contour map
│   └── final map 2.dxf                # Secondary high-detail vector map
├── surfer/
│   ├── Plot1.srf                      # Surfer 2D contour layout
│   └── Plot2.srf                      # Surfer 3D surface model plot
├── data/
│   ├── raw/
│   │   ├── contours.kml               # Google Earth path / placemark capture
│   │   └── contour22mi10054.csv       # Raw TCX converter GPS stream
│   └── processed/
│       ├── csv excel file.csv         # Cleaned 136-point XYZ coordinate dataset
│       └── csv excel file.grd         # Golden Software Surfer grid matrix
├── docs/
│   ├── Softwares.pdf                  # Step-by-step workflow documentation
│   └── GridDataReport-csv excel file.rtf # Gridding statistics & variance report
├── archive/
│   └── 22MI31013_KURRA SRINIVAS.zip   # Packaged archive deliverable
├── .gitignore                         # AutoCAD, Surfer, and system file ignore rules
└── README.md                          # Project documentation
```

---

## 🚀 How to Use

1. **CAD Exploration**: Open `.dwg` or `.dxf` files located in [`cad/`](cad/) using Autodesk AutoCAD or any standard DWG viewer.
2. **Surface Plots**: Open `.srf` project files in [`surfer/`](surfer/) using Golden Software Surfer to interact with 3D elevation meshes and adjust contour intervals.
3. **Survey Points**: Access raw and processed XYZ data in [`data/`](data/) for custom GIS or Python spatial analysis (`numpy`, `scipy.spatial`, `matplotlib`).

---

## 👤 Author

- **Kurra Srinivas** (Roll No: `22MI31013`) — Department of Mining Engineering
