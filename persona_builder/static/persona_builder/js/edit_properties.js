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

    /* Load the rows from query */
    function load_query(query) {
        var filters = query.split(' AND ');
        var infos = [];

        for (var f=0; f<filters.length; f++) {
            var info = {'name': '', 'comp': '', 'val': ''};
            var keys = ['name', 'comp', 'val'];
            var pos = 0;

            var filter = filters[f];
            console.log(filter);
            for (var i=0; i<filter.length; i++) {
                //detect in which part of the query we are
                if (['>', '<', '=', '!'].indexOf(filter[i]) >= 0) {
                    if (pos == 0) {
                        pos++;
                    }
                } else {
                    if (pos == 1) {
                        pos++;
                    }
                }

                info[keys[pos]] += filter[i];
            }

            infos.push(info);
        }

        //create the UI elements again
        for (var i=0; i<infos.length; i++) { //foreach filter
            $('.property-row:last-of-type').find('select.filter-select').val(infos[i]['name']);
            $('.property-row:last-of-type').find('select.comparison-select').val(infos[i]['comp']);
            $('.property-row:last-of-type').find('input').val(infos[i]['val']);

            //add new row
            if (i < infos.length - 1) {
                $('.add-property-row').click();
            }
        }
    }

    load_query($('.query-box input').val());

    /* Create the query from rows */
    $('body').on('submit', '.persona-filters-form', function() {
        var query = '';

        for(var i=0; i<$('.property-row').length; i++) {
            var row = $($('.property-row')[i]);

            if (query != '') {
                query += ' AND ';
            }

            if (row.find('select.filter-select').val() != '') {
                query += row.find('select.filter-select').val() + row.find('select.comparison-select').val() + row.find('input').val();
            }
        }

        $('.query-box input').val(query);
    });
});