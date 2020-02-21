//더보기 토글
function showplay() {
    var flag = $('#hidTempSynopsis');
    var SynopsisDiv = $('#SynopsisDiv');
    var flagValue = flag.val();
    if (flag != null) {
        if (flagValue == "0") {
            SynopsisDiv.css({
                "display": "block",
                "line-height": "1.5em"
            });
            $("#synopMore").html('');
            $("#synopMore").append('<div><i class="fas fa-chevron-up"></i></div><div>올리기</div>');
            flag.val("1");
        } else {
            SynopsisDiv.css("display", "-webkit-box");
            $("#synopMore").html('');
            $("#synopMore").append('<div>내리기</div><div><i class="fas fa-chevron-down"></i></div>');
            flag.val("0");
        }
    } else {
        alert("추가 정보가 없습니다.");
    }
}
