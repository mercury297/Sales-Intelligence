from app import app,db
from app.models import User,Data,CompanyData


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,'Data':Data,'CompanyData':CompanyData}
# CompanyData.query.filter_by(or_(CompanyData.Company = "Google"))