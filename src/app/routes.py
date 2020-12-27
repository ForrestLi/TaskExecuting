from flask import request, jsonify, redirect, url_for
from flask import Flask
from flask import render_template
from src.taskcore.task_utilities import TaskBuilder

app = Flask(__name__)


@app.route("/")
@app.route('/task', methods=['GET','POST'])
def task():
    if request.method == 'GET':
       return render_template('task.html', title='Task')
    if request.method == 'POST':
       request_result = request.form.to_dict()
       if request_result is None:
           request_result = {}
       result=request_result
       return redirect(url_for("task_result", res=result))

@app.route('/<res>')
def task_result(res):
    dic_a = {'stage1': eval(res)}
    tb = TaskBuilder(dic_a)
    result = tb.execute()
    return f"<h1>{result}<h1>"
    #return render_template('result.html', title='TaskResult')

