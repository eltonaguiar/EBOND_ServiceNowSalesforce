public class CaseEscalationQueueable implements Queueable, Database.AllowsCallouts {
    private final Id caseId;

    public CaseEscalationQueueable(Id caseId) {
        this.caseId = caseId;
    }

    public void execute(QueueableContext ctx) {
        Case c = [
            SELECT Id, Subject, Description, Priority, Snow_Sys_Id__c, Snow_Sync_Source__c
            FROM Case
            WHERE Id = :caseId
            LIMIT 1
        ];
        if (c.Snow_Sync_Source__c == 'servicenow') {
            return;
        }
        Map<String, Object> body = SnowIncidentService.pushCase(c);
        String sysId = (String) body.get('sys_id');
        String numberVal = (String) body.get('number');
        if (String.isBlank(sysId)) {
            return;
        }
        Case updateRow = new Case(
            Id = c.Id,
            Snow_Sys_Id__c = sysId,
            Snow_Number__c = numberVal,
            Snow_Sync_Source__c = 'salesforce'
        );
        update updateRow;
    }
}
