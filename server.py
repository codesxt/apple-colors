import os
import uuid
import datetime
from sanic import Sanic
from sanic.response import json, html, text
from sanic.config import Config
from sanic_cors import CORS, cross_origin
#Config.KEEP_ALIVE = False
Config.REQUEST_TIMEOUT    = 60*100
Config.RESPONSE_TIMEOUT   = 60*100
Config.KEEP_ALIVE_TIMEOUT = 60*100
Config.KEEP_ALIVE         = True
Config.REQUEST_MAX_SIZE   = 100000000000
import server_analyzer as img_analyzer
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.tz import tzlocal
from pathlib import Path

def log_message(message):
  print(datetime.datetime.now(tzlocal()).strftime('[%Y-%m-%d %H:%M:%S %z] ' + message))

app = Sanic(__name__)
CORS(app)

app.static('/', './static')

scheduler = BackgroundScheduler()
scheduler.start()
def crear_image_folder():
  log_message('Cleaning image folder. Clean static/results/*.png')
  for p in Path("./static/results/").glob("*.png"):
    p.unlink()
scheduler.add_job(crear_image_folder, trigger='cron', hour='0')

@app.route("/", methods=['GET'])
async def test(request):
  return text('It\'s working!')

@app.route("/api/v1/test", methods=['GET'])
async def api_test(request):
  return text('It\'s working!')

@app.route('/api/v1/upload', methods=['POST'])
async def post_handler(request):
  log_message('An image upload was received')
  if request.files.get('image') is None:
    return json(
      {'message': 'Upload data is not valid.', 'error':'IMAGE_NOT_SET'},
        headers={'X-Served-By': 'sanic'},
        status=400
    )
  else:
    log_message('Opening image.')
    image_filename, image_extension = os.path.splitext(request.files.get('image').name)
    image_filetype = request.files.get('image').type
    # Extrae los datos del archivo recibido
    log_message('Loading image data.')
    image_data = bytearray(request.files.get('image').body)
    id = uuid.uuid4().hex
    input_file = '.temp/'+id+'.jpg'
    file_storage = open(input_file, 'wb')  # Output file
    file_storage.write(image_data)
    file_storage.close()

    log_message('Starting analysis.')
    response  = img_analyzer.analyze_apples(input_file, 'images/red-template.png', id)
    response2 = img_analyzer.hsv_analysis(input_file, id)
    log_message('Analysis done.')
    os.remove(input_file)
    return json(
      {
        'results': response,
        'results2' : response2
        },
        headers={'X-Served-By': 'sanic'},
        status=200
    )

app.run(host="0.0.0.0", port=8264)
