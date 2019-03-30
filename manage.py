from main import app, db, User, Blog, Post, Comment, Tag, migrate

@app.shell_context_processor
def make_shell_context():
  return dict(app=app, db=db, User=User, Blog=Blog, Post=Post, Comment=Comment, Tag=Tag, migrate=migrate) 

