from app import create_app

from app.models import User, Task

import sqlalchemy as sa
import sqlalchemy.orm as so

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'User': User, 'Task': Task} 


if __name__ == "__main__":
    app.run(debug=True, passthrough_errors=True,
    use_debugger=False, use_reloader=False, host="0.0.0.0")