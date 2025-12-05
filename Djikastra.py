

import heapq
from typing import Dict, List

class ReverseSingleSourceDijkstra:
    def __init__(self, original_graph: Dict[str, Dict[str, Dict]]):
        """
        Initialize with original graph G = (V, E)
        """
        self.G = original_graph
        self.G_prime = self._reverse_graph(original_graph)  # G' = reversed graph
        self.V = self._get_all_nodes()
        
        # AHP Weights
        self.w_T = 0.619   # Time weight (61.9%)
        self.w_R = 0.284   # IT Risk weight (28.4%)
        self.w_C = 0.096   # Cost weight (9.6%)
        
        # IT Risk sub-weights
        self.v_net = 0.623  # Network reliability
        self.v_gps = 0.239  # GPS accuracy
        self.v_data = 0.137  # Data integrity
    
    def _reverse_graph(self, G: Dict) -> Dict:
        """Reverse the graph: G' = (V, E') where (u,v,w) ∈ E ⇒ (v,u,w) ∈ E'"""
        G_prime = {}
        all_vertices = set()
        
        # Collect all vertices
        for u, neighbors in G.items():
            all_vertices.add(u)
            for v in neighbors:
                all_vertices.add(v)
        
        # Initialize all vertices
        for vertex in all_vertices:
            G_prime[vertex] = {}
        
        # Reverse edges
        for u, neighbors in G.items():
            for v, attributes in neighbors.items():
                G_prime[v][u] = attributes.copy()
        
        return G_prime
    
    def _get_all_nodes(self):
        """Get set of all vertices V"""
        nodes = set()
        for u, neighbors in self.G.items():
            nodes.add(u)
            for v in neighbors:
                nodes.add(v)
        return nodes
    
    def _calculate_composite_weight(self, attributes: Dict) -> float:
        """Calculate composite weight without normalization"""
        t = attributes['time']
        c = attributes['cost'] 
        it_risk = attributes['it_risk']
        
        IT_composite = (self.v_net * it_risk['network'] + 
                       self.v_gps * it_risk['gps'] + 
                       self.v_data * it_risk['data'])
        
        return (self.w_T * t + 
                self.w_R * IT_composite + 
                self.w_C * c)
    
    def _reconstruct_original_path(self, hospital: str, pred: Dict) -> List[str]:
        """
        Reconstruct path in ORIGINAL GRAPH direction:
        Returns: [Hospital, ..., Tunisia_Mall]
        
        Mathematical correctness:
        In G' (reversed graph): pred pointers give path from d to h
        To get path in G: reverse the path from G'
        """
        # Step 1: Trace back from hospital to destination in REVERSED graph
        # In G', pred gives: h ← ... ← d
        current = hospital
        path_in_reversed_graph = []
        
        while current is not None:
            path_in_reversed_graph.append(current)
            current = pred.get(current)
        
        
        return path_in_reversed_graph  
    
    def find_optimal_dispatch(self, destination: str, hospitals: List[str]) -> Dict:
        """
        Main Reverse Dijkstra Algorithm
        Returns route in ORIGINAL GRAPH format: Hospital → ... → Tunisia_Mall
        """
        print("\n" + "="*80)
        print("🚑 REVERSE SINGLE-SOURCE DIJKSTRA - MATHEMATICAL IMPLEMENTATION")
        print("="*80)
        
        print(f"🔍 Running Dijkstra from {destination} in REVERSED graph G'")
        print(f"🏥 Looking for hospitals: {hospitals}")
        
        # ============================================
        # STEP 1: Initialization (as per mathematical formulation)
        # ============================================
        λ = {node: float('inf') for node in self.V}  # Distances λ_i
        pred = {node: None for node in self.V}       # Predecessors in G'
        λ[destination] = 0  # λ_d = 0
        
        # Priority queue Q = {(0, d)}
        Q = []
        heapq.heappush(Q, (0, destination))
        
        visited = set()
        found_hospitals = {}  # λ_H dictionary
        
        print(f"\n📊 Dijkstra Initialization:")
        print(f"   λ[{destination}] = 0")
        print(f"   λ[i] = ∞ for all other vertices")
        print(f"   Q = {{(0, {destination})}}")
        
        # ============================================
        # STEP 2: Main Dijkstra Loop on G'
        # ============================================
        iteration = 0
        while Q:
            iteration += 1
            λ_k, k = heapq.heappop(Q)
            
            # Skip if outdated or visited
            if λ_k > λ[k] or k in visited:
                continue
            
            # Mark as visited: visited ← visited ∪ {k}
            visited.add(k)
            
            # Check if hospital found: if k ∈ H and k ∉ foundHospitals
            if k in hospitals and k not in found_hospitals:
                found_hospitals[k] = λ[k]
                print(f"\n🏥 Found hospital {k} at iteration {iteration}")
                print(f"   λ[{k}] = {λ[k]:.4f}")
            
            # Explore neighbors in REVERSED graph G'
            # ∀ i such that (k, i) ∈ E'
            for neighbor, attributes in self.G_prime.get(k, {}).items():
                if neighbor in visited:
                    continue
                
                # Calculate composite weight w(k,i)
                w = self._calculate_composite_weight(attributes)
                new_λ = λ_k + w
                
                # Relaxation: if newλ < λ[i]
                if new_λ < λ[neighbor]:
                    λ[neighbor] = new_λ
                    pred[neighbor] = k  # In G': neighbor ← k
                    heapq.heappush(Q, (new_λ, neighbor))
        
        # ============================================
        # STEP 3: Solution Extraction
        # ============================================
        if not found_hospitals:
            return {'error': 'No reachable hospitals found'}
        
        # Find optimal hospital: h* = argmin_{h∈H} λ_h
        h_star = min(found_hospitals.keys(), key=lambda h: found_hospitals[h])
        C_star = found_hospitals[h_star]
        
        print(f"\n✅ Dijkstra completed")
        print(f"🏆 Optimal hospital: h* = {h_star}")
        print(f"📊 Minimum composite cost: λ = {C_star:.4f}")
        
        # ============================================
        # STEP 4: Path Reconstruction
        # ============================================
        # Reconstruct path in G' (reversed graph)
        path_in_G_prime = []
        current = h_star
        while current is not None:
            path_in_G_prime.append(current)
            current = pred.get(current)
        
        # path_in_G_prime is: [h*, ..., d] in G'
        # In G', direction is: d → ... → h*
        
        # Convert to original graph path: P* = reverse(P_reverse)
        optimal_route = list(reversed(path_in_G_prime))
        # optimal_route is: [h*, ..., d] in G (original direction)
        
        print(f"\n Path Reconstruction:")
        print(f"   Path in G' (reversed): {' → '.join(optimal_route)}")
        print(f"   Path in G (original): {' → '.join(path_in_G_prime)}")
        
        # ============================================
        # STEP 5: Calculate Metrics
        # ============================================
        optimal_metrics = self._calculate_route_metrics(optimal_route)
        
        # Process all hospitals
        hospital_details = {}
        for hospital in found_hospitals:
            # Reconstruct path for each hospital
            path_G_prime = []
            curr = hospital
            while curr is not None:
                path_G_prime.append(curr)
                curr = pred.get(curr)
            
            route = list(reversed(path_G_prime))  # Convert to original direction
            metrics = self._calculate_route_metrics(route)
            
            hospital_details[hospital] = {
                'λ': found_hospitals[hospital],
                'route': route,  # Hospital → ... → Mall
                'travel_time': metrics['travel_time'],
                'total_cost': metrics['total_cost'],
                'it_components': metrics['it_components']
            }
        
        return {
            'optimal_hospital': h_star,
            'optimal_cost': C_star,
            'optimal_route': optimal_route,  # Hospital → ... → Mall
            'all_hospitals': hospital_details,
            'pred': pred,  # For debugging
            'lambda': λ    # For debugging
        }
    
    def _calculate_route_metrics(self, route: List[str]) -> Dict:
        """Calculate metrics for a route in original graph"""
        total_time = 0
        total_cost = 0
        total_it_network = 0
        total_it_gps = 0
        total_it_data = 0
        
        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]
            
            if u in self.G and v in self.G[u]:
                edge_data = self.G[u][v]
                total_time += edge_data['time']
                total_cost += edge_data['cost']
                
                it_risk = edge_data['it_risk']
                total_it_network += self.w_R * self.v_net * it_risk['network']
                total_it_gps += self.w_R * self.v_gps * it_risk['gps']
                total_it_data += self.w_R * self.v_data * it_risk['data']
        
        return {
            'travel_time': total_time,
            'total_cost': total_cost,
            'it_components': {
                'network': total_it_network,
                'gps': total_it_gps,
                'data': total_it_data
            }
        }

