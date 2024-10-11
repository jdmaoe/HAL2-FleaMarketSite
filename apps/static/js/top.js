$(".contents").hover(
  function () {
    // ホバーした要素に対してのみ処理を行う
    $(this).find(".description").slideDown();
    $(this).find(".image").addClass("open");
  },
  function () {
    // ホバーした要素に対してのみ処理を行う
    $(this).find(".description").slideUp();
    $(this).find(".image").removeClass("open");
  }
);
