window.addEventListener('load', function() {
  var editors = document.getElementsByClassName('markdown-editor');
  for (let editor of editors) {
    var sourceLink = editor.getElementsByClassName('markdown-editor-source-link')[0];
    var previewLink = editor.getElementsByClassName('markdown-editor-preview-link')[0];
    var editorTextarea = editor.getElementsByClassName('markdown-editor-source')[0];
    var preview = editor.getElementsByClassName('markdown-editor-preview')[0];
    var fileUploader = editor.getElementsByClassName('file-uploader')[0];
    if (fileUploader === undefined) {
      continue;
    }
    var fileUploaderInput = fileUploader.getElementsByClassName('file-uploader-input')[0];
    var fileUploaderLink = fileUploader.getElementsByClassName('file-uploader-link')[0];
    if (
      sourceLink === undefined ||
      previewLink === undefined ||
      editorTextarea === undefined ||
      preview === undefined ||
      fileUploaderInput === undefined ||
      fileUploaderLink === undefined
    ) {
      continue;
    }

    sourceLink.onclick = function() {
      if (editorTextarea.classList.contains('d-none')) {
        editorTextarea.classList.remove('d-none');
        preview.classList.add('d-none');
        sourceLink.classList.add('active');
        previewLink.classList.remove('active');
        fileUploader.classList.remove('d-none');
      }
    }

    previewLink.onclick = function() {
      if (preview.classList.contains('d-none')) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
          if (xhr.readyState == 4 && xhr.status == 200) {
            preview.innerHTML = xhr.responseText;
            preview.querySelectorAll('pre code').forEach(function(block) {
              hljs.highlightBlock(block);
            });
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, preview]);
            preview.classList.remove('d-none');
            editorTextarea.classList.add('d-none');
            previewLink.classList.add('active');
            sourceLink.classList.remove('active');
            fileUploader.classList.add('d-none');
          }
        }
        xhr.open('POST', '/md', true);
        xhr.send(editorTextarea.value);
      }
    }

    fileUploaderLink.onclick = function() {
      fileUploaderInput.click();
    }

    fileUploaderInput.onchange = function() {
      var file = fileUploaderInput.files[0];
      if (file === undefined) {
        return;
      }

      var formData = new FormData();
      formData.append('file', file);

      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var fileLink = '[' + file.name + '](' + xhr.responseText + ')';
          if (file.type.startsWith('image/')) {
            fileLink = '!' + fileLink;
          }
          if (editorTextarea.value.slice(-1) != '\n') {
            editorTextarea.value += '\n';
          }
          editorTextarea.value += fileLink;
        }
      };
      xhr.open('POST', '/upload', true);
      xhr.send(formData);
    }
  }
});
