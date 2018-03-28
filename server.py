from sanic import Sanic
from sanic.response import json, html, text
from sanic.config import Config
from sanic_cors import CORS, cross_origin
Config.KEEP_ALIVE = False
import os
import uuid
import server_analyzer as img_analyzer

app = Sanic(__name__)
CORS(app)

app.static('/', './static')

@app.route("/", methods=['GET'])
async def test(request):
  return text('It\'s working!')

@app.route("/api/v1/test", methods=['GET'])
async def api_test(request):
  return text('It\'s working!')

@app.route('/api/v1/upload', methods=['POST'])
async def post_handler(request):
  if request.files.get("image") is None:
    return json(
      {'message': 'Upload data is not valid.', 'error':'IMAGE_NOT_SET'},
        headers={'X-Served-By': 'sanic'},
        status=400
    )
  else:
    image_filename, image_extension = os.path.splitext(request.files.get('image').name)
    image_filetype = request.files.get('image').type
    # Extrae los datos del archivo recibido
    image_data = bytearray(request.files.get('image').body)
    id = uuid.uuid4().hex
    input_file = '.temp/'+id+'.jpg'
    file_storage = open(input_file, 'wb')  # Output file
    file_storage.write(image_data)
    file_storage.close()

    response = img_analyzer.analyze_apples(input_file, 'images/red-template.png')
    os.remove(input_file)
    return json(
      {'results': response},
        headers={'X-Served-By': 'sanic'},
        status=200
    )

app.run(host="0.0.0.0", port=8264)
