let _direction = true;
let _move = () => {
    let lists = document.querySelectorAll('.item');
    if(_direction){
        document.querySelector('#slide').appendChild(lists[0]);
    }else{
        document.querySelector('#slide').prepend(lists[lists.length - 1]);
    }
}

let timer = setInterval(_move,2500);
document.querySelector('.LBT').addEventListener('mouseover', () => {
    clearInterval(timer);
})
document.querySelector('.LBT').addEventListener('mouseout', () => {
    timer = setInterval(_move,2500);
})

document.querySelectorAll('.s_button')[1].onclick = () => {
    _direction = true;
    _move();
    console.log(666);
}

document.querySelectorAll('.s_button')[0].onclick = () => {
    _direction = false;
    _move();
}