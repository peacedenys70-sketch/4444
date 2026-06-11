"""
Script d'initialisation de la base de données.
À exécuter UNE SEULE FOIS après le déploiement sur Render.

Usage :
  python init_db.py

Ce script :
  1. Crée toutes les tables définies dans models.py
  2. (Optionnel) Insère des données de test si --seed est passé
"""
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / '.env')

from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès.")

    if '--seed' in sys.argv:
        from werkzeug.security import generate_password_hash
        from app.models import Utilisateur, Competence, user_competence, user_lacune
        from sqlalchemy import insert

        # Utilisateurs de démonstration
        users_data = [
            dict(nom='AHOUANTO', prenom='Léonce',  email='leonce@ifri.bj', telephone='+22901000001',
                 mot_de_passe=generate_password_hash('password123'), filiere='SI', niveau='M2',
                 bio='Passionné de sécurité et de développement web.'),
            dict(nom='DEGUENNON', prenom='Jeffry',  email='jeffry@ifri.bj', telephone='+22901000002',
                 mot_de_passe=generate_password_hash('password123'), filiere='GL', niveau='M1',
                 bio='Développeur backend Python/Flask.'),
            dict(nom='PARE', prenom='Ibrahim', email='ibrahim@ifri.bj', telephone='+22901000003',
                 mot_de_passe=generate_password_hash('password123'), filiere='IA', niveau='M2',
                 bio='Machine Learning et algorithmes.'),
            dict(nom='TOSSOU', prenom='Salomon', email='salomon@ifri.bj', telephone='+22901000004',
                 mot_de_passe=generate_password_hash('password123'), filiere='GL', niveau='L3',
                 bio='Développeur fullstack.'),
            dict(nom='EDAH', prenom='Laurine', email='laurine@ifri.bj', telephone='+22901000005',
                 mot_de_passe=generate_password_hash('password123'), filiere='SI', niveau='L2',
                 bio='Sécurité des réseaux.'),
        ]

        comps_data = ['Python', 'JavaScript', 'SQL', 'Algorithmique', 'Réseaux',
                      'Machine Learning', 'HTML/CSS', 'Linux', 'Java', 'C/C++']

        with app.app_context():
            # Compétences
            comps = {}
            for nom in comps_data:
                c = Competence.query.filter_by(nom_competence=nom).first()
                if not c:
                    c = Competence(nom_competence=nom)
                    db.session.add(c)
                    db.session.flush()
                comps[nom] = c

            # Utilisateurs
            created = []
            for ud in users_data:
                u = Utilisateur.query.filter_by(email=ud['email']).first()
                if not u:
                    u = Utilisateur(**ud)
                    db.session.add(u)
                    db.session.flush()
                created.append(u)

            # Compétences / lacunes de démo
            demo = [
                (created[0], ['Python','JavaScript','HTML/CSS','SQL'],     ['Machine Learning','Linux']),
                (created[1], ['Python','SQL','Linux','Java'],               ['Machine Learning','JavaScript']),
                (created[2], ['Python','Machine Learning','Algorithmique'], ['SQL','Réseaux']),
                (created[3], ['JavaScript','HTML/CSS','SQL','Java'],        ['Machine Learning','Linux']),
                (created[4], ['Réseaux','Linux','Algorithmique'],           ['Python','Machine Learning']),
            ]
            for user, comp_noms, lac_noms in demo:
                for nom in comp_noms:
                    db.session.execute(insert(user_competence).prefix_with('OR IGNORE').values(
                        id_user=user.id_user, id_competence=comps[nom].id_competence
                    ) if db.engine.dialect.name == 'sqlite' else
                    insert(user_competence).values(
                        id_user=user.id_user, id_competence=comps[nom].id_competence
                    ).on_conflict_do_nothing())
                for nom in lac_noms:
                    db.session.execute(
                        insert(user_lacune).values(
                            id_user=user.id_user, id_competence=comps[nom].id_competence
                        ).on_conflict_do_nothing()
                    )

            db.session.commit()
            print("✅ Données de test insérées.")
            print("   Comptes créés (mot de passe : password123) :")
            for u in created:
                print(f"   → {u.email}  ({u.prenom} {u.nom}, {u.niveau} {u.filiere})")
