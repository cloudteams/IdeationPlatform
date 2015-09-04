$(function() {
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

        //update the management form
        $('#id_form-TOTAL_FORMS').val(n + 1);
        $('#id_form-INITIAL_FORMS').val(n + 1);
    });
});