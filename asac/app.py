from flask import *
from dbconnect import connection
from wtforms import *
from functools import wraps
import re, math
from collections import Counter
import gc
from nltk.tokenize import word_tokenize,PunktSentenceTokenizer,sent_tokenize,RegexpTokenizer
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz,process

app = Flask(__name__)
app.debug = True

i=0
sc = int()
@app.route('/')
def homepage():
    c,conn = connection()
    c.execute('truncate table userdata')
    c.close()

    return render_template('home.html')

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("you need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route("/logout")
@login_required
def logout():
    session.clear()
    gc.collect()
    return redirect(url_for('homepage'))

@app.route('/login',methods=['GET','POST'])
def login():
    try:
        error = ""
        c, conn = connection()
        if request.method == 'POST':
            usr = request.form["username"]
            pss = request.form["password"]
            data = c.execute("select * from users where username = %s",(usr,))
            data = c.fetchone()[3]
            if pss==data:

                session["logged_in"] = True
                session["username"] = request.form['username']

                flash("you are now logged in")
                return redirect(url_for('dashboard'))

            else:
                flash( "Invalid credentials! please retry again ")
        gc.collect()

        return render_template('login.html')
    except Exception as e:
        flash("invalid Credentials Try Again!!!")
        return render_template('login.html')

class RegistrationForm(Form):
    name = StringField('name', [validators.Length(min=3, max=20)])
    username = StringField('username',[validators.Length(min=3,max=15)])
    password = PasswordField("password",[validators.DataRequired(),validators.Length(min=4,max=15),validators.EqualTo('confirm',message="password must match")])
    confirm = PasswordField("Repeat password")

@app.route('/register' , methods=['GET','POST'])
def signup():
    try:
        frm = RegistrationForm(request.form)

        if request.method == 'POST' and frm.validate():
            name = frm.name.data
            username = frm.username.data
            password = frm.password.data
            c,conn = connection()

            x = c.execute('Select * from users where username = (%s)',(username,))

            if int(x)>0:
                flash(
                    "that username is already taken"
                )
                return render_template('register.html', form=frm)
            else:
                c.execute('insert into users (name,username,password) values(%s,%s,%s)',(name,username,password,))
                conn.commit()
                flash('Thanks for registering')
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))
        return render_template('register.html', form=frm)

    except Exception as e:
        return (str(e))

class Quiz(Form):
    question = Label('question',text=None)
    answer = TextAreaField('answer',[validators.DataRequired(),validators.Length(min=1,max=750)],render_kw={'class': 'form-control', 'rows': 7},default="")

@app.route("/about")
def about():

    return render_template('about.html')

@app.route('/quizover')
def overquiz():
    return render_template('fin_quiz.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/quiz_next/<int:idx>',methods=['GET',"POST"])
