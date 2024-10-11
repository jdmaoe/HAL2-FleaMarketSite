// ページ読み込み時に最下部にスクロール
window.onload = function() {
    var element = document.getElementById("chat-messages");
    if(element) {
        element.scrollTop = element.scrollHeight;
    }
};

// フォームが送信された後に最下部にスクロール
var form = document.getElementById("chat-form");
if(form) {
    form.addEventListener("submit", function() {
        var element = document.getElementById("chat-messages");
        if(element) {
            element.scrollTop = element.scrollHeight;
        }
    });
}
