from flask import Flask, render_template, jsonify, request, abort, Response
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import requests
import json
import sqlite3 
from sqlite3 import Error
import re
import csv
from datetime import datetime

#modules required for ML - tags
from gensim import corpora, models, similarities
import jieba
import numpy as np

#modules required for sentiment analysis
#import numpy as np - already included
import pandas as pd 
#import re 
import nltk 
#nltk.download('stopwords') already up to date
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import confusion_matrix 

app = Flask(__name__)
api = Api(app)

CORS(app)

@app.route("/register", methods = ["POST"])
def register():
    username = request.get_json()['username']
    password = request.get_json()['password']
    email = request.get_json()['email']
    print("im here")
    print(email)

    checkquery = "SELECT * FROM login WHERE username='"+username+"';"
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(checkquery)
    conn.commit()
    rows = c.fetchall()
    if rows:
        return jsonify({"returned":0})
    else:
        
        insertquery = "INSERT INTO login VALUES('"+username+"','"+email+"','"+password+"',' ', 0,0,0);"
        print(insertquery)

        database = r"pythonsqlite.db"
        conn = create_connection(database)
        c = conn.cursor()
        c.execute(insertquery)
        conn.commit()
        res = c.fetchall()
        if res:
            return jsonify({"returned":1})
    
    return jsonify({})

@app.route("/login", methods = ["POST"])
def validate():
    username = request.get_json()['username']
    password = request.get_json()['password']
    print("username: ", username, "pwd: ", password)
    
    query = "SELECT * FROM login WHERE username='"+username+"' AND password='"+password+"';"
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    rows = c.fetchall()
    if rows:
        return jsonify({"returned":1})
    else:
        return jsonify({"returned":0})
    
    return jsonify({})

@app.route("/check",methods = ["GET"])
def check_user():
    username = request.args.get('username')
    query = "select * from login where username = '{}';".format(username)
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    print(query)
    conn.commit()
    print(rows)

    if(len(rows) == 1):
        print("returning 1")
        return jsonify({"returned":1})
    else:
        print("returning 0")
        return jsonify({"returned":0})
    
    return jsonify({})


@app.route("/blogstop/recommendtags", methods = ["GET"])
def recommend_tags():
    content = request.args.get('content')
    print("contentttttttlo", content)
    

    def gettag(argument): 
        switcher = { 
            1: "Travel", 
            2: "Fitness", 
            3: "Sports", 
            4: "Political",
            5: "Finance",
            6: "Food",
            7: "Fashion"
        } 
        return switcher.get(argument, "nothing") 


    texts = [
        "The two best places to travel to are japan,new york.The mast travelled to destination are crowded. The main places that are within easy reach  of the city are Matka Canyon travel and Vodno Mountain. Whilst Matka Canyon is no doubt the prettiest. The bus to Vodno travel Mountain ran more frequently, so I plumped for there. Getting a ticket travel for the bus appeared to be a bit of a ballache as you cannot buy travel tickets on the bus and have to buy and pre-load a card with credit. They can only be bought from special green booths which are scattered around the city. The transport company really needs to update their English webpage to make it easier for tourists to figure out how to buy tickets without having to rely on others for help. Luckily, the hostel I was staying at had cards available, but didn't know how much credit was on them. Since I was staying near the bus terminal, which is home to intercity and international buses, and also next to it is the terminal for the red London style Routemaster city buses."
        ,"It’s hard to deny the aesthetic appeal of a good six-pack, but building a strong core is about more than countless crunches and the visual progress of rippling abs. That’s where football cricket rotational moves come into play. To target those all-important football muscles, you’ve got to think (and train) in all three planes cricket basketball of motion. Pushups, pullups, biceps curls, and crunches occur in the forward-and-back sagittal plane. Others, like side lunges or chest flies, occur in the side-to-side frontal plane.If you’re not training your body for that, you’ll lose strength and stability and be more prone to injuries."
        ,"India though can be proud of the fact that they are yet unbeaten in this World Cup with one game being washed out. Football West Indies will be tough opponents who will pose basketball a threat as the two time world champions cricket are all but knocked out. Football India need to play good cricket and avoid slip-ups.All hard teams gym done now, mostly and here comes a slightly lesser team. Afghanistan gym are the next opponents and shouldn’t be taken lightly. workout Two points are all but a guarantee from this game for India and hopefully the weather will help. Batsmen are in good touch and Bowling and Fielding will also be on the agenda for a complete performance."
        ,"Politics is the set of activities that are associated with the governance of a country, state or area. Political government country It involves making decisions that UN UN United Nations apply to groups of members and achieving and exercising positions of governance—organized control over a human community. The academic study of politics is referred to as political science.In modern nation states, people often form political parties to represent their ideas. Members of a party often agree to take the same position on many issues and agree to support the same changes to law and the same leaders.An election is usually a competition between different parties. Some examples of political parties worldwide are: the Democratic Party (D) in the United States, the Conservative Party in the United Kingdom and the Indian National Congress in India, which has the highest number of political parties in the world "
        ,"Market investments are most likely to lose significant value which can cause you to panic and finance liquidate in an economy economy attempt to recover as much of your money as possible. Be calm and seek professional help to assess your portfolio especially if your investments financial assets are in affected sectors, before taking any investment decisions.While its money essential to have a health insurance in place for yourself and your family, it’s also important to know what all it covers. Check with your insurance company or TPA, the extent of coverage of medical expenses related to the pandemic. This can help you be prepared with spare funds to meet uncovered medical costs."
        ,"When I think of comfort food, I inevitably think of chicken. chicken rice, chicken congee, chicken, chicken noodle soup, chicken with mashed potatoes is just good. give me ALL the chicken, carbs and I am one happy comforted ball of joy. I can forever come up with chicken and carb combinations and lately, lemony pepper chicken with cous cous is the one that has been bringing me joy.Juicy lemon slices turn jammy and extra sweet in the oven, mixing with savory chicken juices to create the most delicious sauce. It’s perfect for spooning over cous cous. Those fluffy little kernels just soak it up turning into tiny little bits of pure flavor"
        ,"Another significant factor which influences Fashion trend is technology. There certainly has been a rapid growth of technology in the Fashion industry. For example, wearable technology has become a popular Fashion trend. Furthermore, 3D printing technology and the internet have also made an impact on Fashion.Social influences are probably the strongest influences on the Fashion trend. Many music stars strongly influence Fashion choice. For example, wearing hoodies became famous due to rap musicians. Furthermore, movie and television actors create a big impact on Fashion. Many youngsters love to emulate the Fashion sense of their favourite celebrity"
    ]
    keyword = content

    texts = [jieba.lcut(text) for text in texts]
    dictionary = corpora.Dictionary(texts)
    feature_cnt = len(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus) 
    kw_vector = dictionary.doc2bow(jieba.lcut(keyword))
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
    sim = index[tfidf[kw_vector]]

    sim = list(sim)

    for i in range(len(sim)):
        sim[i] = round(sim[i],2)
    #print(sim)
    max1 = max(sim)
    maxpos1 = sim.index(max1)
    sim[maxpos1] = 0
    max1 = max(sim)
    maxpos2 = sim.index(max1)
    #print(maxpos1,maxpos2)


    mystr = gettag(maxpos1+1)+";"+gettag(maxpos2+1)
    print(mystr)
    d={}
    d["content"] = mystr
    return jsonify(d)


