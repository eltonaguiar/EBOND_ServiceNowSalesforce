public with sharing class SnowIncidentService {
    public class CalloutException extends Exception {}

    public static Map<String, Object> pushCase(Case c) {
        if (c == null || c.Id == null) {
            throw new CalloutException('Case Id is required');
        }
        if (Limits.getCallouts() + 2 > Limits.getLimitCallouts()) {
            throw new CalloutException('Callout limit reached');
        }
        String existing = lookupSysId(c.Id);
        if (existing != null) {
            return patchIncident(existing, c);
        }
        return createIncident(c);
    }

    public static String mapUrgency(String priority) {
        if (priority == 'High') {
            return '1';
        }
        if (priority == 'Medium') {
            return '2';
        }
        return '3';
    }

    private static String lookupSysId(Id caseId) {
        String query = 'u_ebond_sf_case_id=' + EncodingUtil.urlEncode(String.valueOf(caseId), 'UTF-8');
        HttpResponse res = send('GET', '/api/now/table/incident?sysparm_query=' + query + '&sysparm_fields=sys_id,number&sysparm_limit=1', null);
        Map<String, Object> parsed = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
        List<Object> rows = (List<Object>) parsed.get('result');
        if (rows == null || rows.isEmpty()) {
            return null;
        }
        return (String) ((Map<String, Object>) rows[0]).get('sys_id');
    }

    private static Map<String, Object> createIncident(Case c) {
        HttpResponse res = send('POST', '/api/now/table/incident', payload(c));
        return unwrap(res);
    }

    private static Map<String, Object> patchIncident(String sysId, Case c) {
        HttpResponse res = send('PATCH', '/api/now/table/incident/' + sysId, payload(c));
        return unwrap(res);
    }

    private static Map<String, Object> payload(Case c) {
        return new Map<String, Object>{
            'u_ebond_sf_case_id' => c.Id,
            'u_sync_source' => 'salesforce',
            'correlation_id' => c.Id,
            'short_description' => c.Subject,
            'description' => c.Description,
            'urgency' => mapUrgency(c.Priority),
            'impact' => '2'
        };
    }

    private static HttpResponse send(String method, String path, Map<String, Object> body) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:EBOND_ServiceNow' + path);
        req.setMethod(method);
        req.setHeader('Accept', 'application/json');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(20000);
        if (body != null) {
            req.setBody(JSON.serialize(body));
        }
        HttpResponse res = new Http().send(req);
        Integer code = res.getStatusCode();
        if (code < 200 || code >= 300) {
            throw new CalloutException('ServiceNow HTTP ' + code + ' ' + res.getBody());
        }
        return res;
    }

    private static Map<String, Object> unwrap(HttpResponse res) {
        Map<String, Object> parsed = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
        Object result = parsed.get('result');
        if (result instanceof Map<String, Object>) {
            return (Map<String, Object>) result;
        }
        return parsed;
    }
}
