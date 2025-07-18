import requests
import json
import time
from typing import Dict, Any

class ErlangCClient:
    """Test client for the Erlang C Simulation Server"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def test_connection(self) -> bool:
        """Test if server is running"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and healthy")
                return True
            else:
                print(f"❌ Server responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to server: {e}")
            return False
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information and available endpoints"""
        try:
            response = self.session.get(f"{self.base_url}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting server info: {e}")
            return {}
    
    def run_simulation(self, **kwargs) -> Dict[str, Any]:
        """Run a single simulation"""
        default_params = {
            'arrival_rate': 1.67,
            'mean_service_time': 5,
            'num_servers': 12,
            'sim_time': 1000,
            'sla_target_pct': 80,
            'sla_threshold_seconds': 20,
            'abandonment_threshold_minutes': 10,
            'seed': None
        }
        
        # Update with provided parameters
        params = {**default_params, **kwargs}
        
        try:
            response = self.session.post(f"{self.base_url}/simulate", json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error running simulation: {e}")
            return {}
    
    def optimize_agents(self, **kwargs) -> Dict[str, Any]:
        """Find minimum agents needed"""
        default_params = {
            'arrival_rate': 1.67,
            'mean_service_time': 5,
            'sim_time': 1000,
            'sla_target_pct': 80,
            'sla_threshold_seconds': 20,
            'abandonment_threshold_minutes': 10,
            'max_abandonment_rate': 15.0,
            'min_agents': 1,
            'max_agents': 25,
            'num_replications': 3,
            'seed': 42
        }
        
        # Update with provided parameters
        params = {**default_params, **kwargs}
        
        try:
            response = self.session.post(f"{self.base_url}/optimize", json=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error optimizing agents: {e}")
            return {}

def print_simulation_results(results: Dict[str, Any], title: str = "Simulation Results"):
    """Pretty print simulation results"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Input parameters
    if 'input_parameters' in results:
        params = results['input_parameters']
        print(f"📋 Input Parameters:")
        print(f"   • Arrival rate: {params.get('arrival_rate', 'N/A')} calls/min")
        print(f"   • Service time: {params.get('mean_service_time', 'N/A')} minutes")
        print(f"   • Number of servers: {params.get('num_servers', 'N/A')}")
        print(f"   • SLA target: {params.get('sla_target_pct', 'N/A')}% within {params.get('sla_threshold_seconds', 'N/A')}s")
        print(f"   • Abandonment threshold: {params.get('abandonment_threshold_minutes', 'N/A')} minutes")
        print()
    
    # Results
    print(f"📊 Results:")
    if 'total_arrivals' in results:
        print(f"   • Total arrivals: {results['total_arrivals']}")
        print(f"   • Customers served: {results['total_served']}")
        print(f"   • Customers abandoned: {results['total_abandoned']}")
        print(f"   • Abandonment rate: {results['abandonment_rate']:.1f}%")
        print(f"   • Avg wait time (served): {results['avg_wait_seconds']:.2f} seconds")
        if results['total_abandoned'] > 0:
            print(f"   • Avg wait before abandon: {results['avg_abandon_wait_seconds']:.2f} seconds")
        print(f"   • SLA performance: {results['pct_within_sla']:.1f}%")
        print(f"   • Agent utilization: {results['utilization_pct']:.1f}%")
        print(f"   • Meets SLA target: {'✅ Yes' if results['meets_sla'] else '❌ No'}")
    
    # Optimization results
    if 'minimum_agents' in results:
        print(f"   • Minimum agents needed: {results['minimum_agents']}")
        print(f"   • Traffic intensity: {results.get('traffic_intensity', 'N/A'):.2f} Erlangs")
        print(f"   • Theoretical minimum: {results.get('theoretical_min', 'N/A')}")
        print(f"   • Average SLA: {results['avg_sla_percentage']:.1f}%")
        print(f"   • Average abandonment: {results['avg_abandonment_rate']:.1f}%")
        print(f"   • Average utilization: {results['avg_utilization']:.1f}%")
        print(f"   • Average wait time: {results['avg_wait_seconds']:.2f} seconds")

