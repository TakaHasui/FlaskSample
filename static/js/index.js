// 書籍API
// https://openbd.jp/
// https://dubdesign.net/javascript/openbd-book/
let addNewBook = function () {
  let isbn = document.getElementById("addIsbn").value;

  callOpenBdApi(isbn);
};

function callOpenBdApi(isbn) {
  // var isbn = userInput.split(' ').join('+');
  const url = "https://api.openbd.jp/v1/get?isbn=" + isbn + "&pretty";

  // fetchについて
  // https://lorem-co-ltd.com/fetch-basic/
  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      for (let i = 0; i < data.length; i++) {
        // サムネイル
        const bookImg = document.getElementById("thumbnail");
        const bookImgSrc = data[0].summary.cover;
        if (bookImgSrc) {
          bookImg.setAttribute("src", bookImgSrc);
          document.querySelector('#addForm input[name="image"]').value =
            data[0].summary.cover;
        }

        let bookData = new Map([
          ["isbn", data[0].summary.isbn],
          ["title", data[0].summary.title],
          ["publisher", data[0].summary.publisher],
          ["author", data[0].summary.author],
          ["published", data[0].summary.pubdate],
          ["description", data[0].onix.CollateralDetail.TextContent[0].Text],
        ]);

        bookData.forEach(function (val, key) {
          document.querySelector('#addForm input[name="' + key + '"]').value =
            val;
        });

        // // ISBN
        // document.querySelector('#addForm input[name="isbn"]').value =
        //   data[0].summary.isbn;
        // //書籍名
        // document.querySelector('#addForm input[name="title"]').value =
        //   data[0].summary.title;
        // //出版社
        // document.querySelector('#addForm input[name="publisher"]').value =
        //   data[0].summary.publisher;
        // //作者
        // document.querySelector('#addForm input[name="author"]').value =
        //   data[0].summary.author;
        // //出版日
        // document.querySelector('#addForm input[name="published"]').value =
        //   data[0].summary.pubdate;
        // //詳細
        // document.querySelector('#addForm textarea[name="description"]').value =
        //   data[0].onix.CollateralDetail.TextContent[0].Text;
      }
    })
    .catch((err) => {
      console.log("Error: " + err);
    });
}

function displayModalWindow() {
  let button = document.getElementById("addButton");
  let menu = document.getElementById("modalForm");
  let js_yes = document.getElementById("register");
  let js_no = document.getElementById("cancel");

  /* ボタンがクリックされたら、 メニュー表示させる */
  button.addEventListener("click", () => {
    menu.classList.add("is-show");
    return false;
  });

  /* はい ボタンがクリックされたら、 アラート後画面を閉じる */
  js_yes.addEventListener("click", () => {
    menu.classList.remove("is-show");
    return false;
  });

  /* いいえ ボタンを押したら メニューを閉じる */
  js_no.addEventListener("click", (event) => {
    menu.classList.remove("is-show");
    return false;
  });
}

let addBtnElem = document.getElementById("addButton");
addBtnElem.addEventListener("click", addNewBook);
window.addEventListener("DOMContentLoaded", displayModalWindow);
