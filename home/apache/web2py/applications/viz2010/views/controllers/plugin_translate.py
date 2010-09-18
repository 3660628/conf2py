def translate():
    return "jQuery(document).ready(function(){jQuery('#page').translate('%s');});" % request.args(0).split('.')[0]

