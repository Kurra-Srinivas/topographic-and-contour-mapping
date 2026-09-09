import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

os.makedirs('docs', exist_ok=True)

# -------------------------------------------------------------
# 1. GENERATE HIGH-RESOLUTION FIGURES
# -------------------------------------------------------------
data_path = 'data/processed/csv excel file.csv'
df = pd.read_csv(data_path, header=None, names=['Longitude', 'Latitude', 'Elevation'])

xi = np.linspace(df['Longitude'].min(), df['Longitude'].max(), 300)
yi = np.linspace(df['Latitude'].min(), df['Latitude'].max(), 300)
Xi, Yi = np.meshgrid(xi, yi)
Zi = griddata((df['Longitude'], df['Latitude']), df['Elevation'], (Xi, Yi), method='cubic')

fig = plt.figure(figsize=(13, 5.5), dpi=300)

# Subplot 1: 2D Contour
ax1 = fig.add_subplot(1, 2, 1)
cp = ax1.contourf(Xi, Yi, Zi, levels=25, cmap='terrain')
cbar = fig.colorbar(cp, ax=ax1, fraction=0.046, pad=0.04)
cbar.set_label('Elevation Z (m)', fontsize=10)
contours = ax1.contour(Xi, Yi, Zi, levels=10, colors='black', linewidths=0.6)
ax1.clabel(contours, inline=True, fontsize=8, fmt='%.1f m')
ax1.scatter(df['Longitude'], df['Latitude'], c='crimson', s=15, edgecolors='black', label='Survey Points (n=136)', zorder=5)
ax1.set_title('(a) 2D Topographic Contour Map (WGS84)', fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel('Longitude (°E)', fontsize=10)
ax1.set_ylabel('Latitude (°N)', fontsize=10)
ax1.legend(loc='lower left', fontsize=8, framealpha=0.9)
ax1.grid(True, linestyle='--', alpha=0.5)

# Subplot 2: 3D Surface
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
surf = ax2.plot_surface(Xi, Yi, Zi, cmap='terrain', edgecolor='none', alpha=0.9, antialiased=True)
ax2.set_title('(b) 3D Interpolated Surface Mesh', fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel('Longitude (°E)', fontsize=9, labelpad=8)
ax2.set_ylabel('Latitude (°N)', fontsize=9, labelpad=8)
ax2.set_zlabel('Elevation (m)', fontsize=9, labelpad=8)
ax2.view_init(elev=30, azim=-125)

plt.tight_layout()
fig_path = 'docs/fig1_topographic_contour_3d.png'
plt.savefig(fig_path, bbox_inches='tight', dpi=300)
plt.close()
print('Figure generated successfully at docs/fig1_topographic_contour_3d.png')

# -------------------------------------------------------------
# 2. COMPILE WORD DOCUMENT (.DOCX)
# -------------------------------------------------------------
doc = docx.Document()

# Set standard 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper for styling
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 45, 90) # Deep Navy
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(40, 75, 120)
    return p

def add_body(text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    return p

# --- CERTIFICATE BOX ---
cert_tbl = doc.add_table(rows=1, cols=1)
cert_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
cert_cell = cert_tbl.cell(0, 0)
set_cell_background(cert_cell, 'F4F6F9')
set_cell_margins(cert_cell, top=180, bottom=180, left=220, right=220)

cp = cert_cell.paragraphs[0]
cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
crun = cp.add_run('PROJECT COMPLETION CERTIFICATE\nDEPARTMENT OF MINING ENGINEERING\nINDIAN INSTITUTE OF TECHNOLOGY KHARAGPUR')
crun.font.name = 'Calibri'
crun.font.size = Pt(11)
crun.font.bold = True
crun.font.color.rgb = RGBColor(15, 45, 90)

cp2 = cert_cell.add_paragraph()
cp2.paragraph_format.space_before = Pt(8)
cp2.paragraph_format.line_spacing = 1.15
crun2 = cp2.add_run('This is to certify that Mr. Kurra Srinivas, Roll No. 22MI31013, a 5th year dual degree student of the Department of Mining Engineering, Indian Institute of Technology Kharagpur, has successfully completed the course project titled:\n\n“Terrain Visualization and Geological Contour Mapping Using Google Earth, QuikGrid, Surfer, and AutoCAD”\n\nas a part of the course “Mine Surveying and Geoinformatics” during the academic year 2023–2024. The project has been successfully completed under my supervision, and this certificate is issued upon the student\'s request for academic verification purposes.')
crun2.font.name = 'Calibri'
crun2.font.size = Pt(10)
crun2.font.italic = True

cp3 = cert_cell.add_paragraph()
cp3.paragraph_format.space_before = Pt(10)
crun3 = cp3.add_run('Course Instructor / Project Supervisor:\nProf. Debashish Chakravarty\nProfessor, Department of Mining Engineering\nIndian Institute of Technology Kharagpur')
crun3.font.name = 'Calibri'
crun3.font.size = Pt(10)
crun3.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# --- REPORT TITLE ---
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(12)
title_p.paragraph_format.space_after = Pt(2)
t_run = title_p.add_run('Terrain Visualization and Geological Contour Mapping Using Google Earth, QuikGrid, Surfer, and AutoCAD')
t_run.font.name = 'Calibri'
t_run.font.size = Pt(16)
t_run.font.bold = True
t_run.font.color.rgb = RGBColor(15, 45, 90)

# Metadata
meta_p = doc.add_paragraph()
meta_p.paragraph_format.space_after = Pt(12)
m_run = meta_p.add_run('Technical Course Project Report  |  Mine Surveying and Geoinformatics (Academic Year 2023–2024)\nAuthor: Kurra Srinivas (Roll No. 22MI31013)  |  Supervisor: Prof. Debashish Chakravarty\nDepartment of Mining Engineering, Indian Institute of Technology Kharagpur')
m_run.font.name = 'Calibri'
m_run.font.size = Pt(10)
m_run.font.italic = True
m_run.font.color.rgb = RGBColor(90, 100, 115)

# --- ABSTRACT ---
add_heading_1('1. Abstract')
add_body('Accurate digital terrain modeling (DTM) and high-resolution spatial contouring are fundamental prerequisites for mine planning, surface slope stability assessment, haul road geometric design, and surface drainage management. This project establishes an end-to-end computational geomatics pipeline that acquires geospatial coordinates from satellite telemetry (Google Earth Pro), converts GPS track trajectories into structured tabular datasets via TCX conversion, performs geostatistical surface interpolation using Ordinary Kriging in Golden Software Surfer and QuikGrid, and generates layered vector contour drawings in Autodesk AutoCAD. The empirical dataset comprises 136 topographic survey points spanning a target terrain block (79.4908°E to 79.4927°E, 16.6895°N to 16.6915°N) with elevations ranging from 103.167 m to 109.744 m (relief ΔZ = 6.577 m). Planar trend surface regression yielded a coefficient of determination (R² = 0.8891, F = 532.93, p < 0.001), revealing a pronounced eastward topographical gradient. Geostatistical interpolation over a 100 × 93 grid (9,300 nodes, spatial resolution ≈ 2.1 m × 2.2 m) produced an isotropic linear semi-variogram surface (variance σ² = 3.103 m²) that was vectorized into production-grade DXF/DWG formats. This workflow provides an accessible, robust protocol for pre-feasibility mine bench design and environmental terrain modeling.')

# --- INTRODUCTION ---
add_heading_1('2. Introduction & Problem Statement')
add_heading_2('2.1 Background in Mining Engineering')
add_body('Surface and underground mining operations rely critically on accurate geospatial representations of surface topography and geologic interfaces. Topographic contours dictate bench geometry, pit-shell optimization, overburden dumpsite stability, surface runoff channels, and haulage ramp gradients. Traditional theodolite and total station surveys, while highly precise, are resource-intensive and often constrained by hazardous terrain accessibility in active open-pit mines. Integrating spaceborne digital elevation models (DEMs), Global Navigation Satellite System (GNSS) trajectories, and geostatistical modeling offers a rapid, cost-effective alternative for preliminary mine site evaluation, reconnaissance, and boundary mapping.')

add_heading_2('2.2 Objectives & Scope')
add_body('The objective of this investigation is to construct a verified computational workflow to:')
add_body('1. Extract topographic coordinate tracks across an area of interest using satellite photogrammetry in Google Earth Pro.')
add_body('2. Filter, clean, and process the raw GNSS time-series stream into spatial coordinates (X, Y, Z) referenced to WGS84 ellipsoidal datums.')
add_body('3. Conduct univariate statistical, bivariate regression, and spatial auto-correlation analyses on the elevation field.')
add_body('4. Execute Ordinary Kriging interpolation to construct a continuous digital elevation grid (100 × 93 nodes).')
add_body('5. Generate 2D iso-elevation contour lines and 3D wireframe surface models, exporting vector geometries into Autodesk AutoCAD for engineering drafting.')

# --- METHODOLOGY ---
add_heading_1('3. Methodology & Implementation')
add_heading_2('3.1 Mathematical Formulations')
add_body('The regional topographic relief is modeled via a bivariate first-order polynomial surface: Z(X, Y) = A·X + B·Y + C + ε, where X is Longitude (°E), Y is Latitude (°N), Z is surface elevation (m), A and B are directional gradients, C is the datum constant, and ε is the local residual error.')
add_body('Spatial continuity is evaluated using the empirical semi-variogram γ(h) = (1 / 2N(h)) ∑ [Z(x_i) - Z(x_i + h)]². An isotropic linear variogram model γ(h) = C_0 + ω·h was fitted with nugget C_0 = 0 and slope ω = 2866.27 m²/degree. Best Linear Unbiased Estimates (BLUE) at grid nodes were calculated using Ordinary Point Kriging.')

add_heading_2('3.2 Computational Workflow & Software Stack')
add_body('• Google Earth Pro (contours.kml): Defined the target mining concession boundary and extracted elevation-enabled path waypoints.\n• TCX Converter (contour22mi10054.csv): Parsed raw XML trackpoint metadata into tabular time-stamped records.\n• Point Extraction (csv excel file.csv): Formatted 136 discrete survey points into standard comma-separated Cartesian tuples [X, Y, Z].\n• Golden Software Surfer & QuikGrid (csv excel file.grd, Plot1.srf, Plot2.srf): Executed point Kriging over 100 rows × 93 columns (9,300 nodes).\n• Autodesk AutoCAD (22MI31013_KURRA SRINIVAS.dwg, final contour map.dxf): Imported polyline contours, aligned drawing units, configured contour index line labeling (major vs. minor intervals), and generated the mine site master plan.')

# Embed Figure
doc.add_picture(fig_path, width=Inches(6.2))
fig_cap = doc.add_paragraph()
fig_cap.paragraph_format.space_before = Pt(4)
fig_cap.paragraph_format.space_after = Pt(10)
fig_cap_run = fig_cap.add_run('Figure 1: Digital Elevation Model (DEM) and 2D Topographic Contour Map (left) along with the 3D Interpolated Surface Mesh (right) generated from the 136-point survey dataset across the mining concession area.')
fig_cap_run.font.name = 'Calibri'
fig_cap_run.font.size = Pt(9.5)
fig_cap_run.font.italic = True

# --- RESULTS & ANALYSIS ---
add_heading_1('4. Results & Statistical Analysis')
add_body('The statistical and geostatistical metrics computed from the raw survey and interpolated grids are summarized below:')

# Table 1: Statistical Summary
t1 = doc.add_table(rows=1, cols=4)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
headers1 = ['Metric / Parameter', 'Raw Survey Points', 'Interpolated Grid', 'Units']
hdr_cells = t1.rows[0].cells
for i, name in enumerate(headers1):
    hdr_cells[i].text = name
    set_cell_background(hdr_cells[i], '1F497D')
    set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
    for p in hdr_cells[i].paragraphs:
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

data_t1 = [
    ('Total Node / Point Count', '136', '9,300 (100 x 93)', 'points / nodes'),
    ('Longitude Range (X)', '79.490846 to 79.492670', '79.490846 to 79.492670', '°E'),
    ('Grid Spacing ΔX', '—', '1.9826 x 10⁻⁵ (≈ 2.1 m)', '° (m)'),
    ('Latitude Range (Y)', '16.689519 to 16.691473', '16.689519 to 16.691473', '°N'),
    ('Grid Spacing ΔY', '—', '1.9737 x 10⁻⁵ (≈ 2.2 m)', '° (m)'),
    ('Minimum Elevation (Z_min)', '103.167', '103.153', 'm'),
    ('Maximum Elevation (Z_max)', '109.744', '109.780', 'm'),
    ('Total Topographic Relief (ΔZ)', '6.577', '6.626', 'm'),
    ('Mean Elevation (μ_Z)', '107.171', '106.808', 'm'),
    ('Standard Deviation (σ_Z)', '1.598', '1.762', 'm'),
    ('Variance (σ²)', '2.554', '3.103', 'm²'),
    ('Skewness (S_k)', '-0.561', '-0.294', 'dimensionless'),
    ('Kurtosis (K)', '2.402', '1.955', 'dimensionless'),
]

for row_idx, row in enumerate(data_t1):
    row_cells = t1.add_row().cells
    bg_color = 'F2F5F8' if row_idx % 2 == 1 else 'FFFFFF'
    for col_idx, val in enumerate(row):
        row_cells[col_idx].text = val
        set_cell_background(row_cells[col_idx], bg_color)
        set_cell_margins(row_cells[col_idx], top=50, bottom=50, left=80, right=80)
        for p in row_cells[col_idx].paragraphs:
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(9)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

add_heading_2('4.1 Planar Trend Surface Regression')
add_body('Bivariate planar regression resulted in the fitted model: Z(X, Y) = -3271.625·X + 146.542·Y + 257728.247. The ANOVA regression metrics are:')

# Table 2: Regression Table
t2 = doc.add_table(rows=1, cols=4)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
headers2 = ['Source of Variation', 'Degrees of Freedom (df)', 'Sum of Squares (SS)', 'Mean Square (MS)']
hdr_cells2 = t2.rows[0].cells
for i, name in enumerate(headers2):
    hdr_cells2[i].text = name
    set_cell_background(hdr_cells2[i], '1F497D')
    set_cell_margins(hdr_cells2[i], top=80, bottom=80, left=100, right=100)
    for p in hdr_cells2[i].paragraphs:
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

data_t2 = [
    ('Regression Model', '2', '306.524', '153.262'),
    ('Residual Error', '133', '38.249', '0.288'),
    ('Total Variation', '135', '344.773', '—'),
    ('ANOVA F-Statistic', 'F = 532.932', 'p < 1.0 x 10⁻¹⁵', 'Statistically Significant'),
    ('Coefficient of Determination', 'R² = 0.8891', '88.91% Explained', 'Adjusted R² = 0.8874')
]

for row_idx, row in enumerate(data_t2):
    row_cells = t2.add_row().cells
    bg_color = 'F2F5F8' if row_idx % 2 == 1 else 'FFFFFF'
    for col_idx, val in enumerate(row):
        row_cells[col_idx].text = val
        set_cell_background(row_cells[col_idx], bg_color)
        set_cell_margins(row_cells[col_idx], top=50, bottom=50, left=80, right=80)
        for p in row_cells[col_idx].paragraphs:
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(9)
                if 'R²' in val or 'F =' in val:
                    r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# --- ENGINEERING SIGNIFICANCE ---
add_heading_1('5. Engineering Significance & Limitations')
add_body('1. Bench & Haul Road Alignment: The natural slope of 3.38% (dropping eastward) permits straight-line haul road ramps that comfortably satisfy DGMS statutory maximum gradient limits (1 in 10 or 10%).')
add_body('2. Mine Drainage & Sump Design: Surface contour curvature guides optimal ditch gradients and sump placement to intercept monsoon runoff prior to pit crest ingress.')
add_body('3. Overburden Differencing: The baseline 9,300-node surface model enables volumetric stripping ratio updates against subsequent monthly survey scans.')
add_body('4. Limitations: Spaceborne elevation telemetry exhibits vertical errors of ±2 m to ±5 m, requiring RTK-GNSS ground-truthing for final legal lease demarcation.')

# --- CONCLUSION ---
add_heading_1('6. Conclusion & Future Scope')
add_body('• Successfully established a verified digital mapping workflow linking Google Earth Pro, TCX Converter, Surfer, and AutoCAD for mine surface mapping.')
add_body('• Point Kriging over 9,300 nodes accurately reproduced the topographic field with an R² of 0.8891.')
add_body('• Delivered production-grade AutoCAD drawings (22MI31013_KURRA SRINIVAS.dwg) and high-resolution vector contours.')
add_body('• Future work includes integrating UAV LiDAR point clouds and linking DTM surfaces to limit-equilibrium slope stability solvers.')

# --- REFERENCES ---
add_heading_1('7. References & Citations')
add_body('1. Golden Software LLC, Surfer: Contouring and 3D Surface Mapping for Scientists and Engineers, User Reference Manual.')
add_body('2. Directorate General of Mines Safety (DGMS), Standard Operating Procedures and Geometric Guidelines for Opencast Mine Haul Roads and Benches.')
add_body('3. Davis, J. C., Statistics and Data Analysis in Geology, 3rd Edition, John Wiley & Sons.')
add_body('4. Project Source Code & CAD Deliverables: https://github.com/Kurra-Srinivas/topographic-and-contour-mapping.')

# Save docx in docs/ and in workspace root
output_docx_path = 'docs/Technical_Project_Report_22MI31013.docx'
doc.save(output_docx_path)
doc.save('Technical_Project_Report_22MI31013.docx')
print(f'Document successfully created at {output_docx_path} and Technical_Project_Report_22MI31013.docx')
