window.onload = function(){
  let textarea = document.getElementById('post-textarea');
  textarea.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.keyCode == 13) { // Ctrl-Enter pressed
      let form = document.getElementById('post-form');
      form.submit();
    }
  });
};
