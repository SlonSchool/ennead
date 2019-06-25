window.addEventListener("load", function() {
  let forms = document.getElementsByTagName('form');
  for (let form of forms) {
    let textareas = form.getElementsByTagName('textarea');
    for (let textarea of textareas) {
      textarea.addEventListener('keydown', function(event) {
        if (event.ctrlKey && event.keyCode == 13) { // Ctrl-Enter pressed
          form.submit();
        }
      });
    }
  }
});
