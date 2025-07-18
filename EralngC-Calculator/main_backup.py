import json
import math
import random
import statistics
import time
from typing import Dict, Any

def erlang_c_server(request):
    """
    Google Cloud Function entry point for Erlang C simulation server.
    Handles CORS and routes requests to appropriate handlers.
    """
    
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for actual requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        # Route based on request method and path
        if request.method == 'GET':
            if request.path == '/health':
                return (json.dumps(health_check()), 200, headers)
            else:
                return (json.dumps(home_info()), 200, headers)
                
        elif request.method == 'POST':
            if request.path == '/simulate' or 'simulate' in request.path:
                return (json.dumps(simulate_handler(request)), 200, headers)
            elif request.path == '/optimize' or 'optimize' in request.path:
                return (json.dumps(optimize_handler(request)), 200, headers)
            else:
                return (json.dumps({'error': 'Endpoint not found'}), 404, headers)
        else:
            return (json.dumps({'error': 'Method not allowed'}), 405, headers)
            
    except Exception as e:
        error_response = {'error': str(e), 'type': type(e).__name__}
        return (json.dumps(error_response), 500, headers)


def home_info():
    """Return server information"""
    return {
        'message': 'Erlang C Simulation Server (Cloud Function)',
        'version': '1.0',
        'endpoints': {
            '/simulate': 'POST - Run single simulation',
            '/optimize': 'POST - Find minimum agents needed',
            '/health': 'GET - Health check'
        }
    }


def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'timestamp': time.time()}


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
            std_dev = service_params.get('std_dev', mean_time * 0.2)
            
            if std_dev <= 0:
                raise ValueError("Standard deviation must be positive")
            
            service_time = random.normalvariate(mean_time, std_dev)
            return max(0.1, service_time)
            
        elif distribution == 'lognormal':
            mean_time = service_params['mean']
            cv = service_params.get('cv', 0.5)
            
            if cv <= 0:
                raise ValueError("Coefficient of variation must be positive")
            
            variance = (cv * mean_time) ** 2
            mu = math.log(mean_time ** 2 / math.sqrt(variance + mean_time ** 2))
            sigma = math.sqrt(math.log(1 + variance / (mean_time ** 2)))
            return random.lognormvariate(mu, sigma)
            
        elif distribution == 'uniform':
            mean_time = service_params['mean']
            range_factor = service_params.get('range_factor', 0.5)
            
            if not (0 < range_factor < 1):
                raise ValueError("Range factor must be between 0 and 1")
            
            range_value = mean_time * range_factor
            min_time = mean_time - range_value
            max_time = mean_time + range_value
            return random.uniform(max(0.1, min_time), max_time)
            
        elif distribution == 'gamma':
            mean_time = service_params['mean']
            cv = service_params.get('cv', 0.5)
            
            if cv <= 0:
                raise ValueError("Coefficient of variation must be positive")
            
            alpha = 1 / (cv ** 2)
            beta = mean_time / alpha
            return random.gammavariate(alpha, beta)
            
        elif distribution == 'deterministic':
            return service_params['mean']
            
        else:
            raise ValueError(f"Unknown distribution type: {distribution}")
            
    except Exception as e:
        raise ValueError(f"Error generating service time for {distribution} distribution: {str(e)}")


class Customer:
    def __init__(self, customer_id, arrival_time):
        self.id = customer_id
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.service_end_time = None
        self.wait_time = 0
        self.service_time = 0
        self.abandoned = False
        self.abandonment_time = None


def customer_process(env, customer, servers, service_params, abandonment_threshold_minutes, 
                    patience_time_minutes, retrial_rate, retrial_delay_minutes, max_capacity,
                    metrics):
    """Simulate a customer's journey through the system"""
    
    arrival_time = customer.arrival_time
    
    # Check system capacity
    if max_capacity and len(servers.queue) + servers.count >= max_capacity:
        metrics['blocked'] += 1
        return
    
    # Request server
    server_request = servers.request()
    
    # Handle abandonment/patience
    patience_timeout = None
    if patience_time_minutes and patience_time_minutes > 0:
        patience_timeout = env.timeout(patience_time_minutes)
    
    abandonment_timeout = None
    if abandonment_threshold_minutes and abandonment_threshold_minutes > 0:
        abandonment_timeout = env.timeout(abandonment_threshold_minutes)
    
    # Wait for server or timeout
    if patience_timeout or abandonment_timeout:
        timeouts = [t for t in [patience_timeout, abandonment_timeout] if t]
        result = yield server_request | env.any_of(timeouts)
        
        if server_request not in result:
            # Customer abandoned
            customer.abandoned = True
            customer.abandonment_time = env.now
            customer.wait_time = env.now - arrival_time
            metrics['abandonments'] += 1
            
            # Handle retrial
            if retrial_rate and random.random() < (retrial_rate / 100.0):
                yield env.timeout(retrial_delay_minutes or 5)
                # Create new customer for retrial
                retrial_customer = Customer(f"{customer.id}_retry", env.now)
                env.process(customer_process(env, retrial_customer, servers, service_params,
                                           abandonment_threshold_minutes, patience_time_minutes,
                                           retrial_rate, retrial_delay_minutes, max_capacity, metrics))
            return
    else:
        yield server_request
    
    # Customer got server
    customer.service_start_time = env.now
    customer.wait_time = customer.service_start_time - arrival_time
    
    # Generate service time
    customer.service_time = generate_service_time(service_params)
    
    # Serve customer
    yield env.timeout(customer.service_time)
    
    customer.service_end_time = env.now
    metrics['completed'] += 1
    
    # Release server
    servers.release(server_request)


