$(function() {
    // disable double form submit
    $('form').on('submit', function() {
        $(this).find('input[type="submit"]').prop('disabled', true);
    })

    $('a').on('click', function() {
        console.log('opa!')
    })
});