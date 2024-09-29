from flask import Flask, request, jsonify, render_template_string
import io

app = Flask(__name__)

@app.context_processor
def inject_file_class():
    return dict(file=io.TextIOWrapper)  

@app.route("/", methods=["GET"])
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Practical Exam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f4f4f4;
                }
                h1 {
                    color: #333;
                }
                form {
                    background: #fff;
                    padding: 15px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    margin-top: 20px;
                    max-width: 400px; /* Set a max-width to make the form smaller */
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                }
                input[type="text"], input[type="submit"] {
                    width: 100%;
                    padding: 8px; /* Reduced padding */
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #5cb85c;
                    color: white;
                    border: none;
                    cursor: pointer;
                    padding: 6px; /* Reduced button padding */
                    font-size: 14px; /* Smaller font size for the button */
                }
                input[type="submit"]:hover {
                    background-color: #4cae4c;
                }
                #result {
                    margin-top: 20px;
                    font-weight: bold;
                }
            </style>
            <script>
                function submitForm(event) {
                    event.preventDefault();  
                    const formData = new FormData(document.getElementById("usernameForm"));
                    
                    fetch("/process", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Update the result without refreshing the page
                        document.getElementById("result").innerHTML = data.result;
                    });
                }
            </script>
        </head>
        <body>
            <h1>SSTI Lab</h1>
            <div>
                <h2>Instructions:</h2>
                <ol>
                    <li>Read the file <code>hash.txt</code>  file ( use <code>os</code> command )</li>
                    <li>Read the file <code>wordlist.txt</code> ( crack the hash using <code>John The Ripper</code> )</li>                   
                    <li>Write your name in <code>secret.txt</code> file</li>
                </ol>
            </div>
            <form id="usernameForm" onsubmit="submitForm(event)">
                <label for="username">Enter your name:</label>
                <input type="text" id="username" name="username" placeholder="Enter your name">
                <input type="submit" value="Submit">
            </form>
    
            <div id="result"></div>
        </body>
        </html>
    ''')

@app.route("/process", methods=["POST"])
def process():
    username = request.form.get('username', '')
    template = "Hello " + username
    result = render_template_string(template)
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
