# noxfile.py
import nox


@nox.session(python=['3.9.0', '3.8.2', '3.6.9'])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")
