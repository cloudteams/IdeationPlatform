/**
 * Created by dimitris on 20/9/2016.
 */
$(function() {
    /* On add existing story click show existing stories */
    $('.add-existing-story').on('click', function(e) {
        // prevent default action
        e.preventDefault();
        e.stopPropagation();

        // get scenario ID
        var scenarioId = $(this).data('scenario_id');

        // setup the popup
        var $modal = $('#story-modal');
        $modal.find('.modal-title').text('Add an existing story');
        $modal.find('.modal-body').html('');
        $modal.modal('show');

        // get possible stories
        $.ajax({
            type: 'GET',
            url: '/stories/scenarios/' + scenarioId + '/stories-to-add/',
            success: function(data) {
                $modal.find('.modal-body').html(data)
            },
            error: function() {
                $modal.find('.modal-body').html('An error occurred, please try again later.')
            }
        })
    });

    /* On "Add Story" button click add the story*/
    $('body').on('click', '.add-existing-story', function() {
        var $modal = $('#story-modal');
        var scenarioId = $(this).data('scenario_id');
        var storyId = $(this).data('story_id');

        // add the story
        $.ajax({
            type: 'POST',
            url: '/stories/scenarios/' + scenarioId + '/add-story/',
            data: {
                story_id: storyId
            },
            success: function(data) {
                $modal.modal('hide');

                // reload the scenario
                window.document.location.reload();
            },
            error: function() {
                $modal.find('.modal-body').html('An error occurred, please try again later.')
            }
        });
    });
});