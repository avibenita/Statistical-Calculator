#!/bin/bash

# Google Cloud Functions Deployment Script for Erlang C Server
# Make sure you have gcloud CLI installed and authenticated

# Configuration
FUNCTION_NAME="erlang-c-server"
REGION="us-central1"  # Change this to your preferred region
RUNTIME="python39"
MEMORY="512MB"
TIMEOUT="540s"

echo "🚀 Deploying Erlang C Server to Google Cloud Functions..."
echo "Function Name: $FUNCTION_NAME"
echo "Region: $REGION"
echo "Runtime: $RUNTIME"
echo ""

# Deploy the function
gcloud functions deploy $FUNCTION_NAME \
    --runtime $RUNTIME \
    --trigger-http \
    --allow-unauthenticated \
    --memory $MEMORY \
    --timeout $TIMEOUT \
    --region $REGION \
    --entry-point erlang_c_server \
    --source . \
    --project $(gcloud config get-value project)

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "📝 Function URL:"
    gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(httpsTrigger.url)"
    echo ""
    echo "📋 Test your function:"
    FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(httpsTrigger.url)")
    echo "Health check: curl \"$FUNCTION_URL/health\""
    echo "Simulation: curl -X POST \"$FUNCTION_URL/simulate\" -H \"Content-Type: application/json\" -d '{\"arrival_rate\": 1.67, \"mean_service_time\": 5, \"num_servers\": 12}'"
    echo ""
    echo "🌐 Update your frontend to use this URL instead of localhost:5000"
else
    echo ""
    echo "❌ Deployment failed!"
    echo "Please check the error messages above and try again."
fi 