def run_simulation(arrival_rate, service_params, num_servers, sim_time, sla_target_pct, 
                  sla_threshold_seconds, abandonment_threshold_minutes=None,
                  patience_time_minutes=None, retrial_rate=None, retrial_delay_minutes=None,
                  max_capacity=None, seed=None):
    """Run the simulation and return results"""
    
    # Import simpy here to handle potential import issues in cloud environment
    try:
        import simpy
    except ImportError:
        raise ImportError("simpy package is required. Add it to requirements.txt for Cloud Functions.")
    
    if seed is not None:
        random.seed(seed)
    
    # Create environment
    env = simpy.Environment()
    servers = simpy.Resource(env, capacity=num_servers)
    
    # Metrics tracking
    metrics = {
        'completed': 0,
        'abandonments': 0,
        'blocked': 0
    }
    
    customers = []
    
    def customer_generator():
        customer_id = 0
        while True:
            # Generate inter-arrival time (exponential distribution)
            inter_arrival_time = random.expovariate(arrival_rate)
            yield env.timeout(inter_arrival_time)
            
            customer = Customer(customer_id, env.now)
            customers.append(customer)
            
            env.process(customer_process(env, customer, servers, service_params,
                                       abandonment_threshold_minutes, patience_time_minutes,
                                       retrial_rate, retrial_delay_minutes, max_capacity, metrics))
            customer_id += 1
    
    # Start customer generator
    env.process(customer_generator())
    
    # Run simulation
    env.run(until=sim_time)
    
    # Calculate metrics
    completed_customers = [c for c in customers if not c.abandoned and c.service_end_time is not None]
    
    if not completed_customers:
        return {
            'error': 'No customers completed service',
            'total_customers': len(customers),
            'metrics': metrics
        }
    
    # Wait times and service levels
    wait_times = [c.wait_time for c in completed_customers]
    service_times = [c.service_time for c in completed_customers]
    
    avg_wait_time = statistics.mean(wait_times)
    avg_service_time = statistics.mean(service_times)
    
    # Calculate service level
    sla_threshold_minutes = sla_threshold_seconds / 60.0
    customers_within_sla = sum(1 for wt in wait_times if wt <= sla_threshold_minutes)
    service_level_achieved = (customers_within_sla / len(completed_customers)) * 100
    
    # Server utilization
    total_service_time = sum(service_times)
    total_server_time = num_servers * sim_time
    utilization = (total_service_time / total_server_time) * 100
    
    return {
        'avg_wait_time_minutes': round(avg_wait_time, 2),
        'avg_wait_time_seconds': round(avg_wait_time * 60, 2),
        'avg_service_time_minutes': round(avg_service_time, 2),
        'service_level_achieved': round(service_level_achieved, 2),
        'service_level_target': sla_target_pct,
        'utilization': round(utilization, 2),
        'total_customers': len(customers),
        'completed_customers': len(completed_customers),
        'abandoned_customers': metrics['abandonments'],
        'blocked_customers': metrics['blocked'],
        'abandonment_rate': round((metrics['abandonments'] / len(customers)) * 100, 2) if len(customers) > 0 else 0,
        'num_servers': num_servers,
        'simulation_time': sim_time
    }


def simulate_handler(request):
    """Handle simulation requests"""
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No JSON data provided")
        
        # Required parameters
        arrival_rate = data.get('arrival_rate', 1.67)
        mean_service_time = data.get('mean_service_time', 5)
        num_servers = data.get('num_servers', 12)
        sim_time = data.get('sim_time', 1000)
        sla_target_pct = data.get('sla_target_pct', 80)
        sla_threshold_seconds = data.get('sla_threshold_seconds', 20)
        
        # Distribution parameters
        service_distribution = data.get('service_distribution', 'exponential')
        
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
        
        # Optional parameters
        abandonment_threshold_minutes = data.get('abandonment_threshold_minutes', 10)
        patience_time_minutes = data.get('patience_time_minutes')
        retrial_rate = data.get('retrial_rate')
        retrial_delay_minutes = data.get('retrial_delay_minutes')
        max_capacity = data.get('max_capacity')
        seed = data.get('seed')
        
        # Convert rates to proper format
        if patience_time_minutes is not None and patience_time_minutes > 0:
            patience_time_minutes = patience_time_minutes / 60.0  # Convert to minutes
        
        results = run_simulation(
            arrival_rate=arrival_rate,
            service_params=service_params,
            num_servers=num_servers,
            sim_time=sim_time,
            sla_target_pct=sla_target_pct,
            sla_threshold_seconds=sla_threshold_seconds,
            abandonment_threshold_minutes=abandonment_threshold_minutes,
            patience_time_minutes=patience_time_minutes,
            retrial_rate=retrial_rate,
            retrial_delay_minutes=retrial_delay_minutes,
            max_capacity=max_capacity,
            seed=seed
        )
        
        return results
        
    except Exception as e:
        return {'error': str(e), 'type': type(e).__name__}


