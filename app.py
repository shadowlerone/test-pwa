from flask import Flask, render_template, send_file, request
import glob
from pathlib import Path
import os
import zipfile
from datetime import datetime
import shutil
import os
from padder import pad_file


app = Flask(__name__)



@app.route("/image/<fp>")
def get_image(fp):
	return send_file("photos/" +fp)

@app.route("/")
def hello_world():
	files = sorted([Path(f).relative_to("photos") for f in glob.glob("photos/*.jpg")], reverse=True)

	return render_template('photos.html', files=files)


@app.route("/download", methods=['POST'])
def download():
	request_data = request.get_json()
	files = request_data['files']
	print(request_data)

	fname = f"download-{datetime.today().strftime('%Y-%m-%d %H-%M-%S')}"
	tmp_path = (Path("tmp")/ Path(fname))
	originals = tmp_path/"originals"
	padded = tmp_path/"padded"
	originals.mkdir(exist_ok=True, parents=True)
	padded.mkdir(exist_ok=True, parents=True)
	for fp in files:
		path = Path("photos/" +fp)
		shutil.copy(path, dst=originals)
		pad_file(path, padded/fp)
	zname = shutil.make_archive(tmp_path, base_dir=fname, root_dir="tmp", format="zip")

	return send_file(zname)

	