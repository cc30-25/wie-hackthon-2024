from flask import Flask, render_template, request, redirect, url_for, flash
import holidays
from datetime import date, datetime
import calendar

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

holiday_db = holidays.US(years=2024) + holidays.CA(years=2024)

def add_holiday(date_str, holiday_name):
    try:
        year, month, day = map(int, date_str.split('-'))
        holiday_date = date(year, month, day)
        holiday_db[holiday_date] = holiday_name
        return True, f"Added: {holiday_name} on {holiday_date}"
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."

def get_month_data(year, month):
    cal = calendar.monthcalendar(year, month)
    holidays_in_month = []
    for week in cal:
        for day in week:
            if day != 0:
                current_date = date(year, month, day)
                if current_date in holiday_db:
                    holidays_in_month.append((day, holiday_db[current_date]))
    return cal, holidays_in_month

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

    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Generate data for 12 months starting from the current month
    months_data = []
    for i in range(12):
        year = current_year + (current_month + i - 1) // 12
        month = (current_month + i - 1) % 12 + 1
        cal, holidays = get_month_data(year, month)
        months_data.append({
            'year': year,
            'month': calendar.month_name[month],
            'calendar': cal,
            'holidays': holidays
        })

    return render_template('index.html', months_data=months_data)

if __name__ == '__main__':
    app.run(debug=True)
