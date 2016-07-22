$(function() {

    var $pp = $('#persona-processing')
    if ($pp.length == 0) { // no need
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
    }, 1000);
})