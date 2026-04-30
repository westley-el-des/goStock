// static/js/main.js
// Scripts utilitários do GoStock

// Auto-dismiss nos alertas flash após 5 segundos
document.addEventListener("DOMContentLoaded", function () {
  const alertas = document.querySelectorAll(".gs-alert");
  alertas.forEach(function (alerta) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
      bsAlert.close();
    }, 5000);
  });
});