@app.route("/profile", methods = ["GET"])
def profile_details():
    username = request.args.get('username')
    print("hello", username)

    query = "SELECT * FROM login WHERE username = '" + username+ "';"

    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    print(rows)
    conn.commit()

    if(len(rows) == 0):
        return jsonify({})
    

    '''
    {
        username = vishal
        email = abc@gmail
        posts = 1#4#7
    }
    '''
    
    d={}
    d["username"] = rows[0][0]
    d["email"] = rows[0][1]
    if(rows[0][3] == " "):
        d["num"] = 0
    else:
        d["num"] = len(rows[0][3].split(';'))
    d["posts"] = rows[0][3]
    d["likes"] = rows[0][4]
    return jsonify(d)
    
@app.route("/blogstop/update", methods = ["GET"])
def update():
    username = request.args.get('username')
    post_id = request.args.get('postid')
    date = request.args.get('date')
    print(date)

    query = "SELECT * FROM login WHERE username = '" + username+ "';"
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    mystr = rows[0][3]
    if(mystr == " "):
        mystr = post_id
    else:
        mystr += ";"+post_id
    conn.commit()

    query1 = "UPDATE login SET posts = '"+mystr+"' WHERE username = '" + username + "';"
    print(query1)
    database1 = r"pythonsqlite.db"
    conn1 = create_connection(database1)
    c1 = conn1.cursor()
    c1.execute(query1)
    conn1.commit()

    query = "SELECT * FROM data WHERE username = '" + username+ "' and date = '"+ date + "';"
    database = r"pythonsqlite.db"
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.commit()
    if(rows):
        query1 = "UPDATE data SET posts = posts + 1 WHERE username = '" + username+ "' and date = '"+ date + "';"
    else:
        query1 = "INSERT INTO data VALUES('"+username+"','"+date+"', 1);"
    database1 = r"pythonsqlite.db"
    conn1 = create_connection(database1)
    c1 = conn1.cursor()
    c1.execute(query1)
    conn1.commit()

    return jsonify({})

@app.route("/like_update", methods = ["GET"])
def update_like():
    username = request.args.get('username')

    query1 = "UPDATE login SET likes = likes + 1 where username='"+username+"';"
    print(query1)
    database1 = r"pythonsqlite.db"
    conn1 = create_connection(database1)
    c1 = conn1.cursor()
    c1.execute(query1)
    conn1.commit()

    return jsonify({})

