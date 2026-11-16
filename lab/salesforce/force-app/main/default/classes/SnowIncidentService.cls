public with sharing class SnowIncidentService {
    public class CalloutException extends Exception {}

    public static Map<String, Object> pushCase(Case c) {
        if (c == null || c.Id == null) {
            throw new CalloutException('Case Id is required');
        }
        if (Limits.getCallouts() >= Limits.getLimitCallouts()) {
            throw new CalloutException('Callout limit reached');
        }

        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:EBOND_ServiceNow/api/x_ebond/bond/case');
        req.setMethod('POST');
        req.setHeader('Accept', 'application/json');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(20000);
        req.setBody(JSON.serialize(new Map<String, Object>{
            'salesforce_id' => c.Id,
            'short_description' => c.Subject,
            'description' => c.Description,
            'urgency' => mapUrgency(c.Priority),
            'impact' => '2'
        }));

        HttpResponse res = new Http().send(req);
        Integer code = res.getStatusCode();
        if (code != 200 && code != 201) {
            throw new CalloutException('ServiceNow HTTP ' + code + ' ' + res.getBody());
        }
        return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
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
}
