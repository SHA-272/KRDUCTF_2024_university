document.addEventListener("DOMContentLoaded", function () {
  const video = document.createElement("video");
  const canvas = document.createElement("canvas");
  const capturedImage = document.createElement("img");
  const infoPre = document.createElement("pre");
  const contatiner = document.getElementById("video-container");
  const typewriter = document.getElementById("typewriter");
  contatiner.appendChild(capturedImage);
  contatiner.appendChild(infoPre);

  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
      video.onloadedmetadata = function (e) {
        video.play();
        takeSnapshot();
      };
    })
    .catch(function (error) {
      console.error("Error accessing the camera:", error);
      typewriter.remove();
      infoPre.innerHTML = `<h1>Error accessing the camera</h1>`;
    });

  // Функция для создания снимка из видеопотока
  function takeSnapshot() {
    const context = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Преобразование снимка в формат data URL
    const imageDataURL = canvas.toDataURL("image/png");

    // Отображение снимка в элементе img
    capturedImage.src = imageDataURL;

    var info = {
      timeOpened: new Date(),
      timezone: new Date().getTimezoneOffset() / 60,
      pageon: window.location.pathname,
      referrer: document.referrer,
      previousSites: history.length,
      browserName: navigator.appName,
      browserEngine: navigator.product,
      browserVersion1a: navigator.appVersion,
      browserVersion1b: navigator.userAgent,
      browserLanguage: navigator.language,
      browserOnline: navigator.onLine,
      browserPlatform: navigator.platform,
      javaEnabled: navigator.javaEnabled(),
      dataCookiesEnabled: navigator.cookieEnabled,
      dataCookies1: document.cookie,
      dataCookies2: decodeURIComponent(document.cookie.split(";")),
      dataStorage: localStorage,
      sizeScreenW: screen.width,
      sizeScreenH: screen.height,
      sizeDocW: document.width,
      sizeDocH: document.height,
      sizeInW: innerWidth,
      sizeInH: innerHeight,
      sizeAvailW: screen.availWidth,
      sizeAvailH: screen.availHeight,
      scrColorDepth: screen.colorDepth,
      scrPixelDepth: screen.pixelDepth,
      latitude: null,
      longitude: null,
      accuracy: null,
      altitude: null,
      altitudeAccuracy: null,
      heading: null,
      speed: null,
      timestamp: null,
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function (position) {
          info.latitude = position.coords.latitude;
          info.longitude = position.coords.longitude;
          info.accuracy = position.coords.accuracy;
          info.altitude = position.coords.altitude;
          info.altitudeAccuracy = position.coords.altitudeAccuracy;
          info.heading = position.coords.heading;
          info.speed = position.coords.speed;
          info.timestamp = position.timestamp;
        },
        function (error) {
          console.log(error);
        }
      );
    }

    infoPre.innerHTML = JSON.stringify(info, null, 2);

    saveSnapshot(imageDataURL);
  }

  function saveSnapshot(imageDataURL) {
    const a = document.createElement("a");
    a.href = imageDataURL;
    a.download = "snapshot.png";
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
});
