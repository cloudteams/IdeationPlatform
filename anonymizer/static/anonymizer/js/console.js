var ConfigurationConsole = {
    start: function(id) {
        this.client_url = '/team-ideation-platform/anonymizer/connection/' + id + '/query/?q=';
    },

    status: 'DEFAULT',
};

$(function() {
    $('body').on('keydown', "#test-console", function(e) {
        if (e.keyCode == 13) { //send request on enter
            //allow only one request at a time
            if (ConfigurationConsole.status == 'PENDING') {
                e.preventDefault();
                e.stopPropagation();

                return;
            }
            ConfigurationConsole.status = 'PENDING';

            var that = this;
            var content = this.value;
            var q = content.substr(content.lastIndexOf("\n") + 2);

            $.ajax({
                type: "GET",
                url: ConfigurationConsole.client_url + q,
                success: function(data, textStatus, jqXHR) {
                    var new_val = $(that).val() + '\n' + jqXHR.responseText;
                    if (jqXHR.responseText) {
                        new_val += '\n$';
                    } else {
                        new_val += '$';
                    }

                    $(that).val(new_val);
                    $(that).scrollTop($(that)[0].scrollHeight);
                    ConfigurationConsole.status = 'DEFAULT';
                },
                error: function(jqXHR, textStatus) {
                    $(that).val( $(that).val() + '\n[ERROR]: ' + jqXHR.responseText + '\n$');
                    $(that).scrollTop($(that)[0].scrollHeight);
                    ConfigurationConsole.status = 'DEFAULT';
                }
            });

            e.preventDefault();
            e.stopPropagation();
        } else if (e.keyCode == 8) { //don't allow backspace before current line
            var content = this.value;
            if (content[content.length - 1] === '$') {
                e.preventDefault();
                e.stopPropagation();
            }
        }
    });

    $('#test-console').on('cut', function () {
        return false;
    });
});

