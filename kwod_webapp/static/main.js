function closeDialog(){
    var whitebg = document.getElementById("white-background");
    var dlg = document.getElementById("dlgbox");
    whitebg.style.display = "none";
    dlg.style.display = "none";
}

function showDialog(){
    var whitebg = document.getElementById("white-background");
    var dlg = document.getElementById("dlgbox");
    whitebg.style.display = "block";
    dlg.style.display = "block";

    var winWidth = window.innerWidth;
    var winHeight = window.innerHeight;

    dlg.style.left = (winWidth/2) - 480/2 + "px";
    dlg.style.top = "150px";
}

function ClearDialogFields() {

     document.getElementById("dlgName").value = "";
     document.getElementById("dlgSurname").value = "";
     document.getElementById("dlgFileHeader").value = "";
     document.getElementById("dlgFileDat").value = "";
}


function validateForm() {

    if (document.getElementById("dlgName").value == "") {
        alert("Wpisz imię");
        return false;
    }
    if (document.getElementById("dlgSurname").value == "") {
        alert("Wpisz nazwiskko");
        return false;
    }
    var header = document.getElementById("dlgFileHeader").value
    var dat = document.getElementById("dlgFileDat").value

    if (header.length > 4) {
        if (header.substr(header.length - 4, 4).toLowerCase() == ".hea") {

        return true
        }

        alert("Dołącz poprawny plik nagłówkowy");
        return false;
    }
    else {

        alert("Dołącz plik nagłówkowy");
        return false;
    }

    if (dat.length > 4) {
        if (dat.substr(dat.length - 4, 4).toLowerCase() == ".dat") {

        return true
        }

        alert("Dołącz poprawny plik z danymi");
        return false;
    }
    else {

        alert("Dołącz plik z danymi");
        return false;
    }
}