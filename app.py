from flask import Flask, render_template, request, jsonify, send_file, make_response, 
from flask_mail import Mail, Message
from flask_cors import CORS
from flask import render_template_string

#for ytubefetch......
from pytube import YouTube
from urllib.parse import urlencode


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



# API endpoint to fetch video information
@app.route("ytubefetch/api/video_info", methods=["GET"])
def api_video_info():
    url = request.args.get("url")
    if url:
        try:
            yt = YouTube(url)
            video_streams = yt.streams.filter(file_extension="mp4", progressive=True)
            thumbnail_url = yt.thumbnail_url
            resolutions = [{"resolution": stream.resolution, "size_mb": stream.filesize / (1024 * 1024), "download_link": f"/api/download?url={url}&resolution={stream.resolution}"} for stream in video_streams]
            # resolutions = [{"resolution": stream.resolution, "size": stream.filesize, "download_link": f"/api/download?url={url}&resolution={stream.resolution}"} for stream in video_streams]
            return jsonify({"title": yt.title, "resolutions": resolutions, "thumbnail_url": thumbnail_url})
        except Exception as e:
            return jsonify({"error": "An error occurred: " + str(e)})
    return jsonify({"error": "URL parameter is required."})
# API endpoint to download a video
@app.route("ytubefetch/api/download", methods=["GET"])
def api_download():
    url = request.args.get("url")
    resolution = request.args.get("resolution")
    if not url or not resolution:
        return jsonify({"error": "URL and resolution are required parameters."})
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(res=resolution, file_extension="mp4", progressive=True).first()
        video_file = video_stream.download()
        filename = f"{yt.title}_{resolution}.mp4"
        with open(video_file, 'rb') as file:
            video_content = file.read()
        response = make_response(video_content)
        response.headers['Content-Type'] = 'video/mp4'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    except Exception as e:
        return jsonify({"error": "An error occurred while downloading: " + str(e)})




if __name__ == '__main__':
    app.run(debug=True)
