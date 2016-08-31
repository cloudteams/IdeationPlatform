
$(function() {
    /* Initially add remove form button */
    $('.column-form').prepend('<span class="remove-form pull-right">x</span>');

    function on_option_input_change(selector) {
        $(selector).closest('.column-form').find('.option-input').closest('p').addClass('hidden');
        $(selector).closest('.column-form').find('.option-input[data-about="' + $(selector).val() + '"]').closest('p').removeClass('hidden');
    }

    /*Add a new property*/
    $('body').on('click', '.add-property-row', function() {
        //get last form
        var form_html = $('.form-list .column-form:last-of-type').html();

        //create a copy of it with increased counter
        var n = Number($('#id_form-TOTAL_FORMS').val());

        //replace all manually - form html has too weird chars to bother with a regex
        var old_form_html = '';
        while (old_form_html != form_html) {
            old_form_html = form_html;
            form_html = form_html.replace('form-' + (n - 1) + '-', 'form-' + (n) + '-');
        }

        form_html = '<div class="column-form">' + form_html + '</div>';
        $('.form-list').append(form_html);

        //clear initial values
        $('.form-list .column-form:last-of-type input[type="checkbox"]').prop("checked", true);
        $('.form-list .column-form:last-of-type input[type="text"]').val('');
        $('.form-list .column-form:last-of-type select').val('');
        $('.form-list .column-form:last-of-type select').change();

        //select2
        // $('.source-options').select2();

        //update the management form
        $('#id_form-TOTAL_FORMS').val(n + 1);
        $('#id_form-INITIAL_FORMS').val(n + 1);
    });

    /*Show only appropriate option fields at start*/
    $('.option-input').closest('p').addClass('hidden');
    for (var i=0; i<$('.source-options').length; i++) {
        on_option_input_change('#' + $('.source-options')[i].id);
    }

    /* Update shown option fields on change*/
    $('body').on('change', 'select.source-options', function() {
        on_option_input_change(this);
    });

    /* Remove a form */
    $('body').on('click', '.column-form .remove-form', function() {
        //get the position of the removed form
        var name = $(this).closest('.column-form').find('p:first-of-type input').attr('name');
        var current = Number(name.split('-')[1]);

        //remove this form
        var form_list = $(this).closest('.form-list');
        $(this).closest('.column-form').remove();

        //update all forms after this one
        var n = Number($('#id_form-TOTAL_FORMS').val());
        var labels = $(form_list).find('label');
        var inputs = $(form_list).find('input');
        var selects = $(form_list).find('select');
        for (var i=current; i<n; i++) {
            //foreach label
            $(labels).each(function() {
                //replace for
                var _for = $(this).attr('for');
                if (_for.indexOf('form-' + (i+1) + '-') >= 0) {
                    $(this).attr('for', _for.replace('form-' + (i+1) + '-', 'form-' + i + '-'))
                }
            });

            //foreach input
            $(inputs).each(function() {
                //replace id
                var id = $(this).attr('id');
                if (id.indexOf('form-' + (i+1) + '-') >= 0) {
                    $(this).attr('id', id.replace('form-' + (i+1) + '-', 'form-' + i + '-'))
                }
                //replace name
                var name = $(this).attr('name');
                if (name.indexOf('form-' + (i+1) + '-') >= 0) {
                    $(this).attr('name', name.replace('form-' + (i+1) + '-', 'form-' + i + '-'))
                }
            });

            //foreach select
            $(selects).each(function() {
                //replace id
                var id = $(this).attr('id');
                if (id.indexOf('form-' + (i+1) + '-') >= 0) {
                    $(this).attr('id', id.replace('form-' + (i+1) + '-', 'form-' + i + '-'))
                }
                //replace name
                var name = $(this).attr('name');
                if (name.indexOf('form-' + (i+1) + '-') >= 0) {
                    $(this).attr('name', name.replace('form-' + (i+1) + '-', 'form-' + i + '-'))
                }
            });
        }

        //update the management form
        $('#id_form-TOTAL_FORMS').val(n - 1);
        $('#id_form-INITIAL_FORMS').val(n - 1);
    });
});