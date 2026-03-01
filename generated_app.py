from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Flask App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; margin: 0 auto; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            button:hover { background: #0056b3; }
            .message { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Simple Flask Web App</h1>
            <form action="/submit" method="post">
                <input type="text" name="name" placeholder="Your Name" required>
                <textarea name="message" placeholder="Your Message" rows="4" required></textarea>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Message Submitted</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .success {{ background: #d4edda; color: #155724; padding: 15px; border: 1px solid #c3e6cb; }}
            a {{ color: #007bff; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success">
                <h2>Thank you, {name}!</h2>
                <p>Your message: "{message}"</p>
                <p>Message has been received successfully.</p>
            </div>
            <a href="/">← Back to Home</a>
        </div>
    </body>
    </html>
    '''

@app.route('/about')
def about():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>About</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; margin: 0 auto; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>About This App</h1>
            <p>This is a simple Flask web application that demonstrates basic functionality including:</p>
            <ul>
                <li>Form handling</li>
                <li>POST requests</li>
                <li>HTML templating</li>
                <li>Multiple routes</li>
            </ul>
            <a href="/">← Back to Home</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)