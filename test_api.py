"""
Test script for Thyroid Cancer Detection API
"""
import requests
import base64
import json
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
API_V1_URL = f"{API_BASE_URL}/api/v1"


def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    response = requests.get(f"{API_V1_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*50)
    print("Testing Model Info Endpoint")
    print("="*50)
    
    response = requests.get(f"{API_V1_URL}/model-info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_predict(image_path: str):
    """Test prediction endpoint"""
    print("\n" + "="*50)
    print("Testing Prediction Endpoint")
    print("="*50)
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    # Encode image
    image_base64 = encode_image_to_base64(image_path)
    
    # Make request
    payload = {
        "image": image_base64,
        "filename": Path(image_path).name
    }
    
    response = requests.post(f"{API_V1_URL}/predict", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n📊 Prediction Results:")
        print(f"  Class: {result['prediction']['class']}")
        print(f"  Label: {result['prediction']['label']}")
        print(f"  Confidence: {result['prediction']['confidence_percentage']:.2f}%")
        print(f"  Risk Assessment: {result['risk_assessment']}")
        print(f"  Recommendation: {result['recommendation']}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False


def test_gradcam(image_path: str, save_output: bool = True):
    """Test Grad-CAM endpoint"""
    print("\n" + "="*50)
    print("Testing Grad-CAM Endpoint")
    print("="*50)
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    # Encode image
    image_base64 = encode_image_to_base64(image_path)
    
    # Make request
    payload = {
        "image": image_base64,
        "filename": Path(image_path).name
    }
    
    response = requests.post(f"{API_V1_URL}/gradcam", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n🔍 Grad-CAM Results:")
        print(f"  Layer Used: {result['layer_used']}")
        print(f"  Prediction: {result['prediction']['label']}")
        print(f"  Confidence: {result['prediction']['confidence_score']:.4f}")
        
        if save_output:
            # Save Grad-CAM images
            from PIL import Image
            import io
            
            output_dir = Path("test_outputs")
            output_dir.mkdir(exist_ok=True)
            
            for img_type in ['original', 'heatmap', 'overlay']:
                img_data = base64.b64decode(result['images'][img_type])
                img = Image.open(io.BytesIO(img_data))
                output_path = output_dir / f"gradcam_{img_type}.png"
                img.save(output_path)
                print(f"  Saved: {output_path}")
        
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False


def test_analyze(image_path: str, include_gradcam: bool = True):
    """Test complete analysis endpoint"""
    print("\n" + "="*50)
    print("Testing Complete Analysis Endpoint")
    print("="*50)
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    # Encode image
    image_base64 = encode_image_to_base64(image_path)
    
    # Make request
    payload = {
        "image": image_base64,
        "filename": Path(image_path).name,
        "include_gradcam": include_gradcam
    }
    
    response = requests.post(f"{API_V1_URL}/analyze", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n📊 Complete Analysis Results:")
        print(f"  Classification: {result['prediction']['label']}")
        print(f"  Confidence: {result['prediction']['confidence_percentage']:.2f}%")
        print(f"  Risk: {result['risk_assessment']}")
        print(f"  Recommendation: {result['recommendation']}")
        
        if result.get('gradcam'):
            print(f"  Grad-CAM included: Yes (Layer: {result['gradcam']['layer_used']})")
        else:
            print(f"  Grad-CAM included: No")
        
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🦋 THYROID CANCER DETECTION API - TEST SUITE")
    print("="*60)
    
    # Test basic endpoints
    print("\n📋 Testing Basic Endpoints...")
    health_ok = test_health()
    model_info_ok = test_model_info()
    
    if not (health_ok and model_info_ok):
        print("\n❌ Basic tests failed. Please ensure the API server is running:")
        print("   python app.py")
        return
    
    # Test with image (if available)
    print("\n📸 Testing Image Analysis Endpoints...")
    
    # Look for test images
    test_image_paths = [
        "test_image.jpg",
        "test_image.png",
        "thyroid_scan.jpg",
        "sample.jpg"
    ]
    
    image_path = None
    for path in test_image_paths:
        if Path(path).exists():
            image_path = path
            break
    
    if image_path:
        print(f"\nUsing test image: {image_path}")
        test_predict(image_path)
        test_gradcam(image_path, save_output=True)
        test_analyze(image_path, include_gradcam=True)
    else:
        print("\n⚠️  No test images found. Skipping image analysis tests.")
        print("   To test with images, place a test image in the project directory")
        print(f"   Supported names: {', '.join(test_image_paths)}")
    
    print("\n" + "="*60)
    print("✅ Test Suite Completed!")
    print("="*60)
    print(f"\nAPI Documentation: {API_BASE_URL}/docs")
    print(f"Alternative Docs: {API_BASE_URL}/redoc")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("   Please ensure the API server is running:")
        print("   python app.py")
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
