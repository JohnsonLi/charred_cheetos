const body = document.querySelector('body');
const puzzle = document.getElementById('puzzle');
const letters = document.querySelectorAll('.letter');
const selectedLetters = document.getElementById('selected');

let anchor = null;
let selected = [];
let correct = [];
let words = ['cat','bobcat','rhinoceros','communism','dog'];

let direction;
let startX;
let startY;

let directionList = ["right", "uprightdiag", "up", "upleftdiag", "left", "downleftdiag", "down", "downrightdiag"];
let directionChosen = false;
let currentDirection;
let lockedDirection = null;

letters.forEach(item => {

    item.addEventListener('mousedown', e => {
        if (anchor == null) { // first letter selected
            if (selected.indexOf(item) == -1) {
                selectedLetters.innerHTML = selectedLetters.innerHTML + item.innerHTML;
                selected.push(item);
            }
            item.style.color = 'blue';
            anchor = item;
        }
        startX = e.clientX;
        startY = e.clientY;
    });

    item.addEventListener('mouseover', (e) => {

        if (anchor != null) {
            if (!directionChosen) {
                currentDirection = direction;
                directionChosen = true;
            }
            drawPath(e, item);
        }
    });

});

body.addEventListener('mouseup', () => {
    check();
    clearselected();
    anchor = null;
    lockedDirection = null;
});

body.addEventListener('mousemove', e => {
    // console.log(e)
    let clientY = e.clientY;
    currentX = e.clientX - startX;
    currentY = e.clientY - startY;
    hyp = Math.sqrt(currentX * currentX + currentY * currentY);
    angle = Math.asin(currentX / hyp) * (180 / Math.PI); // angle from starting position to current
    direction = getDirection(normalizeAngle(angle, currentX, currentY, clientY));
    // console.log(getDirection(normalizeAngle(angle, currentX, currentY, clientY)));
});

let clearselected = () => {
    selected.forEach(item => {
        if (correct.indexOf(item) == -1) {
            item.style.color = 'black';
        } else { // word already found
            item.style.color = 'teal';
        }
    });
    directionChosen = false;
    selectedLetters.innerHTML = '';
    selected = [];
    startX = 0;
    startY = 0;
};

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

let change_color = (e, direc) => {
    // prevent selection overlap
    if (lockedDirection == null) {
        lockedDirection = direc
    }
    if (selected.indexOf(e.target) == -1) {
        // color the element to show selection
        e.target.style.color = 'red';
        selectedLetters.innerHTML = selectedLetters.innerHTML + e.target.innerHTML;
        selected.push(e.target);
        anchor = e.target
    }
};

let check = () => {
    // console.log(selected);
    // console.log(words.indexOf(selectedLetters.innerHTML) != -1);
    if (words.indexOf(selectedLetters.innerHTML) != -1) {
        selected.forEach(item => {
            item.style.color = 'teal';
            correct.push(item);
        });
        words = words.filter(word => {
            word != selectedLetters.innerHTML;
        });
    }
};

let drawPath = (e) => {
    if (lockedDirection == null) {
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

        if (currentDirection == 'upleftdiag' && anchorRow - 1 == currRow && anchorCol -1 == currCol) {
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
    } else {
        if (currentDirection == lockedDirection) {
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

            if (currentDirection == 'upleftdiag' && anchorRow - 1 == currRow && anchorCol -1 == currCol) {
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
    }
};
