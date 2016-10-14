def team_platform_info(request):
    tp_url = 'https://teams.cloudteams.eu/bscw/bscw.cgi/'
    return {
        'tp_url': tp_url,
        'all_projects_url': '%s%s?op=cloudteams.getstdb&action=cloudteams.myprojects' % (tp_url, request.session['dashboard_id'])
    }
