from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Location URL", validators=[DataRequired(), URL()])
    open_time = StringField("Open Time", validators=[DataRequired()])
    close_time = StringField("Close Time", validators=[DataRequired()])
    coffee = SelectField(
        "Coffee Rating",
        choices=[("✘", "☕️ 0"), ("☕️", "☕️ 1"), ("☕️☕️", "☕️☕️ 2"), ("☕️☕️☕️", "☕️☕️☕️ 3"), ("☕️☕️☕️☕️", "☕️☕️☕️☕️ 4"), ("☕️☕️☕️☕️☕️", "☕️☕️☕️☕️☕️ 5")],
        validators=[DataRequired()]
    )
    wifi = SelectField(
        "WiFi Rating",
        choices=[("✘", "✘ 0"), ("💪", "💪 1"), ("💪💪", "💪💪 2"), ("💪💪💪", "💪💪💪 3"), ("💪💪💪💪", "💪💪💪💪 4"), ("💪💪💪💪💪", "💪💪💪💪💪 5")],
        validators=[DataRequired()]
    )
    power = SelectField(
        "Power Outlet Rating",
        choices=[("✘", "✘ 0"), ("🔌", "🔌 1"), ("🔌🔌", "🔌🔌 2"), ("🔌🔌🔌", "🔌🔌🔌 3"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌 4"), ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌 5")],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print(form.cafe.data, form.location.data, form.open_time.data, form.close_time.data, form.coffee.data,
              form.wifi.data, form.power.data)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([
                form.cafe.data,
                form.location.data,
                form.open_time.data,
                form.close_time.data,
                form.coffee.data,
                form.wifi.data,
                form.power.data,
            ])
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',', quotechar='"')
        next(csv_data) # 첫번째 행 건너띄기
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
