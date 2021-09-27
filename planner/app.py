import json
import logging

from attr import asdict
from flask import Flask, render_template, request

from planner.planning import ActionPlanSelector, Task

application = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)


@application.route('/', methods=['POST', 'GET'])
def index():
    select_action_plan = ActionPlanSelector()
    context = {}
    status_code = 200
    if request.method == 'POST':
        f = request.files['tasks-file']
        try:
            data = json.load(f)
            tasks = [Task(**el) for el in data]
            application.logger.info("Tasks received: tasks=%d", len(tasks))

            action_plan = select_action_plan(tasks)
            application.logger.info("Winner found: tasks=%d reward=%d", len(action_plan.tasks), action_plan.reward)

            context['result'] = {}
            context['result']['selected_tasks'] = [asdict(t) for t in action_plan.tasks]
            context['result']['excluded_tasks'] = [asdict(t) for t in tasks if t not in action_plan.tasks]
        except (json.JSONDecodeError, TypeError):
            application.logger.error("Corrupted JSON file received or tasks in wrong format")
            context['error'] = "Corrupted JSON file received or tasks in wrong format"
            status_code = 400
    return render_template('index.html', context=context), status_code


if __name__ == "__main__":
    application.run()
