// 文件读取和处理的函数
function handleFileUpload() {
    var thumbnailInput = $('#FileUpload1')[0];
    if (thumbnailInput.files && thumbnailInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var base64ImageData = e.target.result;
            var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
            var encodedThumbnail = encodeURIComponent(base64Data);

            // 调用提交文章的函数，传入缩略图编码
            submitArticle(encodedThumbnail);
        };

        reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
    } else {
        // 处理没有选择文件的情况
        bootbox.alert({title: "错误提示", message: "请选择自定义缩略图."});
    }
}


// 更新用户设置
function update_usershezhi() {
    var thumbnailInput = $('#FileUpload1')[0];
    var avatar = null;
    if (thumbnailInput.files && thumbnailInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var base64ImageData = e.target.result;
            var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
            var avatar = encodeURIComponent(base64Data);

            // 调用提交文章的函数，传入缩略图编码
            user_update(avatar);
        };

        reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
    } else {
         // 如果没有上传新的图片，可以保持原有图片或传递一个空值给服务器
        user_update(avatar);
    }
}



//新建外链设置
function handleFileUpload1_editor() {
    var thumbnailInput1 = $('#FileUpload1_editor')[0];
    var thumbnailInput2 = $('#FileUpload2_editor')[0];
    var wang_img; // 用来存储第一个图片编码的变量
    var wang_user_avatar; // 用来存储第二个图片编码的变量
    var bothLoaded = false; // 标记两个文件是否都已加载完成

    // 检查两个文件输入是否都有文件被选中
    if (thumbnailInput1.files && thumbnailInput1.files[0] && thumbnailInput2.files && thumbnailInput2.files[0]) {
        // 读取第一个文件
        var reader1 = new FileReader();
        reader1.onload = function (e1) {
            var base64ImageData1 = e1.target.result;
            wang_img = encodeURIComponent(base64ImageData1.replace(/^data:image\/\w+;base64,/, ""));
            checkBothLoaded(); // 检查是否两个文件都已加载完成
        };
        reader1.readAsDataURL(thumbnailInput1.files[0]); // 开始读取第一个文件

        // 读取第二个文件
        var reader2 = new FileReader();
        reader2.onload = function (e2) {
            var base64ImageData2 = e2.target.result;
            wang_user_avatar = encodeURIComponent(base64ImageData2.replace(/^data:image\/\w+;base64,/, ""));
            checkBothLoaded(); // 检查是否两个文件都已加载完成
        };
        reader2.readAsDataURL(thumbnailInput2.files[0]); // 开始读取第二个文件
    } else {
        // 处理没有选择文件的情况
        bootbox.alert({title: "错误提示", message: "请选择自定义缩略图."});
        return;
    }

    // 检查是否两个文件都已加载完成的函数
    function checkBothLoaded() {
        if (wang_img && wang_user_avatar) {
            bothLoaded = true;
            submituser_editor(wang_img, wang_user_avatar); // 两个文件都已加载，调用提交函数
        }
    }
}


//更新外链设置
function handleFileUpload1_update() {
    var thumbnailInput1 = $('#FileUpload1_editor_update')[0];
    var thumbnailInput2 = $('#FileUpload2_editor_update')[0];
    var wang_img = null; // 用来存储第一个图片编码的变量，初始化为null
    var wang_user_avatar = null; // 用来存储第二个图片编码的变量，初始化为null

    // 检查第一个文件输入是否有文件被选中
    if (thumbnailInput1.files && thumbnailInput1.files[0]) {
        var reader1 = new FileReader();
        reader1.onload = function (e1) {
            var base64ImageData1 = e1.target.result;
            wang_img = encodeURIComponent(base64ImageData1.replace(/^data:image\/\w+;base64,/, ""));
            submituser_editor_update(wang_img, wang_user_avatar); // 读取完成后直接调用提交函数
        };
        reader1.readAsDataURL(thumbnailInput1.files[0]); // 开始读取第一个文件
    } else {
        // 如果没有选中文件，则直接调用提交函数，wang_img 为 null
        submituser_editor_update(wang_img, wang_user_avatar);
    }

    // 检查第二个文件输入是否有文件被选中
    if (thumbnailInput2.files && thumbnailInput2.files[0]) {
        var reader2 = new FileReader();
        reader2.onload = function (e2) {
            var base64ImageData2 = e2.target.result;
            wang_user_avatar = encodeURIComponent(base64ImageData2.replace(/^data:image\/\w+;base64,/, ""));
            // 由于第一个文件可能已经完成处理，这里再次调用提交函数可能不是最高效的方式
            // 但由于函数内部会检查两个变量是否都已设置，所以仍然可以工作
            submituser_editor_update(wang_img, wang_user_avatar);
        };
        reader2.readAsDataURL(thumbnailInput2.files[0]); // 开始读取第二个文件
    } else {
        // 如果没有选中文件，则不会再次调用提交函数，因为已经在第一个文件的onload事件中调用过了
    }
}





//提交工具设置
function submit_tools() {
    var thumbnailInput = $('#upload_ico')[0];
    if (thumbnailInput.files && thumbnailInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var base64ImageData = e.target.result;
            var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
            var encodedThumbnail = encodeURIComponent(base64Data);

            // 调用提交文章的函数，传入缩略图编码
            submittools_add(encodedThumbnail);
        };

        reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
    } else {
        // 处理没有选择文件的情况
        // bootbox.alert({title: "错误提示", message: "请选择工具设置图例."});
        alert('请选择为工具设置图标')
    }
}



//编辑工具设置
function editor_tools() {
    var thumbnailInput = $('#upload_ico')[0];
    if (thumbnailInput.files && thumbnailInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var base64ImageData = e.target.result;
            var base64Data = base64ImageData.replace(/^data:image\/\w+;base64,/, "");
            var encodedThumbnail = encodeURIComponent(base64Data);

            // 调用提交文章的函数，传入缩略图编码
            editortools_add(encodedThumbnail);
        };

        reader.readAsDataURL(thumbnailInput.files[0]); // 开始读取文件
    } else {
        // 处理没有选择文件的情况
        // bootbox.alert({title: "错误提示", message: "请选择工具设置图例."});
        alert('请选择为工具设置图标')
    }
}
