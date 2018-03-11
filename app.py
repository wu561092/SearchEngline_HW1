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

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/info')
def info():
    return jsonify(es.info())


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form['search']
      res = es.search(index='test_index', body={  'query': {    'match': {      'title': result,     }  }})
      tmplist=[]
      for doc in res['hits']['hits']:
          print(" %s" % ( doc['_source']['author']))
          tmplist.append(doc['_source']['author'])
      return render_template("result.html",result=tmplist)


if __name__ == '__main__':
    es.index(index='test_index', doc_type='post', id=1, body={
        'author': 'John Doe',
        'blog': 'Learning Elasticsearch',
        'title': 'Using Python with Elasticsearch',
        'tags': ['python', 'elasticsearch', 'tips'],
    })
    es.index(index='test_index', doc_type='post', id=2, body={
        'author': 'John Doe2',
        'blog': 'Learning Elasticsearch',
        'title': 'Using Python with Elasticsearch is not happy',
        'tags': ['python', 'elasticsearch', 'tips'],
    })
    es.index(index='test_index', doc_type='post', id=3, body={
        'author': 'John Doe3',
        'blog': 'Learning Elasticsearch',
        'title': 'Using Python with Elasticsearch is maybe not happy',
        'tags': ['python', 'elasticsearch', 'tips'],
    })

    app.run()
