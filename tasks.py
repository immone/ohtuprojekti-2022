from invoke import task


@task
def start(ctx, help=False, add=False, delete=False, edit=False, list=False, bibtex=False, search=False):
    if help:
        ctx.run("python3 src/index.py help", pty=True)
    elif add:
        ctx.run("python3 src/index.py add", pty=True)
    elif delete:
        ctx.run("python3 src/index.py delete", pty=True)
    elif edit:
        ctx.run("python3 src/index.py edit", pty=True)
    elif list:
        ctx.run("python3 src/index.py list", pty=True)
    elif bibtex:
        ctx.run("python3 src/index.py bibtex", pty=True)
    elif search:
        ctx.run("python3 src/index.py search", pty=True)
    else:
        ctx.run("python3 src/index.py", pty=True)

@task
def build(ctx):
    ctx.run("python3 src/build.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def lint(ctx):
    ctx.run("pylint --fail_under=8 src", pty=True)

@task
def format(ctx):  # pylint: disable=redefined-builtin
    ctx.run("autopep8 --in-place --recursive src", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
