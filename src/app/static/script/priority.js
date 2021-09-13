$(document).ready(function () {
    function hsl_col_perc(percent, start=240, end=0) {
        var a = percent / 100,
        b = (end - start) * a,
        c = b + start;
        return 'hsl('+c+', 100%, 35%)';
    }

    $(".priority").each(function() {
        console.log($(this));
        var val = parseFloat($(this).textContent);
        $(this).css({'color': hsl_col_perc(val)})
    });
});