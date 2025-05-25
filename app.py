from flask import Flask, render_template, send_file, request
import glob
from pathlib import Path
import os
import zipfile
from datetime import datetime
import shutil

app = Flask(__name__)

class UploadedImage():
	def __init__():

		pass


@app.route("/image/<fp>")
def get_image(fp):
	return send_file("photos/" +fp)

@app.route("/")
def hello_world():
	files = [Path(f).relative_to("photos") for f in glob.glob("photos/*.jpg")]

	return render_template('photos.html', files=files)


@app.route("/download", methods=['POST'])
def download():
	request_data = request.get_json()
	print(request_data)
	# TODO: pad each file
	fname = zipfiles(request_data['files'])
	return send_file(fname)

def zipfiles(files):
	fname = f"download-{datetime.today().strftime('%Y-%m-%d %H-%M-%S')}"
	# with zipfile.ZipFile(fname, mode="w") as zipf:
	# 	for fp in files:
	# 		zipf.write("photos/" +fp)
	tmp_path = (Path("tmp")/ Path(fname))
	tmp_path.mkdir(exist_ok=True)
	for fp in files:
		shutil.copy("photos/" +fp, dst=tmp_path)
	zname = shutil.make_archive(fname, base_dir=tmp_path, format="zip")
	return zname
	