$(function() {
    var Autocomplete = {
        $autocomplete: $('#autocomplete-suggestions'),
        simplemde: undefined,
        startPosition: undefined,
        active: false,

        // when the autocomplete is triggered
        trigger: function(simplemde) {
            // TODO re-enable
            // this.$autocomplete.css('visibility', 'visible');

            this.active = true;
            this.simplemde = simplemde;
            this.startPosition = simplemde.codemirror.getCursor('start');

            this.fetchTerms()
        },

        fetchTerms: function() {
            var that = this;
            var fn = function() {
                var endPosition = that.simplemde.codemirror.getCursor('end');

                that.simplemde.codemirror.setSelection(that.startPosition, endPosition);
                var term = that.simplemde.codemirror.getSelection();
                console.log(term);
                that.simplemde.codemirror.setSelection(endPosition, endPosition);

                //this.simplemde.replaceSelection();
                $.ajax({
                    url: 'suggest-term/',
                    success: function (data) {
                        var $list = that.$autocomplete.find('.suggestions-list');

                        $list.html('');
                        $.each(data, function (idx, term) {
                            $list.append('<li>' + term.text + '</li>')
                        });
                    }
                })
            };

            setTimeout(fn, 50)
        }
    };

    var BusinessModelCanvas = {
        editors: {},
        editedEntry: {},
        palette: ['FFFFFF', 'EF4836', '7D3C8C', '4183D7', 'E9D460', '67809F', '1BBC9B', 'F89406', '65C6BB', '6C7A89',
                  'BDC3C7', '333333'],

        mdeConfig: function(element) {
            return {
                element: element,
                toolbar: false,
                status: false,
            }
        },

        init: function() {
            // add the new item form to each section
            var $ne = $('.new-entry-template').clone().removeClass('new-entry-template').addClass('new-entry');
            $('.block-section .entry-region').append($ne.clone());

            // make entries sortable
            var that = this;
            $('.entry-region').sortable({
                items: '> .entry:not(.editing)',
                axis: 'y',

                /* Cancel sort on edit */
                cancel: ".editing",

                /* Update order in the DB as well */
                update: function(event, ui) {
                    $entries = $(this).find('.entry');
                    that.updateEntryListOrder($entries)
                }
            });

            // inject markdown editors & color pickers
            $('#business-model-canvas .block-section').each(function() {
                var $this = $(this);

                // create & render the editor
                $textarea = $this.find('textarea');
                var simplemde = new SimpleMDE(that.mdeConfig($textarea[0]));
                simplemde.render();

                // catch `@` to trigger autocomplete
                simplemde.codemirror.on("keypress", function(instance, event) {
                    if (Autocomplete.active) { // already triggered
                        Autocomplete.fetchTerms()
                    }
                    else if (event.keyCode == 64) { // @ = 64
                        Autocomplete.trigger(simplemde)
                    }
                });

                // save the editor for future reference
                that.editors[$this.attr('id')] = simplemde;

                // add color picker
                // init color pickers
                $this.find('input[name="new-entry-color"]').colorPicker({colors: that.palette, $container: $this});
            });
        },

        csrfmiddlewaretoken: function() {
            return $('#business-model-canvas').data('csrfmiddlewaretoken');
        },

        addEntry: function($entry) {
            var blockId = $entry.closest('.block-section').attr('id');
            var projectId = $('#business-model-canvas').data('project_id');
            var canvasId = $('#business-model-canvas').data('canvas_id');
            var simplemde = this.editors[blockId];
            var $bs = $entry.closest('.block-section')
            var section_arr = $bs.attr('id').split('-');
            var order = Number($bs.find('.entry-region .entry:last').data('order')) + 1 || 0;
            var section = section_arr[section_arr.length - 1];
            var color = $entry.find('input[name="new-entry-color"]').val();

            // post the entry
            $.ajax({
                url: '/team-ideation-tools/business-model/projects/' + projectId + '/' + canvasId + '/add-entry/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': this.csrfmiddlewaretoken(),
                    'text': simplemde.value(),
                    'section': section,
                    'order': order,
                    'groupColor': color
                },
                success: function(data) {
                    // add the new entry
                    $(data).insertBefore($entry.closest('.entry-region .new-entry'));

                    // clear "Add an item" message
                    $entry.closest('.canvas-content').find('> .empty').remove();

                    // clear the editor
                    simplemde.value('');
                }
            });
        },

        showEditEntry: function($entry) {
            // get markdown content
            var entryId = $entry.data('id');
            var markdownContent = $entry.find('.markdown-content').text();
            var textareaId = 'entry-textarea-' + entryId;
            var color = $entry.find('.clr-val').css('background-color');

            // add class to mark as editing, save info
            $entry.addClass('editing').closest('.block-section').addClass('editing');
            this.editedEntry.output = $entry.find('.rendered-output').html();

            // replace content with text area
            var $form = $('<div class="update-entry-form" />')
                .append('<textarea id="' + textareaId + '">' + markdownContent + '</textarea>')
                .append('<span class="cancel-update-entry pull-left"><i class="fa fa-times" /> Cancel</span>')
                .append('<span class="update-entry pull-right"><i class="fa fa-save" /> Save</span>')
                .append('<div class="pull-right colorpicker"><input type="text" name="update-entry-color" value="' + color + '" /><label>Group</label></div>')

            $entry.find('.rendered-output').replaceWith($form);

            // create & render the editor & colorpicker
            var simplemde = new SimpleMDE(this.mdeConfig($form.find('textarea')[0]));
            simplemde.render();

            $entry.find('input[name="update-entry-color"]').colorPicker({colors: this.palette,
                                                                         $container: $entry.closest('.block-section')});

            // save it in the editedEntry object
            this.editedEntry.simplemde = simplemde;
            this.editedEntry.$entry = $entry;
        },

        updateEntry: function($entry) {
            // explicit or through state
            $entry = $entry || this.editedEntry.$entry;
            var entryId = $entry.data('id');

            // update the entry
            var that = this;
            $.ajax({
                url: '/team-ideation-tools/business-model/entries/' + entryId + '/update/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': this.csrfmiddlewaretoken(),
                    'text': that.editedEntry.simplemde.value(),
                    'groupColor': that.editedEntry.$entry.find('input[name="update-entry-color"]').val(),
                },
                success: function(data) {
                    // update the UI
                    that.editedEntry.$entry.closest('.block-section').removeClass('editing');
                    $entry.replaceWith($(data));

                    // clear edit info
                    that.editedEntry = {};
                }
            });
        },

        updateEntryListOrder: function($entries) {
            var data = [];
            $.each($entries, function(index, entry) {
                var $entry = $(entry);
                $entry.data('order', index);
                $entry.attr('data-order', index);
                data.push({id: $entry.data('id'), order: index});
            });

            // update the orders
            var that = this;
            $.ajax({
                url: '/team-ideation-tools/business-model/entries/update-orders/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': that.csrfmiddlewaretoken(),
                    'data': JSON.stringify(data)
                },
                success: function() {
                    // nothing
                }
            });
        },

        isEditing: function() {
            return !$.isEmptyObject(this.editedEntry);
        },

        clearEdit: function() {
            if (this.isEditing()) {
                var entryId = this.editedEntry.$entry.data('id');

                var that = this;
                $.ajax({
                    url:  '/team-ideation-tools/business-model/entries/' + entryId + '/',
                    method: 'GET',
                    success: function(data) {
                        // update the UI
                        that.editedEntry.$entry.closest('.block-section').removeClass('editing');
                        that.editedEntry.$entry.replaceWith($(data));

                        // clear edit info
                        that.editedEntry = {};
                    }
                });
            }
        },

        removeEntry: function($entry) {
            var entryId = $entry.data('id');

            if (confirm('Are you sure you want to delete this entry?')) {
                // remove the entry
                $.ajax({
                    url: '/team-ideation-tools/business-model/entries/' + entryId + '/remove/',
                    method: 'POST',
                    data: {
                        'csrfmiddlewaretoken': this.csrfmiddlewaretoken(),
                    },
                    success: function() {
                        var $cc = $entry.closest('.canvas-content');

                        $entry.remove();

                        // add "Add an item" message if necessary
                        if ($cc.find('> .entry-region > .entry').length == 0) {
                            $cc.append('<div class="empty"><p class="col-md-12 text-center">Add an item</p></div>');
                        }
                    }
                });
            }
        }
    };

    // initialize the canvas
    BusinessModelCanvas.init();

    // connect events
    $('#business-model-canvas').on('click', '.new-entry', function() {
        $('.new-entry').removeClass('active')
        $(this).addClass('active');
    });
    
    $('#business-model-canvas').on('click', '.add-entry', function(e) {
        BusinessModelCanvas.addEntry($(this).closest('.new-entry'))
        e.stopPropagation();
    });

    $('#business-model-canvas').on('click', '.remove-entry', function(e) {
        BusinessModelCanvas.removeEntry($(this).closest('.entry'))
        e.stopPropagation();
    });

    $('#business-model-canvas').on('click', '.edit-entry', function(e) {
        e.stopPropagation();
        e.preventDefault();

        BusinessModelCanvas.showEditEntry($(this).closest('.entry'))

        $(this).closest('.tooltip-container').find('.custom-tooltip').toggleClass('active')
    });

    $('#business-model-canvas').on('click', '.update-entry', function(e) {
        e.stopPropagation();
        e.preventDefault();

        BusinessModelCanvas.updateEntry($(this).closest('.entry'))
    });

    $('#business-model-canvas').on('click', '.update-entry-form', function(e) {
        e.stopPropagation();
    });
    
    $('#business-model-canvas').on('click', function(e) {
        if ($(e.target).hasClass('colorPicker-swatch')) {
            return
        }

        if (BusinessModelCanvas.isEditing()) {
            BusinessModelCanvas.updateEntry();
        }
    });

    $('#business-model-canvas').on('click', '.cancel-update-entry', function(e) {
        BusinessModelCanvas.clearEdit();
    });

    // scrolling
    $('.canvas-content').perfectScrollbar();

    // move customers segment to correct place
    var $customerSegments = $('li.customer-segments');

    $customerSegments
        .css('top', ($('#block-section-CS').offset().top - 65) + 'px')
        .css('position', 'absolute')
        .css('display', 'block');

    // load customer segments
    $customerSegments
        .find('ul')
        .empty();

    $.ajax({
        url: 'suggest-term',
        success: function(personas) {
            $.each(personas, function(idx, persona) {
                $customerSegments
                    .find('ul')
                    .append($('<li />')
                        .text(persona.text)
                        .data('personaid', persona.id)
                        .attr('data-personaid', persona.id)
                    );
            });

            $customerSegments
                .find('ul')
                .perfectScrollbar();
        }
    })
});