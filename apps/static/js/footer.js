$(function () {
  var changecount = 0;
  $(".f-logo img:first-child").show(); // 一つ目の画像を表示
  $(".f-logo img:last-child").hide();

  $(".f-ul li").hover(
    function () {
      if (changecount == 0) {
        $(".g-footer").css("background-color", "#F7DC69");
        $(".f-ul li").css("color", "#6984f7");
        $(".page-top").css("color", "#6984f7");
        $(".page-top").css("border-top", "3px solid #6984f7");
        $(".page-top").css("border-left", "3px solid #6984f7");
        $(".f-logo img:first-child").hide(); // 一つ目の画像を非表示
        $(".f-logo img:last-child").show(); // 二つ目の画像を表示
        changecount = 1;
      } else if (changecount == 1) {
        $(".g-footer").css("background-color", "#E684C3");
        $(".f-ul li").css("color", "#84e6a7");
        $(".page-top").css("color", "#84e6a7");
        $(".page-top").css("border-top", "3px solid #84e6a7");
        $(".page-top").css("border-left", "3px solid #84e6a7");
        $(".f-logo img:first-child").hide(); // 一つ目の画像を非表示
        $(".f-logo img:last-child").show(); // 二つ目の画像を表示
        changecount = 2;
      } else if (changecount == 2) {
        $(".g-footer").css("background-color", "#7CE6D7");
        $(".f-ul li").css("color", "#e67c8b");
        $(".page-top").css("color", "#e67c8b");
        $(".page-top").css("border-top", "3px solid #e67c8b");
        $(".page-top").css("border-left", "3px solid #e67c8b");
        $(".f-logo img:first-child").hide(); // 一つ目の画像を非表示
        $(".f-logo img:last-child").show(); // 二つ目の画像を表示
        changecount = 0;
      }
    },
    function () {
      $(".g-footer").css("background-color", "");
      $(".f-ul li").css("color", "");
      $(".page-top").css("color", "");
      $(".page-top").css("border-top", "");
      $(".page-top").css("border-left", "");
      $(".f-logo img:first-child").show(); // 一つ目の画像を表示
      $(".f-logo img:last-child").hide();
      // マウスが要素から離れたときの追加のコード
    }
  );
  function PageTopAnime() {
    var scroll = $(window).scrollTop();
    if (scroll >= 100) {
      //上から100pxスクロールしたら
      $("#page-top").removeClass("DownMove"); //#page-topについているDownMoveというクラス名を除く
      $("#page-top").addClass("UpMove"); //#page-topについているUpMoveというクラス名を付与
    } else {
      if ($("#page-top").hasClass("UpMove")) {
        //すでに#page-topにUpMoveというクラス名がついていたら
        $("#page-top").removeClass("UpMove"); //UpMoveというクラス名を除き
        $("#page-top").addClass("DownMove"); //DownMoveというクラス名を#page-topに付与
      }
    }
  }

  // 画面をスクロールをしたら動かしたい場合の記述
  $(window).scroll(function () {
    PageTopAnime(); /* スクロールした際の動きの関数を呼ぶ*/
  });

  // ページが読み込まれたらすぐに動かしたい場合の記述
  $(window).on("load", function () {
    PageTopAnime(); /* スクロールした際の動きの関数を呼ぶ*/
  });

  // #page-topをクリックした際の設定
  $("#page-top a").click(function () {
    var scroll = $(window).scrollTop(); //スクロール値を取得
    $("#page-top span").hide(); // スクロール中は非表示
    if (scroll > 0) {
      $("#page-top").addClass("floatAnime"); //クリックしたらfloatAnimeというクラス名が付与
      $("body,html").animate(
        {
          scrollTop: 0,
        },
        2000,
        function () {
          //スクロールの速さ。数字が大きくなるほど遅くなる
          $("#page-top").removeClass("floatAnime"); //上までスクロールしたらfloatAnimeというクラス名を除く
          $("#page-top span").show(); // ページトップに戻ったら表示
        }
      );
    }
    return false; //リンク自体の無効化
  });

  $(".grandnav .menu>li").find(".dropdown-menu").hide();

  $(".grandnav .menu>li").hover(
    function () {
      $(this).children(".dropdown-menu").stop().slideDown(500);
    },
    function () {
      $(this).children(".dropdown-menu").stop().slideUp(500);
    }
  );
});
