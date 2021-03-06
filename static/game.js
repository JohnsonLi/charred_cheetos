const body = document.querySelector('body');
const puzzle = document.getElementById('puzzle');
const letters = document.querySelectorAll('.letter');
const selectedLetters = document.getElementById('selected');
const timer = document.getElementById('timer-number');
const wordBank = document.querySelectorAll('#word');

let anchor = null;
let selected = [];
let correct = [];
// let words = ['cat', 'bobcat', 'rhinoceros', 'communism', 'dog'];

let direction;
let startX;
let startY;
let time = -1;

let directionList = ["right", "uprightdiag", "up", "upleftdiag", "left", "downleftdiag", "down", "downrightdiag"];
let directionChosen = false;
let currentDirection;
let lockedDirection = null;

// ============== event listeners for interacting with puzzle ==============
var choose = function(e) {
    // console.log("down")
    if (anchor == null) { // first letter selected
        if (selected.indexOf(this) == -1) {
            if(selectedLetters.innerHTML == 'Select a Word'){
                selectedLetters.innerHTML = ''
                selectedLetters.innerHTML = selectedLetters.innerHTML + this.innerHTML;
            } else {
                selectedLetters.innerHTML = selectedLetters.innerHTML + this.innerHTML;

            }
            selected.push(this);
        }
        this.style.color = '#ffb7c3';
        anchor = this;
    }
    startX = e.clientX;
    startY = e.clientY;
};

var drag_letter = function(e) {
    if (anchor != null) {
        if (!directionChosen) {
            currentDirection = direction;
            directionChosen = true;
        }
        drawPath(e, this);
    }
};

letters.forEach(item => {
    item.addEventListener('mousedown', choose);
    item.addEventListener('mouseover', drag_letter);
})

var drag = function(e) {
    // console.log(e)
    let clientY = e.clientY;
    currentX = e.clientX - startX;
    currentY = e.clientY - startY;
    hyp = Math.sqrt(currentX * currentX + currentY * currentY);
    angle = Math.asin(currentX / hyp) * (180 / Math.PI); // angle from starting position to current
    direction = getDirection(normalizeAngle(angle, currentX, currentY, clientY));
}

body.addEventListener('mousemove', drag);

var release = function() {
    anchor = null;
    lockedDirection = null;
    check();
}

body.addEventListener('mouseup', release);

// ============== selecting words in game ==============
let change_color = (e, direc) => {
    // prevent selection overlap
    if (lockedDirection == null) {
        lockedDirection = direc
    }
    if (selected.indexOf(e.target) == -1) {
        // color the element to show selection
        e.target.style.color = '#ffb7c3';
        selectedLetters.innerHTML = selectedLetters.innerHTML + e.target.innerHTML;
        selected.push(e.target);
        anchor = e.target
    }
};

let drawPath = (e) => {
    if (lockedDirection == null || lockedDirection == currentDirection) {
        currRow = e.target.parentNode.rowIndex
        currCol = e.target.cellIndex
        anchorRow = anchor.parentNode.rowIndex
        anchorCol = anchor.cellIndex

        if (currentDirection == 'right' && anchorRow == currRow && anchorCol + 1 == currCol) {
            change_color(e, directionList[0])
        }

        if (currentDirection == 'uprightdiag' && anchorRow - 1 == currRow && anchorCol + 1 == currCol) {
            change_color(e, directionList[1])
        }

        if (currentDirection == 'up' && anchorRow - 1 == currRow && anchorCol == currCol) {
            change_color(e, directionList[2])
        }

        if (currentDirection == 'upleftdiag' && anchorRow - 1 == currRow && anchorCol - 1 == currCol) {
            change_color(e, directionList[3])
        }

        if (currentDirection == 'left' && anchorRow == currRow && anchorCol - 1 == currCol) {
            change_color(e, directionList[4])
        }

        if (currentDirection == 'downleftdiag' && anchorRow + 1 == currRow && anchorCol - 1 == currCol) {
            change_color(e, directionList[5])
        }

        if (currentDirection == 'down' && anchorRow + 1 == currRow && anchorCol == currCol) {
            change_color(e, directionList[6])
        }

        if (currentDirection == 'downrightdiag' && anchorRow + 1 == currRow && anchorCol + 1 == currCol) {
            change_color(e, directionList[7])
        }
    }
};

