(function executeRule(current, previous) {
    if (current.u_sync_source == 'salesforce') {
        return;
    }
    if (!current.u_sf_case_id) {
        return;
    }
    if (previous && current.state == previous.state && current.short_description == previous.short_description) {
        return;
    }

    try {
        var r = new sn_ws.RESTMessageV2('EBOND Salesforce Case', 'patch_case');
        r.setStringParameterNoEscape('snow_sys_id', current.getUniqueValue());
        r.setStringParameterNoEscape('subject', current.getValue('short_description') || '');
        r.setStringParameterNoEscape('description', current.getValue('description') || '');
        r.setStringParameterNoEscape('state', current.getValue('state') || '');
        r.setStringParameterNoEscape('number', current.getValue('number') || '');
        r.setHttpTimeout(20000);
        var resp = r.execute();
        var code = resp.getStatusCode();
        if (code < 200 || code >= 300) {
            gs.error('EBOND Salesforce patch failed status=' + code + ' body=' + resp.getBody());
        }
    } catch (ex) {
        gs.error('EBOND Salesforce patch exception: ' + ex.message);
    }
})(current, previous);
