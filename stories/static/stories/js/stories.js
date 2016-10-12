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
            url: '/team-ideation-platform/stories/scenarios/' + scenarioId + '/team-ideation-platform/stories-to-add/',
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
            url: '/team-ideation-platform/stories/scenarios/' + scenarioId + '/add-story/',
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

    /* On scenario toggle stories */
    $('.toggle-stories').on('click', function() {
        $(this).closest('article.scenario').find('.stories-list').toggle(500);
    });

    /* Redirect on current project change */
    $('#id_current_project').on('change', function() {
        window.document.location = '/team-ideation-platform/stories/projects/' + $(this).val() + '/';
    });

    /* Order scenarios in project */
    $('#id_order_scenarios_by').on('change', function() {
        $(this).closest('form').submit();
    })
});