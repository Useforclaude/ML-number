"""
API Application for Phone Number Price Prediction
By Alex - World-Class AI Expert

Supports both FastAPI and Flask
"""
import os
import sys
from typing import List, Dict, Optional
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.prediction import PredictionPipeline, create_prediction_service

# ====================================================================================
# FASTAPI IMPLEMENTATION
# ====================================================================================

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    
    # Pydantic models for request/response
    class PhoneNumberRequest(BaseModel):
        phone_number: str = Field(..., description="Thai phone number")
    
    class BatchPredictionRequest(BaseModel):
        phone_numbers: List[str] = Field(..., description="List of phone numbers")
    
    class PredictionResponse(BaseModel):
        success: bool
        phone_number: str
        predicted_price: Optional[float] = None
        price_range: Optional[Dict[str, float]] = None
        tier: Optional[str] = None
        error: Optional[str] = None
        timestamp: str
    
    # Create FastAPI app
    fastapi_app = FastAPI(
        title="Phone Number Price Prediction API",
        description="AI-powered phone number valuation service by Alex",
        version="1.0.0"
    )
    
    # Add CORS middleware
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize prediction service
    prediction_service = None
    
    @fastapi_app.on_event("startup")
    async def startup_event():
        """Load model on startup"""
        global prediction_service
        
        model_path = os.getenv("MODEL_PATH", "../models/deployed/best_model.pkl")
        
        try:
            prediction_service = create_prediction_service(model_path)
            print("✅ FastAPI: Model loaded successfully")
        except Exception as e:
            print(f"❌ FastAPI: Error loading model: {str(e)}")
    
    @fastapi_app.get("/")
    async def root():
        """API information"""
        return {
            "service": "Phone Number Price Prediction API",
            "version": "1.0.0",
            "model": prediction_service.model_info if prediction_service else "Not loaded",
            "endpoints": {
                "/predict": "Single phone number prediction",
                "/predict_batch": "Batch prediction",
                "/explain": "Prediction explanation",
                "/health": "Service health check"
            }
        }
    
    @fastapi_app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy" if prediction_service else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "model_loaded": prediction_service is not None
        }
    
    @fastapi_app.post("/predict", response_model=PredictionResponse)
    async def predict_single(request: PhoneNumberRequest):
        """Predict price for a single phone number"""
        if not prediction_service:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        result = prediction_service.predict_single(request.phone_number)
        return PredictionResponse(**result)
    
    @fastapi_app.post("/predict_batch")
    async def predict_batch(request: BatchPredictionRequest):
        """Predict prices for multiple phone numbers"""
        if not prediction_service:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        if len(request.phone_numbers) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 phone numbers per request")
        
        result = prediction_service.predict_batch(request.phone_numbers)
        return result
    
    @fastapi_app.post("/explain")
    async def explain_prediction(request: PhoneNumberRequest):
        """Get detailed explanation for prediction"""
        if not prediction_service:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        result = prediction_service.explain_prediction(request.phone_number)
        return result
    
    # Exception handler
    @fastapi_app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(exc),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    FASTAPI_AVAILABLE = True
    
except ImportError:
    print("⚠️ FastAPI not installed. Install with: pip install fastapi uvicorn")
    FASTAPI_AVAILABLE = False

