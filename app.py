from flask import Flask, request, Response , render_template,url_for, jsonify
from flask_restful import reqparse, Resource, Api
from datetime import datetime
from elasticsearch import Elasticsearch
import requests
import json



app=Flask(__name__)
app.debug = True
es = Elasticsearch()

@app.route('/')
def index():
        return  render_template('index.html')




@app.route('/info')
def info():
    return jsonify(es.info())


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form['search']
      res = es.search(index='news', body={  'query': {    'match': {      'body': result,     }  }})
      all_body_list=[]
      all_title_list=[]
      all_url_list=[]
      for doc in res['hits']['hits']:
          all_body_list.append(doc['_source']['body'])
          all_title_list.append(doc['_source']['title'])
          all_url_list.append(doc['_source']['url'])
      return render_template("result.html",all_body=all_body_list,all_title=all_title_list,all_url=all_url_list,result_text=result)


if __name__ == '__main__':
    es.index(index='news', doc_type='post', id=1, body={
        'title': '外星人回到地球了',
        'url': 'http://travel.ettoday.net/article/1.htm',
        'body':'記者吳光中／台北報導 熄燈3年半，ETtoday回來了，這次不叫「達康」，改叫「達內」，如果把ETtoday.net的net解釋為new ET，倒也還蠻有趣的',
    })


    es.index(index='news', doc_type='post', id=2, body={
        'title': '2011年第46屆電視金鐘奨完整入圍名單',
        'url': 'http://travel.ettoday.net/article/3.htm',
        'body':'熄燈3年半，ETtoday回來了，這次不叫「達康」，改叫「達內」，如果把ETtoday.net的net解釋為new ET，倒也還蠻有趣的；既然叫new ET，總要有點創新吧？',
    })

    es.index(index='news', doc_type='post', id=3, body={
        'title': '外星人回到地球了22222',
        'url': 'http://travel.ettoday.net/article/1.htm2222',
        'body': '222記者吳光中／台北報導 熄燈3年半，ETtoday回來了，這次不叫「達康」，改叫「達內」，如果把ETtoday.net的net解釋為new ET，倒也還蠻有趣的',
    })

    app.run()
