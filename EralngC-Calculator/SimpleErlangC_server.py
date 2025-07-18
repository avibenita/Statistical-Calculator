from flask import Flask, request, jsonify
from flask_cors import CORS
import simpy
import random
import statistics
import time
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for web requests

# ─── Optional seed for reproducibility ───
RANDOM_SEED = None  # Set to None for different results each time, or use a number for reproducible results

def generate_service_time(service_params):
    """Generate service time based on distribution type and parameters"""
    distribution = service_params.get('distribution', 'exponential')
    
    try:
        if distribution == 'exponential':
            mean_time = service_params['mean']
            service_rate = 1.0 / mean_time
            return random.expovariate(service_rate)
            
        elif distribution == 'normal':
            mean_time = service_params['mean']
            std_dev = service_params.get('std_dev', mean_time * 0.2)  # Default to 20% CV
            
            # Validate parameters
            if std_dev <= 0:
                raise ValueError("Standard deviation must be positive")
            
            # Ensure non-negative service time
            service_time = random.normalvariate(mean_time, std_dev)
            return max(0.1, service_time)  # Minimum 0.1 minutes to avoid zero service times
            
        elif distribution == 'lognormal':
            mean_time = service_params['mean']
            cv = service_params.get('cv', 0.5)  # Coefficient of variation
            
            # Validate parameters
            if cv <= 0:
                raise ValueError("Coefficient of variation must be positive")
            
            # Convert mean and CV to mu and sigma for lognormal
            variance = (cv * mean_time) ** 2
            mu = math.log(mean_time ** 2 / math.sqrt(variance + mean_time ** 2))
            sigma = math.sqrt(math.log(1 + variance / (mean_time ** 2)))
            return random.lognormvariate(mu, sigma)
            
        elif distribution == 'uniform':
            mean_time = service_params['mean']
            range_factor = service_params.get('range_factor', 0.5)  # Range as factor of mean
            
            # Validate parameters
            if range_factor <= 0 or range_factor >= 1:
                raise ValueError("Range factor must be between 0 and 1")
            
            half_range = mean_time * range_factor
            min_time = max(0.1, mean_time - half_range)
            max_time = mean_time + half_range
            return random.uniform(min_time, max_time)
            
        elif distribution == 'gamma':
            mean_time = service_params['mean']
            cv = service_params.get('cv', 0.5)  # Coefficient of variation
            
            # Validate parameters
            if cv <= 0:
                raise ValueError("Coefficient of variation must be positive")
            
            # Convert mean and CV to alpha and beta for gamma distribution
            alpha = 1.0 / (cv ** 2)  # Shape parameter
            beta = alpha / mean_time   # Rate parameter
            return random.gammavariate(alpha, 1.0 / beta)  # Python uses scale parameter
            
        elif distribution == 'deterministic':
            return service_params['mean']
            
        else:
            # Fallback to exponential
            mean_time = service_params['mean']
            service_rate = 1.0 / mean_time
            return random.expovariate(service_rate)
            
    except (KeyError, ValueError, ZeroDivisionError) as e:
        # Fallback to exponential distribution with mean service time
        print(f"Warning: Distribution parameter error ({e}), falling back to exponential")
        mean_time = service_params.get('mean', 5.0)
        service_rate = 1.0 / mean_time
        return random.expovariate(service_rate)

def customer(env, service_params, wait_times, abandoned_customers, abandonment_threshold_minutes=10):
    arrival = env.now
    
    # Create a timeout process for abandonment
    abandonment_timeout = env.timeout(abandonment_threshold_minutes)
    
    with env.servers.request() as req:
        # Race between getting served and abandoning
        result = yield req | abandonment_timeout
        
        if abandonment_timeout in result:
            # Customer abandoned - they waited too long
            abandoned_customers.append(env.now - arrival)
            return  # Exit without being served
        
        # Customer got served
        wait = env.now - arrival
        wait_times.append(wait)
        
        # Generate service time based on distribution type
        service_time = generate_service_time(service_params)
        yield env.timeout(service_time)

def setup(env, arrival_rate, service_params, num_servers, wait_times, abandoned_customers, abandonment_threshold_minutes):
    env.servers = simpy.Resource(env, capacity=num_servers)
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        env.process(customer(env, service_params, wait_times, abandoned_customers, abandonment_threshold_minutes))

