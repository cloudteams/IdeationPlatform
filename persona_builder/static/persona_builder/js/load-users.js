$(function() {
    /* If persona users are not available by default, this means the Persona is still updating.
     * Check every two seconds if processing has been completed & replace loading placeholder with user information
     */

    $('form').submit(function() {
        $('body').prepend('<div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%">Matching customers... / This might take a few moments</div></div>');
        $('body').animate({ scrollTop: 0 }, 600);
    })
    
    var $pp = $('#persona-processing')
    if ($pp.length == 0) { // no processing done
        return
    }

    var intv = setInterval(function() {
        $.ajax({
            type: 'GET',
            url: document.location.pathname + 'load-users/',
            success: function(data) {
                console.log(data)
                if (data == '') {
                    return
                }

                // stop looking for users
                clearInterval(intv);

                // replace loading with content
                $pp.replaceWith($(data));
            }
        })
    }, 2000);
})