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
            return this.$pb.find('input[name="csrfmiddlewaretoken"]').val()
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

    /* Open persona */
    $('body').on('click', 'a.pb-open', function(e) {
        console.log($(this).attr('href'))
        e.preventDefault();
        e.stopPropagation();

        PB.get($(this).attr('href'));
    })
});