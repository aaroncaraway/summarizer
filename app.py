from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup
import urllib.request
import nltk
import re

app = Flask(__name__)

def run_the_thing(input):
    try:
        clean_input = '_'.join(input.split(' '))
        scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/'+ clean_input)
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
        stopwords = nltk.corpus.stopwords.words('english')
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        max_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/max_frequency)
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower())[:50]:
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        sorted_sentences = sorted(sentence_scores.items(), key=lambda kv: kv[1], reverse=True)
        summary = [sent[0] for sent in sorted_sentences[:5]]
        clean_summary = ''.join(summary).strip()
        return clean_summary
    except:
        return "Oh shoot! Wikipedia doesn't have an article on " + input + " yet!"

    

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