# Erlang C Server - Google Cloud Functions Deployment

This guide helps you deploy the Erlang C simulation server to Google Cloud Functions.

## 📋 Prerequisites

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud CLI**: Install from [cloud.google.com/sdk](https://cloud.google.com/sdk)
3. **Project Setup**: Create a Google Cloud project

## 🚀 Quick Deployment

### 1. Authenticate with Google Cloud
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs
```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Deploy the Function
```bash
# Make the deployment script executable
chmod +x deploy.sh

# Run the deployment
./deploy.sh
```

### 4. Get Your Function URL
After successful deployment, the script will show your function URL. It will look like:
```
https://us-central1-YOUR_PROJECT.cloudfunctions.net/erlang-c-server
```

## 🔧 Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
gcloud functions deploy erlang-c-server \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --memory 512MB \
    --timeout 540s \
    --region us-central1 \
    --entry-point erlang_c_server \
    --source .
```

## 🌐 Update Your Frontend

Replace the localhost URL in your HTML file:

**Old (local):**
```javascript
const response = await fetch('http://localhost:5000/simulate', {
```

**New (cloud):**
```javascript
const response = await fetch('https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/erlang-c-server/simulate', {
```

## 🧪 Testing Your Deployment

### Health Check
```bash
curl "https://YOUR_FUNCTION_URL/health"
```

### Simulation Test
```bash
curl -X POST "https://YOUR_FUNCTION_URL/simulate" \
     -H "Content-Type: application/json" \
     -d '{
       "arrival_rate": 1.67,
       "mean_service_time": 5,
       "num_servers": 12,
       "sim_time": 1000,
       "sla_target_pct": 80,
       "sla_threshold_seconds": 20
     }'
```

### Optimization Test
```bash
curl -X POST "https://YOUR_FUNCTION_URL/optimize" \
     -H "Content-Type: application/json" \
     -d '{
       "arrival_rate": 1.67,
       "mean_service_time": 5,
       "target_service_level": 80,
       "sla_threshold_seconds": 20
     }'
```

## 📊 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server information |
| `/health` | GET | Health check |
| `/simulate` | POST | Run simulation |
| `/optimize` | POST | Find minimum agents |

## 🔍 Monitoring and Logs

View function logs:
```bash
gcloud functions logs read erlang-c-server --region us-central1
```

View real-time logs:
```bash
gcloud functions logs tail erlang-c-server --region us-central1
```

## 💰 Cost Considerations

- **Free Tier**: 2 million invocations, 400,000 GB-seconds per month
- **Typical Cost**: $0.0000004 per invocation + $0.0000025 per GB-second
- **Your Usage**: For simulation workloads, expect ~$0.001-0.01 per simulation

## 🔧 Configuration Options

### Memory Settings
- **256MB**: Basic simulations (< 1000 customers)
- **512MB**: Standard simulations (recommended)
- **1GB**: Large simulations (> 10,000 customers)

### Timeout Settings
- **60s**: Quick simulations
- **540s**: Complex simulations (maximum for HTTP functions)

### Environment Variables
Set environment variables if needed:
```bash
gcloud functions deploy erlang-c-server \
    --set-env-vars RANDOM_SEED=42,MAX_SIMULATION_TIME=2000
```

## 🔒 Security

The function is deployed with `--allow-unauthenticated` for public access. For production:

1. **Remove public access**:
   ```bash
   gcloud functions remove-iam-policy-binding erlang-c-server \
       --member="allUsers" \
       --role="roles/cloudfunctions.invoker"
   ```

2. **Add specific users**:
   ```bash
   gcloud functions add-iam-policy-binding erlang-c-server \
       --member="user:your-email@domain.com" \
       --role="roles/cloudfunctions.invoker"
   ```

## 🆘 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **APIs Not Enabled**
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

3. **Function Timeout**
   - Increase timeout: `--timeout 540s`
   - Increase memory: `--memory 1GB`

4. **CORS Issues**
   - The function includes CORS headers
   - Make sure you're using the correct URL

### Debug Mode
For detailed logs, check the Cloud Console:
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Navigate to Cloud Functions
3. Click on your function
4. View logs and metrics

## 🔄 Updates

To update your function:
1. Make changes to `main.py`
2. Run `./deploy.sh` again
3. Test the updated function

The deployment will automatically replace the existing function with zero downtime.

## 📞 Support

If you encounter issues:
1. Check the [Cloud Functions documentation](https://cloud.google.com/functions/docs)
2. View function logs for error details
3. Test locally first before deploying
4. Ensure all dependencies are in `requirements.txt`

## 🎯 Next Steps

1. **Custom Domain**: Set up a custom domain for your function
2. **Authentication**: Add authentication for production use
3. **Monitoring**: Set up alerts for function performance
4. **CI/CD**: Automate deployment with Cloud Build 