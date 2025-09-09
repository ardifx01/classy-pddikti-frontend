from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime
import os
import urllib.parse

app = Flask(__name__)

# Configuration
API_BASE_URL = "https://api-pddikti.ridwaanhall.com"
API_HEADERS = {
    'User-Agent': 'PDDikti-Flask-App/1.0',
    'Accept': 'application/json'
}

class PDDiktiAPI:
    """PDDikti API Client - FIXED VERSION"""
    
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(API_HEADERS)
        self.session.timeout = 30  # Add timeout
    
    def get_api_status(self):
        """Get API status and information"""
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            return {"error": str(e)}
    
    def search_mahasiswa(self, query, limit=20):
        """Search students by name - FIXED ENDPOINT"""
        try:
            # URL encode the query to handle special characters
            encoded_query = urllib.parse.quote(query.strip())
            url = f"{self.base_url}/search/mhs/{encoded_query}/"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Apply limit if there are more results than requested
                if 'data' in data and isinstance(data['data'], list):
                    if len(data['data']) > limit:
                        data['data'] = data['data'][:limit]
                return data
            else:
                return {"error": f"HTTP {response.status_code}: Data tidak ditemukan"}
                
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def search_dosen(self, query, limit=20):
        """Search lecturers by name - FIXED ENDPOINT"""
        try:
            encoded_query = urllib.parse.quote(query.strip())
            url = f"{self.base_url}/search/dosen/{encoded_query}/"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and isinstance(data['data'], list):
                    if len(data['data']) > limit:
                        data['data'] = data['data'][:limit]
                return data
            else:
                return {"error": f"HTTP {response.status_code}: Data tidak ditemukan"}
                
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def search_prodi(self, query, limit=20):
        """Search study programs - FIXED ENDPOINT"""
        try:
            encoded_query = urllib.parse.quote(query.strip())
            url = f"{self.base_url}/search/prodi/{encoded_query}/"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and isinstance(data['data'], list):
                    if len(data['data']) > limit:
                        data['data'] = data['data'][:limit]
                return data
            else:
                return {"error": f"HTTP {response.status_code}: Data tidak ditemukan"}
                
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def search_pt(self, query, limit=20):
        """Search universities - FIXED ENDPOINT"""
        try:
            encoded_query = urllib.parse.quote(query.strip())
            url = f"{self.base_url}/search/pt/{encoded_query}/"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and isinstance(data['data'], list):
                    if len(data['data']) > limit:
                        data['data'] = data['data'][:limit]
                return data
            else:
                return {"error": f"HTTP {response.status_code}: Data tidak ditemukan"}
                
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def search_all(self, query, limit=20):
        """Search all categories - NEW METHOD"""
        try:
            encoded_query = urllib.parse.quote(query.strip())
            url = f"{self.base_url}/search/all/{encoded_query}/"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Apply limit to each category if needed
                if 'data' in data and isinstance(data['data'], dict):
                    for category in data['data']:
                        if isinstance(data['data'][category], list) and len(data['data'][category]) > limit:
                            data['data'][category] = data['data'][category][:limit]
                return data
            else:
                return {"error": f"HTTP {response.status_code}: Data tidak ditemukan"}
                
        except Exception as e:
            return {"error": f"Error: {str(e)}"}
    
    def get_mahasiswa_detail(self, id_mhs):
        """Get student details by ID - FIXED ENDPOINT"""
        try:
            url = f"{self.base_url}/mhs/detail/{id_mhs}/"
            response = self.session.get(url)
            return response.json() if response.status_code == 200 else {"error": "Data tidak ditemukan"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_dosen_detail(self, id_dosen):
        """Get lecturer details by ID - FIXED ENDPOINT"""
        try:
            url = f"{self.base_url}/dosen/profile/{id_dosen}/"
            response = self.session.get(url)
            return response.json() if response.status_code == 200 else {"error": "Data tidak ditemukan"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_prodi_detail(self, id_prodi):
        """Get program study details by ID - NEW METHOD"""
        try:
            url = f"{self.base_url}/prodi/detail/{id_prodi}/"
            response = self.session.get(url)
            return response.json() if response.status_code == 200 else {"error": "Data tidak ditemukan"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_pt_detail(self, id_pt):
        """Get university details by ID - NEW METHOD"""
        try:
            url = f"{self.base_url}/pt/detail/{id_pt}/"
            response = self.session.get(url)
            return response.json() if response.status_code == 200 else {"error": "Data tidak ditemukan"}
        except Exception as e:
            return {"error": str(e)}

# Initialize API client
api_client = PDDiktiAPI()

@app.route('/')
def index():
    """Main dashboard"""
    api_status = api_client.get_api_status()
    return render_template('index.html', api_status=api_status, current_year=datetime.now().year)

@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for search - IMPROVED VERSION"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
            
        search_type = data.get('type', 'mahasiswa')
        query = data.get('query', '').strip()
        limit = min(int(data.get('limit', 20)), 100)  # Max 100 results
        
        if not query:
            return jsonify({"error": "Query tidak boleh kosong"}), 400
        
        if len(query) < 2:
            return jsonify({"error": "Query minimal 2 karakter"}), 400
        
        print(f"API Search - Type: {search_type}, Query: '{query}', Limit: {limit}")
        
        # Perform search based on type
        result = None
        if search_type == 'mahasiswa':
            result = api_client.search_mahasiswa(query, limit)
        elif search_type == 'dosen':
            result = api_client.search_dosen(query, limit)
        elif search_type == 'prodi':
            result = api_client.search_prodi(query, limit)
        elif search_type == 'pt':
            result = api_client.search_pt(query, limit)
        elif search_type == 'all':
            result = api_client.search_all(query, limit)
        else:
            return jsonify({"error": "Tipe pencarian tidak valid"}), 400
        
        print(f"API Search Result: {result}")
        
        if 'error' in result:
            return jsonify(result), 500
        
        # Ensure we always return the same format to frontend
        if 'data' in result:
            # Backend already formatted it correctly
            return jsonify(result)
        else:
            # If backend returned raw data, wrap it
            return jsonify({
                "data": result if isinstance(result, list) else [],
                "total": len(result) if isinstance(result, list) else 0,
                "query": query
            })
        
    except Exception as e:
        print(f"API Search Exception: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/detail', methods=['POST'])
def api_detail():
    """API endpoint for getting details - IMPROVED VERSION"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
            
        detail_type = data.get('type', 'mahasiswa')
        identifier = data.get('id', '').strip()
        
        if not identifier:
            return jsonify({"error": "ID tidak boleh kosong"}), 400
        
        # Get details based on type (only mahasiswa and dosen)
        result = None
        if detail_type == 'mahasiswa':
            result = api_client.get_mahasiswa_detail(identifier)
        elif detail_type == 'dosen':
            result = api_client.get_dosen_detail(identifier)
        else:
            return jsonify({"error": "Hanya detail mahasiswa dan dosen yang tersedia"}), 400
        
        if 'error' in result:
            return jsonify(result), 404
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', current_year=datetime.now().year)

@app.route('/api/status')
def api_status():
    """Get API status"""
    status = api_client.get_api_status()
    return jsonify(status)

@app.route('/api/test/<search_type>/<query>')
def api_test(search_type, query):
    """Test endpoint for debugging"""
    if search_type == 'mahasiswa':
        result = api_client.search_mahasiswa(query, 5)
    elif search_type == 'dosen':
        result = api_client.search_dosen(query, 5)
    elif search_type == 'prodi':
        result = api_client.search_prodi(query, 5)
    elif search_type == 'pt':
        result = api_client.search_pt(query, 5)
    else:
        result = {"error": "Invalid search type"}
    
    return jsonify(result)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad request"}), 400

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("Starting PDDikti Flask Application...")
    print(f"API Base URL: {API_BASE_URL}")
    print("Available routes:")
    print("  / - Home page")
    print("  /search - Search page") 
    print("  /about - About page")
    print("  /api/search - Search API endpoint")
    print("  /api/detail - Detail API endpoint")
    print("  /api/status - API status")
    print("  /api/test/<type>/<query> - Test endpoint")
    print("  /api/debug/<type>/<query> - Debug endpoint with encoding tests")
    print("\nTo debug your issue, try:")
    print("  http://localhost:5000/api/debug/mhs/ridwan halim")
    print("  http://localhost:5000/api/test/mhs/ridwan halim")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
