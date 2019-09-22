import pandas as pd
import numpy as np
import pickle
import os
from flask import Flask, render_template, request

app = Flask(__name__)
def mobile(filename):
    dat=pd.read_csv("checking for flask.csv")
    dat1=dat.copy()
    dat.drop('ID',axis=1,inplace= True)
    model_get=open("saved_modell.dat", "rb")
    model=pickle.load(model_get)
    pred = pd.DataFrame(model.predict_proba(dat),columns= [ 'no_financial_services', 'other_only', 'mm_only', 'mm_plus'])
    df=pd.concat([dat1['ID'],pred],axis=1)
    return(df)



UPLOAD_FOLDER = '/static/uploads/'


ALLOWED_EXTENSIONS = set(['csv', 'csv', 'csv'])




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            
            df = mobile(file)

            
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   tables=[df.to_html(classes='data')], titles=df.columns.values
                                   )
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()