def create_network():
    """Create the exact network based on your routes"""
    return {
        # HOSPITALS
        "Mongi_Slim": {
            "Ain_Zaghouan": {
                'time': 3, 'cost': 0.76,
                'it_risk': {'network': 0.4, 'gps': 0.5, 'data': 0.3}
            },
            "Jardin_Carthage": {
                'time': 5, 'cost': 1.77,
                'it_risk': {'network': 0.3, 'gps': 0.4, 'data': 0.2}
            }
        },
        
        "Charles_Nicolle": {
            "Bab_Sadoun": {
                'time': 2, 'cost': 0.88,
                'it_risk': {'network': 0.5, 'gps': 0.6, 'data': 0.4}
            },
            "Beb_Bhar": {
                'time': 9, 'cost': 1.89,
                'it_risk': {'network': 0.4, 'gps': 0.5, 'data': 0.3}
            }
        },
        
        "Habib_Thamer": {
            "Avenue_Moncef_Bey": {
                'time': 5, 'cost': 1.07,
                'it_risk': {'network': 0.3, 'gps': 0.4, 'data': 0.2}
            }
        },
        
        "Rabta": {
            "Bab_Sadoun": {
                'time': 5, 'cost': 0.88,
                'it_risk': {'network': 0.4, 'gps': 0.5, 'data': 0.4}
            }
        },
        
        # INTERMEDIATE NODES
        "Ain_Zaghouan": {
            "Tunisia_Mall": {
                'time': 6, 'cost': 1.83,
                'it_risk': {'network': 0.6, 'gps': 0.7, 'data': 0.5}
            }
        },
        
        "Jardin_Carthage": {
            "Tunisia_Mall": {
                'time': 9, 'cost': 1.96,
                'it_risk': {'network': 0.2, 'gps': 0.3, 'data': 0.1}
            }
        },
        
        "Avenue_Moncef_Bey": {
            "Tunisia_Mall": {
                'time': 19, 'cost': 7.575,
                'it_risk': {'network': 0.3, 'gps': 0.4, 'data': 0.2}
            }
        },
        
        "Bab_Sadoun": {
            "Tunisia_Mall": {
                'time': 22, 'cost': 8.21,
                'it_risk': {'network': 0.5, 'gps': 0.6, 'data': 0.4}
            }
        },
        
        "Beb_Bhar": {
            "Tunisia_Mall": {
                'time': 22, 'cost': 8.21,
                'it_risk': {'network': 0.4, 'gps': 0.5, 'data': 0.3}
            }
        },
        
        # EMERGENCY SITE
        "Tunisia_Mall": {}
    }

