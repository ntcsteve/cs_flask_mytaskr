from flask import Flask, render_template, request, flash, redirect, url_for, g
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import DataRequired
import sqlite3

# configuration settings
DATABASE = 'mytaskr.db'

# WTF_CSRF is used by Flask WTF for cross site request forgery prevention
WTF_CSRF_ENABLED = True
SECRET_KEY = 'hard_to_guess'

# create the application package called app
app = Flask(__name__)

# Flask looks for variables within the object passed to config that are defined using ALL CAPITAL LETTERS aka DATABASE
app.config.from_object(__name__)

# create a function to connect to our database
def connect_db():

    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def tasks():

    g.db = connect_db()

    # SQL query to retrieve all the tasks flagged as Open Tasks
    cursor = g.db.execute('select name, due_date, task_id from tasks where status=1')

    # represent Open Tasks in a dictionary
    open_tasks = [dict(name=row[0], due_date=row[1], task_id=row[2]) for row in cursor.fetchall()]

    # SQL query to retrieve all the tasks flagged as Closed Tasks
    cursor = g.db.execute('select name, due_date, task_id from tasks where status=0')

    # represent Closed Tasks in a dictionary
    closed_tasks = [dict(name=row[0], due_date=row[1], task_id=row[2]) for row in cursor.fetchall()]

    g.db.close()

    # render the right html page
    return render_template('tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks)

# Add new tasks
@app.route('/add/', methods=['POST'])
def new_task():

    g.db = connect_db()
    name = request.form['name']
    date = request.form['due_date']

    # data validation to ensure all the fields are required
    if not name or not date:
        flash("All fields are required. Please try again.")
        return redirect(url_for('tasks'))

    else:
        # SQL query to insert a new task
        g.db.execute('insert into tasks (name, due_date, status) values (?, ?, 1)',
                     [request.form['name'], request.form['due_date']])
        g.db.commit()
        g.db.close()

        # a short message to acknowledge a successful post
        flash('New entry was successfully posted.')
        return redirect(url_for('tasks'))

# Mark tasks as completed using dynamic routes - task ID
@app.route('/complete/<int:task_id>/')
def complete(task_id):

    g.db = connect_db()

    # SQL query to mark a task
    g.db.execute('update tasks set status = 0 where task_id='+str(task_id))
    g.db.commit()
    g.db.close()

    # a short message to acknowledge a task is mark as completed
    flash('The task was marked as complete.')
    return redirect(url_for('tasks'))

# Delete Tasks using dynamic routes - task ID
@app.route('/delete/<int:task_id>/')
def delete_entry(task_id):

    g.db = connect_db()

    # SQL query to mark a task
    g.db.execute('delete from tasks where task_id='+str(task_id))
    g.db.commit()
    g.db.close()

    # a short message to acknowledge a task is deleted
    flash('The task was deleted.')
    return redirect(url_for('tasks'))

# A function to help with form handling and data validation
class AddTaskForm(FlaskForm):

    task_id = IntegerField()

    name = StringField(
        'Task Name',
        validators=[DataRequired()])

    due_date = DateField(
        'Date Due (dd/mm/yyyy)',
        validators=[DataRequired()],
        format='%d/%m/%Y')

    status = IntegerField('Status')

# start the development server using the run() method in debug mode
if __name__ == '__main__':
    app.run(debug=True)
