// カテゴリーを取得するためのJavaScriptファイル
$(document).ready(function () {
  // ページが読み込まれたら実行する処理
  var firstcategory_id = $("#firstcategory").val();
  if (firstcategory_id) {
    $.ajax({
      url: "/get_firstcategorys/", // 適切なエンドポイントに変更する必要があります
      type: "GET",
      success: function (response) {
        $("#firstcategory").html(response);
      },
      error: function (error) {
        console.log(error);
      },
    });
  }

  // firstcategoryが変更されたときの処理
  $("#firstcategory").change(function () {
    var firstcategory_id = $(this).val();
    if (firstcategory_id) {
      $.ajax({
        url: "/get_secondcategorys/" + firstcategory_id, // 適切なエンドポイントに変更する必要があります
        type: "GET",
        success: function (response) {
          $("#secondcategory").html(response);
        },
        error: function (error) {
          console.log(error);
        },
      });
    } else {
      $("#secondcategory").empty();
      $("#thirdcategory").empty();
    }
  });

  // secondcategoryが変更されたときの処理
  $("#secondcategory").change(function () {
    var secondcategory_id = $(this).val();
    if (secondcategory_id) {
      $.ajax({
        url: "/get_thirdcategorys/" + secondcategory_id, // 適切なエンドポイントに変更する必要があります
        type: "GET",
        success: function (response) {
          $("#thirdcategory").html(response);
        },
        error: function (error) {
          console.log(error);
        },
      });
    } else {
      $("#thirdcategory").empty();
    }
  });
});