document.addEventListener("DOMContentLoaded", function () {
  var audioPlayer = document.createElement("audio");
  audioPlayer.src = "../static/music/voice.ogg";
  audioPlayer.controls = true;

  var playButton = document.getElementById("voice-btn");

  playButton.addEventListener("click", function () {
    if (audioPlayer.paused) {
      audioPlayer.play();
      playButton.textContent = "Disconnect";
    } else {
      audioPlayer.pause();
      playButton.textContent = "Connect";
    }
  });

  audioPlayer.addEventListener("ended", function () {
    playButton.textContent = "Connect";
  });
});
