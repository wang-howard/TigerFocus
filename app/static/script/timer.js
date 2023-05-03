var setTime = 25;
var screen = document.getElementById("screen");
var timer = document.getElementById("minutes");
var videoframe = document.getElementById("videoframe");
var pd_btn = document.getElementsByName("pd");
var sb_btn = document.getElementsByName("sb");
var lb_btn = document.getElementsByName("lb");

videoframe.setAttribute("src", "https://www.youtube.com/embed/Kz1QJ4-lerk?autoplay=1&mute=1");
var pomodoro = {
  started: false,
  minutes: 0,
  seconds: 0,

  interval: null,
  minutesDom: null,
  secondsDom: null,
  init: function () {
    var self = this;
    this.minutesDom = document.querySelector("#minutes");
    this.secondsDom = document.querySelector("#seconds");
    this.interval = setInterval(function () {
      self.intervalCallback.apply(self);
    }, 1000);
    document.querySelector("#work").onclick = function () {
      self.startWork.apply(self);
    };
    document.querySelector("#stop").onclick = function () {
      self.stopTimer.apply(self);
    };
  },
  resetVariables: function (mins, secs, started) {
    this.minutes = mins;
    this.seconds = secs;
    this.started = started;
  },
  startWork: function () {
    this.resetVariables(setTime, 0, true);
  },
  stopTimer: function () {
    this.resetVariables(setTime, 0, false);
    this.updateDom();
  },
  toDoubleDigit: function (num) {
    if (num < 10) {
      return "0" + parseInt(num, 10);
    }
    return num;
  },
  updateDom: function () {
    this.minutesDom.innerHTML = this.toDoubleDigit(this.minutes);
    this.secondsDom.innerHTML = this.toDoubleDigit(this.seconds);
  },
  intervalCallback: function () {
    if (!this.started) return false;
    if (this.seconds == 0) {
      if (this.minutes == 0) {
        this.timerComplete();
        return;
      }
      this.seconds = 59;
      this.minutes--;
    } else {
      this.seconds--;
    }
    this.updateDom();
  },
  timerComplete: function () {
    this.started = false;
  },
};

window.onload = function () {
  pomodoro.init();
};

function pd_button_clicked() {
  timer.textContent = 25;
  setTime = 25;
  screen.style.background = "#a6b5de";
  videoframe.setAttribute("src", "https://www.youtube.com/embed/Kz1QJ4-lerk?autoplay=1&mute=1");
  document.querySelector("#stop").click();
}

function sb_button_clicked() {
  timer.textContent = 5;
  setTime = 5;
  screen.style.background = "#ABC787";
  videoframe.setAttribute("src", "https://www.youtube.com/embed/g1WfKpFQdOg?autoplay=1&mute=1");
  document.querySelector("#stop").click();
}

function lb_button_clicked() {
  timer.textContent = 10;
  setTime = 10;
  screen.style.background = "#D9C1B9";
  videoframe.setAttribute("src", "https://www.youtube.com/embed/FqKjFMr28rA?autoplay=1&mute=1");
  document.querySelector("#stop").click();
}
