$(function() {
    var BusinessModelCanvas = {
        editors: {},
        editedEntry: {},
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
                items: '> .entry',
                update: function(event, ui) {
                    $entries = $(this).find('.entry');
                    that.updateEntryListOrder($entries)
                }
            });

            // inject markdown editors
            var that = this;
            $('#business-model-canvas textarea').each(function() {
                // create & render the editor
                var simplemde = new SimpleMDE(that.mdeConfig(this));
                simplemde.render();

                // save the editor for future reference
                that.editors[$(this).closest('.block-section').attr('id')] = simplemde;
            });
        },

        csrfmiddlewaretoken: function() {
            return $('#business-model-canvas').data('csrfmiddlewaretoken');
        },

        addEntry: function($entry) {
            var blockId = $entry.closest('.block-section').attr('id');
            var projectId = $('#business-model-canvas').data('project_id');
            var simplemde = this.editors[blockId];
            var $bs = $entry.closest('.block-section')
            var section_arr = $bs.attr('id').split('-');
            var order = Number($bs.find('.entry-region .entry:last').data('order')) + 1 || 0;
            var section = section_arr[section_arr.length - 1];

            // post the entry
            $.ajax({
                url: '/business-model/projects/' + projectId + '/add-entry/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': this.csrfmiddlewaretoken(),
                    'text': simplemde.value(),
                    'section': section,
                    'order':order
                },
                success: function(data) {
                    // add the new entry
                    $(data).insertBefore($entry.closest('.entry-region .new-entry'));

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

            // add class to mark as editing, save info
            $entry.addClass('editing').closest('.block-section').addClass('editing');
            this.editedEntry.output = $entry.find('.rendered-output').html();

            // replace content with text area
            var $form = $('<div class="update-entry-form" />')
                .append('<textarea id="' + textareaId + '">' + markdownContent + '</textarea>')
                .append('<span class="cancel-update-entry pull-left"><i class="fa fa-times" /> Cancel</span>')
                .append('<span class="update-entry pull-right"><i class="fa fa-save" /> Save</span>');

            $entry.find('.rendered-output').replaceWith($form);

            // create & render the editor
            var simplemde = new SimpleMDE(this.mdeConfig($form.find('textarea')[0]));
            simplemde.render();

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
                url: '/business-model/entries/' + entryId + '/update/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': this.csrfmiddlewaretoken(),
                    'text': that.editedEntry.simplemde.value()
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
                url: '/business-model/entries/update-orders/',
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
                    url:  '/business-model/entries/' + entryId + '/',
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
                    url: '/business-model/entries/' + entryId + '/remove/',
                    method: 'POST',
                    data: {
                        'csrfmiddlewaretoken': this.csrfmiddlewaretoken(),
                    },
                    success: function() {
                        $entry.remove();
                    }
                });
            }
        }
    }

    // initialize the canvas
    BusinessModelCanvas.init();

    // connect events
    $('#business-model-canvas').on('click', '.add-entry', function(e) {
        BusinessModelCanvas.addEntry($(this).closest('.new-entry'))
        e.stopPropagation();
    });

    $('#business-model-canvas').on('click', '.remove-entry', function(e) {
        BusinessModelCanvas.removeEntry($(this).closest('.entry'))
        e.stopPropagation();
    });

    $('#business-model-canvas').on('click', '.edit-entry', function(e) {
        BusinessModelCanvas.showEditEntry($(this).closest('.entry'))
        e.stopPropagation();
    });

    $('#business-model-canvas').on('click', '.update-entry', function(e) {
        BusinessModelCanvas.updateEntry($(this).closest('.entry'))
        e.stopPropagation();
    });

    $('#business-model-canvas').on('click', '.update-entry-form', function(e) {
        e.stopPropagation();
    });

    $('#business-model-canvas').on('click', function() {
        if (BusinessModelCanvas.isEditing()) {
            BusinessModelCanvas.updateEntry();
        }
    });

    //BusinessModelCanvas.clearEdit();
    $('#business-model-canvas').on('click', '.cancel-update-entry', function(e) {
        BusinessModelCanvas.clearEdit();
    });
})