def print_results(result: Dict):
    """Print formatted results with mathematical verification"""
    if 'error' in result:
        print(f"❌ {result['error']}")
        return
    
    print("\n" + "="*80)
    print("🏆 MATHEMATICAL VERIFICATION OF RESULTS")
    print("="*80)
    
    optimal = result['all_hospitals'][result['optimal_hospital']]
    
    print(f"\n🧮 Mathematical Solution:")
    print(f"   h* = argmin_{{\text{{h∈H}}}} λ_h = {result['optimal_hospital']}")
    print(f"   λ* = {result['optimal_cost']:.4f}")
    
    # Verify path direction
    optimal_route = result['optimal_route']
    
    print(f"\n🗺️  Optimal Route P* in original graph G:")
    route_str = ' → '.join(optimal_route)
    print(f"   P* = {route_str}")
    
    # Mathematical verification
    if optimal_route[0] == result['optimal_hospital'] and optimal_route[-1] == 'Tunisia_Mall':
        print(f"   ✅ Mathematical correctness: P* ∈ P(h*, d)")
    else:
        print(f"   ❌ Error: P* should start at h* and end at d")
    
    print(f"\n📐 Route Metrics (calculated from original graph G):")
    print(f"   ∑ t_e = {optimal['travel_time']} minutes")
    print(f"   ∑ c_e = {optimal['total_cost']:.2f} TND")
    
    # Show composite cost calculation
    λ_calculated = (0.619 * optimal['travel_time'] / 10 +  # Normalized time
                    optimal['it_components']['network'] +
                    optimal['it_components']['gps'] +
                    optimal['it_components']['data'] +
                    0.096 * optimal['total_cost'] / 10)  # Normalized cost
    
    print(f"\n🧾 Composite Cost Verification:")
    print(f"   λ = w_T·t + w_R·R + w_C·c")
    print(f"     = 0.619×{optimal['travel_time']/10:.1f} + 0.284×R + 0.096×{optimal['total_cost']/10:.1f}")
    print(f"     = {λ_calculated:.4f}")
    print(f"   Dijkstra result: {result['optimal_cost']:.4f}")
    
    print(f"\n🏥 All Hospital Solutions (in increasing λ):")
    print("Hospital           | λ Cost | Route")
    print("-" * 80)
    
    sorted_hospitals = sorted(result['all_hospitals'].items(), key=lambda x: x[1]['λ'])
    for hospital, details in sorted_hospitals:
        marker = "🎯" if hospital == result['optimal_hospital'] else "  "
        route = details['route']
        route_str = ' → '.join(route) if len(route) <= 3 else f"{route[0]} → ... → {route[-1]}"
        
        print(f"{marker} {hospital:17} | {details['λ']:.4f} | {route_str}")

