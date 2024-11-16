from flask import Flask, render_template, request, jsonify
import holidays
from datetime import date, datetime
import calendar

app = Flask(__name__)

# Create a base holiday dictionary
holiday_db = holidays.US(years=2024)  # You can change the country and year as needed

def add_holiday(date_str, holiday_name):
    try:
        # Parse the date string (assuming format is YYYY-MM-DD)
        year, month, day = map(int, date_str.split('-'))
        holiday_date = date(year, month, day)
        
        # Add the new holiday to the database
        holiday_db[holiday_date] = holiday_name
        return True, f"Added: {holiday_name} on {holiday_date}"
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."

def validate_holiday(date_str):
    try:
        # Parse the date string
        year, month, day = map(int, date_str.split('-'))
        check_date = date(year, month, day)
        
        # Check if the date is in the holiday database
        if check_date in holiday_db:
            return True, holiday_db[check_date]
        else:
            return False, None
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_calendar')
def get_calendar():
    year = datetime.now().year
    month = datetime.now().month
    cal = calendar.monthcalendar(year, month)
    holidays_in_month = [
        (day, holiday_db[date(year, month, day)])
        for day in range(1, 32)
        if date(year, month, day) in holiday_db
    ]
    return jsonify({
        'calendar': cal,
        'holidays': holidays_in_month,
        'month': calendar.month_name[month],
        'year': year
    })

@app.route('/add_holiday', methods=['POST'])
def add_holiday_route():
    data = request.json
    success, message = add_holiday(data['date'], data['name'])
    return jsonify({'success': success, 'message': message})

@app.route('/check_holiday', methods=['POST'])
def check_holiday():
    data = request.json
    is_holiday, holiday_name = validate_holiday(data['date'])
    return jsonify({'is_holiday': is_holiday, 'holiday_name': holiday_name})

if __name__ == '__main__':
    app.run(debug=True)