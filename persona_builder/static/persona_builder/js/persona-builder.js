/**
 * Created by dimitris on 14/10/2016.
 */
$(function() {
    PB = {
        $pb: $('.persona-popup'),
        $selectedPersona: undefined,

        messages: {
            loading: 'Loading persona...'
        },

        csrfmiddlewaretoken: function () {
            return $.cookie('csrftoken')
        },

        get: function(url, title) {
            PB.$pb.addClass('in').css('display', 'block');
            PB.$pb.find('.modal-header .header-medium').text(title || '');

            var $dBody = PB.$pb.find('.modal-body');
            $dBody.html(PB.messages.loading);

            $.ajax({
                url: url,
                method: 'GET',

                success: function (data) {
                    $dBody.html($(data));

                    // initialize select2 with placeholders
                    $.each($dBody.find('select:not(.comparison-select)'), function(idx, select){
                        var $select = $(select);
                        $select.select2({
                            placeholder: $select.data('placeholder') || ''
                        });
                    });

                    // load the query
                    if ($('#id_query').length === 1) {
                        QueryUI.from_string($('#id_query').val());
                    }

                    $dBody.find('#subpage-2').perfectScrollbar();
                }
            })
        },

        markSubmitAsLoading: function() {
            var $btn = PB.$pb.find('.confirm-button'),
                loadingText = $btn.data('loading_text') || 'Saving';

            console.log($btn);
            $btn.attr('disabled', 'disabled')
                .html('<i class="fa fa-spin fa-spinner" /> ' + loadingText + '...');
        },

        post: function($form, confirmation, actionBefore, actionDuring) {
            if (confirmation) {
                // show popup
                PB.$pb.addClass('in').css('display', 'block');
                var $dBody = PB.$pb.find('.modal-body');
                $dBody.empty();

                // add confirmation message
                var $row = $('<div class="row" />');
                var $content = $('<div />')
                    .addClass('col-xs-12')
                    .css('padding-top', '2em')
                    .css('padding-bottom', '2em')
                    .text(confirmation);
                $row.append($content);

                // add cancel/confirm buttons
                var $fieldset = $('<fieldset class="form-group form-submit" />');
                $fieldset.append('<a href="#nowhere" data-dismiss="modal" class="btn-transparent">Cancel</a>');
                var $confirmBtn = $('<button class="btn confirm-button" />')
                    .text(actionBefore || 'Confirm')
                    .on('click', function() {
                        $(this).html('<i class="fa fa-spin fa-spinner" /> ' + (actionDuring || 'Saving'));

                        $form.submit()
                    });

                $fieldset.append($confirmBtn);
                var $btnContainer = $('<div />').addClass('col-xs-12');
                $btnContainer.append($fieldset);
                $row.append($btnContainer);

                $dBody.append($row);
            } else {
                PB.markSubmitAsLoading();
                $form.submit();
            }
        },

        create: {
            get: function () {
                PB.get('/team-ideation-tools/personas/create/', 'Create a new persona')
            }
        },

        /* Open the chooser & load personas */
        open: function (persona_id) {
            PB.get('/team-ideation-tools/personas/' + persona_id + '/', 'Persona details')
        }
    };

    /* Connect events */
    $('.create-new-persona').on('click', function () {
        PB.create.get();
    });

    /* Create persona */
    $('body').on('click', '.persona-create', function() {
        PB.create.post();
    });

    /* On form submit */
    $('body').on('submit', '.persona-popup form', function(e) {
        PB.markSubmitAsLoading();
    });

    /* Action in persona dialog */
    $('body').on('click', 'a.pb-open', function(e) {
        e.preventDefault();
        e.stopPropagation();

        if ($(this).data('submit')) {
            PB.post($(this).closest('form'), $(this).data('confirmation'),
                $(this).data('action_before'), $(this).data('action_during'));
        } else {
            PB.get($(this).attr('href'), '');
        }
    });

    /* Close modals */
    $('body').on('click', '.modal [data-dismiss="modal"]', function() {
       $(this).closest('.modal').removeClass('in').css('display', 'none');
    });

    /* On persona avatar change */
    $('body').on('change', '#file-upload', function (e) {
        var tgt = e.target || window.event.srcElement,
            files = tgt.files;

        // FileReader support
        if (FileReader && files && files.length) {
            var fr = new FileReader();
            fr.onload = function () {
                $('.file-upload-image-container').get(0).style.backgroundImage = "url('" +fr.result + "')";
            };
            fr.readAsDataURL(files[0]);
        }
    });
});