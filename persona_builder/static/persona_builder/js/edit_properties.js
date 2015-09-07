$(function() {
    /* Add another property */
    $('body').on('click', ".add-property-row", function(e) {
        /* duplicate last row */
        var html = $('.property-row:last-of-type').html();
        html = '<div class="property-row">' + html + '</div>';
        $('.property-row-container').append(html);

        /* clean values */
        $('.property-row:last-of-type select.filter-select').val('0');
        $('.property-row:last-of-type select.comparison-select').val('0');
        $('.property-row:last-of-type input').val('');
    });

    /* Remove an existing property */
    $('body').on('click', ".property-row .remove-row", function(e) {
        if ($('.property-row').length === 1) {
            //clean this row
            $(this).find('select.filter-select').val('0');
            $(this).find('select.comparison-select').val('0');
            $(this).find('input').val('');
        } else {
            //remove this row
            $(this).closest('.property-row').remove();
        }
    });

    $('body').on('submit', '.persona-filters-form', function() {
        var query = '';

        for(var i=0; i<$('.property-row').length; i++) {
            var row = $($('.property-row')[i]);

            if (query != '') {
                query += ' AND ';
            }

            query += row.find('select.filter-select').val() + row.find('select.comparison-select').val() + row.find('input').val()
        }

        $('.query-box input').val(query);
    });
});