# ====================================================================================
# FLASK IMPLEMENTATION
# ====================================================================================

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    
    # Create Flask app
    flask_app = Flask(__name__)
    CORS(flask_app)
    
    # Initialize prediction service
    flask_prediction_service = None
    
    def init_flask_model():
        """Initialize model for Flask"""
        global flask_prediction_service
        
        model_path = os.getenv("MODEL_PATH", "../models/deployed/best_model.pkl")
        
        try:
            flask_prediction_service = create_prediction_service(model_path)
            print("✅ Flask: Model loaded successfully")
        except Exception as e:
            print(f"❌ Flask: Error loading model: {str(e)}")
    
    @flask_app.route("/")
    def flask_root():
        """API information"""
        return jsonify({
            "service": "Phone Number Price Prediction API (Flask)",
            "version": "1.0.0",
            "model": flask_prediction_service.model_info if flask_prediction_service else "Not loaded",
            "endpoints": {
                "/predict": "Single phone number prediction (POST)",
                "/predict_batch": "Batch prediction (POST)",
                "/explain": "Prediction explanation (POST)",
                "/health": "Service health check (GET)"
            }
        })
    
    @flask_app.route("/health")
    def flask_health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy" if flask_prediction_service else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "model_loaded": flask_prediction_service is not None
        })
    
    @flask_app.route("/predict", methods=["POST"])
    def flask_predict():
        """Predict price for a single phone number"""
        if not flask_prediction_service:
            return jsonify({"error": "Model not loaded"}), 503
        
        data = request.get_json()
        
        if not data or "phone_number" not in data:
            return jsonify({"error": "phone_number required"}), 400
        
        result = flask_prediction_service.predict_single(data["phone_number"])
        return jsonify(result)
    
    @flask_app.route("/predict_batch", methods=["POST"])
    def flask_predict_batch():
        """Predict prices for multiple phone numbers"""
        if not flask_prediction_service:
            return jsonify({"error": "Model not loaded"}), 503
        
        data = request.get_json()
        
        if not data or "phone_numbers" not in data:
            return jsonify({"error": "phone_numbers array required"}), 400
        
        if len(data["phone_numbers"]) > 100:
            return jsonify({"error": "Maximum 100 phone numbers per request"}), 400
        
        result = flask_prediction_service.predict_batch(data["phone_numbers"])
        return jsonify(result)
    
    @flask_app.route("/explain", methods=["POST"])
    def flask_explain():
        """Get detailed explanation for prediction"""
        if not flask_prediction_service:
            return jsonify({"error": "Model not loaded"}), 503
        
        data = request.get_json()
        
        if not data or "phone_number" not in data:
            return jsonify({"error": "phone_number required"}), 400
        
        result = flask_prediction_service.explain_prediction(data["phone_number"])
        return jsonify(result)
    
    @flask_app.errorhandler(Exception)
    def flask_handle_exception(e):
        """Handle exceptions"""
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500
    
    FLASK_AVAILABLE = True
    
except ImportError:
    print("⚠️ Flask not installed. Install with: pip install flask flask-cors")
    FLASK_AVAILABLE = False

# ====================================================================================
# CREATE APP FUNCTION
# ====================================================================================

def create_app(framework="fastapi"):
    """
    Create API application
    
    Parameters:
    -----------
    framework : str
        'fastapi' or 'flask'
    
    Returns:
    --------
    app : FastAPI or Flask app
    """
    if framework.lower() == "fastapi":
        if not FASTAPI_AVAILABLE:
            raise ImportError("FastAPI not available. Install with: pip install fastapi uvicorn")
        return fastapi_app
    
    elif framework.lower() == "flask":
        if not FLASK_AVAILABLE:
            raise ImportError("Flask not available. Install with: pip install flask flask-cors")
        
        # Initialize Flask model
        init_flask_model()
        return flask_app
    
    else:
        raise ValueError(f"Unknown framework: {framework}. Choose 'fastapi' or 'flask'")

# ====================================================================================
# RUN SERVERS
# ====================================================================================

def run_fastapi(host="0.0.0.0", port=8000):
    """Run FastAPI server"""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI not available")
        return
    
    try:
        import uvicorn
        print(f"🚀 Starting FastAPI server on http://{host}:{port}")
        print("📖 API documentation available at http://localhost:8000/docs")
        uvicorn.run(fastapi_app, host=host, port=port)
    except ImportError:
        print("❌ Uvicorn not installed. Install with: pip install uvicorn")

def run_flask(host="0.0.0.0", port=5000, debug=False):
    """Run Flask server"""
    if not FLASK_AVAILABLE:
        print("❌ Flask not available")
        return
    
    # Initialize model
    init_flask_model()
    
    print(f"🚀 Starting Flask server on http://{host}:{port}")
    flask_app.run(host=host, port=port, debug=debug)

# ====================================================================================
# MAIN
# ====================================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Phone Number Price Prediction API")
    parser.add_argument(
        "--framework", 
        choices=["fastapi", "flask"], 
        default="fastapi",
        help="Web framework to use"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (Flask only)")
    
    args = parser.parse_args()
    
    if args.framework == "fastapi":
        run_fastapi(host=args.host, port=args.port)
    else:
        run_flask(host=args.host, port=args.port, debug=args.debug)
