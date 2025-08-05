from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['ANNOUNCEMENT_FOLDER'] = 'data/announcements'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Ensure data directories exist
os.makedirs('data', exist_ok=True)
os.makedirs(app.config['ANNOUNCEMENT_FOLDER'], exist_ok=True)

# Initialize ads database if not exists
if not os.path.exists('data/ads.json'):
    with open('data/ads.json', 'w') as f:
        json.dump([], f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_ads():
    with open('data/ads.json', 'r') as f:
        return json.load(f)

def save_ads(ads):
    with open('data/ads.json', 'w') as f:
        json.dump(ads, f, indent=2)

def get_announcement():
    files = os.listdir(app.config['ANNOUNCEMENT_FOLDER'])
    return files[0] if files else None

@app.route('/')
def index():
    announcement = get_announcement()
    return render_template('index.html', announcement=announcement)

@app.route('/post_ad', methods=['GET', 'POST'])
def post_ad():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        contact = request.form.get('contact')
        category = request.form.get('category')
        
        if not all([title, description, contact, category]):
            return "All fields are required!", 400
        
        ads = get_ads()
        new_ad = {
            'id': len(ads) + 1,
            'title': title,
            'description': description,
            'contact': contact,
            'category': category
        }
        ads.append(new_ad)
        save_ads(ads)
        
        return redirect(url_for('ads_list'))
    
    return render_template('post_ad.html')

@app.route('/ads')
def ads_list():
    category = request.args.get('category')
    ads = get_ads()
    
    if category:
        ads = [ad for ad in ads if ad['category'] == category]
    
    return render_template('ads_list.html', ads=ads)

@app.route('/upload_announcement', methods=['POST'])
def upload_announcement():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file and allowed_file(file.filename):
        # Clear existing announcements
        for f in os.listdir(app.config['ANNOUNCEMENT_FOLDER']):
            os.remove(os.path.join(app.config['ANNOUNCEMENT_FOLDER'], f))
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['ANNOUNCEMENT_FOLDER'], filename))
        return redirect(url_for('index'))
    
    return "Invalid file type", 400

@app.route('/delete_announcement', methods=['POST'])
def delete_announcement():
    announcement = get_announcement()
    if announcement:
        os.remove(os.path.join(app.config['ANNOUNCEMENT_FOLDER'], announcement))
    return redirect(url_for('index'))

@app.route('/announcements/<filename>')
def get_announcement_file(filename):
    return send_from_directory(app.config['ANNOUNCEMENT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