// ============== check for correct selections ==============
var record_time = function() {
    document.getElementById("time").value = timer.innerHTML
    document.getElementById("timerForm").submit();
};

let check = () => {
    // console.log(selected);
    // console.log(words.indexOf(selectedLetters.innerHTML) != -1);
    index = words.indexOf(selectedLetters.innerHTML);
    let word = words[index]
    if (index != -1) {
        selected.forEach(item => {
            item.style.color = '#a9dbdc';
            correct.push(item);
        });
        // console.log(wordBank)
        wordBank.forEach(item => {
          // console.log(word)
          // console.log(item)
          if (word == item.innerHTML) {
            item.style["text-decoration"] = "line-through";
          }
        });

        words.splice(index, 1);
    }

    else {
        selected.forEach(item => {
            if(correct.indexOf(item) == -1){
                item.style.color = 'black';
            } else {
                item.style.color = '#a9dbdc';
            }
        });
    }
    // console.log(correct);
    // console.log(words);
    if(words.length == 0){
      //   if (submit_time) {
      //     document.getElementById("time").value = timer.innerHTML
      //     // console.log(document.getElementById("time").value)
      //     // console.log(timer.innerHTML)
      //     document.getElementById("timerForm").submit();
      //     // console.log("form submmitted");
      // }
      clearInterval(timerInterval);
      var msg = document.getElementById("finish_msg");
      msg.style.display = 'block';
      var buttons = document.getElementById("finish_game");
      buttons.style.display = 'block';
      // remove all event listeners
      letters.forEach(item => {
        // var clone0 = item.cloneNode(true);
        // item.parentNode.replaceChild(clone0, item);
        item.removeEventListener('mousedown', choose);
        item.removeEventListener('mouseover', drag_letter);
      });

      body.removeEventListener('mouseover', drag);
      body.removeEventListener('mouseup', release);
    }

    var time_button = document.getElementById("save_time");
    if (time_button != null) {
        time_button.addEventListener('click', record_time);
    }

    var try_button = document.getElementById("try_again");
    try_button.addEventListener('click', function() {
        var new_game = document.getElementById("gameForm");
        new_game.submit();
    });

    directionChosen = false;
    selectedLetters.innerHTML = "Select a Word";
    selected = [];
    startX = 0;
    startY = 0;
};

// ============== helper functions to determine direction ==============
let normalizeAngle = (angle, currentX, currentY, clientY) => {
    // The angle is weird because the top left of the browser is (0,0)

    // Special angles
    if (angle == 90) {
        return 0;
    }
    if (angle == -90) {
        return 180;
    }
    if (angle == 0 && clientY < startY) {
        return 90;
    }
    if (angle == 0 && clientY > startY) {
        return 270;
    }

    // Quadrants
    // Q1
    if (currentX > 0 && currentY < 0) {
        return -1 * angle + 90;
    }
    // Q2
    if (currentX < 0 && currentY < 0) {
        return -1 * angle + 90;
    }
    // Q3
    if (currentX < 0 && currentY > 0) {
        return angle + 270;
    }
    // Q4
    if (currentX > 0 && currentY > 0) {
        return angle + 270;
    }
};

// get direction based on the angle.
// each direction gets like 60 degrees.
let getDirection = angle => {
    var val = Math.floor((angle / 45) + 0.5);
    return directionList[(val % 8)];
};

let timerInterval = setInterval(() => {
    //console.log(timer.innerHTML)
    timer.innerHTML = (parseInt(timer.innerHTML) + 1).toString()
}, 1000);
