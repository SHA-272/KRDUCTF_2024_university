from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

ids_with_images = {
    '111': '111.png',
    '11': '11.jpg',
    '12': '12.jpg',
    '13': '13.png',
    '15': '15.png',
    '21': '21.png',
    '22': '22.png',
    '23': '23.png',
    '42': '42.png',
    '73': '73.png',
    '85': '85.png',
    '91': '91.png',
    '72': '72.png',
    '53': '53.png',
}

hidden_id = '1195'

@app.route('/')
def home():
    return render_template('home.html', ids_with_images=ids_with_images, hidden_id=hidden_id)

@app.route('/object/id=<string:id>')
def object(id):
    if id in ids_with_images or id == hidden_id:
        image_path = ids_with_images.get(id, '787.png')
        return render_template('object.html', id=id, image_path=image_path)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
