$(document).ready(function () {
  $(".title").lettering();

  // ページが読み込まれたときにanimation()関数を呼び出す
  animation();
});

function animation() {
  var title1 = new TimelineMax();

  // タイトルコンテナを表示させる
  title1.to(".title-container", 0.2, { visibility: "visible", opacity: 1 });

  title1.staggerFromTo(
    ".title span",
    0.5,
    { ease: Back.easeOut.config(1.7), opacity: 0, bottom: -80 },
    { ease: Back.easeOut.config(1.7), opacity: 1, bottom: 0 },
    0.05
  );
}
