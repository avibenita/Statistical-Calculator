# Erlang C Simulation System

A comprehensive Erlang C simulation system with customer abandonment, agent optimization, and web API functionality.

## 📁 Files Overview

- **`SimpleErlangC.py`** - Original standalone simulation script
- **`SimpleErlangC_server.py`** - Flask web server for API access
- **`test_server.py`** - Comprehensive test client
- **`run_tests.py`** - Helper script to manage server and tests
- **`Erlang_SimpleAndSimulation.html`** - Web interface (cleaned)
- **`requirements.txt`** - Python dependencies

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Option A: Use the Helper Script

```bash
# Interactive menu
python run_tests.py

# Or use direct commands:
python run_tests.py --server      # Start server
python run_tests.py --test        # Run tests
python run_tests.py --interactive # Interactive mode
```

### 3. Option B: Manual Setup

**Terminal 1 - Start Server:**
```bash
python SimpleErlangC_server.py
```

**Terminal 2 - Run Tests:**
```bash
python test_server.py
```

## 🌐 API Endpoints

The server runs on `http://localhost:5000` with these endpoints:

### `GET /` - Server Information
Returns server info and available endpoints.

### `GET /health` - Health Check
Check if server is running properly.

### `POST /simulate` - Run Simulation
Run a single simulation with custom parameters.

**Request Example:**
```json
{
    "arrival_rate": 1.67,
    "mean_service_time": 5,
    "num_servers": 12,
    "sim_time": 1000,
    "sla_target_pct": 80,
    "sla_threshold_seconds": 20,
    "abandonment_threshold_minutes": 10,
    "seed": 42
}
```

**Response Example:**
```json
{
    "total_arrivals": 1653,
    "total_served": 1598,
    "total_abandoned": 55,
    "avg_wait_seconds": 8.4,
    "avg_abandon_wait_seconds": 598.2,
    "pct_within_sla": 89.1,
    "abandonment_rate": 3.3,
    "utilization_pct": 69.6,
    "meets_sla": true
}
```

### `POST /optimize` - Find Minimum Agents
Automatically find the minimum number of agents needed to meet SLA.

**Request Example:**
```json
{
    "arrival_rate": 2.0,
    "mean_service_time": 6,
    "sla_target_pct": 85,
    "sla_threshold_seconds": 30,
    "max_abandonment_rate": 10.0,
    "num_replications": 5
}
```

**Response Example:**
```json
{
    "minimum_agents": 14,
    "avg_sla_percentage": 87.2,
    "avg_abandonment_rate": 8.1,
    "avg_utilization": 85.7,
    "traffic_intensity": 12.0,
    "theoretical_min": 13
}
```

## 🧪 Testing Features

The test client (`test_server.py`) provides:

### Comprehensive Test Suite
- **Connection Testing** - Verify server connectivity
- **Basic Simulation** - Default parameter testing
- **Custom Simulation** - User-defined parameters
- **Agent Optimization** - Find minimum staffing
- **High Traffic Scenarios** - Stress testing
- **Performance Testing** - Speed benchmarks

### Interactive Mode
- Real-time parameter input
- Custom scenario testing
- Health monitoring
- User-friendly interface

## 📊 Simulation Features

### Core Capabilities
- **Customer Arrivals** - Poisson process
- **Service Times** - Exponential distribution
- **Customer Abandonment** - After specified wait time
- **Multiple Agents** - Configurable staffing levels
- **SLA Tracking** - Service level monitoring

### Advanced Features
- **Agent Optimization** - Find minimum staffing automatically
- **Multiple Replications** - Statistical accuracy
- **Abandonment Constraints** - Max abandonment rate limits
- **Traffic Analysis** - Erlang theory integration
- **Real-time Results** - Instant feedback

## 🎯 Use Cases

1. **Call Center Staffing** - Determine optimal agent counts
2. **SLA Compliance** - Ensure service level targets
3. **Cost Optimization** - Balance staffing vs performance
4. **Capacity Planning** - Handle traffic fluctuations
5. **What-if Analysis** - Test different scenarios

## 🔧 Configuration

### Default Parameters
- **Arrival Rate**: 1.67 calls/minute
- **Service Time**: 5 minutes average
- **Servers**: 12 agents
- **SLA Target**: 80% within 20 seconds
- **Abandonment**: After 10 minutes

### Customizable Settings
- All timing parameters
- Traffic patterns
- Abandonment thresholds
- SLA requirements
- Optimization constraints

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check dependencies
python run_tests.py --check

# Install missing packages
pip install -r requirements.txt
```

### Connection Errors
```bash
# Verify server is running
curl http://localhost:5000/health

# Or use the health check
python run_tests.py --interactive
# Then choose option 4
```

### Import Errors
```bash
# Make sure all files are in the same directory
ls -la *.py

# Check Python version (3.7+ recommended)
python --version
```

## 🚀 Advanced Usage

### Custom API Clients
```python
import requests

# Run simulation
response = requests.post('http://localhost:5000/simulate', json={
    'arrival_rate': 2.5,
    'mean_service_time': 4,
    'num_servers': 15
})

results = response.json()
print(f"SLA: {results['pct_within_sla']:.1f}%")
```

### Batch Processing
```python
from test_server import ErlangCClient

client = ErlangCClient()

# Test multiple scenarios
scenarios = [
    {'arrival_rate': 1.0, 'num_servers': 8},
    {'arrival_rate': 2.0, 'num_servers': 12},
    {'arrival_rate': 3.0, 'num_servers': 18}
]

for scenario in scenarios:
    result = client.run_simulation(**scenario)
    print(f"Scenario {scenario}: SLA = {result['pct_within_sla']:.1f}%")
```

## 📈 Performance

- **Single Simulation**: ~0.5-2 seconds
- **Optimization**: ~5-15 seconds (depends on range)
- **Concurrent Requests**: Supported via Flask
- **Memory Usage**: Low (~50MB typical)

## 🔮 Future Enhancements

- [ ] Web dashboard interface
- [ ] Database integration
- [ ] Historical analysis
- [ ] Real-time monitoring
- [ ] Multi-skill routing
- [ ] Schedule-based staffing

---

**Happy Simulating!** 🎯📊 