def run_simulation(arrival_rate, service_params, num_servers, sim_time,
                   sla_target_pct, sla_threshold_seconds, abandonment_threshold_minutes=10, seed=None):
    # Set seed if provided, otherwise use system entropy for different results each time
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()  # Uses system time and entropy for randomness
    
    wait_times = []
    abandoned_customers = []
    env = simpy.Environment()
    env.process(setup(env, arrival_rate, service_params, num_servers, wait_times, abandoned_customers, abandonment_threshold_minutes))
    env.run(until=sim_time)

    # Convert threshold to minutes for comparison
    sla_threshold_minutes = sla_threshold_seconds / 60.0
    total_served = len(wait_times)
    total_abandoned = len(abandoned_customers)
    total_arrivals = total_served + total_abandoned
    
    avg_wait_sec = (statistics.mean(wait_times) * 60) if total_served else 0.0
    avg_abandon_wait_sec = (statistics.mean(abandoned_customers) * 60) if total_abandoned else 0.0
    
    pct_within_sla = (
        sum(1 for w in wait_times if w <= sla_threshold_minutes) / total_served * 100
        if total_served else 0.0
    )
    abandonment_rate = (total_abandoned / total_arrivals * 100) if total_arrivals else 0.0
    mean_service_time = service_params.get('mean', 5.0)  # Extract mean from service params
    utilization = (arrival_rate * mean_service_time) / num_servers * 100

    return {
        'total_arrivals': total_arrivals,
        'total_served': total_served,
        'total_abandoned': total_abandoned,
        'avg_wait_seconds': avg_wait_sec,
        'avg_abandon_wait_seconds': avg_abandon_wait_sec,
        'pct_within_sla': pct_within_sla,
        'abandonment_rate': abandonment_rate,
        'utilization_pct': utilization,
        'meets_sla': pct_within_sla >= sla_target_pct
    }

def find_minimum_agents(arrival_rate, service_params, sim_time, sla_target_pct, 
                       sla_threshold_seconds, abandonment_threshold_minutes=10, 
                       max_abandonment_rate=None, min_agents=1, max_agents=50, 
                       num_replications=3, seed=None):
    """
    Find the minimum number of agents needed to meet SLA requirements.
    """
    
    # Calculate theoretical minimum based on Erlang theory
    mean_service_time = service_params.get('mean', 5.0)  # Use mean service time from params
    traffic_intensity = arrival_rate * mean_service_time
    theoretical_min = max(min_agents, int(traffic_intensity) + 1)
    
    for num_agents in range(max(min_agents, theoretical_min), max_agents + 1):
        # Run multiple replications to get average performance
        replication_results = []
        
        for rep in range(num_replications):
            # Use different seeds for each replication if base seed provided
            rep_seed = seed + rep if seed is not None else None
            
            result = run_simulation(
                arrival_rate=arrival_rate,
                service_params=service_params,
                num_servers=num_agents,
                sim_time=sim_time,
                sla_target_pct=sla_target_pct,
                sla_threshold_seconds=sla_threshold_seconds,
                abandonment_threshold_minutes=abandonment_threshold_minutes,
                seed=rep_seed
            )
            replication_results.append(result)
        
        # Calculate average metrics across replications
        avg_sla_pct = statistics.mean([r['pct_within_sla'] for r in replication_results])
        avg_abandonment = statistics.mean([r['abandonment_rate'] for r in replication_results])
        avg_utilization = statistics.mean([r['utilization_pct'] for r in replication_results])
        avg_wait_time = statistics.mean([r['avg_wait_seconds'] for r in replication_results])
        
        # Check if SLA is met
        meets_sla = avg_sla_pct >= sla_target_pct
        meets_abandonment = max_abandonment_rate is None or avg_abandonment <= max_abandonment_rate
        
        # If both SLA and abandonment criteria are met, return result
        if meets_sla and meets_abandonment:
            return {
                'minimum_agents': num_agents,
                'avg_sla_percentage': avg_sla_pct,
                'avg_abandonment_rate': avg_abandonment,
                'avg_utilization': avg_utilization,
                'avg_wait_seconds': avg_wait_time,
                'meets_sla': meets_sla,
                'meets_abandonment_target': meets_abandonment,
                'traffic_intensity': traffic_intensity,
                'theoretical_min': theoretical_min,
                'replication_results': replication_results
            }
    
    return {
        'error': f'No solution found with {max_agents} or fewer agents',
        'traffic_intensity': traffic_intensity,
        'theoretical_min': theoretical_min
    }

