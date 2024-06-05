function enviarDatos() {
  var fileinput = document.getElementById('file-upload');
  var file = fileinput.files[0];
  var formData = new FormData();
  formData.append('file', file);

  var checkedTechniques = [];
  var checkboxes = document.querySelectorAll('.tecnica:checked');
  checkboxes.forEach(checkbox => {
    checkedTechniques.push(checkbox.value);
  });
  formData.append('tecnica', checkedTechniques.join(','));

  fetch('http://localhost:5000/csv', {
      method: 'POST',
      body: formData,
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      console.log(data);
    })
    .catch(function(error) {
      console.error('Error:', error);
    });
}

    // Obtener el botón por su ID
    var btnGenerarAnalisis = document.getElementById('btn-generar-analisis');

    // Agregar un evento de clic al botón
    btnGenerarAnalisis.addEventListener('click', function() {
        // Redireccionar a dashboard.html
        window.location.href = 'layout-static.html';
    });