def find_minimum_agents(arrival_rate, service_params, sla_target_pct, sla_threshold_seconds,
                       abandonment_threshold_minutes=None, patience_time_minutes=None,
                       retrial_rate=None, retrial_delay_minutes=None, max_capacity=None,
                       min_agents=1, max_agents=50, num_replications=3, seed=None):
    """Find minimum number of agents needed to achieve target service level"""
    
    for num_agents in range(min_agents, max_agents + 1):
        service_levels = []
        
        for replication in range(num_replications):
            replication_seed = seed + replication if seed is not None else None
            
            result = run_simulation(
                arrival_rate=arrival_rate,
                service_params=service_params,
                num_servers=num_agents,
                sim_time=500,  # Shorter simulation for optimization
                sla_target_pct=sla_target_pct,
                sla_threshold_seconds=sla_threshold_seconds,
                abandonment_threshold_minutes=abandonment_threshold_minutes,
                patience_time_minutes=patience_time_minutes,
                retrial_rate=retrial_rate,
                retrial_delay_minutes=retrial_delay_minutes,
                max_capacity=max_capacity,
                seed=replication_seed
            )
            
            if 'error' in result:
                continue
                
            service_levels.append(result['service_level_achieved'])
        
        if service_levels:
            avg_service_level = statistics.mean(service_levels)
            if avg_service_level >= sla_target_pct:
                return num_agents, avg_service_level
    
    return max_agents, 0  # Could not achieve target


def optimize_handler(request):
    """Handle optimization requests"""
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No JSON data provided")
        
        # Debug: Log the received data
        print(f"Optimize handler received data: {data}")
        
        # Required parameters
        arrival_rate = data.get('arrival_rate', 1.67)
        mean_service_time = data.get('mean_service_time', 5)
        sla_target_pct = data.get('sla_target_pct', 80)
        sla_threshold_seconds = data.get('sla_threshold_seconds', 20)
        
        # Debug: Log the parameters
        print(f"Parameters: arrival_rate={arrival_rate}, mean_service_time={mean_service_time}, sla_target_pct={sla_target_pct}")
        
        # Distribution parameters
        service_distribution = data.get('service_distribution', 'exponential')
        
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
        
        # Optional parameters
        abandonment_threshold_minutes = data.get('abandonment_threshold_minutes', 10)
        patience_time_minutes = data.get('patience_time_minutes')
        retrial_rate = data.get('retrial_rate')
        retrial_delay_minutes = data.get('retrial_delay_minutes')
        max_capacity = data.get('max_capacity')
        min_agents = data.get('min_agents', 1)
        max_agents = data.get('max_agents', 50)
        num_replications = data.get('num_replications', 3)
        seed = data.get('seed')
        
        # Convert rates
        if patience_time_minutes is not None and patience_time_minutes > 0:
            patience_time_minutes = patience_time_minutes / 60.0
        
        # Debug: About to call find_minimum_agents
        print(f"About to call find_minimum_agents with sla_target_pct={sla_target_pct}")
        
        min_agents_needed, achieved_service_level = find_minimum_agents(
            arrival_rate=arrival_rate,
            service_params=service_params,
            sla_target_pct=sla_target_pct,
            sla_threshold_seconds=sla_threshold_seconds,
            abandonment_threshold_minutes=abandonment_threshold_minutes,
            patience_time_minutes=patience_time_minutes,
            retrial_rate=retrial_rate,
            retrial_delay_minutes=retrial_delay_minutes,
            max_capacity=max_capacity,
            min_agents=min_agents,
            max_agents=max_agents,
            num_replications=num_replications,
            seed=seed
        )
        
        results = {
            'minimum_agents_needed': min_agents_needed,
            'achieved_service_level': round(achieved_service_level, 2),
            'target_service_level': sla_target_pct,
            'arrival_rate': arrival_rate,
            'service_params': service_params,
            'sla_threshold_seconds': sla_threshold_seconds,
            'min_agents': min_agents,
            'max_agents': max_agents,
            'num_replications': num_replications,
            'seed': seed
        }
        
        return results
        
    except Exception as e:
        return {'error': str(e), 'type': type(e).__name__} 