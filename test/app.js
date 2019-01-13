const body = document.querySelector('body');
const tbody = document.querySelector('tbody');
const puzzle = document.getElementById('puzzle');
const letters = document.querySelectorAll('.letter');
const selectedLetters = document.getElementById('selected');

let anchor = null;
let selected = [];
let correct = [];
let words = ['cat'];

let direction;
let startX;
let startY;

let directionChosen = false;
let currentDirection;

// add event listeners to each letter so they can act accordingly
letters.forEach(item => {
  // when clicked, it will set the first thing you clicked as an anchor.
  // that will be the starting point.
  item.addEventListener('mousedown', e => {
    if (anchor == null) {
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

  // when you let go, clear the anchor.
  // also, check if selection is a valid word
  item.addEventListener('mouseup', () => {
    anchor = null;
  });

  // when you go over a letter, it changed the color to show selection.
  // it selects direction by choosing the first direction you go after your mouse leaves the anchor
  item.addEventListener('mouseover', () => {
    // console.log(anchor);
    if (anchor != null) {
      if (!directionChosen) {
        currentDirection = direction;
        directionChosen = true;
      }
      drawPath(item);
    }
  });

  // keeps the anchor blue for debugging
  // item.addEventListener('mouseout', () => {
  //   if (item == anchor) {
  //     item.style.color = 'blue';
  //   }
  // console.log(anchor);
  // item.style.color = 'black';
  // });

  // for debug
  // item.addEventListener('click', () => {
  //   let viewportOffset = item.getBoundingClientRect();
  //   console.log(viewportOffset.x, viewportOffset.y);
  // });
});

// clears the selected after you let go
puzzle.addEventListener('mouseup', () => {
  check();
  clearselected();
});

// this continuously checks the direction so it can change when you start somewhere else
body.addEventListener('mousemove', e => {
  let clientY = e.clientY;
  currentX = e.clientX - startX;
  currentY = e.clientY - startY;
  hyp = Math.sqrt(currentX * currentX + currentY * currentY);
  angle = Math.asin(currentX / hyp) * (180 / Math.PI);
  // console.log(
  // direction = getDirection(
  //   normalizeAngle(angle, currentX, currentY, clientY)
  // )
  direction = getDirection(normalizeAngle(angle, currentX, currentY, clientY));
});

// sets everything back to black and clears everything
let clearselected = () => {
  selected.forEach(item => {
    if (correct.indexOf(item) == -1) {
      item.style.color = 'black';
    } else {
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
  // console.log(angle);
  if ((angle > 0 && angle < 30) || angle > 330 || angle == 0) {
    return 'right';
  }
  if ((angle > 60 && angle < 120) || angle == 90) {
    return 'up';
  }
  if ((angle > 150 && angle < 210) || angle == 180) {
    return 'left';
  }
  if ((angle > 240 && angle < 300) || angle == 270) {
    return 'down';
  }

  if (angle >= 30 && angle <= 60) {
    return 'uprightdiag';
  }
  if (angle >= 120 && angle <= 150) {
    return 'upleftdiag';
  }
  if (angle >= 210 && angle <= 270) {
    return 'downleftdiag';
  }
  if (angle >= 300 && angle <= 330) {
    return 'downrightdiag';
  }
};

let drawPath = item => {
  // console.log(currentDirection);
  // gets the element's coordinates in relation to it's container
  let viewportOffset = item.getBoundingClientRect();
  let aviewportOffset = anchor.getBoundingClientRect();

  // calculate slop to see if it's diagonal to start point
  slope =
    (viewportOffset.x - aviewportOffset.x) /
    (viewportOffset.y - aviewportOffset.y);

  // console.log(slope);
  // check to see if diagonal is like this -> /
  if (
    slope == -1 &&
    (currentDirection == 'uprightdiag' || direction == 'downleftdiag')
  ) {
    change_color(item);
  }

  // check to see if diagonal i slike this -> \
  if (
    slope == 1 &&
    (currentDirection == 'upleftdiag' || direction == 'downrightdiag')
  ) {
    change_color(item);
  }

  // checking for up down left right
  if (
    viewportOffset.y == aviewportOffset.y &&
    (currentDirection == 'right' || currentDirection == 'left')
  ) {
    change_color(item);
  }
  if (
    viewportOffset.x == aviewportOffset.x &&
    (currentDirection == 'up' || currentDirection == 'down')
  ) {
    change_color(item);
  }
  // console.log(
  // aviewportOffset.top,
  // aviewportOffset.bottom,

  // viewportOffset.top,
  // viewportOffset.bottom
  // );
};

let change_color = item => {
  // prevent selection overlap
  if (selected.indexOf(item) == -1) {
    // color the element to show selection
    item.style.color = 'red';
    selectedLetters.innerHTML = selectedLetters.innerHTML + item.innerHTML;
    selected.push(item);
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
