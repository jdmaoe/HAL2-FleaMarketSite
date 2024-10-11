window.onload = function () {
  // クレジットカード決済を選択した状態に設定し、関連する入力フィールドを表示する
  document.getElementById("paymentMethod").value = "creditCard";
  togglePaymentFields();
};

function validateForm() {
  // エラーメッセージをリセットする
  resetErrorMessages();
  // フォームが妥当かどうかを示すフラグ
  var isValid = true;
  // 各項目のバリデーションを行う

  // 配送先住所のバリデーション
  var shippingAddress = document.getElementById("shippingAddress").value;
  if (shippingAddress.trim() === "") {
    document.getElementById("shippingAddressError").innerText = "配送先住所を入力してください。";
    document.getElementById("shippingAddressError").style.display = "block";
    isValid = false; // バリデーションエラーがあるため、フォームは無効
  }

  var paymentMethod = document.getElementById("paymentMethod").value;

  if (paymentMethod === "creditCard") {
    // クレジットカード番号のバリデーション
    var creditCardNumber = document.getElementById("creditCardNumber").value;
    if (!/^\d{12,16}$/.test(creditCardNumber)) {
      document.getElementById("creditCardNumberError").innerText = "クレジットカード番号は12桁から16桁の半角数字で入力してください。";
      document.getElementById("creditCardNumberError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }

    var expiryMonth = parseInt(document.getElementById("expiryMonth").value, 10);
    if (isNaN(expiryMonth) || expiryMonth < 1 || expiryMonth > 12) {
      document.getElementById("expiryMonthError").innerText = "有効期限（月）は1から12までの値を入力してください。";
      document.getElementById("expiryMonthError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }

    var expiryYear = parseInt(document.getElementById("expiryYear").value, 10);
    if (isNaN(expiryYear) || expiryYear < 24 || expiryYear > 34) {
      document.getElementById("expiryYearError").innerText = "有効期限（年）は24から34までの値を入力してください。";
      document.getElementById("expiryYearError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }

    var pin = document.getElementById("pin").value;
    if (!/^\d{3,4}$/.test(pin)) {
      document.getElementById("pinError").innerText = "PINは3桁から4桁の半角数字で入力してください。";
      document.getElementById("pinError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }

    var cardHolderName = document.getElementById("cardHolderName").value;
    if (!/^[\u00-\uFFA5]+$/.test(cardHolderName)) {
      document.getElementById("cardHolderNameError").innerText = "カード名義人は英字・ひらがな・カタカナ・漢字のみ入力してください。";
      document.getElementById("cardHolderNameError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  } else if (paymentMethod === "bankTransfer") {
    var bankCode = document.getElementById("bankCode").value;
    if (!/^\d{4}$/.test(bankCode)) {
      document.getElementById("bankCodeError").innerText = "金融機関コードは4桁の半角数字で入力してください。";
      document.getElementById("bankCodeError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }

    var branchCode = document.getElementById("branchCode").value;
    if (!/^\d{3}$/.test(branchCode)) {
      document.getElementById("branchCodeError").innerText = "支店コードは3桁の半角数字で入力してください。";
      document.getElementById("branchCodeError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }

    var accountType = document.getElementById("accountType").value;
    if (accountType !== "1" && accountType !== "2") {
      return false;
    }

    var accountNumber = document.getElementById("accountNumber").value;
    if (!/^\d{7}$/.test(accountNumber)) {
      document.getElementById("accountNumberError").innerText = "口座番号は7桁の半角数字で入力してください。";
      document.getElementById("accountNumberError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }

    var accountHolderName = document.getElementById("accountHolderName").value;
    if (!/^[\u00-\uFFA5]+$/.test(accountHolderName)) {
      document.getElementById("accountHolderNameError").innerText = "口座名義人は英字・ひらがな・カタカナ・漢字のみ入力してください。";
      document.getElementById("accountHolderNameError").style.display = "block";
      isValid = false; // バリデーションエラーがあるため、フォームは無効
    }
  }

  return isValid;
}


function togglePaymentFields() {
  var paymentMethod = document.getElementById("paymentMethod").value;
  var creditCardFields = document.getElementById("creditCardFields");
  var bankTransferFields = document.getElementById("bankTransferFields");

  if (paymentMethod === "creditCard") {
    creditCardFields.style.display = "block";
    bankTransferFields.style.display = "none";
  } else if (paymentMethod === "bankTransfer") {
    creditCardFields.style.display = "none";
    bankTransferFields.style.display = "block";
  }
}

function resetErrorMessages() {
  var errorMessages = document.querySelectorAll('.error-message');
  errorMessages.forEach(function (element) {
    element.innerText = '';
    element.style.display = 'none';
  });
}

document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("orderForm");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (validateForm()) {
        this.submit();
      }
    });
  }
});

