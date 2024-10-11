$(document).ready(function () {
  $(".image-container").slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000, // 3秒ごとにスライド切り替え
    pauseOnHover: true, // マウスオーバー時に一時停止
  });
});
