$(function() {
    // disable double form submit
    $('form').on('submit', function() {
        $(this).find('input[type="submit"]').prop('disabled', true);
    });

    // fix tooltips
    $('body').on('click', '.open-tooltip-button', function() {
        $(this).closest('.tooltip-container').find('.custom-tooltip').toggleClass('active')
    })
});