def quiz_next(idx=0):
    global i
    frm = Quiz(request.form)
    c,conn =connection()
    x = c.execute("select question from questiontable")
    questions = c.fetchall()
    if i < len(questions):
        # logic if for exiting quiz
        frek = questions[i]# iterrating tuple
        frm.question.text = frek[0]  # calling the element in  tuple
        r = len(questions)
        print(r)
        c.close()
        conn.close()

    else:
        #exiting else logig of quiz
        return render_template('fin_Quiz.html')

    if request.method == "POST" :#when button is pressed

        if request.form['action'] == 'submit':#checking submit button is pressed
            call = False
            c, conn = connection()
            check_answer = frm.question.text
            print("check", check_answer)
            var = c.execute("select question from userdata where question = %s", (check_answer,))#query execution for getting question list
            print(var)
            if var == 1:
                #if true (exists) redirect to next question
                i = i + 1
                idx = int(i)
                print('executing if')
                return redirect(url_for('quiz_next', idx=idx))

            else:
                #if doesnt exist save in database and redirect to next question
                print('executing else')
                c, conn = connection()
                answer = frm.answer.data
                print('ans is', answer)
                c.execute("insert into userdata (question,answer) values (%s,%s)", (frek[0], answer,))

                conn.commit()
                c.close()
                conn.close()
                r = len(questions)
                i = i + 1
                idx = int(i)
                return redirect(url_for('quiz_next', idx=idx,call = call))

        elif request.form['action']== 'score': #checking if score button is pressed

            c, conn = connection()
            check_answer = frm.question.text
            print("check", check_answer)
            var = c.execute("select question from userdata where question = %s", (check_answer,))#query execution for getting question list
            print(var)
            if var == 1:#if true (exists) dont save just extract and solve


                # #############-----cosine similarity-----############
                c, conn = connection()
                x = c.execute("select answer from userdata")
                ans = c.fetchall()
                print(i)
                usans = ans[i]
                text1 = usans[0]
                print(ans)
                y = c.execute("select answer from serverdata")
                sans = c.fetchall()
                saans = sans[i]
                text2 = saans[0]
                cosine = similarity(text1,text2)
                cosine = cosine *4
                call = True

                if cosine >1.5:
                    sentence_similarity = sent(idx)
                    print(sentence_similarity)
                    sc_keywords = check2(idx)
                    print(sc_keywords)
                    sc_keywords = sc_keywords * 2
                    lengthsc =length(idx)

                    total = cosine + sentence_similarity + sc_keywords + lengthsc

                    return render_template('quiz.html', form=frm, idx=idx, total=total, call=call, cosine=cosine,
                                           sent_cosine=sentence_similarity, keywords_match=sc_keywords,lengthsc=lengthsc)
                else:
                    return render_template('quiz.html', form=frm, idx=idx, total=0, call=call, cosine=0,
                                           sent_cosine=0, keywords_match=0,lengthsc=0)

            else:# doesnt exsist save extract and give score

                c, conn = connection()
                answer = frm.answer.data
                c.execute("insert into userdata (question,answer) values (%s,%s)", (frek[0], answer,))

                conn.commit()
                c.close()
                conn.close()

                #############-----cosine similarity-----############

                c, conn = connection()
                x = c.execute("select answer from userdata")
                ans = c.fetchall()
                print(i)
                usans = ans[i]
                text1 = usans[0]
                print(ans)
                y = c.execute("select answer from serverdata")
                sans = c.fetchall()
                saans = sans[i]
                text2 = saans[0]
                cosine = similarity(text1,text2)
                cosine = float(format(cosine,'.4f'))
                cosine = cosine * 4
                call = True

                if cosine > 1.5:
                    sentence_similarity = sent(idx)
                    sc_keywords = check2(idx)

                    sc_keywords = sc_keywords * 2
                    lengthsc = length(idx)

                    total = cosine + sentence_similarity + sc_keywords+lengthsc

                    return render_template('quiz.html', form=frm, idx=idx, total=total, call=call, cosine=cosine,
                                           sent_cosine=sentence_similarity, keywords_match=sc_keywords,lengthsc=lengthsc)
                else:
                    return render_template('quiz.html', form=frm, idx=idx, total=0, call=call, cosine=0,
                                           sent_cosine=0, keywords_match=0)

    return render_template('quiz.html',form = frm ,idx =idx)

#cosine similarity algorithm
def similarity(text1,text2):
    WORD = re.compile(r'\w+')

    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)


    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    cosine = get_cosine(vector1, vector2)
    print('Cosine:', cosine)

    return cosine

##sentence to para similarity which we dont need
def check(idx):
    try:
        global sc
        sc=0
        c, conn = connection()
        x = c.execute('select answer from userdata')
        user_text3 = c.fetchall()
        user_text = user_text3[idx]

        user_text = list(user_text)
        print(user_text)
        y = c.execute('select answer from serverdata')
        ans_text3 = c.fetchall()
        ans_text = ans_text3[idx]

        ans_text = list(ans_text)
        print(ans_text)

        tokenized_user_sentence = sent_tokenize(user_text[0])
        print(tokenized_user_sentence)
        wrd_tokenized_user = word_tokenize(user_text[0])
        tokenized_ans_sent = sent_tokenize(ans_text[0])
        print(tokenized_ans_sent)
        wrd_tokenized_ans = word_tokenize(ans_text[0])
        scs = 0
        counter = 0
        for w in tokenized_user_sentence:
            counter +=1
            cosine =similarity(w,ans_text[0])
            sc = sc +cosine
            print(sc)

        print(sc)
        sc = sc/counter
        sc=sc*2

        sc1 =0
        counter2 = 0

        for w in tokenized_ans_sent:
            counter2 +=1
            cosine =similarity(w,user_text[0])
            sc1 = sc1 +cosine
            print(sc1)

        print(sc)
        sc1 = sc1 / counter
        sc1 = sc1 * 2


        xxy = sc+sc1
        xxy=float(format(xxy,'.4f'))
        return xxy

    except Exception as e:
        print(str(e))

