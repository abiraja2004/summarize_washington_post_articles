from flask import Flask, render_template, request
import numpy as np

# custom imports
import summarize

app=Flask(__name__)

def valid_url(url):
    if url.startswith('https://www.washingtonpost.com') or url.startswith('http://washingtonpost.com'):
        return True
    else:
        return False

@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html")


# when the form press submit, it links it to the action /result which will be sent here:
@app.route('/result', methods = ['POST'])
def result():
    summary=''
    
    # make sure nltk is installed in this init function:
    summarize.init()

    if request.method == 'POST':
        # from the request form, convert it to a dictionary saved as this variable
        url = request.form.get('wpost_url')

        if not valid_url(url):
            summary = ["Sorry, that was not a valid URL. Make sure to copy the entire link from the Washington Post article."]
        else:
            summary = summarize.summarize_wpost(url, n=5)

        # passing the string of our summary to our results template
        return render_template("result.html", summary=summary) 
        

if __name__ == "__main__":
    app.run(debug=True)