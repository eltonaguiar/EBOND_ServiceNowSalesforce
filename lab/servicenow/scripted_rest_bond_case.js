(function process(request, response) {
    var body = request.body.data;
    if (!body || !body.salesforce_id) {
        response.setStatus(400);
        response.setBody({ error: 'salesforce_id is required' });
        return;
    }
    if (!body.short_description) {
        response.setStatus(400);
        response.setBody({ error: 'short_description is required' });
        return;
    }

    var gr = new GlideRecord('incident');
    gr.addQuery('u_ebond_sf_case_id', body.salesforce_id);
    gr.setLimit(1);
    gr.query();

    var created = false;
    if (!gr.next()) {
        gr.initialize();
        gr.u_ebond_sf_case_id = body.salesforce_id;
        created = true;
    }

    gr.short_description = body.short_description;
    if (body.description) {
        gr.description = body.description;
    }
    if (body.urgency) {
        gr.urgency = String(body.urgency);
    }
    if (body.impact) {
        gr.impact = String(body.impact);
    }
    gr.u_sync_source = 'salesforce';
    gr.correlation_id = body.salesforce_id;

    var sysId = created ? gr.insert() : (gr.update(), gr.getUniqueValue());
    response.setStatus(created ? 201 : 200);
    response.setBody({
        sys_id: sysId,
        number: gr.getValue('number'),
        created: created
    });
})(request, response);
