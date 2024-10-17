/* Manages dashboard loading and initializes interactive elements

Copyright (c) 2024-present Hannah Esther Augustijn, MSc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('reload').addEventListener('change', function() {
      if (this.checked) {
        document.getElementById('reload-content').classList.remove('d-none');
        document.getElementById('startAnalysis-content').classList.add('d-none');
        document.getElementById('load-content').classList.add('d-none');
      }
    });

    document.getElementById('startAnalysis').addEventListener('change', function() {
      if (this.checked) {
        document.getElementById('reload-content').classList.add('d-none');
        document.getElementById('startAnalysis-content').classList.remove('d-none');
        document.getElementById('load-content').classList.add('d-none');
      }
    });

    document.getElementById('load').addEventListener('change', function() {
      if (this.checked) {
        document.getElementById('reload-content').classList.add('d-none');
        document.getElementById('startAnalysis-content').classList.add('d-none');
        document.getElementById('load-content').classList.remove('d-none');
      }
    });

});

function checkFileExtensionPeaks() {
  var fileInput = document.getElementById('peaktable_file');
  var filePath = fileInput.value;
  var allowedExtensions = /(\.csv)$/i;
  if (!allowedExtensions.exec(filePath)) {
    fileInput.value = '';

    var alertContainer = document.getElementById('alert-container-peaks');
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
      Invalid file type. Only CSV files are allowed. The peaktable should be a MZmine3 formatted table.
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertContainer.appendChild(alertDiv);

    return false;
  }
  return true;
}

function checkFileExtensionMsms() {
  var fileInput = document.getElementById('msms_file');
  var filePath = fileInput.value;
  var allowedExtensions = /(\.mgf)$/i;
  if (!allowedExtensions.exec(filePath)) {
    fileInput.value = '';

    var alertContainer = document.getElementById('alert-container-msms');
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
      Invalid file type. Only mgf files are allowed. The peaktable should be a MZmine3 formatted table.
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertContainer.appendChild(alertDiv);

    return false;
  }
  return true;
}