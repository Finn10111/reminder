from flask import Blueprint, render_template, send_file
from icalendar import Calendar, Alarm
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import IntegerField, SubmitField
from wtforms.widgets import NumberInput
import tempfile

index = Blueprint('index', __name__, template_folder='templates')


@index.route("/", methods=['GET', 'POST'])
def addreminder():
    form = IcsForm()
    content = render_template('index.html', form=form)
    file = form.icsfile.data
    if not file:
        return content

    hours = form.hours.data
    minutes = form.minutes.data
    try:
        # try to read ics file
        calendar = Calendar.from_ical(file.read())
    except ValueError:
        error = 'can\'t read file'
        return render_template('index.html', form=form, error=error)

    # iterate over every event in ics file
    for component in calendar.walk('VEVENT'):
        valarm_found = False
        for k, v in component.property_items():
            if k == 'BEGIN' and v == 'VALARM':
                valarm_found = True

        # add alarm if not already set
        if not valarm_found:
            # add alarms with given times
            alarm = Alarm()
            alarm.add('ACTION', 'DISPLAY')
            alarm.add('DESCRIPTION', component.get('SUMMARY'))
            alarm.add('TRIGGER;VALUE=DURATION', '-PT%dH%dM' % (hours, minutes))
            component.add_component(alarm)

    new_ics = tempfile.TemporaryFile()
    new_ics.write(calendar.to_ical())
    new_ics.seek(0)
    new_filename = file.filename.rstrip('.ics') + '_with_reminders' + '.ics'
    return send_file(new_ics, as_attachment=True,
                     download_name=new_filename)


class IcsForm(FlaskForm):
    icsfile = FileField('ICS File', validators=[FileRequired()])
    hours = IntegerField('Hours', default=0,
                         widget=NumberInput(step=1, min=0, max=24))
    minutes = IntegerField('Minutes', default=0,
                           widget=NumberInput(step=5, min=0, max=55))
    submit = SubmitField('Submit')
