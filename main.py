import os
import shutil
from flask import Flask,Blueprint,render_template,redirect,url_for,request,flash
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
import socket
from init import db, create_app
from modele import Fisier,User


# Blueprint este un obiect pentru acces fisier
main = Blueprint('main',__name__)


def verifica_fisier(nume_fisier):
    return '.' in nume_fisier and \
           nume_fisier.rsplit('.', 1)[1].lower() in \
           {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','pdf','doc'}


@main.route('/RepairStorageDevice',methods=['POST'])
def incarca_fisier():
    if 'file' not in request.files:
        flash('Nu este fisier')
        return redirect(url_for('main.repairstorage'))
    fisier = request.files['file']

    if fisier.filename == '':
        flash('Nu este fisier')
        return redirect(url_for('main.repairstorage'))

    if not verifica_fisier(fisier.filename):
        extensie = fisier.filename[fisier.filename.index('.'):len(fisier.filename)]
        flash('Nu este permis fisierul de tip ' + extensie)
        return redirect(url_for('main.repairstorage'))

    if fisier and verifica_fisier(fisier.filename):
        nume_fisier = secure_filename(fisier.filename)
        backup_utilizator = 'backup\\'+current_user.name
        if not os.path.exists(backup_utilizator):
            os.mkdir(backup_utilizator)
        fisier.save(os.path.join(backup_utilizator, nume_fisier))

        fisier = Fisier.query.filter_by(calefisier=secure_filename(os.path.join(backup_utilizator, nume_fisier))).first()

        if not fisier:
            # inregistreaza fisier in baza de date
            new_fisier = Fisier(calefisier=secure_filename(os.path.join(backup_utilizator, nume_fisier)),
                                userid=current_user.id)
            db.session.add(new_fisier)
            db.session.commit()
            fisier = Fisier.query.filter_by(calefisier=secure_filename(os.path.join(backup_utilizator, nume_fisier))).first()

            flash('Fisierul ' + fisier.calefisier + ' s-a adaugat in baza de date')
            return redirect(url_for('main.repairstorage', name=nume_fisier))

        if fisier:
            flash('Fisierul ' + fisier.calefisier + ' este deja incarcat')
        return redirect(url_for('main.repairstorage', name=nume_fisier))

    return redirect(url_for('main.repairstorage'))


@main.route('/profile')
def profile():
    return render_template('profile.html')


@main.route('/RepairStorageDevice')
@login_required
def repairstorage():

    user = User.query.filter_by(id=current_user.id).first()
    fisierequery = Fisier.query.filter_by(userid=user.id)
    cai_fisier = []

    for fisier in fisierequery:
        cai_fisier.append(fisier.calefisier)
    return render_template("repairstorage.html",
                           name=current_user.name,
                           fisiere=cai_fisier
                           )


@main.route('/')
def index():
    return render_template('index.html')


def parcurgeFisier(fisier=os.getcwd()):
    caidirectoare = []
    os.mkdir('backup') if not os.path.exists('backup') else print('Are fisier backup.')
    for root,files,subdirectories in os.walk(fisier):
        for file in files:
            try:
                shutil.copy(os.path.join(root,file),os.path.join('backup',file))
            except Exception as e:
                print('Nu se poate copia ', e)
            caidirectoare.append(os.path.join(root[0:int(len(root)/4)],'...'+file[int(len(file)/4):len(file)]))
    return caidirectoare


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # socket.gethostname() pentru a lua numele calculatorului
    # socket.gethostbyname(nume_calculator) pentru a seta host la adresa IP a calculatorului
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host=socket.gethostbyname(socket.gethostname()))
