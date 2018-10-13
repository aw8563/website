// Initialise the date picker
$(document).ready(function () {
    $('.datepicker').datepicker({
        format: 'dd/mm/yyyy'
    });
});

// Initialise the timepicker
$(document).ready(function () {
    $('.timepicker').timepicker({
        twelveHour: false
    });
});

// Initialise the 'select' box.
$(document).ready(function () {
    $('select').formSelect();
});
