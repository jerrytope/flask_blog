from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'sammy sammy',
        'title': 'The Rhythmic Heartbeat of Nigeria: A Glimpse into its Vibrant Music Scene',
        'content': """A Tapestry of Sounds and Styles

        Nigerian music is a colorful tapestry woven from a multitude of sounds and styles. From the rhythmic beats of Afrobeat, the soulful melodies of Highlife, to the infectious tunes of Afro-pop, there's something for everyone. It's no wonder Nigeria's music has gained global recognition, with artists like Fela Kuti, Burna Boy, and Wizkid making waves on the international stage.

        Afrobeats: The Global Sensation

        One cannot delve into Nigerian music without mentioning Afrobeats. This genre, characterized by its fusion of traditional African rhythms, high-energy beats, and contemporary lyrics, has taken the world by storm. Afrobeats stars like Davido, Tiwa Savage, and Yemi Alade have carved out a niche for themselves, becoming household names worldwide.""",
        'date_posted': 'August 29, 2023'
    },
    {
        'author': 'Jane Doe',
        'title': 'The Passion and Growth of Football in Nigeria',
        'content': """Football in Nigeria is not just a sport; it's a way of life. The beautiful game has captured the hearts of millions in this West African nation, becoming more than just a pastime. It's a source of unity, pride, and inspiration.

The Early Days:

        Football's history in Nigeria dates back to the early 20th century when British colonialists introduced the game to the locals. It didn't take long for Nigerians to embrace the sport, and by the 1940s, football clubs began to emerge across the country. The passion for football grew, and soon, Nigeria had a thriving football culture.

        The Rise of Nigerian Footballers:

        One of the most remarkable aspects of Nigerian football is the talent it has produced over the years. Players like Nwankwo Kanu, Jay-Jay Okocha, and Austin Okocha have achieved international stardom, plying their trade in top European leagues and representing Nigeria on the global stage. Their success has not only brought glory to the nation but has also inspired countless young Nigerians to pursue football as a career.

""",
      'date_posted': 'August 30, 2023'
    },

        {
        'author': 'sammy boy',
        'title': 'Navigating the Complex Landscape of Nigerian Politics',
        'content': """When it comes to politics, few countries rival Nigeria in terms of complexity and vibrancy. Situated in West Africa, Nigeria is not only the continent's most populous nation but also one with a rich and intricate political history. In this short blog, we'll take a glimpse into the multifaceted world of Nigerian politics.

        1. Diversity and Unity:
        Nigeria's diversity is one of its defining features. With over 250 ethnic groups and numerous languages spoken, the nation is a tapestry of cultures and traditions. This diversity, while a source of pride, has also posed challenges in terms of political unity. Nigerian politics often revolves around the delicate balance between these various ethnic and religious identities.

        2. The Power Struggle:
        Like many democracies, Nigeria has experienced its fair share of political power struggles. Since gaining independence from British colonial rule in 1960, the nation has seen periods of military rule and civilian governance. A competitive two-party system has evolved, with the All Progressives Congress (APC) and the People's Democratic Party (PDP) being the dominant players.""",
        'date_posted': 'August 31, 2023'
    }
]




@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
