/**
 * Created by dimitris on 14/10/2016.
 */
$(function() {
    var PB = {
        $pb: $('.persona-popup'),
        $selectedPersona: undefined,

        messages: {
            loading: 'Loading persona...'
        },

        csrfmiddlewaretoken: function () {
            return $.cookie('csrftoken')
        },

        get: function(url) {
            PB.$pb.addClass('in').css('display', 'block');

            var $dBody = PB.$pb.find('.modal-body');
            $dBody.html(PB.messages.loading);

            $.ajax({
                url: url,
                method: 'GET',

                success: function (data) {
                    $dBody.html($(data));
                    $dBody.find('select:not(.comparison-select)').select2();
                    $dBody.find('#subpage-2').perfectScrollbar();

                    // ajax forms
                    $dBody.find('form').ajaxForm(function(url) {
                        PB.get(url);
                    });
                }
            })
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
                        $(this)
                            .append('<i class="fa fa-spin fa-spinner" />')
                            .text(actionDuring || 'Saving');

                        // $form.submit()
                    });

                $fieldset.append($confirmBtn);
                var $btnContainer = $('<div />').addClass('col-xs-12');
                $btnContainer.append($fieldset);
                $row.append($btnContainer);

                $dBody.append($row);
            } else {
                $form.submit();
            }
        },

        create: {
            get: function () {
                PB.get('/team-ideation-tools/personas/create/')
            }
        },

        /* Open the chooser & load personas */
        open: function (persona_id) {
            PB.get('/team-ideation-tools/personas/' + persona_id + '/')
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

    /* Action in persona dialog */
    $('body').on('click', 'a.pb-open', function(e) {
        e.preventDefault();
        e.stopPropagation();

        if ($(this).data('submit')) {
            PB.post($(this).closest('form'), $(this).data('confirmation'),
                $(this).data('action_before'), $(this).data('action_during'));
        } else {
            PB.get($(this).attr('href'));
        }
    });

    /* Close modals */
    $('body').on('click', '.modal [data-dismiss="modal"]', function() {
       $(this).closest('.modal').removeClass('in').css('display', 'none');
    });
});