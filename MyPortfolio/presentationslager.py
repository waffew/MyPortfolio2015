#!/bin/env python3
#-*- coding: utf-8 -*-

from flask import Flask
from flask import url_for
from flask import render_template
import datetime
import json
from operator import itemgetter
from flask import request
from data import load, search, get_project, get_project_c, get_project_count, get_technique_stats, get_techniques, get_fields, sorting
from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder
from werkzeug.exceptions import HTTPException, NotFound
import logging
app = Flask(__name__)

def view(request):
	app.logger.error('An error occurred')
	raise NotFound()

@responder
def application(environ, start_response):
	request = BaseRequest(environ)
	app.logger.debug('An error occurred')
	try:
		return view(request)
	except NotFound as e:
		return not_found(request)
	except HTTPException as e:
		return e

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/')
def index():
	db=load()
	Pname=db[0]['project_name']
	Stext=db[0]['short_description']
	Simage=db[0]['small_image']
	Ltext=db[0]['long_description']
	Bimage=db[0]['big_image']
	return render_template('index.html', Stext=Stext, Ltext=Ltext, Simage=Simage, Pname=Pname, Bimage=Bimage)

@app.route('/list', methods=['GET','POST'])
def listPage():
	if request.method == 'GET':
		db=load()
		srch=True
		techniques=get_techniques(db)
		projects=search(db, sort_by='start_date',sort_order='desc',techniques=None,search=None,search_fields=None)
		field=get_fields(db)
		return render_template('list.html',srch=srch,projects=projects, field=field, techniques=techniques)
		

@app.route('/list/search', methods=['POST'])
def listSearch():
	db=load()
	srch=True
	field=get_fields(db)
	techniques=get_techniques(db)	
	Search=request.form['Search']
	techniqs=request.form.getlist('filters')
	sorting=request.form.getlist('Sort')
	fields=request.form.getlist('search_fields')
	if Search== '':
		Search=None
	if sorting[0] == 'date':
		date=True
	else:
		date=False
	if sorting[0] == 'etad':
		etad=True
	else:
		etad=False
	if sorting[0] == 'abcd':
		abcd=True
	else:
		abcd=False
	if sorting[0] == 'project_no':
		count=True
	else:
		count=False
	Stext=' '
	projects=[]
	if fields==[]:
		if techniqs==[]:
			if Search == None:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=None,search=None,search_fields=None)
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=None,search=None,search_fields=None)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=None,search=None,search_fields=None)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=None,search=None,search_fields=None)
			if search(db, sort_by='start_date',sort_order='desc',techniques=None,search=Search,search_fields=None) == 'error':
				Stext='Couldn\'t find what you were looking for, please try again.'
				srch=False
			else:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=None,search=Search,search_fields=None)
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=None,search=Search,search_fields=None)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=None,search=Search,search_fields=None)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=None,search=Search,search_fields=None)
			return render_template('list.html',srch=srch, projects=projects, Stext=Stext, field=field, techniques=techniques)
		else:
			if Search == None:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=techniqs,search=None,search_fields=None)	
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=techniqs,search=None,search_fields=None)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=techniqs,search=None,search_fields=None)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=techniqs,search=None,search_fields=None)
			if search(db, sort_by='start_date',sort_order='desc',techniques=techniqs,search=Search,search_fields=None) == 'error':
				Stext='Couldn\'t find what you were looking for, please try again.'
				srch=False
			else:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=techniqs,search=Search,search_fields=None)
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=techniqs,search=Search,search_fields=None)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=techniqs,search=Search,search_fields=None)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=techniqs,search=Search,search_fields=None)
			return render_template('list.html',srch=srch, projects=projects, Stext=Stext, field=field, techniques=techniques)
	else:
		if techniqs==[]:
			if Search == None:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=None,search=None,search_fields=fields)
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=None,search=None,search_fields=fields)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=None,search=None,search_fields=fields)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=None,search=None,search_fields=fields)
			if search(db, sort_by='start_date',sort_order='desc',techniques=None,search=Search,search_fields=fields) == 'error':
				Stext='Couldn\'t find what you were looking for, please try again.'
				srch=False
			else:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=None,search=Search,search_fields=fields)
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=None,search=Search,search_fields=fields)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=None,search=Search,search_fields=fields)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=None,search=Search,search_fields=fields)
			return render_template('list.html',srch=srch, projects=projects, Stext=Stext, field=field, techniques=techniques)
		else:
			if Search == None:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=techniqs,search=None,search_fields=fields)	
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=techniqs,search=None,search_fields=fields)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=techniqs,search=None,search_fields=fields)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=techniqs,search=None,search_fields=fields)
			if search(db, sort_by='start_date',sort_order='desc',techniques=techniqs,search=Search,search_fields=fields) == 'error':
				Stext='Couldn\'t find what you were looking for, please try again.'
				srch=False
			else:
				if count==True:
					projects=search(db, sort_by='project_no',sort_order='desc',techniques=techniqs,search=Search,search_fields=fields)
				elif etad==True:
					projects=search(db, sort_by='start_date',sort_order='asc',techniques=techniqs,search=Search,search_fields=fields)
				elif abcd==True:
					projects=search(db, sort_by='project_name',sort_order='desc',techniques=techniqs,search=Search,search_fields=fields)
				else:
					projects=search(db, sort_by='start_date',sort_order='desc',techniques=techniqs,search=Search,search_fields=fields)
			return render_template('list.html',srch=srch, projects=projects, Stext=Stext, field=field, techniques=techniques)


@app.route('/project/<int:pid>', methods=['GET', 'POST'])
def project(pid):
	db=load()
	project=get_project(db, pid)
	return render_template('project.html',project=project)

@app.route('/techniques', methods=['GET', 'POST'])
def techniques():
	db=load()
	techs=get_techniques(db)
	techniqs=get_technique_stats(db)
	return render_template('techniques.html',techs=techs, techniqs=techniqs)

if __name__ == '__main__':
	app.debug = True
	app.run()
	db.commit()

logging.basicConfig(filename='error.log',level=logging.DEBUG)
app.run(host="127.0.0.1")

url_for('static', filename='style.css')
