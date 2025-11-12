#!/bin/bash
# Script to help upload models to GitHub Releases
# Run this after generating models from the notebook

echo "📦 Preparing models for GitHub Release..."

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "❌ Error: models/ directory not found"
    echo "Please run the notebook to generate models first"
    exit 1
fi

# Check if all model files exist
REQUIRED_FILES=("scaler.pkl" "label_encoders.pkl" "kmeans_model.pkl" "feature_info.pkl" "cluster_profiles.pkl")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "models/$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo "❌ Missing model files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "   - $file"
    done
    echo "Please run the notebook to generate all models"
    exit 1
fi

# Create release directory
RELEASE_DIR="models-release"
mkdir -p "$RELEASE_DIR"

# Copy models
echo "📋 Copying model files..."
cp models/*.pkl "$RELEASE_DIR/"

# Create zip file
echo "📦 Creating zip archive..."
zip -r models-release.zip "$RELEASE_DIR"/*.pkl

echo ""
echo "✅ Models prepared for release!"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/likhitha281/DiabetesHospitalReadmission/releases/new"
echo "2. Create a new release (e.g., tag: v1.0.0-models)"
echo "3. Upload models-release.zip OR upload individual .pkl files"
echo "4. Publish the release"
echo "5. Update MODEL_BASE_URL in api/predict.py or Vercel environment variables"
echo ""
echo "Release URL format will be:"
echo "https://github.com/likhitha281/DiabetesHospitalReadmission/releases/download/v1.0.0-models/{filename}"

