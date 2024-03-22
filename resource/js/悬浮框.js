const box = document.querySelector('.Box_xuanfu');
let isDragging = false;
let offsetX, offsetY;
const pageWidth = window.innerWidth;
const pageHeight = window.innerHeight;

// 鼠标事件监听器
function handleStart(e) {
  if (e.type === 'mousedown') {
    offsetX = e.clientX - box.offsetLeft;
    offsetY = e.clientY - box.offsetTop;
  } else if (e.type === 'touchstart') {
    const touch = e.touches[0];
    offsetX = touch.clientX - box.offsetLeft;
    offsetY = touch.clientY - box.offsetTop;
  }
  isDragging = true;
  document.addEventListener('mousemove', moveBox);
  document.addEventListener('mouseup', endDrag);
  document.addEventListener('touchmove', moveBox);
  document.addEventListener('touchend', endDrag);
}

function moveBox(e) {
  if (!isDragging) return;

  let newX, newY;
  if ('clientX' in e) { // 鼠标事件
    newX = e.clientX - offsetX + window.pageXOffset;
    newY = e.clientY - offsetY + window.pageYOffset;
  } else { // 触摸事件
    const touch = e.touches[0];
    newX = touch.clientX - offsetX + window.pageXOffset;
    newY = touch.clientY - offsetY + window.pageYOffset;
  }

  // 判断是否超出页面边界
  if (newX < 0) {
    box.style.left = 0;
  } else if (newX + box.offsetWidth > pageWidth) {
    box.style.left = pageWidth - box.offsetWidth + 'px';
  } else {
    box.style.left = newX + 'px';
  }

  if (newY < 0) {
    box.style.top = 0;
  } else if (newY + box.offsetHeight > pageHeight) {
    box.style.top = pageHeight - box.offsetHeight + 'px';
  } else {
    box.style.top = newY + 'px';
  }
}

function endDrag() {
  isDragging = false;
  document.removeEventListener('mousemove', moveBox);
  document.removeEventListener('mouseup', endDrag);
  document.removeEventListener('touchmove', moveBox);
  document.removeEventListener('touchend', endDrag);
}

// 添加事件监听器
box.addEventListener('mousedown', handleStart);
box.addEventListener('touchstart', handleStart, { passive: true }); // 对于touchstart需要设置passive选项以避免阻止默认滚动行为
