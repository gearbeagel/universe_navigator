from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash, generate_password_hash

from models import db, Work, Character, Terminology, Relationship, Universe, User
from utils import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Funnyhaha111@localhost:3306/universe_navigator'
db.init_app(app)
bcrypt = Bcrypt(app)
app.static_folder = 'static'
app.secret_key = 'macdon7t'
with app.app_context():
    db.create_all()

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            e = 'Username is already taken. Please choose another.'
            return render_template("failure_page.html", failure_message=e)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main_page'))
        else:
            flash('Login failed. Check your username and password.')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/')
def main_page():
    if current_user.is_authenticated:
        return render_template("main_page.html", username=current_user.username)
    else:
        return render_template("main_unlogged.html")


@app.route('/create')
def create_route():
    return render_template("create.html")


@app.route('/delete')
def delete_route():
    return render_template("delete.html")


@app.route('/show_all')
def show_all_route():
    return render_template("show_all.html")


@app.route('/edit')
def edit_route():
    return render_template("edit.html")


@app.route('/success_page')
def success_page():
    return render_template('success_page.html')


@app.route('/failure_page')
def failure_page():
    return render_template('failure_page.html')


@app.route('/create_universe', methods=['GET', 'POST'])
def create_universe_route():
    if request.method == 'POST':
        try:
            data = request.form
            title = data['title']
            author = current_user.username
            create_a_universe(db.session, title, author)
            success = True
            if success:
                success_message = "Universe created successfully!"
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)

    return render_template("create_a_universe.html")


@app.route('/create_character', methods=['GET', 'POST'])
def create_character_route():
    if request.method == 'POST':
        try:
            data = request.form
            universe_name = data['universe_name']
            universe_id = get_universe_id_by_name(universe_name)
            create_a_character(
                db.session,
                universe_id,
                data['char_name'],
                data['gender'],
                int(data['age']),
                data['status'],
                data['biography'],
            )
            success = True
            if success:
                success_message = "Character created successfully!"
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)
    universes = Universe.query.all()
    return render_template("create_a_character.html", universes=universes)


@app.route('/create_work', methods=['GET', 'POST'])
def create_work_route():
    if request.method == 'POST':
        try:
            data = request.form
            universe_name = data['universe_name']
            universe_id = get_universe_id_by_name(universe_name)
            create_a_work(db.session, universe_id, data['work_title'], data['ext_link'])
            success = True
            if success:
                success_message = "Work created successfully!"
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)
    universes = Universe.query.all()
    return render_template("create_a_work.html", universes=universes)


@app.route('/create_relationship', methods=['GET', 'POST'])
def create_relationship_route():
    if request.method == 'POST':
        try:
            data = request.form
            universe_name = data['universe_name']
            universe_id = get_universe_id_by_name(universe_name)
            char_1 = get_character_id_by_name(char_name=data['char_1_name'])
            char_2 = get_character_id_by_name(char_name=data['char_2_name'])
            character_1 = Character.query.filter_by(char_id=char_1).first()
            character_2 = Character.query.filter_by(char_id=char_2).first()
            if character_1.universe_id is not character_2.universe_id:
                e = f"The characters are from different universes. It's not canon!"
                return render_template('failure_page.html', failure_message=e)
            else:
                create_a_relationship(session=db.session, universe_id=universe_id, char_1=char_1, char_2=char_2,
                                      rel_type=data['rel_type'])
                success_message = "Relationship created successfully!"
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)

    universes = Universe.query.all()
    characters = Character.query.all()
    return render_template("create_a_relationship.html", universes=universes, characters=characters)


@app.route('/create_terminology', methods=['GET', 'POST'])
def create_terminology_route():
    if request.method == 'POST':
        try:
            data = request.form
            universe_name = data['universe_name']
            universe_id = get_universe_id_by_name(universe_name)
            create_terminology(db.session, universe_id, data['term_name'], data['definition'])
            success = True
            if success:
                success_message = "Terminology created successfully!"
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)
    universes = Universe.query.all()
    return render_template("create_terminology.html", universes=universes)


@app.route('/show_all_characters', methods=['GET'])
def show_all_characters():
    universes = Universe.query.all()
    return render_template("show_all_characters.html", universes=universes)


@app.route('/show_characters_by_universe', methods=['GET'])
def show_characters_by_universe():
    universes = Universe.query.all()
    universe_name = request.args.get('universe_name')
    if universe_name:
        universe_id = get_universe_id_by_name(universe_name)
        characters = Character.query.filter_by(universe_id=universe_id).all()
        return render_template("show_all_characters.html", universes=universes, characters=characters,
                               universe_name=universe_name)
    else:
        return render_template("show_all_characters.html", universe_name=None)


@app.route('/show_all_works', methods=['GET'])
def show_all_works():
    universes = Universe.query.all()
    return render_template("show_all_works.html", universes=universes)


@app.route('/show_all_works_by_universe', methods=['GET'])
def show_all_works_by_universe():
    universes = Universe.query.all()
    universe_name = request.args.get('universe_name')
    if universe_name:
        universe_id = get_universe_id_by_name(universe_name)
        works = Work.query.filter_by(universe_id=universe_id).all()
        return render_template("show_all_works.html", universes=universes,
                               works=works, universe_name=universe_name)
    else:
        return render_template("show_all_works.html", universe_name=None)


@app.route('/show_all_relationships', methods=['GET'])
def show_all_relationships():
    universes = Universe.query.all()
    return render_template("show_all_relationships.html", universes=universes)


