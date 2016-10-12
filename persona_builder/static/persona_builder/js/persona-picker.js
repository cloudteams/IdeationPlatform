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
                url: '/team-ideation-tools/personas/pool/',
                method: 'GET',

                success: function(data) {
                   $dBody.html($(data))
                    // make persona list scrollable
                   $('#persona-pool-list-content').perfectScrollbar();
                }
            })
        },

        unselect: function() {
            if (typeof(this.$selectedPersona) != 'undefined') {
                this.$selectedPersona.removeClass('selected')
                this.$selectedPersona.find('.picker > .fa').removeClass('fa-check-circle').addClass('fa-plus')
                this.$selectedPersona = undefined
            }
        },

        toggleSelect: function($persona) {
            var selected = $persona.hasClass('selected');
            this.unselect();

            if (!selected) { // select
                $persona.addClass('selected')
                $persona.find('.picker > .fa').removeClass('fa-plus').addClass('fa-check-circle')
                this.$selectedPersona = $persona
            }
        },

        filter: function(text) {
            $.each($('.selectable-persona'), function(idx, persona) {
                var $persona = $(persona);
                var name = $persona.find('h3').text().toLowerCase();
                var description = $persona.find('.persona-description').text().toLowerCase();

                if ((name.search(text.toLowerCase()) >= 0) || (description.search(text.toLowerCase()) >= 0)) {
                    $persona.removeClass('hidden');
                } else {
                    $persona.addClass('hidden');
                }
            })
        },

        confirm: function() {
            if (typeof(this.$selectedPersona) != 'undefined') {
                var personaId = this.$selectedPersona.data('persona_id')

                $.ajax({
                    url: '/team-ideation-tools/personas/add-from-pool/' + personaId + '/',
                    method: 'POST',
                    data: {
                        'csrfmiddlewaretoken': this.csrfmiddlewaretoken()
                    },
                    success: function(data) {
                       window.location = '/team-ideation-tools/personas/' + data + '/edit-info/'
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

    $('body').on('click', '#persona-pool-search-container', function(e) {
        $(this).addClass('focused');
        e.stopPropagation();
    });

    $('body').on('click', function(e) {
        $('#persona-pool-search-container').removeClass('focused');
    });

    $('body').on('input', '#persona-pool-search', function(e) {
        PersonaPicker.filter($(this).val());
    });

});