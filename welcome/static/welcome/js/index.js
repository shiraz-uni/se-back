window.onload = function () {
  const cf = document.getElementById("clock-face"),
  cf$ = cf.getContext("2d"),
  ch = document.getElementById("clock-hands"),
  ch$ = ch.getContext("2d"),
  // firstColor = '#f44242',
  // secondColor = '#223235',
  // background = '#0f0f0f',
  // handsColor = '#ffffff', // red blue black theme

  // firstColor = '#ff00a5',
  // secondColor = '#2b103a',
  // background = '#0f0f0f',
  // handsColor = '#0087ff', //cold purple theme

  firstColor = "#17b9dc",
  secondColor = "#223235",
  background = "#0f0f0f",
  handsColor = "#ffffff", //dark theme
  sixtieth = 2 * Math.PI / 60,
  twelfth = sixtieth * 5;

  let w = cf.width = ch.width = window.innerWidth,
  h = cf.height = ch.height = window.innerHeight,
  shortestSide = w <= h ? w : h,
  i,
  r,
  v,
  currentAngle,
  handsWidth,
  time,
  secondsAngle,
  minutesAngle,
  hoursAngle,
  timeElapsed,
  last,
  clockRadius = shortestSide / 2 - shortestSide / 20;

  function drawface() {
    cf$.fillStyle = background;
    cf$.fillRect(0, 0, cf$.canvas.width, cf$.canvas.height);

    for (r = 1; r <= 6; r++) {
      cf$.fillStyle = firstColor;
      v = Math.pow(2, r - 1);

      for (i = 0; i < 60; i++) {
        currentAngle = i * sixtieth - Math.PI / 2;

        if (i % v === 0) {
          cf$.fillStyle = cf$.fillStyle === firstColor ?
          secondColor :
          firstColor;
        }

        cf$.beginPath();
        cf$.arc(
        cf$.canvas.width / 2 +
        Math.cos(currentAngle) * (clockRadius - r * clockRadius / 15),
        cf$.canvas.height / 2 +
        Math.sin(currentAngle) * (clockRadius - r * clockRadius / 15),
        clockRadius / 40,
        0,
        Math.PI * 2);

        cf$.fill();
      }
    }

    for (r = 1; r <= 4; r++) {
      cf$.fillStyle = firstColor;
      v = Math.pow(2, r - 1);

      for (i = 0; i < 12; i++) {
        currentAngle = i * twelfth - Math.PI / 2;

        if (i % v === 0) {
          cf$.fillStyle = cf$.fillStyle === firstColor ?
          secondColor :
          firstColor;
        }

        cf$.beginPath();
        cf$.arc(
        cf$.canvas.width / 2 +
        Math.cos(currentAngle) * (clockRadius / 1.8 - r * clockRadius / 11),
        cf$.canvas.height / 2 +
        Math.sin(currentAngle) * (clockRadius / 1.8 - r * clockRadius / 11),
        clockRadius / 27,
        0,
        Math.PI * 2);

        cf$.fill();
      }
    }
  }

  function initHandsAngles() {
    time = new Date();

    last = time.getTime();

    secondsAngle =
    sixtieth * time.getSeconds() + sixtieth / 1000 * time.getMilliseconds();
    minutesAngle =
    sixtieth * time.getMinutes() + sixtieth / 60 * time.getSeconds();
    hoursAngle =
    twelfth * (
    time.getHours() > 12 ? time.getHours() - 12 : time.getHours()) +
    twelfth / 60 * time.getMinutes();
  }

  function updateHandsAngles() {
    timeElapsed = +new Date() - last;

    last = +new Date();

    secondsAngle += sixtieth / 1000 * timeElapsed;
    minutesAngle += sixtieth / 60 * (timeElapsed / 1000);
    hoursAngle += twelfth / 60 * (timeElapsed / 1000 / 60);
  }

  function drawHands() {
    handsWidth = clockRadius / 130;

    ch$.clearRect(0, 0, ch$.canvas.width, ch$.canvas.height);
    ch$.fillStyle = handsColor;
    ch$.strokeStyle = handsColor;
    ch$.lineWidth = handsWidth;

    ch$.save();
    ch$.beginPath();
    ch$.translate(ch$.canvas.width / 2, ch$.canvas.height / 2);
    ch$.rotate(secondsAngle);
    ch$.fillRect(
    -handsWidth / 2,
    -handsWidth / 2,
    handsWidth,
    -clockRadius + clockRadius / 15);

    ch$.fill();
    ch$.restore();

    ch$.save();
    ch$.beginPath();
    ch$.translate(ch$.canvas.width / 2, ch$.canvas.height / 2);
    ch$.rotate(minutesAngle);
    ch$.fillRect(
    -handsWidth / 2,
    -handsWidth / 2,
    handsWidth,
    -clockRadius + clockRadius / 5);

    ch$.fill();
    ch$.restore();

    ch$.save();
    ch$.beginPath();
    ch$.translate(ch$.canvas.width / 2, ch$.canvas.height / 2);
    ch$.rotate(hoursAngle);
    ch$.fillRect(
    -handsWidth / 2,
    -handsWidth / 2,
    handsWidth,
    -clockRadius + clockRadius / 1.5);

    ch$.fill();
    ch$.restore();

    ch$.beginPath();
    ch$.arc(
    ch$.canvas.width / 2,
    ch$.canvas.height / 2,
    clockRadius / 1.87,
    0,
    Math.PI * 2);

    ch$.stroke();

    ch$.beginPath();
    ch$.arc(
    ch$.canvas.width / 2,
    ch$.canvas.height / 2,
    clockRadius,
    0,
    Math.PI * 2);

    ch$.stroke();

    ch$.beginPath();
    ch$.arc(
    ch$.canvas.width / 2,
    ch$.canvas.height / 2,
    clockRadius / 30,
    0,
    Math.PI * 2);

    ch$.fill();

    ch$.fillStyle = background;
    ch$.beginPath();
    ch$.arc(
    ch$.canvas.width / 2,
    ch$.canvas.height / 2,
    clockRadius / 33,
    0,
    Math.PI * 2);

    ch$.fill();
  }

  drawface();
  initHandsAngles();

  (function loop() {
    updateHandsAngles();
    drawHands();
    requestAnimationFrame(loop);
  })();

  window.addEventListener("resize", function () {
    w = cf.width = ch.width = window.innerWidth;
    h = cf.height = ch.height = window.innerHeight;
    shortestSide = w <= h ? w : h;
    clockRadius = shortestSide / 2 - shortestSide / 20;
    drawface();
  });
};