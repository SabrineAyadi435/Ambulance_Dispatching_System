# Ambulance_Dispatching_System
## 📋 Project Overview
This Python implementation solves the **ambulance dispatch optimization problem** using a **Reverse Single-Source Dijkstra algorithm** with **Analytic Hierarchy Process (AHP)** weights. The algorithm finds the optimal hospital to dispatch an ambulance from to an emergency location, considering multiple criteria: travel time, IT risk factors, and operational cost.

## 🧮 Mathematical Foundation

### Problem Formulation
- **Original Problem**: Find hospital h* ∈ H that minimizes the composite cost to emergency site d
- **Graph Representation**: G = (V, E) where vertices are locations and edges have multi-attribute weights
- **Mathematical Transformation**: Run Dijkstra from destination d in reversed graph G' = (V, E')
- **Solution**: h* = argmin_{h∈H} λ_h where λ_h is the shortest path distance in G'

### Multi-Criteria Decision Making
The algorithm uses AHP weights to combine three primary factors:
- **Travel Time (61.9%)**: w_T = 0.619
- **IT Risk (28.4%)**: w_R = 0.284
- **Cost (9.6%)**: w_C = 0.096

IT Risk is further decomposed into:
- Network Reliability (62.3%): v_net = 0.623
- GPS Accuracy (23.9%): v_gps = 0.239  
- Data Integrity (13.7%): v_data = 0.137

## 🏗️ Algorithm Architecture

### Core Components
1. **Graph Reversal**: Creates G' by reversing all edges from original graph G
2. **Reverse Dijkstra**: Runs single-source shortest path from emergency site in G'
3. **Path Reconstruction**: Converts paths back to original graph direction
4. **Multi-criteria Weighting**: Computes composite edge weights using AHP

### Key Features
- ✅ **Mathematically exact implementation**
- ✅ **Correct path direction handling** (Hospital → Emergency Site)
- ✅ **Comprehensive metric calculation**
- ✅ **Visual step-by-step execution**
- ✅ **All hospital comparison**


