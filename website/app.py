from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Background Tasks</h1>
    <form action="/run_task" method="post">
        <button type="submit" name="task" value="colour_detection">Color Detection</button>
        <button type="submit" name="task" value="emotion_detection">Emotion Detection</button>
        <button type="submit" name="task" value="object_detection">Object Detection</button>
        <button type="submit" name="task" value="picture_to_text">Picture to Text</button>
        <button type="submit" name="task" value="scene_description">Scene Description</button>
        <button type="submit" name="task" value="video_calling">Video Calling</button>
    </form>
    """

@app.route('/run_task', methods=['POST'])
def run_task():
    task = request.form['task']
    if task == 'colour_detection':
        subprocess.Popen(['python', 'C:\\Users\\Debarghya Kundu\\Desktop\\dream project\\colourdetection\\final.py'])
    elif task == 'emotion_detection':
        subprocess.Popen(['python', 'C:\\Users\\Debarghya Kundu\\Desktop\\dream project\\Emotion_Detection\\final.py'])
    elif task == 'object_detection':
        subprocess.Popen(['python', 'C:\\Users\\Debarghya Kundu\\Desktop\\dream project\\object detection\\final.py'])
    elif task == 'picture_to_text':
        subprocess.Popen(['python', 'C:\\Users\\Debarghya Kundu\\Desktop\\dream project\\picture to text conversion\\Final.py'])
    elif task == 'scene_description':
        subprocess.Popen(['python', 'C:\\Users\\Debarghya Kundu\\Desktop\\dream project\\Scene describer\\final.py'])
    elif task == 'video_calling':
        # Add your logic for video calling here
        pass
    return 'Task started in the background.'

if __name__ == '__main__':
    app.run(debug=True)