###keywords similarity
def check2(idx):
    try:
        ###keywords matching percentage
        c, conn = connection()
        print(idx)
        x = c.execute('select answer from userdata')
        user_text3 = c.fetchall()
        user_text = user_text3[idx]

        user_text = list(user_text)
        print("user",user_text)
        y = c.execute('select keywords from serverdata')
        ans_text3 = c.fetchall()
        ans_text = ans_text3[idx]
        print(ans_text)
        ans_text = list(ans_text)
        print("ANSWER",ans_text)
        keywords = word_tokenize(ans_text[0])
        print(keywords)

        wrd_tokenized_user = word_tokenize(user_text[0])
        print(wrd_tokenized_user)
        stp = set(stopwords.words('english'))
        stp_filtered_user = []
        for sw in wrd_tokenized_user:
            if sw not in stp:
                stp_filtered_user.append(sw)

        stp_filtered_user = set(stp_filtered_user)
        print("ddf",stp_filtered_user)
        stp_filtered_user = list(stp_filtered_user)
        match = set()
        print(stp_filtered_user)
        for isd in stp_filtered_user:
            print(isd)
            var = process.extractOne(isd,keywords)

            if var[1] > 90:
                match.add(var[0])

        print(match)

        us_len = len(match)
        ans_len = len(keywords)

        perct_len = us_len/ans_len
        print(perct_len)


        return perct_len

    except Exception as e:
        print(e)

    return render_template('check.html')

@app.route('/check')
def length(idx):
    c, conn = connection()
    x = c.execute('select answer from userdata')
    user_text3 = c.fetchall()
    user_text = user_text3[idx]

    user_text = list(user_text)
    print(user_text)
    y = c.execute('select answer from serverdata')
    ans_text3 = c.fetchall()
    ans_text = ans_text3[idx]

    ans_text = list(ans_text)
    print(ans_text)

    tokenized_user_sentence = sent_tokenize(user_text[0])
    print("tokenised user",tokenized_user_sentence)

    tokenized_ans_sent = sent_tokenize(ans_text[0])
    print("tokenised answer",tokenized_ans_sent)
    tokenizer = RegexpTokenizer(r'\w+')
    ans_length_list = []
    user_length_list = []
    for i in tokenized_ans_sent:
        w_token = tokenizer.tokenize(i)
        print(w_token)
        ans_length_list.append(len(w_token))

    for j in tokenized_user_sentence:
        u_token = tokenizer.tokenize(j)
        print(u_token)
        user_length_list.append(len(u_token))

    print("the list of words and punctuations in answer sentences",ans_length_list)
    print("the list of words and punctuations in user sentences", user_length_list)

    min_len = min(ans_length_list)
    print(min_len)
    u_min_len = min(user_length_list)
    print(u_min_len)


    if u_min_len < min_len:
        xc = min_len-u_min_len
        print(xc)
        v = xc/min_len*100
        scr = 1-(v/100)
        print('sfsdfsd',v)
        print(scr)

        return scr
    else:
        scr = 1
        return scr
    return render_template('check.html')

##sentence to sentence similarity
def sent(idx):
    try:
        global sc
        sc=0
        c, conn = connection()
        x = c.execute('select answer from userdata')
        user_text3 = c.fetchall()
        user_text = user_text3[idx]

        user_text = list(user_text)
        print(user_text)
        y = c.execute('select answer from serverdata')
        ans_text3 = c.fetchall()
        ans_text = ans_text3[idx]

        ans_text = list(ans_text)
        print(ans_text)

        tokenized_user_sentence = sent_tokenize(user_text[0])
        print(tokenized_user_sentence)

        tokenized_ans_sent = sent_tokenize(ans_text[0])
        print(tokenized_ans_sent)

        scs = []
        cos_list = []
        sim_list = []
        trial = []
        counter = 0
        for word in tokenized_ans_sent:
            print('word is:',word)
            for uword in tokenized_user_sentence:
                print('uword is :',uword)
                z=similarity(uword,word)
                print(z)
                sim_list.append(z)

                if z > 0.9:
                    cos_list.append(z)

                    scs.append(uword)
            trial.append(max(sim_list))

        for tri in trial:
            counter = counter + 1

        x =0
        for tr in trial:
            x =  x + tr


        y =x/counter
        y = float(format(y,'.4f'))
        print(y)

        y=y*3

        return y

    except Exception as e:
        print(str(e))

def xxyi():
    return render_template('check.html')

def score(x):
    x+=x
    return x

if __name__ == '__main__':
    app.secret_key="secret"
    app.run()

