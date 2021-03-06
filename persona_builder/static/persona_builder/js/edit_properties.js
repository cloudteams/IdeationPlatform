$(function() {
    QueryUI = {
        clear: function() {
            $('.filter-value').val('').trigger('change').trigger('chosen:updated');
        },

        // load UI from query text
        from_string: function(query) {
            // initially clear the UI
            this.clear();

            // turn [(activity="Running")] to (activity="Running")
            if (query.indexOf('[') >= 0) {
                query = query.substring(1, query.length - 2);
            }

            // turn activity="Running" to (activity="Running")
            if (query.indexOf('(') < 0) {
                query = '(' + query + ')';
            }

            // split parts based on parentheses
            // remember - no support for multiple levels & complex logic
            var parts = query.split('(');
            for (var i=1; i<parts.length; i++) {  //ignore first part - empty
                var f = parts[i];
                // detect different parts of the expression
                // e.g activity!="Running" must be split into activity / != / Running
                var exp = ["", "", ""], ptr = 0, special = false, symbols = ['=', '<', '>', '!'];
                for (var c=0; c<f.length; c++) {
                    if ((symbols.indexOf(f[c]) >= 0) != special) {
                        special = !special;
                        ptr++;
                    }
                    if (f[c] == ')') { // end of property
                        break;
                    }
                    if (f[c] != '"') {
                        exp[ptr] += f[c];
                    }
                }

                // find the values -- could be more than one
                var vals = exp[2].split('||');

                // mark the filter as selected in the UI
                var fr = $('.filter-row[data-name="' + exp[0] + '"]');
                fr.find('.comparison-select').val(exp[1]);
                fr.find('.filter-value').val(vals);
                fr.find('select.filter-value').trigger('change').trigger('chosen:updated');
            }
        },

        // save UI to query text
        to_string: function() {
            var result = '[';
            var fs = $('.filter-row');
            for (var i=0; i<fs.length; i++) {
                var fr = $(fs[i]);
                var prop = fr.data('name');
                var tp = fr.data('type');
                var comp = fr.find('.comparison-select').val()
                var vals = fr.find('.filter-value').val();
                if (!(vals instanceof Array)) {
                    vals = [vals];
                }

                result += '(';
                var n = 0;
                for (var j=0; j<vals.length; j++) { // add value in the OR clause
                    if ((vals[j] == '') || (vals[j] === null)) {
                        continue;
                    }

                    n++;
                    if (n == 1) {
                        result += prop + comp;
                    }

                    if (tp != 'integer') {
                        result += '"';
                    }
                    result += vals[j];
                    if (tp != 'integer') {
                        result += '"';
                    }
                    result += '||';
                }
                if (n > 0) {
                    // remove trailing OR
                    result = result.substring(0, result.lastIndexOf('||'));
                }

                result += ')';
                if (i < fs.length - 1) {
                    result += ' AND ';
                }
            }
            result += ']';

            // remove empty clauses & return result
            return result.replace(/AND \(\) /g, '').replace(/AND \(\)/g, '')
                         .replace(/ \(\) AND /g, '').replace(/\(\) AND /g, '')
                         .replace(/\[\(\) \]/g, '');
        }
    };

    // update query on changes
    $('body').on('change', '.filter-value', function() {
        $('#id_query').val(QueryUI.to_string());
    });

    // on clear comparison select also clear value
    $('.comparison-select').on('change', function() {
        if ($(this).val() == '') {
            var fr = $(this).closest('.filter-row');
            fr.find('.filter-value').val('');
            fr.find('.filter-value').trigger('change');
            fr.find('select.filter-value').trigger('chosen:updated');
        }
    });

    $('form').submit(function() {
        $('body').prepend('<div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%">Matching customers... / This might take a few moments</div></div>');
        $('body').animate({ scrollTop: 0 }, 600);
    })
});