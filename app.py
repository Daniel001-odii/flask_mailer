from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from flask import render_template_string

app = Flask(__name__)
CORS(app)

# Configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'danielsinterest@gmail.com'
app.config['MAIL_PASSWORD'] = 'qksdojcrljuxzaso'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



#this first function is used for sending a predefined email for test....
@app.route('/custom', methods=['GET', 'POST'])
def custom_email():
    msg = Message(f'{name} via Techzone support form',
        sender='deoscomputers@gmail.com',
        recipients=['xenithheight@gmail.com', 'deoscomputers@gmail.com']
    )
    name = "anon"
    email = "anonTest@techzone.com"
    phone = "234567890"
    message = "this is a test email"
    msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    email_content = render_template_string(
        open('email_template.html').read(),
        name=name, email=email, phone=phone, message=message
    )
    
    msg.html = email_content
    mail.send(msg)
    return jsonify({'message': 'Form submitted successfully'})



def send_email(name, email, phone, message):
    msg = Message( f'{name} via Techzone support form',
        sender='deoscomputers@gmail.com',
        recipients=['xenithheight@gmail.com']
    )
    email_content = render_template_string(
        open('email_template.html').read(),
        name=name, email=email, phone=phone, message=message
    )
    
    msg.html = email_content
    mail.send(msg)



@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        send_email(name, email, phone, message)

        return jsonify({'message': 'Form submitted successfully'})

    return render_template('contact_form.html')


#the email api route is below................
@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

    send_email(name, email, phone, message)

    response = {'message': 'Form submitted successfully'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
