function toggleImageState(fp) {
	checkbox = document.getElementById(`check-${fp}`)
	grid_image = checkbox.parentElement
	current_state = checkbox.checked
	next_state = !current_state
	checkbox.checked = next_state
	if (next_state == true) {
		grid_image.classList.add("checked")
	} else {
		grid_image.classList.remove("checked")

	}
}


function download_files() {
	let files =
		Array.from(document.getElementsByClassName('grid-image-checkbox'))
			.filter(e => e.checked)
			.map(e => e.value)
	console.log(files)
	let headers = {
		// mode: 'cors',
		cache: 'no-cache',
		"Content-Type": "application/json",
	}
	fetch("/download", {
		method: "POST",
		body: JSON.stringify({ files: files }),
		headers: headers
	}).then(
		(response) => {
			// console.log(response.)
			if (response.status == 200) {
				console.debug("attempting download")
				response.blob().then(
					(e) => {
						forceDownload(e)
					}
				)
			} else {
				throw new Error("An error occurred while generating the plugin")
			}
		}
	)
	// send files to download
}

function forceDownload(blob) {
	window.console.log(blob)
	const a = document.createElement('a')
	a.style.display = 'none'
	document.body.appendChild(a)
	a.href = URL.createObjectURL(blob)
	a.setAttribute('download', `images.zip`)
	a.click()
	window.URL.revokeObjectURL(a.href)
	document.body.removeChild(a)
}