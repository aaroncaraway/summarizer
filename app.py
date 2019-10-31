from flask import Flask, render_template, url_for, request

app = Flask(__name__)

def run_the_thing(input):
    return input + ' loves cats'
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # get `content` from form
        task_content = request.form['content']
        gobs_program = run_the_thing(task_content)
        return gobs_program
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)