from flask import Flask, session
import pandas as pd
import os
import csv

app = Flask(__name__)
data = pd.DataFrame(columns=list(['email', 'contact']))
fi = os.path.exists('contact.csv')
if fi == True:
    pass
else:
    data.to_csv('contact.csv')


@app.route('/login/<email>/<password>')
def index(email, password):
    if email == '123@gmail.com' and password == 'abcdefg':
        session['name'] = 'permit'
    return 'now you are permitted'


@app.route('/add_contact/<email>/<number>')
def add(email, number):
    fetch_data = pd.read_csv('contact.csv')

    if fetch_data['email'].str.contains(email).any():
        msg = '<h1>You are not allowed</h1>'
    else:
        newdata = {'email': email, 'contact': number}

        new = pd.DataFrame(data=newdata, index=[1])
        new.to_csv('contact.csv', mode='a', header=False)
        msg = '<h1>Added</h1>'
        print('s')

    return msg


@app.route('/searching/<email>')
def searching(email):
    string = ''
    df = pd.read_csv('contact.csv')
    d = df[df.email.str.contains(email, case=False)]
    print(d)
    pdata = d['email']
    cdata = str(d['contact'])
    s = cdata.split(' ')
    return s[4]


@app.route('/delete/<email>')
def delete(email):
    lines = list()
    with open('contact.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == email:
                    lines.remove(row)

    with open('contact.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    return 'del'


@app.route('/updatec/<email>/<number>')
def updatec(email, number):
    lines = list()
    with open('contact.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == email:
                    lines.remove(row)
                    row[2] = number
                    lines.append(row)
                    print(row, lines)

    with open('contact.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    return 'updated'


app.run()