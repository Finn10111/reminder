document.addEventListener("DOMContentLoaded", function(event) { 
  document.getElementById('icsfile').addEventListener("change", function(e){
    var filename = this.value.replace(/^.*[\\\/]/, '');
    document.getElementById('filename').setAttribute('data-content', filename);
  });
});
