
$(function() {
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
});