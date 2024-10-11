function validateForm() {
  // エラーメッセージをリセットする
  resetErrorMessages();
  // フォームが妥当かどうかを示すフラグ
  var isValid = true;
  // 各項目のバリデーションを行う

  // ユーザーネームのバリデーション
  var userName = document.getElementById("userName").value;
  // 空文字の場合と名前が30文字を超える場合はエラー
  if (userName.trim() === "") {
    document.getElementById("userNameError").innerText =
      "ユーザーネームを入力してください。";
    document.getElementById("userNameError").style.display = "block";
    isValid = false; // バリデーションエラーがあるため、フォームは無効
  } else if (userName.length > 30) {
    document.getElementById("userNameError").innerText =
      "ユーザーネームは30文字以内で入力してください。";
    document.getElementById("userNameError").style.display = "block";
    isValid = false; // バリデーションエラーがあるため、フォームは無効
  }

  // メールアドレスのバリデーション
  var email = document.getElementById("email").value;
  // メールアドレスが空文字の場合とメールアドレスが50文字を超える場合はエラー
  if (email.trim() === "") {
    document.getElementById("emailError").innerText =
      "メールアドレスを入力してください。";
    document.getElementById("emailError").style.display = "block";
    isValid = false; // バリデーションエラーがあるため、フォームは無効
  } else if (email.length > 50) {
    document.getElementById("emailError").innerText =
      "メールアドレスは50文字以内で入力してください。";
    document.getElementById("emailError").style.display = "block";
    isValid = false; // バリデーションエラーがあるため、フォームは無効
  }

  // パスワードのバリデーション
  var password = document.getElementById("password").value;
  // パスワードが20文字を超える場合はエラー
  if (password.length > 20) {
    document.getElementById("passwordError").innerText =
      "パスワードは20文字以内で入力してください。";
    document.getElementById("passwordError").style.display = "block";
    isValid = false; // バリデーションエラーがあるため、フォームは無効
  }

  // 電話番号のバリデーション
  var tel = document.getElementById("tel").value;
  // telが全角数字の場合は半角数字に変換
  tel = tel.replace(/[０-９]/g, function (s) {
    return String.fromCharCode(s.charCodeAt(0) - 0xfee0);
  });
  // 電話番号に入力がある場合のみバリデーションを行う
  if (tel.trim() !== "") {
    // 電話番号が10桁から11桁でない場合はエラー
    if (!/^\d{10,11}$/.test(tel)) {
      document.getElementById("telError").innerText =
        "電話番号は10桁から11桁の半角数字で入力してください。";
      document.getElementById("telError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // 住所のバリデーション
  var address = document.getElementById("address").value;
  // 住所の入力がある場合のみバリデーションを行う
  if (address.trim() !== "") {
    // 住所が50文字を超える場合はエラー
    if (address.length > 100) {
      document.getElementById("addressError").innerText =
        "住所は50文字以内で入力してください。";
      document.getElementById("addressError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // 建物名・部屋番号のバリデーション
  var building_name_number = document.getElementById(
    "building_name_number"
  ).value;
  // 建物名・部屋番号の入力がある場合のみバリデーションを行う
  if (building_name_number.trim() !== "") {
    // 建物名・部屋番号が50文字を超える場合はエラー
    if (building_name_number.length > 50) {
      document.getElementById("building_name_numberError").innerText =
        "建物名・部屋番号は50文字以内で入力してください。";
      document.getElementById("building_name_numberError").style.display =
        "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // 顔画像のバリデーション
  var face_image = document.getElementById("face_image").value;
  // 顔画像の入力がある場合のみバリデーションを行う
  if (face_image.trim() !== "") {
    // 顔画像のファイル形式がjpeg, jpg, pngのいずれでもない場合はエラー
    if (!/\.(jpe?g|png)$/i.test(face_image)) {
      document.getElementById("face_imageError").innerText =
        "顔画像はjpeg, jpg, png形式のファイルを指定してください。";
      document.getElementById("face_imageError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // クレジットカード番号のバリデーション
  var cardnumber = document.getElementById("cardnumber").value;
  // クレジットカード番号が全角数字の場合は半角数字に変換
  cardnumber = cardnumber.replace(/[０-９]/g, function (s) {
    return String.fromCharCode(s.charCodeAt(0) - 0xfee0);
  });
  // クレジットカード番号の入力がある場合のみバリデーションを行う
  if (cardnumber.trim() !== "") {
    // クレジットカード番号が12桁から16桁でない場合はエラー
    if (!/^\d{12,16}$/.test(cardnumber)) {
      document.getElementById("cardnumberError").innerText =
        "クレジットカード番号は12桁から16桁の数字で入力してください。";
      document.getElementById("cardnumberError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // クレジットカード名義人のバリデーション
  var cardnominee = document.getElementById("cardnominee").value;
  // クレジットカード名義人の入力がある場合のみバリデーションを行う
  if (cardnominee.trim() !== "") {
    // クレジットカード名義人が20文字を超える場合はエラー
    if (cardnominee.length > 20) {
      document.getElementById("cardnomineeError").innerText =
        "クレジットカード名義人は20文字以内で入力してください。";
      document.getElementById("cardnomineeError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // 金融機関コードのバリデーション
  var bankcode = document.getElementById("bankcode").value;
  // 金融機関コードが全角数字の場合は半角数字に変換
  bankcode = bankcode.replace(/[０-９]/g, function (s) {
    return String.fromCharCode(s.charCodeAt(0) - 0xfee0);
  });
  // 金融機関コードの入力がある場合のみバリデーションを行う
  if (bankcode.trim() !== "") {
    // 金融機関コードが4桁でない場合はエラー
    if (!/^\d{4}$/.test(bankcode)) {
      document.getElementById("bankcodeError").innerText =
        "金融機関コードは4桁の数字で入力してください。";
      document.getElementById("bankcodeError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // 支店コードのバリデーション
  var branchcode = document.getElementById("branchcode").value;
  // 支店コードが全角数字の場合は半角数字に変換
  branchcode = branchcode.replace(/[０-９]/g, function (s) {
    return String.fromCharCode(s.charCodeAt(0) - 0xfee0);
  });
  // 支店コードの入力がある場合のみバリデーションを行う
  if (branchcode.trim() !== "") {
    // 支店コードが3桁でない場合はエラー
    if (!/^\d{3}$/.test(branchcode)) {
      document.getElementById("branchcodeError").innerText =
        "支店コードは3桁の数字で入力してください。";
      document.getElementById("branchcodeError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // 口座番号のバリデーション
  var accountnumber = document.getElementById("accountnumber").value;
  // 口座番号が全角数字の場合は半角数字に変換
  accountnumber = accountnumber.replace(/[０-９]/g, function (s) {
    return String.fromCharCode(s.charCodeAt(0) - 0xfee0);
  });
  // 口座番号の入力がある場合のみバリデーションを行う
  if (accountnumber.trim() !== "") {
    // 口座番号が7桁から8桁でない場合はエラー
    if (!/^\d{7,8}$/.test(accountnumber)) {
      document.getElementById("accountnumberError").innerText =
        "口座番号は7桁から8桁の数字で入力してください。";
      document.getElementById("accountnumberError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  // 口座名義人のバリデーション
  var accountnominee = document.getElementById("accountnominee").value;
  // 口座名義人の入力がある場合のみバリデーションを行う
  if (accountnominee.trim() !== "") {
    // 口座名義人が20文字を超える場合はエラー
    if (accountnominee.length > 20) {
      document.getElementById("accountnomineeError").innerText =
        "口座名義人は20文字以内で入力してください。";
      document.getElementById("accountnomineeError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  return isValid;
}

// エラーメッセージをリセットする
function resetErrorMessages() {
  var errorMessages = document.querySelectorAll(".error-message");
  errorMessages.forEach(function (element) {
    element.innerText = "";
    element.style.display = "none";
  });
}

// エラーメッセージのある項目までスクロールする関数
function scrollToElement(element) {
  if (!element) {
    console.error("Element does not exist");
    return;
  }

  // offsetTopの取得を遅延させる
  setTimeout(function () {
    var offsetTop = 0;
    window.scrollTo({
      top: offsetTop,
      behavior: "smooth",
    });
  }, 300); // 適切な待ち時間を設定
}

// フォームが送信される前にvalidateForm関数を実行する
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("editForm");
  // フォームが存在する場合のみイベントを追加
  if (form) {
    // フォームが送信される前にvalidateForm関数を実行する
    form.addEventListener("submit", function (event) {
      // フォームのデフォルトのイベントを無効にする
      event.preventDefault();
      // フォームのバリデーションを行う
      if (validateForm()) {
        this.submit();
      }
      document.getElementById("form-flash").innerText = "";
      document.getElementById("formError").innerText =
        "入力内容にエラーがあります。エラーメッセージをご確認の上、再度送信してくだい";
      document.getElementById("formError").style.display = "block";
      // エラーメッセージのある項目までスクロールする
      var firstErrorMessage = document.querySelector(".error-message");
      if (firstErrorMessage) {
        scrollToElement(firstErrorMessage);
      }
    });
  }
});

("use strict"); /* 厳格にエラーをチェック */

{
  /* ローカルスコープ */

  // DOM取得
  const tabMenus = document.querySelectorAll(".tab__menu-item");
  console.log(tabMenus);

  // イベント付加
  tabMenus.forEach((tabMenu) => {
    tabMenu.addEventListener("click", tabSwitch);
  });

  // イベントの処理
  function tabSwitch(e) {
    // クリックされた要素のデータ属性を取得
    const tabTargetData = e.currentTarget.dataset.tab;
    // クリックされた要素の親要素と、その子要素を取得
    const tabList = e.currentTarget.closest(".tab__menu");
    console.log(tabList);
    const tabItems = tabList.querySelectorAll(".tab__menu-item");
    console.log(tabItems);
    // クリックされた要素の親要素の兄弟要素の子要素を取得
    const tabPanelItems =
      tabList.nextElementSibling.querySelectorAll(".tab__panel-box");
    console.log(tabPanelItems);

    // クリックされたtabの同階層のmenuとpanelのクラスを削除
    tabItems.forEach((tabItem) => {
      tabItem.classList.remove("is-active");
    });
    tabPanelItems.forEach((tabPanelItem) => {
      tabPanelItem.classList.remove("is-show");
    });

    // クリックされたmenu要素にis-activeクラスを付加
    e.currentTarget.classList.add("is-active");
    // クリックしたmenuのデータ属性と等しい値を持つパネルにis-showクラスを付加
    tabPanelItems.forEach((tabPanelItem) => {
      if (tabPanelItem.dataset.panel === tabTargetData) {
        tabPanelItem.classList.add("is-show");
      }
    });
  }
}




// 郵便番号から住所を自動入力する機能
$(function () {
  $('#postcode').on('blur', function () {
    AjaxZip3.zip2addr(this, '', 'address', 'address');
  });
});