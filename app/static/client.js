var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "img-fluid img-thumbnail";
    if(el("results")) el("results").innerHTML = '';
    if(el("results_utilities")) el("results_utilities").innerHTML = '';
  };
  reader.readAsDataURL(input.files[0]);
}

function analyze() {
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      result_text = "";
      if(`${response["result"]}`=="burned") {
        result_text = "The uploaded image contains a burned house";
      } else {
        result_text = "No burned houses were found in the uploaded image"
      }
      el("results").innerHTML = '<div class="result-label alert alert-info" role="alert"><div id="result-label" class="para-style-1">'+result_text+'</div></div>'
    }
    el("analyze-button").innerHTML = "Analyze";
  };

  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}


function analyze_utilities() {
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr_utility = new XMLHttpRequest();
  var loc = window.location;
  xhr_utility.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze_utility`,
    true);
    xhr_utility.onerror = function() {
    alert(xhr_utility.responseText);
  };
  xhr_utility.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      result_text = "";
      if(`${response["result"]}`=="pole") {
        result_text = "The uploaded image contains a utility pole";
      } else {
        result_text = "No utility poles were found in the uploaded image"
      }
      el("results_utility").innerHTML = '<div class="result-label alert alert-info" role="alert"><div id="result-label" class="para-style-1">'+result_text+'</div></div>'
    }
    el("analyze-button").innerHTML = "Analyze";
  };
  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr_utility.send(fileData);
}
