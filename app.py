from flask import Flask, render_template, request, redirect, url_for, flash
import holidays
from datetime import date, datetime
import calendar

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

# Create a base holiday dictionary
holiday_db = holidays.US(years=2024) + holidays.CA(years=2024)  # Using US holidays for example

def add_holiday(date_str, holiday_name):
    try:
        year, month, day = map(int, date_str.split('-'))
        holiday_date = date(year, month, day)
        holiday_db[holiday_date] = holiday_name
        return True, f"Added: {holiday_name} on {holiday_date}"
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date_str = request.form['date']
        holiday_name = request.form['name']
        success, message = add_holiday(date_str, holiday_name)
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        return redirect(url_for('index'))

    year = datetime.now().year
    month = datetime.now().month
    cal = calendar.monthcalendar(year, month)
    
    holidays_in_month = []
    for week in cal:
        for day in week:
            if day != 0:
                current_date = date(year, month, day)
                if current_date in holiday_db:
                    holidays_in_month.append((day, holiday_db[current_date]))
    
    return render_template('index.html', 
                           calendar=cal, 
                           holidays=holidays_in_month,
                           month=calendar.month_name[month],
                           year=year)

if __name__ == '__main__':
    app.run(debug=True)
