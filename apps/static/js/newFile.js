document.getElementById("orderForm").addEventListener("submit", function (event) {
  event.preventDefault();
  if (validateForm()) {
    this.submit();
  } else {
    document.getElementById("creditCardNumberError").innerText = "クレジットカード番号は12桁から16桁の半角数字で入力してください。";
    document.getElementById("expiryMonthError").innerText = "有効期限（月）は1から12までの値を入力してください。";
    document.getElementById("expiryYearError").innerText = "有効期限（年）は24から34までの値を入力してください。";
    document.getElementById("pinError").innerText = "PINは3桁から4桁の半角数字で入力してください。";
    document.getElementById("cardHolderNameError").innerText = "カード名義人は英字・ひらがな・カタカナ・漢字のみ入力してください。";
    document.getElementById("bankCodeError").innerText = "金融機関コードは4桁の半角数字で入力してください。";
    document.getElementById("branchCodeError").innerText = "支店コードは3桁の半角数字で入力してください。";
    document.getElementById("accountNumberError").innerText = "口座番号は7桁の半角数字で入力してください。";
    document.getElementById("accountHolderNameError").innerText = "口座名義人は英字・ひらがな・カタカナ・漢字のみ入力してください。";
  }
});