@app.route("/posneg", methods = ["GET"])
def posneg():
    print("IN POSNEG")
    username = request.args.get('username')
    text = request.args.get('text')
    print(username, text, sep='\n')

    tofile = text.split(";;")
    print("to file:",tofile)

    with open('C:\\xampp\\htdocs\\BlogStop\\{}.tsv'.format(username), mode='wt') as myfile:
        myfile.write('Review\tLiked\n')
        myfile.write('\t0\n'.join(tofile))

    dataset = pd.read_csv('C:\\xampp\\htdocs\\BlogStop\\Restaurant_Reviews.tsv', delimiter = '\t')
    test_data = pd.read_csv('C:\\xampp\\htdocs\\BlogStop\\{}.tsv'.format(username), delimiter = '\t')
    #print(test_data)
    #print(dataset)
    data_list = [dataset, test_data]
    
    final_data = pd.concat(data_list, axis=0, ignore_index = True)
    
    print("Final_data ka Length: ",len(final_data), final_data)
    
    corpus = [] 

    # 1000 (reviews) rows to clean 
    for i in range(0, len(final_data)): 

        # column : "Review", row ith 
        review = re.sub('[^a-zA-Z]', ' ', final_data['Review'][i]) 

        # convert all cases to lower cases 
        review = review.lower() 

        # split to array(default delimiter is " ") 
        review = review.split() 

        # creating PorterStemmer object to 
        # take main stem of each word 
        ps = PorterStemmer() 

        # loop for stemming each word 
        # in string array at ith row	 
        review = [ps.stem(word) for word in review 
                    if not word in set(stopwords.words('english'))] 

        # rejoin all string array elements 
        # to create back into a string 
        review = ' '.join(review) 

        # append each string to create 
        # array of clean text 
        corpus.append(review) 
    print("Length of Corpus: ", len(corpus))
    
    cv = CountVectorizer(max_features = 1500) 

    X = cv.fit_transform(corpus).toarray() 

    y = final_data.iloc[:, 1].values 
    print("x: ", X, "y: ", y)
    
    X_train = X[0:1000]
    y_train = y[0:1000]
    X_test = X[1000:1000+len(test_data)]
    y_test = y[1000:1000+len(test_data)]
    print("X_train: ",len(X_train), "y_train: ", len(y_train), "X_test: ",len(X_test), "y_test: ", (y_test))
    # n_estimators can be said as number of 
    # trees, experiment with n_estimators 
    # to get better results  
    model = RandomForestClassifier(n_estimators = 501, criterion = 'entropy') 

    model.fit(X_train, y_train)
    print(model)
    

    # Predicting the Test set results 
    y_pred = model.predict(X_test) 
    print("y_pred: ", y_pred)
  
    cm = confusion_matrix(y_test, y_pred) 

    print("confusion matrix: ",cm)
    print("accuracy: ", (cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1]))
    
    positive = 0
    negative = 0
    
    for i in range(0, len(y_pred)):
        if(y_pred[i] == 1):
            positive+=1
        else:
            negative+=1
    
    query1 = "UPDATE login SET pos = {}, neg = {} where username = '{}';".format(positive, negative, username)
    print(query1)
    database1 = r"pythonsqlite.db"
    conn1 = create_connection(database1)
    c1 = conn1.cursor()
    c1.execute(query1)
    conn1.commit()

    return jsonify({"pos":positive, "neg":negative})
    

@app.route("/get_details", methods = ["GET"])
def get_details():
    username = request.args.get('username')

    query1 = "SELECT date,posts FROM data WHERE username = '" + username+ "' order by date;"
    #print(query1)
    database1 = r"pythonsqlite.db"
    conn1 = create_connection(database1)
    c1 = conn1.cursor()
    c1.execute(query1)
    rows = c1.fetchall()
    conn1.commit()
    #print("rowssss1:  ",rows)

    dates = []
    posts = []
    for i in range(len(rows)):
        dates.append(rows[i][0])
        posts.append(rows[i][1])
    d = {}
    d["dates"] = dates
    d["posts"] = posts
    query1 = "SELECT pos,neg FROM login WHERE username = '" + username+ "';"
    #print(query1)
    database1 = r"pythonsqlite.db"
    conn1 = create_connection(database1)
    c1 = conn1.cursor()
    c1.execute(query1)
    rows = c1.fetchall()
    conn1.commit()
    #print("rowssss2:  ",rows)
    com = []
    for i in range(len(rows)):
        com.append(rows[i][0])
        com.append(rows[i][1])
    d["com"] = com
    print("dataaaaa",d)
    return jsonify(d)


def create_connection(db_file):
    conn = None
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)


database = r"pythonsqlite.db"
create_login_table = """CREATE TABLE IF NOT EXISTS login (username text PRIMARY KEY, email text NOT NULL, password text NOT NULL, posts text, likes INTEGER, pos INTEGER , neg INTEGER );"""     
create_data_table = """CREATE TABLE IF NOT EXISTS data (username text NOT NULL, date text NOT NULL, posts INTEGER,PRIMARY KEY (username, date),FOREIGN KEY (username) REFERENCES login (username));"""     

conn = create_connection(database)
if conn is not None:
    create_table(conn, create_login_table)
    create_table(conn, create_data_table)

else:
    print("Error! Cannot create the database connection")   

if __name__ ==  "__main__":
    app.run(host='0.0.0.0',debug=True)


