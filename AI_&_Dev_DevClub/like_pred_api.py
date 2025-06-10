from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from datetime import datetime
import re
from textblob import TextBlob
import emoji
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for models and encoders
model_low = None
model_mid = None
model_high = None
company_map = None
username_map = None
company_stats = None
tfidf_vectorizer = None
scaler = None

# Load models and encoders
try:
    model_low = joblib.load('like_predictor1.pkl')
    model_mid = joblib.load('like_predictor2.pkl')
    model_high = joblib.load('like_predictor3.pkl')
    logger.info("Models loaded successfully")
    
    company_map = joblib.load("company_encoder.pkl")
    username_map = joblib.load("username_encoder.pkl")
    company_stats = joblib.load('company_stats.pkl')
    tfidf_vectorizer = joblib.load('tfidf_df.pkl')  
    scaler = joblib.load('scaler.pkl')
    logger.info("Encoders and stats loaded successfully")
except Exception as e:
    logger.error(f"Error loading models: {e}")
    raise

PROMO_WORDS = ['buy', 'sale', 'discount', 'offer', 'deal', 'shop']

entity_list = [
    'canada', 'toyota', 'china', 'cisco', 'hong kong', 'us', 'u.s.',
    'india', 'cnn', 'america', 'uk', 'toronto', 'london', 'senate',
    'ottawa', 'florida', 'buhari', 'ibm', 'new york', 'congress', 'russia',
    'australia', 'qatar', 'microsoft', 'california', 'washington', 'texas',
    'liverpool', 'the united states', 'japan', 'supreme court', 'the white house',
    'un', 'paris', 'iran', 'b.c.', 'france', 'fbi', 'georgia', 'germany',
    'gop', 'chicago', 'south africa', 'houston', 'italy', 'white house',
    'new zealand', 'doha'
]

def extract_time_features(created_at):
    """Extract time-based features from datetime string"""
    try:
        dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")    
        return np.array([dt.year, dt.month, dt.hour, dt.weekday()])  # 0 = Monday
    except ValueError as e:
        logger.error(f"Error parsing datetime: {e}")
        # Return current datetime features as fallback
        dt = datetime.now()
        return np.array([dt.year, dt.month, dt.hour, dt.weekday()])

def extract_text_features(content):
    """Extract text-based features from content"""
    words = content.split()
    tb = TextBlob(content)
    sentiment = tb.sentiment
    
    return np.array([
        len(words),                                                    # word count
        len(content),                                                  # character count
        sum(word.lower() in PROMO_WORDS for word in words),          # promo words count
        int(re.search(r'http[s]?://', content) is not None),         # has URL
        content.count("#"),                                           # hashtag count
        content.count("@"),                                           # mention count
        sentiment.polarity,                                           # sentiment polarity
        sentiment.subjectivity                                        # sentiment subjectivity
    ])

def emojicnt(content):
    """Count emojis in content"""
    return np.array([sum(1 for ch in content if ch in emoji.EMOJI_DATA)])

def extract_entity_features(content):
    """Extract entity-based features from content"""
    lowered = content.lower()
    entity_flags = []

    for entity in entity_list:
        pattern = r'\b' + re.escape(entity) + r'\b'
        match = int(bool(re.search(pattern, lowered)))
        entity_flags.append(match)

    entity_count = sum(entity_flags)
    return np.array([entity_count] + entity_flags)

def encode_categorical(company, username):
    """Encode categorical variables with unknown handling"""
    # Handle unknown companies
    if company not in company_map.classes_:
        company_encoded = 0  # Use 0 for unknown
        logger.info(f"Unknown company: {company}, using default encoding")
    else:
        company_encoded = company_map.transform([company])[0]
    
    # Handle unknown usernames
    if username not in username_map.classes_:
        username_encoded = 0  # Use 0 for unknown
        logger.info(f"Unknown username: {username}, using default encoding")
    else:
        username_encoded = username_map.transform([username])[0]
    
    return np.array([company_encoded, username_encoded])

def get_company_features(company_name):
    """Get company-specific statistical features"""
    stats = company_stats.get(company_name)
    if stats:
        return np.array([stats['company_avg_likes'], stats['historical_performance']])
    else:
        # Return default values for unknown companies
        return np.array([0.0, 0.0])

def get_tfidf_features_fallback(content, expected_size=501):
    """
    Fallback TF-IDF feature extraction when vectorizer is not working
    This creates a simple bag-of-words representation
    """
    try:
        # If tfidf_vectorizer is actually a sklearn vectorizer
        if hasattr(tfidf_vectorizer, 'transform') and callable(getattr(tfidf_vectorizer, 'transform')):
            tfidf_matrix = tfidf_vectorizer.transform([content])
            tfidf_array = tfidf_matrix.toarray()
            if tfidf_array.shape[0] > 0:
                logger.info(f"TF-IDF features extracted: {tfidf_array.shape[1]} features")
                return tfidf_array[0]
        
        # If tfidf_vectorizer is a DataFrame with columns
        elif hasattr(tfidf_vectorizer, 'columns'):
            # Create zero vector with same dimensions as the DataFrame
            num_features = len(tfidf_vectorizer.columns)
            logger.info(f"Creating zero TF-IDF vector from DataFrame with {num_features} features")
            
            # Simple word-based features (basic TF-IDF approximation)
            words = content.lower().split()
            feature_vector = np.zeros(num_features)
            
            # Try to match some common words to DataFrame columns if possible
            for i, col in enumerate(tfidf_vectorizer.columns[:min(50, len(words))]):
                if str(col) in words:
                    feature_vector[i] = 1.0
            
            return feature_vector
        
        # Fallback: create zero vector of expected size
        else:
            logger.warning(f"Using fallback TF-IDF with {expected_size} zero features")
            return np.zeros(expected_size)
            
    except Exception as e:
        logger.error(f"Error in TF-IDF transformation: {e}")
        # Ultimate fallback
        return np.zeros(expected_size)