@app.route('/show_all_relationships_by_universe', methods=['GET'])
def show_all_relationships_by_universe():
    universes = Universe.query.all()
    universe_name = request.args.get('universe_name')
    if universe_name:
        universe_id = get_universe_id_by_name(universe_name)
        rels = Relationship.query.filter_by(universe_id=universe_id).all()
        character = Character.query.filter_by(universe_id=universe_id).all()
        return render_template("show_all_relationships.html", universes=universes, rels=rels, character=character,
                               universe_name=universe_name)
    else:
        return render_template("show_all_relationships.html", universe_name=None)


@app.route('/show_all_terminology', methods=['GET'])
def show_all_terminology():
    universes = Universe.query.all()
    return render_template("show_all_terminology.html", universes=universes)


@app.route('/show_all_terminology_by_universe', methods=['GET'])
def show_all_terminology_by_universe():
    universes = Universe.query.all()
    universe_name = request.args.get('universe_name')
    if universe_name:
        universe_id = get_universe_id_by_name(universe_name)
        terms = Terminology.query.filter_by(universe_id=universe_id).all()
        return render_template("show_all_terminology.html", universes=universes, terms=terms,
                               universe_name=universe_name)
    return render_template("show_all_terminology.html")


@app.route('/delete_universe', methods=['GET', 'POST'])
def delete_universe_route():
    if request.method == 'POST':
        universe = request.form.get('universe_name')
        universe_id = get_universe_id_by_name(universe)
        delete_universe(db.session, universe_id)
        success = True
        if success:
            success_message = "Universe deleted successfully."
            return render_template('success_page.html', success_message=success_message)
    universes = Universe.query.all()
    return render_template('delete_universe.html', universes=universes)


@app.route('/delete_work', methods=['GET', 'POST'])
def delete_work_route():
    if request.method == 'POST':
        try:
            title = request.form.get('work_title')
            work_id = get_work_id_by_title(title)
            delete_work(db.session, work_id)
            success = True
            if success:
                success_message = "Work deleted successfully."
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)
    works = Work.query.all()
    return render_template('delete_work.html', works=works)


@app.route('/delete_character', methods=['GET', 'POST'])
def delete_character_route():
    if request.method == 'POST':
        try:
            char_name = request.form.get('character_name')
            char_id = get_character_id_by_name(char_name)
            delete_character(db.session, char_id)
            success = True
            if success:
                success_message = "Character deleted successfully."
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)
    characters = Character.query.all()
    return render_template('delete_character.html', characters=characters)


@app.route('/delete_terminology', methods=['GET', 'POST'])
def delete_terminology_route():
    if request.method == 'POST':
        try:
            term_name = request.form.get('term_name')
            term_id = get_term_id_by_name(term_name)
            delete_terminology(db.session, term_id)
            success = True
            if success:
                success_message = "Terminology deleted successfully."
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)
    terms = Terminology.query.all()
    return render_template('delete_terminology.html', terms=terms)


@app.route('/delete_relationship', methods=['GET', 'POST'])
def delete_relationship_route():
    if request.method == 'POST':
        try:
            character1_name = request.form.get('character1_name')
            character2_name = request.form.get('character2_name')
            rel_type = request.form.get('rel_type')
            character1_id = get_character_id_by_name(character1_name)
            character2_id = get_character_id_by_name(character2_name)
            if not Relationship.query.filter_by(
                    character1_id=character1_id,
                    character2_id=character2_id,
                    relationship_type=rel_type
            ).first():
                e = "Relationship doesn't exist. Welp :("
                return render_template('failure_page.html', failure_message=e)
            delete_relationship(db.session, character1_id, character2_id, rel_type)
            success = True
            if success:
                success_message = "Relationship deleted successfully."
                return render_template('success_page.html', success_message=success_message)
        except Exception as e:
            return render_template('failure_page.html', failure_message=e)
    characters = Character.query.all()
    return render_template('delete_relationship.html', characters=characters)


@app.route("/edit_character", methods=['GET', 'POST'])
def edit_character_route():
    if request.method == 'POST':
        character_name = request.form.get('character_name')
        table_to_edit = 'CHARACTERS'
        char_id = get_character_id_by_name(character_name)
        field_to_edit = request.form['field_to_edit']
        new_values = request.form['values']
        edit_data(db.session, table_to_edit, char_id, field_to_edit, new_values)
        success_message = "Edits made successfully."
        return render_template('success_page.html', success_message=success_message)
    characters = Character.query.all()
    return render_template('edit_character.html', characters=characters)


@app.route("/edit_work", methods=['GET', 'POST'])
def edit_work_route():
    if request.method == 'POST':
        work_title = request.form.get('work_title')
        table_to_edit = 'WORKS'
        work_id = get_work_id_by_title(work_title)
        field_to_edit = request.form['field_to_edit']
        new_values = request.form['values']
        edit_data(db.session, work_id, field_to_edit, new_values)
        success_message = "Edits made successfully."
        return render_template('success_page.html', success_message=success_message)
    works = Work.query.all()
    return render_template('edit_work.html', works=works)


@app.route("/edit_terminology", methods=['GET', 'POST'])
def edit_terminology_route():
    if request.method == 'POST':
        term_name = request.form.get('term_name')
        table_to_edit = 'TERMINOLOGY'
        term_id = get_term_id_by_name(term_name)
        field_to_edit = request.form['field_to_edit']
        new_values = request.form['values']
        edit_data(db.session, table_to_edit, term_id, field_to_edit, new_values)
        success_message = "Edits made successfully."
        return render_template('success_page.html', success_message=success_message)
    terms = Terminology.query.all()
    return render_template('edit_terminology.html', terms=terms)


if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")
