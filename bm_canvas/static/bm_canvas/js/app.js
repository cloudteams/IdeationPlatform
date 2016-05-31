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

        addEntry: function($entry) {
            var blockId = $entry.closest('.block-section').attr('id');
            var projectId = $('#business-model-canvas').data('project_id');
            var simplemde = this.editors[blockId];
            var csrfmiddlewaretoken = $entry.find('.add-entry').data('csrfmiddlewaretoken');
            var section_arr = $entry.closest('.block-section').attr('id').split('-');
            var section = section_arr[section_arr.length - 1];

            // post the entry
            $.ajax({
                url: '/business-model/projects/' + projectId + '/add-entry/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
                    'text': simplemde.value(),
                    'section': section
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
            var csrfmiddlewaretoken = $entry.data('csrfmiddlewaretoken');

            // update the entry
            var that = this;
            $.ajax({
                url: '/business-model/entries/' + entryId + '/update/',
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfmiddlewaretoken,
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
            var csrfmiddlewaretoken = $entry.data('csrfmiddlewaretoken');

            if (confirm('Are you sure you want to delete this entry?')) {
                // remove the entry
                $.ajax({
                    url: '/business-model/entries/' + entryId + '/remove/',
                    method: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrfmiddlewaretoken,
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