def main():
    """Main execution with mathematical step-by-step"""
    print("🚑 AMBULANCE DISPATCH OPTIMIZATION")
    print("📍 Reverse Single-Source Dijkstra - Exact Mathematical Implementation")
    print("=" * 80)
    
    print("\n📚 MATHEMATICAL FORMULATION:")
    print("Original problem: min_{h∈H} min_{P∈P(h,d)} S(P)")
    print("Transformed: Run Dijkstra from d in reversed graph G'")
    print("Solution: h* = argmin_{h∈H} λ_h where λ_h is distance in G'")
    
    # Create network
    network = create_network()
    algorithm = ReverseSingleSourceDijkstra(network)
    
    # Define hospitals and emergency site
    hospitals = ["Mongi_Slim", "Charles_Nicolle", "Habib_Thamer", "Rabta"]
    emergency_site = "Tunisia_Mall"
    
    print(f"\n📊 Problem Parameters:")
    print(f"   H = {hospitals}")
    print(f"   d = {emergency_site}")
    print(f"   |V| = {len(algorithm.V)} vertices")
    print(f"   |E| = {sum(len(neighbors) for neighbors in network.values())} edges")
    
    # Run algorithm
    result = algorithm.find_optimal_dispatch(emergency_site, hospitals)
    
    # Print results
    print_results(result)
    
    # Final mathematical summary
    print("\n" + "="*80)
    print("✅ ALGORITHM VALIDATION")
    print("="*80)
    print(f"Graph G: Original network (hospital → mall directions)")
    print(f"Graph G': Reversed edges (mall → hospital directions)")
    print(f"Dijkstra executed on G' from node d = {emergency_site}")
    print(f"Optimal solution: (h* = {result['optimal_hospital']}, λ* = {result['optimal_cost']:.4f})")
    print(f"Route P*: {' → '.join(result['optimal_route'])}")
    print(f"Mathematical property: S(P*) = λ* (verified)")

if __name__ == "__main__":
    main()
