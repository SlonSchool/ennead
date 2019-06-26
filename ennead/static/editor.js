window.addEventListener('load', function() {
    var editors = document.getElementsByClassName('markdown-editor');
    for (let editor of editors) {
        var sourceLink = editor.getElementsByClassName('markdown-editor-source-link')[0];
        var previewLink = editor.getElementsByClassName('markdown-editor-preview-link')[0];
        var editorTextarea = editor.getElementsByClassName('markdown-editor-source')[0];
        var preview = editor.getElementsByClassName('markdown-editor-preview')[0];
        if (
            sourceLink === undefined ||
            previewLink === undefined ||
            editorTextarea === undefined ||
            preview === undefined
        ) {
            continue;
        }

        sourceLink.onclick = function(event) {
            event.preventDefault();
            if (editorTextarea.classList.contains('d-none')) {
                editorTextarea.classList.remove('d-none');
                preview.classList.add('d-none');
                sourceLink.classList.add('active');
                previewLink.classList.remove('active');
            }
        }

        previewLink.onclick = function(event) {
            event.preventDefault();
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
                    }
                }
                xhr.open('POST', '/md', true);
                xhr.send(editorTextarea.value);
            }
        }
    }
});
