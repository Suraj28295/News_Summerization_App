from Utils.libraries import *
from Utils.Parse_news import BBC_News_scrape
app = Flask(__name__)

model=AutoModelForSeq2SeqLM.from_pretrained("model")
tokenizer=AutoTokenizer.from_pretrained("tokenizer")

@app.route('/')
def hello_world():
    return 'Flask Dockerized'


@app.route('/check_the_summerization',methods=['POST', 'GET'])
def result():
    if request.method=='POST':
        output = request.form["news"]
        # summary_news=str(output)

        inputs = tokenizer("summarize: " + str(output), return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate( inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)

        # print(output)
        summary_news = tokenizer.decode(outputs[0])[4:]
        return render_template('index.html', summary_news = summary_news,Orignal_news = output)
    else:
        return render_template('index.html', summary_news = "")
    
@app.route('/daily_news_BBC',methods=['POST', 'GET']) 
def daily_BBC_updates():
    if request.method=='POST':
        Search_keyword=request.form["keyword"]
        Search_keyword=Search_keyword.replace(" ","+").lower()
        BBC_News_articles=BBC_News_scrape(Search_keyword)
        for output in range(len(BBC_News_articles)):
            inputs = tokenizer("summarize: " + str(BBC_News_articles[output]['Desc']), return_tensors="pt", max_length=512, truncation=True)
            outputs = model.generate( inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary_news = tokenizer.decode(outputs[0])[4:]
            BBC_News_articles[output]['Summary']=summary_news.replace("s>","p>")

        return render_template('blog.html',news=BBC_News_articles)   
    else:
        return render_template('blog.html', news = "")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')