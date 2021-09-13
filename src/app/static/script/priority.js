$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    var text = parseFloat(document.querySelector('.priority').textContent);

    function hsl_col_perc(percent, start=240, end=0) {
        var a = percent / 100,
        b = (end - start) * a,
        c = b + start;
        return 'hsl('+c+', 100%, 50%)';
    };

    $('.priority').css({'color': hsl_col_perc(text)});
});