# API Routes
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Erlang C Simulation Server',
        'version': '1.0',
        'endpoints': {
            '/simulate': 'POST - Run single simulation',
            '/optimize': 'POST - Find minimum agents needed',
            '/health': 'GET - Health check'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json()
        
        # Required parameters
        arrival_rate = data.get('arrival_rate', 1.67)
        mean_service_time = data.get('mean_service_time', 5)
        num_servers = data.get('num_servers', 12)
        sim_time = data.get('sim_time', 1000)
        sla_target_pct = data.get('sla_target_pct', 80)
        sla_threshold_seconds = data.get('sla_threshold_seconds', 20)
        
        # Distribution parameters
        service_distribution = data.get('service_distribution', 'exponential')
        
        # Build service parameters based on distribution type
        service_params = {
            'distribution': service_distribution,
            'mean': mean_service_time
        }
        
        # Add distribution-specific parameters
        if service_distribution == 'normal':
            service_params['std_dev'] = data.get('service_std_dev', service_params['mean'] * 0.2)
        elif service_distribution == 'lognormal':
            service_params['cv'] = data.get('service_cv', 0.5)
        elif service_distribution == 'uniform':
            service_params['range_factor'] = data.get('service_range_factor', 0.5)
        elif service_distribution == 'gamma':
            service_params['cv'] = data.get('service_cv', 0.5)
        # deterministic and exponential don't need additional parameters
        
        # Optional parameters
        abandonment_threshold_minutes = data.get('abandonment_threshold_minutes', 10)
        seed = data.get('seed', None)
        
        # Run simulation
        results = run_simulation(
            arrival_rate=arrival_rate,
            service_params=service_params,
            num_servers=num_servers,
            sim_time=sim_time,
            sla_target_pct=sla_target_pct,
            sla_threshold_seconds=sla_threshold_seconds,
            abandonment_threshold_minutes=abandonment_threshold_minutes,
            seed=seed
        )
        
        # Add input parameters to response
        results['input_parameters'] = {
            'arrival_rate': arrival_rate,
            'mean_service_time': mean_service_time,
            'service_distribution': service_distribution,
            'service_params': service_params,
            'num_servers': num_servers,
            'sim_time': sim_time,
            'sla_target_pct': sla_target_pct,
            'sla_threshold_seconds': sla_threshold_seconds,
            'abandonment_threshold_minutes': abandonment_threshold_minutes,
            'seed': seed
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.get_json()
        
        # Required parameters
        arrival_rate = data.get('arrival_rate', 1.67)
        mean_service_time = data.get('mean_service_time', 5)
        sim_time = data.get('sim_time', 1000)
        sla_target_pct = data.get('sla_target_pct', 80)
        sla_threshold_seconds = data.get('sla_threshold_seconds', 20)
        
        # Distribution parameters
        service_distribution = data.get('service_distribution', 'exponential')
        
        # Build service parameters based on distribution type
        service_params = {
            'distribution': service_distribution,
            'mean': mean_service_time
        }
        
        # Add distribution-specific parameters
        if service_distribution == 'normal':
            service_params['std_dev'] = data.get('service_std_dev', service_params['mean'] * 0.2)
        elif service_distribution == 'lognormal':
            service_params['cv'] = data.get('service_cv', 0.5)
        elif service_distribution == 'uniform':
            service_params['range_factor'] = data.get('service_range_factor', 0.5)
        elif service_distribution == 'gamma':
            service_params['cv'] = data.get('service_cv', 0.5)
        # deterministic and exponential don't need additional parameters
        
        # Optional parameters
        abandonment_threshold_minutes = data.get('abandonment_threshold_minutes', 10)
        max_abandonment_rate = data.get('max_abandonment_rate', 15.0)
        min_agents = data.get('min_agents', 1)
        max_agents = data.get('max_agents', 50)
        num_replications = data.get('num_replications', 3)
        seed = data.get('seed', 42)
        
        # Find minimum agents
        results = find_minimum_agents(
            arrival_rate=arrival_rate,
            service_params=service_params,
            sim_time=sim_time,
            sla_target_pct=sla_target_pct,
            sla_threshold_seconds=sla_threshold_seconds,
            abandonment_threshold_minutes=abandonment_threshold_minutes,
            max_abandonment_rate=max_abandonment_rate,
            min_agents=min_agents,
            max_agents=max_agents,
            num_replications=num_replications,
            seed=seed
        )
        
        # Add input parameters to response
        results['input_parameters'] = {
            'arrival_rate': arrival_rate,
            'mean_service_time': mean_service_time,
            'service_distribution': service_distribution,
            'service_params': service_params,
            'sim_time': sim_time,
            'sla_target_pct': sla_target_pct,
            'sla_threshold_seconds': sla_threshold_seconds,
            'abandonment_threshold_minutes': abandonment_threshold_minutes,
            'max_abandonment_rate': max_abandonment_rate,
            'min_agents': min_agents,
            'max_agents': max_agents,
            'num_replications': num_replications,
            'seed': seed
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting Erlang C Simulation Server...")
    print("📊 Available endpoints:")
    print("   GET  / - Server info")
    print("   GET  /health - Health check")
    print("   POST /simulate - Run simulation")
    print("   POST /optimize - Find minimum agents")
    print("\n🌐 Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 