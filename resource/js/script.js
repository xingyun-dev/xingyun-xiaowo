let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.header .nav');

menu.onclick = () =>{
   menu.classList.toggle('fa-times');
   navbar.classList.toggle('active');
};

window.onscroll = () =>{
   menu.classList.remove('fa-times');
   navbar.classList.remove('active');

   if(window.scrollY > 0){
      document.querySelector('.header').classList.add('active');
   }else{
      document.querySelector('.header').classList.remove('active');
   }
}


//自动弹出文字

 // setRandomColor()函数随机生成颜色
function getRandomColor() {
   var letters = "0123456789ABCDEF";
   var color = "#";
   for (var i = 0; i < 6; i++) {
       color += letters[Math.floor(Math.random() * 16)];
   }
   return color;
}

// 设置随机出现的文字数组
var arr = ["富强", "民主", "文明", "和谐", "诚信", "友善", "爱国", "敬业", "自由", "平等", "公正", "法治"]

document.onclick = function (x) {
   // 创建元素节点对象
   var wenzi = document.createElement("wenzi")

   // 获取当前鼠标的坐标
   wenzi.style.left = x.clientX + "px"
   wenzi.style.top = x.clientY + "px"

   // 让wenzi的值为arr数组内随机的一个值
   wenzi.innerHTML = arr[Math.floor(Math.random() * arr.length)]

   // 设置wenzi的动画效果和随机颜色
   setTimeout(function () {
      wenzi.style.opacity = "1"
      wenzi.style.transform = "translateY(-100px)"
      wenzi.style.color = getRandomColor();
   }, 100);

   setTimeout(function () {
      wenzi.style.opacity = "0"
      wenzi.style.transform = "translateY(-230px)"
   }, 1500)

   // 清掉opacort为0的wenzi
   var chi = document.getElementsByClassName("wenzi")
   for (var i = 0; i < chi.length; i++) {
      if (chi[i].style.opacity === "0") {
         document.body.removeChild(chi[i])
      }
   }

   // 将wenzi添加到body里
   document.body.appendChild(wenzi)
}