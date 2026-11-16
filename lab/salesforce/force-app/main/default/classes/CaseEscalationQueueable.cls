public class CaseEscalationQueueable implements Queueable, Database.AllowsCallouts {
    private static final Integer BATCH = 10;
    private final List<Id> caseIds;

    public CaseEscalationQueueable(Id caseId) {
        this(new List<Id>{ caseId });
    }

    public CaseEscalationQueueable(List<Id> caseIds) {
        this.caseIds = caseIds == null ? new List<Id>() : caseIds;
    }

    public void execute(QueueableContext ctx) {
        Integer take = Math.min(BATCH, caseIds.size());
        List<Id> chunk = new List<Id>();
        for (Integer i = 0; i < take; i++) {
            chunk.add(caseIds[i]);
        }
        List<Case> rows = [
            SELECT Id, Subject, Description, Priority, Snow_Sync_Source__c
            FROM Case
            WHERE Id IN :chunk
        ];
        List<Case> updates = new List<Case>();
        for (Case c : rows) {
            if (c.Snow_Sync_Source__c == 'servicenow') {
                continue;
            }
            Map<String, Object> body = SnowIncidentService.pushCase(c);
            String sysId = (String) body.get('sys_id');
            if (String.isBlank(sysId)) {
                continue;
            }
            updates.add(new Case(
                Id = c.Id,
                Snow_Sys_Id__c = sysId,
                Snow_Number__c = (String) body.get('number'),
                Snow_Sync_Source__c = 'salesforce'
            ));
        }
        if (!updates.isEmpty()) {
            update updates;
        }
        if (caseIds.size() > BATCH) {
            List<Id> rest = new List<Id>();
            for (Integer i = BATCH; i < caseIds.size(); i++) {
                rest.add(caseIds[i]);
            }
            System.enqueueJob(new CaseEscalationQueueable(rest));
        }
    }
}
