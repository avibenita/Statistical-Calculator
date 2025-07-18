#!/bin/bash

# Erlang C Server - Quick Start Deployment Script
# This script guides you through the entire deployment process

echo "🚀 Erlang C Server - Google Cloud Functions Quick Start"
echo "======================================================"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI is not installed."
    echo "📥 Please install it from: https://cloud.google.com/sdk"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ Google Cloud CLI found"

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "🔐 Not authenticated with Google Cloud. Let's fix that..."
    gcloud auth login
else
    echo "✅ Already authenticated with Google Cloud"
fi

# Get current project or ask user to set one
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)

if [ -z "$CURRENT_PROJECT" ]; then
    echo ""
    echo "📝 No project set. Let's configure one..."
    echo "   Available projects:"
    gcloud projects list --format="table(projectId,name)"
    echo ""
    read -p "Enter your project ID: " PROJECT_ID
    gcloud config set project "$PROJECT_ID"
    CURRENT_PROJECT="$PROJECT_ID"
else
    echo "✅ Using project: $CURRENT_PROJECT"
    echo ""
    read -p "Continue with this project? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        echo "   Available projects:"
        gcloud projects list --format="table(projectId,name)"
        echo ""
        read -p "Enter your project ID: " PROJECT_ID
        gcloud config set project "$PROJECT_ID"
        CURRENT_PROJECT="$PROJECT_ID"
    fi
fi

echo ""
echo "🔧 Enabling required APIs..."

# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet

if [ $? -eq 0 ]; then
    echo "✅ APIs enabled successfully"
else
    echo "❌ Failed to enable APIs. Please check permissions."
    exit 1
fi

echo ""
echo "📦 Checking files..."

# Check if required files exist
REQUIRED_FILES=("main.py" "requirements.txt")
for FILE in "${REQUIRED_FILES[@]}"; do
    if [ -f "$FILE" ]; then
        echo "✅ $FILE found"
    else
        echo "❌ $FILE not found"
        echo "   Make sure you're in the correct directory with all deployment files."
        exit 1
    fi
done

echo ""
echo "🚀 Deploying to Google Cloud Functions..."
echo "   This may take a few minutes..."

# Make deploy script executable and run it
chmod +x deploy.sh
./deploy.sh

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment successful!"
    
    # Get the function URL
    FUNCTION_URL=$(gcloud functions describe erlang-c-server --region=us-central1 --format="value(httpsTrigger.url)" 2>/dev/null)
    
    if [ -n "$FUNCTION_URL" ]; then
        echo ""
        echo "🌐 Your function is available at:"
        echo "   $FUNCTION_URL"
        echo ""
        
        # Ask if user wants to test the deployment
        read -p "🧪 Would you like to test the deployment now? (y/n): " TEST_NOW
        if [ "$TEST_NOW" = "y" ] || [ "$TEST_NOW" = "Y" ]; then
            if command -v python3 &> /dev/null; then
                echo ""
                echo "🔍 Running tests..."
                python3 test_cloud_function.py "$FUNCTION_URL"
            elif command -v python &> /dev/null; then
                echo ""
                echo "🔍 Running tests..."
                python test_cloud_function.py "$FUNCTION_URL"
            else
                echo "❌ Python not found. You can test manually:"
                echo "   curl \"$FUNCTION_URL/health\""
            fi
        fi
        
        echo ""
        echo "📋 Next Steps:"
        echo "1. Update your frontend HTML file"
        echo "2. Replace 'http://localhost:5000' with '$FUNCTION_URL'"
        echo "3. Test your application"
        echo ""
        echo "📚 For more details, see CLOUD_DEPLOYMENT.md"
        
    else
        echo "⚠️  Function deployed but URL retrieval failed."
        echo "   Check the Cloud Console: https://console.cloud.google.com/functions"
    fi
    
else
    echo ""
    echo "❌ Deployment failed!"
    echo "   Check the error messages above."
    echo "   Common issues:"
    echo "   - Insufficient permissions"
    echo "   - Billing not enabled"
    echo "   - API quota exceeded"
    echo ""
    echo "📞 For help, see CLOUD_DEPLOYMENT.md"
fi 