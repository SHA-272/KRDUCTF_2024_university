function setupTypewriter(t) {
  var HTML = t.innerHTML;
  t.innerHTML = "";

  var cursorPosition = 0,
    tag = "",
    writingTag = false,
    tagOpen = false,
    typeSpeed = 10,
    tempTypeSpeed = 0;

  var type = function () {
    if (writingTag === true) {
      tag += HTML[cursorPosition];
    }

    if (HTML[cursorPosition] === "<") {
      tempTypeSpeed = 0;
      tag = "";
      writingTag = true;
    } else if (HTML[cursorPosition] === ">") {
      tempTypeSpeed = Math.random() * typeSpeed + 10;
      writingTag = false;
      if (tagOpen) {
        var newSpan = document.createElement("span");
        t.appendChild(newSpan);
        newSpan.innerHTML = tag;
        tag = newSpan.firstChild;
      }
    } else {
      if (!writingTag) {
        if (HTML[cursorPosition] === " ") {
          tempTypeSpeed = 0;
        } else {
          tempTypeSpeed = Math.random() * typeSpeed + 10;
        }
        t.innerHTML += HTML[cursorPosition];
      } else {
        tag += HTML[cursorPosition];
      }
    }

    cursorPosition += 1;
    if (cursorPosition < HTML.length) {
      setTimeout(type, tempTypeSpeed);
    }
  };

  return {
    type: type,
  };
}

var typer = document.getElementById("typewriter");
var typewriter = setupTypewriter(typer);
typewriter.type();