def extract_features(data):
    """
    Robust feature extraction that handles dimension mismatches
    """
    content = data["content"]
    company = data.get("company", "").strip()
    username = data["username"]
    created_at = data["created_at"]
    has_media = data.get("has_media", 0)
    
    if not company:
        company = "unknown"
    
    features = []
    
    # 1. Media feature (1 feature)
    features.extend([int(has_media)])
    
    # 2. Time features (4 features)
    time_features = extract_time_features(created_at)
    features.extend(time_features)
    
    # 3. Text features (8 features)
    text_features = extract_text_features(content)
    features.extend(text_features)
    
    # 4. Entity features (1 + 47 = 48 features for the entity list)
    entity_features = extract_entity_features(content)
    features.extend(entity_features)
    
    # 5. Categorical features (2 features)
    categorical_features = encode_categorical(company, username)
    features.extend(categorical_features)
    
    # 6. Emoji count (1 feature)
    emoji_features = emojicnt(content)
    features.extend(emoji_features)
    
    # 7. Company features (2 features)
    company_features = get_company_features(company)
    features.extend(company_features)
    
    current_feature_count = len(features)
    logger.info(f"Non-TF-IDF features: {current_feature_count}")
    
    # 8. TF-IDF features (remaining features to reach 568)
    target_total = 568  # Your scaler expects this many
    expected_tfidf_size = target_total - current_feature_count
    
    tfidf_features = get_tfidf_features_fallback(content, expected_tfidf_size)
    
    if tfidf_features is None or len(tfidf_features) != expected_tfidf_size:
        actual_size = 0 if tfidf_features is None else len(tfidf_features)
        logger.warning(f"TF-IDF size mismatch. Expected: {expected_tfidf_size}, Got: {actual_size}")
        # Handle None case
        if tfidf_features is None:
            tfidf_features = np.zeros(expected_tfidf_size)
        elif len(tfidf_features) > expected_tfidf_size:
            tfidf_features = tfidf_features[:expected_tfidf_size]
        else:
            # Pad with zeros
            padding = np.zeros(expected_tfidf_size - len(tfidf_features))
            tfidf_features = np.concatenate([tfidf_features, padding])
    
    features.extend(tfidf_features)
    
    logger.info(f"Total features: {len(features)} (target: {target_total})")
    
    # Final check and adjustment
    if len(features) != target_total:
        logger.warning(f"Feature count mismatch! Got {len(features)}, expected {target_total}")
        if len(features) > target_total:
            features = features[:target_total]
        else:
            features.extend([0.0] * (target_total - len(features)))
    
    return np.array(features).reshape(1, -1)

def get_best_prediction(features):
    """Get best prediction from the three models"""
    # Like category thresholds
    LOW_THRESHOLD = 4434.06 
    HIGH_THRESHOLD = 52504.24
    
    # Get predictions from all models
    pred_low = model_low.predict(features)[0]
    pred_mid = model_mid.predict(features)[0] 
    pred_high = model_high.predict(features)[0]
    
    predictions = [pred_low, pred_mid, pred_high]


    best_prediction = 0
    v1 = 0 
    v2 = 0
    if pred_mid <= 15000 :
        if pred_mid <= 5500 :
            if pred_low <= 150 :
                best_prediction = 0.9*pred_low + 0.1*pred_mid
            else :
                best_prediction = 0.4*pred_low + 0.6*pred_mid
                
        elif pred_mid <= 10000 :
            if pred_low <= 500 :
                best_prediction = 0.8*pred_low + 0.2*pred_mid
            else :
                best_prediction = 0.4*pred_low + 0.6*pred_mid
        else :
            best_prediction = 0.8*pred_mid + 0.2*pred_low
            
        v1 = pred_low 
        v2 = pred_mid
    else :
        if pred_mid >= 45000 :
            best_prediction = 0.7*pred_high + 0.3*pred_mid
        else :
            if pred_mid <= 25000 :
                best_prediction = 0.8*pred_mid + 0.2* pred_high
            elif pred_mid <= 35000 :
                best_prediction = 0.7*pred_mid + 0.3* pred_high
            else :
                best_prediction = 0.6*pred_mid + 0.4* pred_high
            
        v1 = pred_mid
        v2 = pred_high
        
    logger.info(f"Model predictions - Low: {pred_low:.2f}, Mid: {pred_mid:.2f}, High: {pred_high:.2f}")


    return max(0, int(round(best_prediction))), int(round(v1)), int(round(v2))


@app.route('/')
def home():
    return render_template('wp.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content', 'username', 'created_at']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        logger.info(f"Processing prediction request: {data}")
        
        # Extract features
        features = extract_features(data)
        logger.info(f"Extracted features shape: {features.shape}")
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        predicted_likes, v1, v2 = get_best_prediction(features_scaled)

        return jsonify({
        'predicted_likes': int(predicted_likes),
        'v1': int(v1),
        'v2': int(v2)
        })

        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)