from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import shutil

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/create', methods=['POST'])
def create():
    try:
        data = request.get_json()
        path = data['path']
        name = data['name']
        full_path = os.path.join(path, name)
        
        os.makedirs(full_path, exist_ok=True)
        return jsonify({"success": True, "message": f"Directory created: {full_path}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/delete', methods=['POST'])
def delete():
    try:
        data = request.get_json()
        path = data['path']
        
        if os.path.exists(path):
            shutil.rmtree(path)
            return jsonify({"success": True, "message": f"Deleted: {path}"})
        return jsonify({"success": False, "message": "Path doesn't exist"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/rename', methods=['POST'])
def rename():
    try:
        data = request.get_json()
        old_path = data['oldPath']
        new_name = data['newName']
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        
        os.rename(old_path, new_path)
        return jsonify({"success": True, "message": f"Renamed to: {new_path}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/move', methods=['POST'])
def move():
    try:
        data = request.get_json()
        src = data['src']
        dest = data['dest']
        
        shutil.move(src, dest)
        return jsonify({"success": True, "message": f"Moved to: {dest}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/copy', methods=['POST'])
def copy():
    try:
        data = request.get_json()
        src = data['src']
        dest = data['dest']
        
        shutil.copytree(src, os.path.join(dest, os.path.basename(src)))
        return jsonify({"success": True, "message": f"Copied to: {dest}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/organize', methods=['POST'])
def organize():
    try:
        data = request.get_json()
        path = data['path']
        
        # Create subdirectories
        os.makedirs(f"{path}/Images", exist_ok=True)
        os.makedirs(f"{path}/Documents", exist_ok=True)
        os.makedirs(f"{path}/Archives", exist_ok=True)
        
        # Organize files
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1].lower()
                if ext in ('.png', '.jpg', '.jpeg', '.gif'):
                    shutil.move(item_path, f"{path}/Images/{item}")
                elif ext in ('.pdf', '.doc', '.docx', '.txt'):
                    shutil.move(item_path, f"{path}/Documents/{item}")
                elif ext in ('.zip', '.rar', '.7z'):
                    shutil.move(item_path, f"{path}/Archives/{item}")
        
        return jsonify({"success": True, "message": "Organization complete!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)