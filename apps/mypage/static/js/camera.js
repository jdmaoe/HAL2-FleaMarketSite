document.addEventListener("DOMContentLoaded", function () {
  var capmessage = document.getElementById('capmessage');
  var cap = document.getElementById('cap');
  var captureButton = document.getElementById('captureButton');
  var face_image = document.getElementById('face_image');
  capmessage.style.display = 'none';

  // captureButtonが押されたら、capに表示されている画像を取得し、face_imageに入れる
  captureButton.addEventListener('click', function () {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = cap.width;
    canvas.height = cap.height;
    context.drawImage(cap, 0, 0, cap.width, cap.height);
    canvas.toBlob(function (blob) {
      var imgFile = new File([blob], 'webcam.jpg', { type: 'image/jpeg' });
      var fileList = new DataTransfer();
      fileList.items.add(imgFile);
      face_image.files = fileList.files;
    }, 'image/jpeg');
    capmessage.style.display = 'block';
    // 3秒後にメッセージを非表示にする
    setTimeout(function () {
      capmessage.style.display = 'none';
    }, 3000);
  });
});