def run_comprehensive_tests():
    """Run a comprehensive test suite"""
    print("🧪 Starting Erlang C Server Tests")
    print("="*60)
    
    # Initialize client
    client = ErlangCClient()
    
    # Test 1: Connection
    print("\n🔍 Test 1: Server Connection")
    if not client.test_connection():
        print("❌ Cannot connect to server. Make sure SimpleErlangC_server.py is running.")
        return
    
    # Test 2: Server Info
    print("\n🔍 Test 2: Server Information")
    server_info = client.get_server_info()
    if server_info:
        print(f"✅ Server: {server_info.get('message', 'Unknown')}")
        print(f"✅ Version: {server_info.get('version', 'Unknown')}")
        print(f"✅ Available endpoints: {list(server_info.get('endpoints', {}).keys())}")
    
    # Test 3: Basic Simulation
    print("\n🔍 Test 3: Basic Simulation")
    basic_results = client.run_simulation()
    if basic_results:
        print_simulation_results(basic_results, "Basic Simulation (Default Parameters)")
    
    # Test 4: Custom Simulation
    print("\n🔍 Test 4: Custom Simulation")
    custom_results = client.run_simulation(
        arrival_rate=2.0,
        mean_service_time=6,
        num_servers=15,
        sla_target_pct=85,
        sla_threshold_seconds=30,
        seed=123
    )
    if custom_results:
        print_simulation_results(custom_results, "Custom Simulation")
    
    # Test 5: Agent Optimization
    print("\n🔍 Test 5: Agent Optimization")
    optimization_results = client.optimize_agents()
    if optimization_results:
        print_simulation_results(optimization_results, "Agent Optimization")
    
    # Test 6: High Traffic Scenario
    print("\n🔍 Test 6: High Traffic Scenario")
    high_traffic_results = client.run_simulation(
        arrival_rate=3.0,
        mean_service_time=8,
        num_servers=10,
        sla_target_pct=75,
        abandonment_threshold_minutes=5
    )
    if high_traffic_results:
        print_simulation_results(high_traffic_results, "High Traffic Scenario")
    
    # Test 7: Optimization for High Traffic
    print("\n🔍 Test 7: Optimization for High Traffic")
    high_traffic_opt = client.optimize_agents(
        arrival_rate=3.0,
        mean_service_time=8,
        sla_target_pct=75,
        max_abandonment_rate=10.0,
        num_replications=5
    )
    if high_traffic_opt:
        print_simulation_results(high_traffic_opt, "High Traffic Optimization")
    
    # Test 8: Performance Test
    print("\n🔍 Test 8: Performance Test")
    start_time = time.time()
    
    # Run multiple simulations
    for i in range(5):
        client.run_simulation(seed=i)
    
    end_time = time.time()
    print(f"✅ Completed 5 simulations in {end_time - start_time:.2f} seconds")
    print(f"✅ Average time per simulation: {(end_time - start_time) / 5:.2f} seconds")

def interactive_mode():
    """Interactive mode for testing specific scenarios"""
    client = ErlangCClient()
    
    if not client.test_connection():
        print("❌ Cannot connect to server. Please start SimpleErlangC_server.py first.")
        return
    
    print("\n🎮 Interactive Mode")
    print("Available commands:")
    print("  1 - Run basic simulation")
    print("  2 - Run custom simulation")
    print("  3 - Optimize agents")
    print("  4 - Server health check")
    print("  q - Quit")
    
    while True:
        try:
            choice = input("\nEnter command (1-4, q): ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '1':
                print("\n🔄 Running basic simulation...")
                results = client.run_simulation()
                print_simulation_results(results)
                
            elif choice == '2':
                print("\n📝 Custom simulation parameters:")
                arrival_rate = float(input("Arrival rate (calls/min) [1.67]: ") or 1.67)
                service_time = float(input("Service time (minutes) [5]: ") or 5)
                num_servers = int(input("Number of servers [12]: ") or 12)
                sla_target = float(input("SLA target (%) [80]: ") or 80)
                sla_threshold = float(input("SLA threshold (seconds) [20]: ") or 20)
                
                print("\n🔄 Running custom simulation...")
                results = client.run_simulation(
                    arrival_rate=arrival_rate,
                    mean_service_time=service_time,
                    num_servers=num_servers,
                    sla_target_pct=sla_target,
                    sla_threshold_seconds=sla_threshold
                )
                print_simulation_results(results)
                
            elif choice == '3':
                print("\n🔄 Finding minimum agents...")
                results = client.optimize_agents()
                print_simulation_results(results)
                
            elif choice == '4':
                print("\n❤️ Health check...")
                if client.test_connection():
                    info = client.get_server_info()
                    print(f"Server: {info.get('message', 'Unknown')}")
                
            else:
                print("❌ Invalid command. Try again.")
                
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Erlang C Server Test Client")
    print("Make sure SimpleErlangC_server.py is running first!")
    print("\nChoose test mode:")
    print("1 - Run comprehensive tests")
    print("2 - Interactive mode")
    
    try:
        choice = input("\nEnter choice (1-2): ").strip()
        
        if choice == '1':
            run_comprehensive_tests()
        elif choice == '2':
            interactive_mode()
        else:
            print("Running comprehensive tests by default...")
            run_comprehensive_tests()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ Testing complete!") 