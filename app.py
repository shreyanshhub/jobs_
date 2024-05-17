from flask import Flask, render_template
from scraper import selenium_scrape

app = Flask(__name__)

@app.route('/')
def home():
    jobs = selenium_scrape()
    return render_template('jobs.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
