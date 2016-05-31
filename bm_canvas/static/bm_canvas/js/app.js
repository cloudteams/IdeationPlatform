$(function() {
    var BusinessModelCanvas = {
        editors: {},
        init: function() {
            // add the new item form to each section
            var $ne = $('.new-entry-template').clone().removeClass('new-entry-template').addClass('new-entry');
            $('.block-section .entry-region').append($ne.clone());

            // inject markdown editors
            var that = this;
            $('#business-model-canvas textarea').each(function() {
                var simplemde = new SimpleMDE({
                    element: this,
                    toolbar: false,
                    status: false,
                });
                // render the editor
                simplemde.render();
                // save the editor for future reference
                that.editors[$(this).closest('.block-section').attr('id')] = simplemde;
            });
        },

        addEntry: function($entry) {
            var blockId = $entry.closest('.block-section').attr('id');
            var projectId = $('#business-model-canvas').data('project_id');
            var simplemde = this.editors[blockId];
            var csrfmiddlewaretoken = $entry.find('.btn-save').data('csrfmiddlewaretoken');
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
        }
    }

    // initialize the canvas
    BusinessModelCanvas.init();

    // connect events
    $('#business-model-canvas .btn-save').on('click', function() {
        BusinessModelCanvas.addEntry($(this).closest('.new-entry'))
    })
})