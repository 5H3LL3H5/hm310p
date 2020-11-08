# noxfile.py
import nox

@nox.session(python=['3.9.0', '3.8.2', '3.6.9'])
def tests(session):
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
