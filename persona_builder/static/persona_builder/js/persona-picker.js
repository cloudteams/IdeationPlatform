$(function() {
    var PersonaPicker = {
        $ppc: $('#persona-pool-chooser'),
        $selectedPersona: undefined,

        messages: {
            loading: 'Listing public personas...'
        },

        csrfmiddlewaretoken: function() {
            return $('#persona-pool-list').data('csrfmiddlewaretoken')
        },

        /* Open the chooser & load personas */
        open: function() {
            this.$ppc.modal('show')
            var $dBody = this.$ppc.find('.modal-body')
            $dBody.html(this.messages.loading)

            $.ajax({
                url: '/persona-builder/personas/pool/',
                method: 'GET',

                success: function(data) {
                   $dBody.html($(data))
                }
            })
        },

        toggleSelect: function($persona) {
            if (!$persona.hasClass('selected')) { // select
                $persona.addClass('selected')
                $persona.find('.picker > .fa').removeClass('fa-plus').addClass('fa-check-circle')
                this.$selectedPersona = $persona
            } else { // un-select
                $persona.removeClass('selected')
                $persona.find('.picker > .fa').removeClass('fa-check-circle').addClass('fa-plus')
                this.$selectedPersona = undefined
            }
        },

        confirm: function() {
            if (typeof(this.$selectedPersona) != 'undefined') {
                var personaId = this.$selectedPersona.data('persona_id')

                console.log(this.csrfmiddlewaretoken())
                $.ajax({
                    url: '/persona-builder/personas/add-from-pool/' + personaId + '/',
                    method: 'POST',
                    data: {
                        'csrfmiddlewaretoken': this.csrfmiddlewaretoken()
                    },
                    success: function(data) {
                       window.location = '/persona-builder/personas/' + data + '/edit-info/'
                    }
                })
            }
        }
    };

    /* Connect events */
    $('.add-from-pool').on('click', function() {
        PersonaPicker.open();
    });

    $('body').on('click', '.selectable-persona', function() {
        PersonaPicker.toggleSelect($(this));
    });

    $('body').on('click', '.add-persona', function() {
        PersonaPicker.confirm();
    });
});