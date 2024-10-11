$(function () {
  // ドキュメントが完全に読み込まれた後にコードが実行されるようにする
  var animationSpeed = 200;
  // 最初の左側の 'img' 要素を取得
  var firstImage = $(".left img:first");

  // 最初の画像の 'src' を取得
  var initialSrc = firstImage.attr("src");

  // '.right img' の初期画像を設定
  $(".right img").attr("src", initialSrc);
  // 左側の 'img' 要素がホバーされた時
  var isHovered = false;

  $(".left li").hover(
    function () {
      // ボックスシャドウを追加
      $(this).css("box-shadow", "0 0 4px 3px #ABE1FA");

      // 前のホバー状態をクリア
      $(".left li").not(this).css("box-shadow", "");

      // ホバーされている状態を更新
      isHovered = true;
    },
    function () {
      // ホバー解除時の処理
      isHovered = false;
    }
  );
  $(".left img").hover(
    function () {
      // ホバーされている画像の 'src' を取得
      var newSrc = $(this).attr("src");

      // '.right img' 内の画像をフェードアウトして、ホバーされた画像にゆっくりと変更
      $(".right img").fadeOut(animationSpeed, function () {
        $(this).attr("src", newSrc).fadeIn(animationSpeed);
      });
    },
    function () {
      // ホバー解除時の処理
    }
  );
});

(function () {
  var zoomArea = document.querySelector(".zoom-area");
  var zoomImage = zoomArea.querySelector("img");
  var size = 172;
  var scale = 500 / size;
  Array.prototype.forEach.call(
    document.querySelectorAll(".m-lens-container"),
    function (container) {
      var lens = container.querySelector(".m-lens");
      var img = container.querySelector("img");
      container.addEventListener("mouseenter", function () {
        var image = container.querySelector("img");
        zoomArea.classList.add("active");
        zoomImage.setAttribute("src", image.src);
        zoomImage.style.width = image.offsetWidth * scale + "px";
      });
      container.addEventListener("mouseleave", function () {
        zoomArea.classList.remove("active");
      });
      var xmax, ymax;
      img.addEventListener("load", function () {
        xmax = img.offsetWidth - size;
        ymax = img.offsetHeight - size;
      });
      container.addEventListener("mousemove", function (e) {
        var rect = container.getBoundingClientRect();
        var mouseX = e.pageX;
        var mouseY = e.pageY;
        var positionX = rect.left + window.pageXOffset;
        var positionY = rect.top + window.pageYOffset;
        var offsetX = mouseX - positionX; /* コンテナの左上からの相対x座標 */
        var offsetY = mouseY - positionY; /* コンテナの左上からの相対y座標 */
        var left = offsetX - size / 2;
        var top = offsetY - size / 2;

        if (left > xmax) {
          left = xmax;
        }
        if (top > ymax) {
          top = ymax;
        }
        if (left < 0) {
          left = 0;
        }
        if (top < 0) {
          top = 0;
        }
        lens.style.top = top + "px";
        lens.style.left = left + "px";
        zoomImage.style.marginLeft = -(left * scale) + "px";
        zoomImage.style.marginTop = -(top * scale) + "px";
      });
    }
  );
})();
