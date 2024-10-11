
const showButtons = document.querySelectorAll('.show-details');
const hideButtons = document.querySelectorAll('.hide-details');
const detailsSections = document.querySelectorAll('.details');
const summarySections = document.querySelectorAll('.summary');

// 詳細を見るボタンをクリックした時の処理
showButtons.forEach((button, index) => {
  button.addEventListener('click', () => {
    // 詳細を見るボタンと詳細表示部分、概要文の切り替え
    button.style.display = 'none';
    detailsSections[index].style.display = 'block';
    summarySections[index].style.display = 'none';
  });
});

// 詳細を閉じるボタンをクリックした時の処理
hideButtons.forEach((button, index) => {
  button.addEventListener('click', () => {
    // 詳細を閉じるボタンと詳細表示部分、概要文の切り替え
    detailsSections[index].style.display = 'none';
    showButtons[index].style.display = 'block';
    summarySections[index].style.display = 'block';
  });
});