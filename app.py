from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup
import urllib.request
import nltk
import re

app = Flask(__name__)

def run_the_thing(input):
    scraped_data = urllib.request.urlopen(input)
    article = scraped_data.read()
    parsed_article = BeautifulSoup(article)
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    article_text = re.sub(r'\[[0-9]*\]', '', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    return sentence_list[:5]

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # get `content` from form
        task_content = request.form['content']
        gobs_program = run_the_thing(task_content)
        return render_template('result.html', passed=gobs_program)
    else:
        return render_template('index.html')

@app.route('/summary/<int:id>', methods=['GET', 'POST'])
def summary(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            # db.session.update(task_to_update)
            # commit() does the update for us don't need ^^
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task'
    else:
        return render_template('update.html', task=task)
    

if __name__ == "__main__":
    app.run(debug=True)