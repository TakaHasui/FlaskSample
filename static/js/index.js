const srcNoimage = "./static/image/common/noimageFull.png";

function initAddForm() {
  document.querySelector("#modalSection .formMsg").style.display = "none";
  bookImgElem = document.getElementById("imageUrl");
  bookImgElem.setAttribute("src", srcNoimage);
  document.querySelector('#addForm input[name="imageUrl"]').value = "";

  let bookData = [
    "isbn",
    "title",
    "publisher",
    "author",
    "published",
    "description",
  ];
  bookData.forEach(function (val) {
    if (val == "description") {
      document.querySelector('#addForm textarea[name="' + val + '"]').value =
        "";
    } else {
      document.querySelector('#addForm input[name="' + val + '"]').value = "";
    }
  });
}

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
      if (!data[0]) {
        document.querySelector("#modalSection .formMsg").style.display =
          "block";
        return false;
      }

      for (let i = 0; i < data.length; i++) {
        // サムネイル
        bookImgElem = document.getElementById("imageUrl");
        let bookImgSrc = data[0].summary.cover;
        if (bookImgSrc) {
          bookImgElem.setAttribute("src", bookImgSrc);
          document.querySelector('#addForm input[name="imageUrl"]').value =
            data[0].summary.cover;
        } else {
          bookImgElem.setAttribute("src", srcNoimage);
          document.querySelector('#addForm input[name="imageUrl"]').value =
            srcNoimage;
        }
        let description = "";
        if (data[0].onix.CollateralDetail.TextContent) {
          description = data[0].onix.CollateralDetail.TextContent[0].Text;
        }

        console.log("************************");
        console.log(data);
        // date = new Date(data[0].summary.pubdate);
        let pubdate = data[0].summary.pubdate;
        if (pubdate.length == 6) {
          pubdate = pubdate + "01";
        }
        let bookData = new Map([
          ["isbn", data[0].summary.isbn],
          ["title", data[0].summary.title],
          ["publisher", data[0].summary.publisher],
          ["author", data[0].summary.author],
          ["published", pubdate],
          [("description", description)],
        ]);
        bookData.forEach(function (val, key) {
          if (key == "description") {
            document.querySelector(
              '#addForm textarea[name="' + key + '"]',
            ).value = val;
          } else {
            document.querySelector('#addForm input[name="' + key + '"]').value =
              val;
          }
        });
      }
    })
    .catch((err) => {
      console.log("Error: " + err);
    });
}

window.addEventListener("DOMContentLoaded", function () {
  let btnSearch = document.getElementById("addButton");
  let modalSect = document.getElementById("modalSection");
  let btnRegister = document.getElementById("register");
  let btnCancel = document.getElementById("cancel");

  btnSearch.addEventListener("click", () => {
    initAddForm();

    let isbn = document.getElementById("addIsbn").value;
    callOpenBdApi(isbn);

    modalSect.classList.add("is-show");
    return false;
  });

  btnRegister.addEventListener("click", () => {
    modalSect.classList.remove("is-show");
    return false;
  });

  btnCancel.addEventListener("click", (event) => {
    modalSect.classList.remove("is-show");
    return false;
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      modalSect.classList.remove("is-show");
      return false;
    }
  });
});
