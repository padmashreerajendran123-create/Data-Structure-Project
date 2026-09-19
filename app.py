from flask import Flask, render_template, request, redirect, url_for
from data_structures import ContactLinkedList, UndoStack, CallQueue

app = Flask(__name__)

directory = ContactLinkedList()
undo_stack = UndoStack()
call_queue = CallQueue(capacity=10)


@app.route('/')
def page_directory():
    return render_template('directory.html', contacts=directory.to_array())


@app.route('/add', methods=['GET', 'POST'])
def page_add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        added = directory.add_contact(name, phone, email)

        if added:
            return redirect(url_for('page_directory'))

        return "Contact already exists!"

    return render_template('add_contact.html')


@app.route('/favorites')
def page_favorites():
    return render_template('favorites.html', favorites=directory.get_favorites())


@app.route('/calls')
def page_calls():
    return render_template('calls.html', calls=call_queue.get_all())


@app.route('/trash')
def page_trash():
    return render_template('trash.html', trash=undo_stack.get_all())


@app.route('/action/favorite/<name>', methods=['POST'])
def action_favorite(name):
    directory.toggle_favorite(name)
    return redirect(request.referrer or url_for('page_directory'))


@app.route('/action/call/<name>', methods=['POST'])
def action_call(name):
    contacts = directory.to_array()

    for contact in contacts:
        if contact['name'].lower() == name.lower():
            call_queue.enqueue(contact)
            break

    return redirect(url_for('page_calls'))


@app.route('/action/delete/<name>', methods=['POST'])
def action_delete(name):
    deleted = directory.delete_contact(name)

    if deleted:
        undo_stack.push(deleted)

    return redirect(url_for('page_directory'))


@app.route('/action/undo', methods=['POST'])
def action_undo():
    restored = undo_stack.pop()

    if restored:
        directory.add_contact(
            restored['name'],
            restored['phone'],
            restored['email'],
            restored.get('is_favorite', False)
        )

    return redirect(url_for('page_trash'))

@app.route('/action/clear-calls', methods=['POST'])
def action_clear_calls():
    call_queue.clear()
    return redirect(url_for('page_calls'))


if __name__ == '__main__':
    app.run(debug=True)
