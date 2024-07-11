import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from generate_blog import generate_content

app = Flask(__name__)

def delete_files():
    try:
        file_paths = ['static/img1.jpg', 'static/img2.jpg', 'text.txt']
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception as e:
        return False, str(e)
    return True, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        if topic:
            keywords, images, blog_post_text = generate_content(topic)
            return redirect(url_for('blog', topic=topic, keywords=keywords, images=images, blog_post_text=blog_post_text))
    return render_template('index.html')

@app.route('/blog/<topic>', methods=['GET'])
def blog(topic):
    keywords = request.args.getlist('keywords')
    images = request.args.getlist('images')
    blog_post_text = request.args.get('blog_post_text')
    return render_template('blog.html', topic=topic, keywords=keywords, images=images, blog_post=blog_post_text)

@app.route('/create_new_blog', methods=['POST'])
def create_new_blog():
    success, error_message = delete_files()
    if success:
        return redirect(url_for('index'))
    else:
        return jsonify({'success': False, 'message': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
