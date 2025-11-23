from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scorer import calculate_overall_score
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200


@app.route('/score', methods=['POST'])
def score_transcript():
    try:
        data = request.get_json()
        
        if not data or 'transcript' not in data:
            return jsonify({'error': 'Transcript is required'}), 400
        
        transcript = data['transcript'].strip()
        
        if not transcript:
            return jsonify({'error': 'Transcript cannot be empty'}), 400
        
        duration = data.get('duration', None)
        
        result = calculate_overall_score(transcript, duration)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
